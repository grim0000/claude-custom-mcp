import os
import sys
import logging
import json
import httpx
import asyncio
import psutil
from typing import Optional, Dict, Any, List
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger("obsidian-utils")

# Load environment variables
script_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(script_dir, ".env")
load_dotenv(env_path)

API_KEY = os.environ.get("OBSIDIAN_API_KEY")
BASE_URL = os.environ.get("OBSIDIAN_BASE_URL", "https://127.0.0.1:27124")

if not API_KEY:
    logger.warning("OBSIDIAN_API_KEY not set in .env file. Tools will fail until configured.")

async def ensure_obsidian_running():
    """Checks if Obsidian is running, launches it if not, and waits for API."""
    is_running = False
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == 'Obsidian.exe':
            is_running = True
            break
            
    if not is_running:
        logger.info("Obsidian is not running. Launching...")
        # Launch via protocol handler (opens last vault)
        if sys.platform == 'win32':
            os.system("start obsidian://open")
        elif sys.platform == 'darwin':
            os.system("open obsidian://open")
        else:
            # Linux (xdg-open)
            os.system("xdg-open obsidian://open")
            
        # Wait for process to appear
        logger.info("Waiting for Obsidian to start...")
        await asyncio.sleep(5)
        
    # Wait for API to be responsive
    retries = 10
    for i in range(retries):
        try:
            # Quick check to see if API is up
            async with httpx.AsyncClient(timeout=2.0, verify=False) as client:
                await client.get(f"{BASE_URL}/", headers={"Authorization": f"Bearer {API_KEY}"})
            return # Success
        except:
            if i == retries - 1:
                logger.warning("Obsidian API not responding after launch.")
            await asyncio.sleep(2)

async def make_request(method: str, endpoint: str, data: Any = None, content_type: str = "application/json") -> str:
    """Helper to make authenticated requests to Obsidian."""
    if not API_KEY:
        return "Error: OBSIDIAN_API_KEY not configured."

    # Ensure Obsidian is running before making request
    await ensure_obsidian_running()

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": content_type,
        "Accept": "application/json"
    }
    
    # Remove leading slash if present to avoid double slashes with base url
    if endpoint.startswith("/"):
        endpoint = endpoint[1:]
        
    url = f"{BASE_URL}/{endpoint}"
    
    # Disable SSL verification for Local REST API (self-signed cert)
    async with httpx.AsyncClient(timeout=30.0, verify=False) as client:
        try:
            if method == "GET":
                response = await client.get(url, headers=headers)
            elif method == "POST":
                if content_type == "application/json":
                    response = await client.post(url, headers=headers, json=data)
                else:
                    response = await client.post(url, headers=headers, content=data)
            elif method == "PUT":
                 if content_type == "application/json":
                    response = await client.put(url, headers=headers, json=data)
                 else:
                    response = await client.put(url, headers=headers, content=data)
            elif method == "DELETE":
                response = await client.delete(url, headers=headers)
            elif method == "PATCH":
                 response = await client.patch(url, headers=headers, content=data)
            else:
                return f"Error: Unsupported method {method}"

            if response.status_code == 401:
                return "Error: Unauthorized. Check your OBSIDIAN_API_KEY."
            if response.status_code == 404:
                return "Error: Resource not found."
            
            # For 204 No Content
            if response.status_code == 204:
                return "Success"

            return response.text
            
        except httpx.RequestError as e:
            return f"Error making request to Obsidian: {str(e)}"
