import requests
import datetime
from zoneinfo import ZoneInfo
from enum import Enum
from fastmcp import FastMCP

mcp_server = FastMCP("my_mcp_tools")


class TimeZone(Enum):
    America_NewYork = "America/New_York"
    Europe_London = "Europe/London"
    Europe_Warsaw = "Europe/Warsaw"
    Europe_Oslo = "Europe/Oslo"


# the tool is registered with the MCP server using the decorator
@mcp_server.tool
def convert_time(
    time_24h: datetime.time, from_time_zone: TimeZone, to_time_zone: TimeZone
) -> str:
    """Converts today's time from one time zone to another.
    time: 'HH:MM[:SS]' (no timezone, no 'Z')
    Example: 10:00
    Returns ISO-8601 with offset, plus target time zone in brackets.
    """
    from_tz = ZoneInfo(from_time_zone.value)
    to_tz = ZoneInfo(to_time_zone.value)
    today = datetime.datetime.now(from_tz).date()
    date_time_24h = datetime.datetime.combine(today, time_24h, tzinfo=from_tz)
    return f"{date_time_24h.astimezone(to_tz).isoformat()} [{to_time_zone.value}]"


class Currency(Enum):
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"
    NOK = "NOK"


# the tool is registered with the MCP server using the decorator
@mcp_server.tool
def convert_currency(
    amount: float, from_currency: Currency, to_currency: Currency
) -> float:
    """Converts money between currencies at today's rate."""
    url = f"https://api.frankfurter.app/latest?amount={amount}&from={from_currency.value}&to={to_currency.value}"
    response = requests.get(url, timeout=60)
    response.raise_for_status()
    data = response.json()
    answer = data["rates"][to_currency.value]
    return answer


if __name__ == "__main__":
    # start the server with stdio transport for local testing
    mcp_server.run(transport="stdio")
