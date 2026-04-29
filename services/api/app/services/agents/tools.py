"""
LangChain tools for the Travel Agent.

Each tool wraps a travel data source (LetsFG, swoop, etc.)
and exposes it to the agent for tool-calling.
"""

from langchain_core.tools import BaseTool

from app.services.letsfg import LetsFGService
from app.services.swoop import SwoopService


class SearchFlightsTool(BaseTool):
    """Search for flights using LetsFG."""

    name: str = "search_flights"
    description: str = (
        "Search for flights between two airports. "
        "Input should be a JSON string with keys: "
        "origin (IATA code), destination (IATA code), "
        "date (YYYY-MM-DD), return_date (optional, YYYY-MM-DD), "
        "adults (number), cabin (economy|premium-economy|business|first), "
        "max_stops (0|1|2, optional)."
    )

    def _run(
        self,
        origin: str,
        destination: str,
        date: str,
        return_date: str | None = None,
        adults: int = 1,
        cabin: str = "economy",
        max_stops: int | None = None,
    ) -> str:
        import asyncio
        service = LetsFGService()
        result = asyncio.run(service.search(
            origin=origin,
            destination=destination,
            date=date,
            return_date=return_date,
            adults=adults,
            cabin=cabin,
            max_stops=max_stops,
        ))
        return str(result)


class ResolveLocationTool(BaseTool):
    """Resolve a city name to an IATA airport code."""

    name: str = "resolve_location"
    description: str = (
        "Find the IATA airport code for a city or airport name. "
        "Input should be a string like 'Seville', 'London', 'Barcelona'."
    )

    def _run(self, query: str) -> str:
        import asyncio
        service = LetsFGService()
        result = asyncio.run(service.locations(query))
        return str(result)


# Export available tools
def get_travel_tools() -> list[BaseTool]:
    return [
        SearchFlightsTool(),
        ResolveLocationTool(),
    ]
