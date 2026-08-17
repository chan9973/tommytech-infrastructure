"""
Async Web Scraper using asyncio and aiohttp
"""
import asyncio
import aiohttp
from typing import List, Optional
from dataclasses import dataclass


@dataclass
class ScrapedPage:
    """Represents a scraped web page."""
    url: str
    status: int
    content: str
    title: Optional[str] = None


async def fetch_page(
    session: aiohttp.ClientSession,
    url: str,
    timeout: int = 30
) -> ScrapedPage:
    """Fetch a single page asynchronously.
    
    Args:
        session: aiohttp client session
        url: URL to fetch
        timeout: Request timeout in seconds
        
    Returns:
        ScrapedPage object with results
    """
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=timeout)) as response:
            content = await response.text()
            title = None
            # Extract title from HTML
            if '<title>' in content:
                import re
                match = re.search(r'<title[^>]*>(.*?)</title>', content, re.IGNORECASE)
                if match:
                    title = match.group(1)
            
            return ScrapedPage(
                url=url,
                status=response.status,
                content=content,
                title=title
            )
    except asyncio.TimeoutError:
        return ScrapedPage(url=url, status=0, content="", title=None)
    except aiohttp.ClientError as e:
        return ScrapedPage(url=url, status=0, content=str(e), title=None)


async def scrape_urls(urls: List[str], max_concurrent: int = 10) -> List[ScrapedPage]:
    """Scrape multiple URLs concurrently.
    
    Args:
        urls: List of URLs to scrape
        max_concurrent: Maximum concurrent requests
        
    Returns:
        List of ScrapedPage objects
    """
    connector = aiohttp.TCPConnector(
        limit=max_concurrent,
        limit_per_host=5,
        enable_cleanup_closed=True
    )
    
    results = []
    
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [fetch_page(session, url) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Filter out exceptions and return only ScrapedPage objects
    return [r for r in results if isinstance(r, ScrapedPage)]


async def scrape_titles(urls: List[str]) -> dict:
    """Extract titles from multiple URLs.
    
    Args:
        urls: List of URLs
        
    Returns:
        Dict mapping URLs to their titles
    """
    pages = await scrape_urls(urls)
    return {page.url: page.title for page in pages}


def run_scraper(urls: List[str]) -> List[ScrapedPage]:
    """Synchronous wrapper to run the async scraper.
    
    Args:
        urls: List of URLs to scrape
        
    Returns:
        List of ScrapedPage objects
    """
    return asyncio.run(scrape_urls(urls))


# Example usage
if __name__ == "__main__":
    test_urls = [
        "https://httpbin.org/html",
        "https://example.com",
    ]
    
    print("Starting async scraper...\n")
    
    # Run scraper
    pages = asyncio.run(scrape_urls(test_urls))
    
    for page in pages:
        print(f"URL: {page.url}")
        print(f"Status: {page.status}")
        print(f"Title: {page.title}")
        print("-" * 40)