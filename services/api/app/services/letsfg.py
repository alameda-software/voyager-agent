"""
LetsFG — Flight search service wrapper.

LetsFG searches 400+ airlines via local connectors.
No API key needed. Free to search.

Install: pip install letsfg
Star their GitHub repo for free access: https://github.com/LetsFG/LetsFG
"""

import asyncio
import subprocess
import json
from typing import Optional


class LetsFGService:
    """Wraps LetsFG CLI for flight search."""

    def __init__(self):
        self.cli_command = ["letsfg"]

    async def search(
        self,
        origin: str,
        destination: str,
        date: str,
        return_date: Optional[str] = None,
        adults: int = 1,
        cabin: str = "economy",
        max_stops: Optional[int] = None,
    ) -> list[dict]:
        """
        Search flights via LetsFG CLI.

        Args:
            origin: IATA code (e.g., "SVQ")
            destination: IATA code (e.g., "LHR")
            date: Departure date (YYYY-MM-DD)
            return_date: Return date for roundtrip (optional)
            adults: Number of adult passengers
            cabin: economy, premium-economy, business, first
            max_stops: None=any, 0=nonstop, 1=1 stop, 2=2 stops
        """
        args = [
            "search",
            origin,
            destination,
            date,
            "--json",
            f"--adults={adults}",
            f"--cabin={cabin}",
        ]

        if return_date:
            args.extend(["--return", return_date])

        if max_stops is not None:
            args.append(f"--max-stops={max_stops}")

        try:
            proc = await asyncio.create_subprocess_exec(
                *args,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, stderr = await proc.communicate()

            if proc.returncode != 0:
                return {"error": stderr.decode(), "results": []}

            data = json.loads(stdout.decode())
            return {"results": data.get("flights", []), "raw": data}

        except FileNotFoundError:
            return {
                "error": "LetsFG CLI not installed. Run: pip install letsfg",
                "results": [],
            }
        except Exception as e:
            return {"error": str(e), "results": []}

    async def locations(self, query: str) -> list[dict]:
        """Resolve a city name to IATA codes."""
        try:
            proc = await asyncio.create_subprocess_exec(
                "letsfg", "locations", query, "--json",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, _ = await proc.communicate()
            return json.loads(stdout.decode())
        except Exception:
            return []
