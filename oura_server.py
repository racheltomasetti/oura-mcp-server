from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP
import os
import logging
# INITIALIZE MCP SERVER
mcp = FastMCP("oura")

# CONSTANTS
OURA_API_BASE = "https://api.ouraring.com/v2"
OURA_ACCESS_TOKEN = os.getenv("OURA_ACCESS_TOKEN")

async def make_oura_request(endpoint: str, params: dict = None) -> dict[str, Any] | None:
    """Make authenticated request to Oura API."""
    headers = {
        "Authorization": f"Bearer {OURA_ACCESS_TOKEN}"
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{OURA_API_BASE}{endpoint}",
                headers=headers,
                params=params,
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            logging.error(f"HTTP error occurred: {e}")
            

    