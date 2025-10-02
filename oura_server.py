from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP
import os
import logging
from dotenv import load_dotenv

# INITIALIZE MCP SERVER
mcp = FastMCP("oura")

load_dotenv()
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
            return None

@mcp.tool()
async def get_personal_info() -> str:
    """Get user's personal information from Oura API."""
    data = await make_oura_request("/usercollection/personal_info")

    if not data:
        return "Unable to fetch personal information. Check your token."
    
    return f"""
Personal Information:
Age:{data.get('age', 'N/A')}
Weight:{data.get('weight', 'N/A')}
Height: {data.get('height', 'N/A')}
Biological Sex: {data.get('biological_sex', 'N/A')}
Email: {data.get('email', 'N/A')}
"""

def main():
    """Run the Oura MCP server."""
    if not OURA_ACCESS_TOKEN:
        logging.error("OURA_ACCESS_TOKEN not found in .env file.")
        return

    logging.info("Starting Oura MCP server...")
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()            

    