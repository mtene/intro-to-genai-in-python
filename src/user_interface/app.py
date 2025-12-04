import threading
import time
from queue import Queue
from dataclasses import dataclass
from pathlib import Path
from typing import Dict
from base64 import b64encode
import streamlit as st
from streamlit_chat import message as st_chat_message
from user_interface.select_chatbot import list_chatbot_names, load_chatbot
from chatbot.chat_context import ChatContext
from chatbot.chat_history import user_message, assistant_message, ChatHistory, ChatRole
from chatbot.utils.logging import configure_logging

configure_logging()


@dataclass
class Profile:
    role: ChatRole
    icon: str


def load_icon(path: Path) -> str:
    mime = "image/svg+xml;base64"
    icon_data = b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime},{icon_data}"


def create_profiles() -> Dict[str, Profile]:
    roles = [ChatRole.HUMAN, ChatRole.AI]
    icon_paths = [
        Path(__file__).parent.parent.parent / "images" / "icons" / "person.svg",
        Path(__file__).parent.parent.parent / "images" / "icons" / "robot.svg",
    ]
    profiles: Dict[str, Profile] = {}
    for role, icon_path in zip(roles, icon_paths):
        profiles[role.value] = Profile(role=role, icon=load_icon(icon_path))
    return profiles


def status_widget_label() -> str:
    finish_time = st.session_state.status["finish_time"] or time.perf_counter()
    elapsed_sec = finish_time - st.session_state.status["start_time"]
    label = ""
    match st.session_state.status["state"]:
        case "running":
            label = "Generating..."
        case "complete":
            label = "Done"
        case "error":
            label = "Error"
    return f"{label} `{elapsed_sec:.1f} s`"


def status_widget():
    expanded = st.session_state.status["state"] != "complete"
    return st.status(
        label=status_widget_label(),
        state=st.session_state.status["state"],
        expanded=expanded,
        width=300,
    )


# --- Page title ---
st.set_page_config(page_title="GenAI Chat", layout="wide")

# --- Session state ---
# metadata of each chat participant
if "profiles" not in st.session_state:
    st.session_state.profiles = create_profiles()
# list of messages in the conversation so far
if "chat_history" not in st.session_state:
    st.session_state.chat_history = ChatHistory()
# chatbot implementation currently selected, among chatbot.lessons.*
if "chatbot" not in st.session_state:
    all_chatbot_names = list_chatbot_names()
    selected_chatbot_name = all_chatbot_names[0]
    st.session_state.chatbot = load_chatbot(selected_chatbot_name)
# flag that is True while the chatbot is generating the answer
if "awaiting_answer" not in st.session_state:
    st.session_state.awaiting_answer = False
# chatbot status updates for the latest response
if "status" not in st.session_state:
    st.session_state.status = None

# --- Header ---
left, right = st.columns([0.6, 0.4], vertical_alignment="bottom")
with left:
    st.title("GenAI Chat")
with right:
    all_chatbot_names = list_chatbot_names()
    current_chatbot_index = (
        all_chatbot_names.index(st.session_state.chatbot.get_name())
        if st.session_state.chatbot is not None
        else 0
    )
    selected_chatbot_index = st.selectbox(
        "Choose a chatbot",
        options=range(len(all_chatbot_names)),
        index=current_chatbot_index,
        format_func=lambda i: all_chatbot_names[i],
        label_visibility="collapsed",
    )
    if selected_chatbot_index != current_chatbot_index:
        selected_chatbot_name = all_chatbot_names[selected_chatbot_index]
        st.session_state.chatbot = load_chatbot(selected_chatbot_name)
        st.session_state.awaiting_answer = False
        st.rerun()

# --- Chat history ---
for id, msg in enumerate(st.session_state.chat_history.messages):
    profile = st.session_state.profiles.get(msg.type, None)
    if profile is not None and isinstance(msg.content, str):
        # message keys have to be unique, even though the content might be repeated
        # is_user: human messages are right-aligned, while AI messages go to the left
        # allow_html: controls markdown rendering
        st_chat_message(
            msg.content,
            key=str(id),
            is_user=profile.role == ChatRole.HUMAN,
            logo=profile.icon,
            allow_html=True,
        )

# --- Chat phase 1: User input ---
input = st.chat_input("Ask a question...")
if input:
    # get the user question and add it to the history
    st.session_state.chat_history.add_message(user_message(content=input))
    # clear the previous status updates
    st.session_state.status = None
    st.session_state.awaiting_answer = True
    st.rerun()

# --- Chat phase 2: Generate answer, while streaming status updates ---
if st.session_state.awaiting_answer:
    # cross-thread data
    # queue operations are atomic
    answer_q: Queue[str] = Queue(maxsize=1)
    events_q: Queue[Dict[str, str]] = Queue()
    stop_ticker = threading.Event()

    # initialize status updates in state
    st.session_state.status = {
        "state": "running",
        "start_time": time.perf_counter(),
        "finish_time": None,
        "events": [],
    }

    # assistant thread
    # IMPORTANT: spawned threads cannot access st.session_state!
    chatbot = st.session_state.chatbot
    # this chat context object can be used by the chatbot to display update messages in the UI
    ctx = ChatContext(
        status_update_func=lambda msg: events_q.put({"type": "status", "text": msg})
    )
    # extract the user question, which was added to the chat history during phase 1
    question = str(
        st.session_state.chat_history.get_last_message_from(ChatRole.HUMAN).content
    )

    def query_chatbot() -> None:
        try:
            if chatbot is None:
                raise RuntimeError("Error loading chatbot")
            answer_q.put(chatbot.get_answer(question, ctx))
            events_q.put({"type": "outcome", "state": "complete"})
        except Exception as e:
            error = repr(e)
            answer_q.put(error)
            events_q.put({"type": "outcome", "state": "error"})

    threading.Thread(target=query_chatbot, daemon=True).start()

    # ticker thread that updates the time in the status label
    # IMPORTANT: spawned threads cannot access st.session_state!
    def ticker(tick_sec: float = 0.1):
        next_tick = time.perf_counter()
        while not stop_ticker.is_set():
            events_q.put({"type": "tick"})
            next_tick += tick_sec
            now = time.perf_counter()
            time.sleep(max(0, next_tick - now))

    threading.Thread(target=ticker, daemon=True).start()

    # display status updates
    with status_widget() as status:

        def stream_status_updates():
            while True:
                event = events_q.get()
                if event["type"] == "tick":
                    status.update(label=status_widget_label())
                elif event["type"] == "outcome":
                    # inference is done: capture outcome and time, stop ticker
                    st.session_state.status["state"] = event["state"]
                    st.session_state.status["finish_time"] = time.perf_counter()
                    stop_ticker.set()
                    break
                else:
                    # stream status update
                    st.session_state.status["events"].append(event["text"])
                    yield f"{event['text']}\n\n"

        st.write_stream(stream_status_updates())

    # add answer to chat history
    st.session_state.chat_history.add_message(assistant_message(answer_q.get()))
    st.session_state.awaiting_answer = False
    st.rerun()

# --- Persist the status updates from last response ---
elif st.session_state.status is not None:
    with status_widget():
        for line in st.session_state.status["events"]:
            st.write(line)
