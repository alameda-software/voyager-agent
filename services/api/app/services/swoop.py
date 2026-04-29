"""
swoop — Google Hotels search service wrapper.

swoop scrapes Google Flights/Hotels RPC endpoints for real-time data.
No API key needed. Runs locally.

Install: pip install swoop
"""

import asyncio
import json
from typing import Optional


class SwoopService:
    """Wraps swoop for flight search via Google Flights."""

    def __init__(self):
        pass

    async def search(
        self,
        origin: str,
        destination: str,
        date: str,
        return_date: Optional[str] = None,
        adults: int = 1,
        cabin: str = "economy",
        max_stops: Optional[int] = None,
    ) -> dict:
        """
        Search flights via swoop (Google Flights RPC).

        Uses swoop's Python SDK to query Google Flights directly.
        """
        try:
            from swoop import search as swoop_search

            cabin_map = {
                "economy": "economy",
                "premium-economy": "premium_economy",
                "business": "business",
                "first": "first",
            }

            result = swoop_search(
                origin=origin,
                destination=destination,
                date=date,
                return_date=return_date,
                adults=adults,
                cabin=cabin_map.get(cabin, "economy"),
                max_stops=max_stops,
            )

            return {
                "results": self._format_results(result),
                "raw": str(result),
            }
        except ImportError:
            return {
                "error": "swoop not installed. Run: pip install swoop",
                "results": [],
            }
        except Exception as e:
            return {"error": str(e), "results": []}

    def _format_results(self, result) -> list[dict]:
        """Format swoop results into our standard flight card format."""
        # swoop returns SearchResult with itineraries
        results = []
        if hasattr(result, "itineraries"):
            for itin in result.itineraries:
                results.append({
                    "price": getattr(itin, "price", None),
                    "currency": "USD",
                    "legs": [
                        {
                            "origin": getattr(leg, "origin", ""),
                            "destination": getattr(leg, "destination", ""),
                            "departure": getattr(leg, "departure", ""),
                            "arrival": getattr(leg, "arrival", ""),
                            "airline": getattr(leg, "airline", ""),
                            "duration": getattr(leg, "duration", ""),
                        }
                        for leg in getattr(itin, "legs", [])
                    ],
                    "stops": getattr(itin, "stops", 0),
                })
        return results
