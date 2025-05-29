import json
import aiohttp
import asyncio

def get_http_response_with_retries(method, url, max_retries, ssl_verify=True, raise_on_status=True, proxy=None, stream=False, **kwargs):
    """
    Performs an HTTP request using Python's aiohttp module and
    return an HTTP response object.
    """
    async def async_request():
        # Create a ClientSession with the specified parameters
        async with aiohttp.ClientSession() as session:
            # Configure SSL verification
            ssl_context = None if ssl_verify else False
            
            # Set up proxy if provided
            proxy_dict = proxy
            
            # Make the HTTP request
            async with session.request(
                method=method,
                url=url,
                ssl=ssl_context,
                proxy=proxy_dict,
                raise_for_status=raise_on_status,
                **kwargs
            ) as response:
                # Check for JSON response
                if response.headers.get('Content-Type') == 'application/json':
                    return await response.json()
                
                else:
                    # Otherwise, return a generator that streams data
                    async def stream_generator():
                        async for chunk in response.content.iter_lines():
                            if chunk:
                                decoded_chunk = chunk.decode('utf-8')
                                if decoded_chunk == '[DONE]':
                                    return
                                yield json.loads(decoded_chunk)
                    
                    return stream_generator()

    # Run the async function synchronously
    response = asyncio.run(async_request())
    return response
