import aiohttp
import asyncio
import logging
from typing import Optional, Any, Dict

async def make_api_request(
    method: str,
    url: str,
    max_retries: int = 3,
    ssl_verify: bool = True,
    raise_on_status: bool = True,
    proxy: Optional[str] = None,
    stream: bool = False,
    **kwargs
) -> Dict[str, Any]:
    """
    Handle API requests with retries using aiohttp.
    
    Args:
        method: HTTP method (GET, POST, etc.)
        url: Target URL for the API request
        max_retries: Maximum number of retry attempts
        ssl_verify: Whether to verify SSL certificates
        raise_on_status: Whether to raise an exception on HTTP errors
        proxy: Optional proxy URL
        stream: Whether to stream the response
        **kwargs: Additional arguments to pass to aiohttp request
    
    Returns:
        Dictionary containing response data or error information
    """
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    async def attempt_request(session, attempt: int) -> Dict[str, Any]:
        try:
            async with session.request(
                method=method.upper(),
                url=url,
                ssl=ssl_verify,
                proxy=proxy,
                **kwargs
            ) as response:
                if raise_on_status:
                    response.raise_for_status()
                
                if stream:
                    # Handle streaming response
                    content = b""
                    async for chunk in response.content.iter_chunked(1024):
                        content += chunk
                    return {"status": response.status, "data": content}
                
                # Handle non-streaming response
                content_type = response.headers.get('content-type', '')
                if 'application/json' in content_type:
                    data = await response.json()
                else:
                    data = await response.text()
                
                return {
                    "status": response.status,
                    "data": data,
                    "headers": dict(response.headers)
                }
                
        except aiohttp.ClientError as e:
            logger.error(f"Attempt {attempt + 1} failed: {str(e)}")
            if attempt + 1 >= max_retries:
                return {
                    "status": None,
                    "error": f"Max retries reached: {str(e)}",
                    "data": None
                }
            raise  # Re-raise to trigger retry
        
    async with aiohttp.ClientSession() as session:
        for attempt in range(max_retries):
            try:
                return await attempt_request(session, attempt)
            except aiohttp.ClientError:
                if attempt + 1 < max_retries:
                    # Exponential backoff
                    await asyncio.sleep(2 ** attempt)
                continue
        # This line should never be reached due to the return in attempt_request
        return {
            "status": None,
            "error": "Unexpected error: Max retries reached",
            "data": None
        }

# Example usage
async def main():
    # Example GET request
    response = await make_api_request(
        method="GET",
        url="https://api.example.com/data",
        max_retries=3,
        headers={"Accept": "application/json"}
    )
    print(response)

if __name__ == "__main__":
    asyncio.run(main())
