"""
Agent Tools - Web Search
Simple web search functionality for agents.
"""
from typing import List, Dict, Any
import httpx


class WebSearchTool:
    """
    Simple web search tool for agents.
    Uses DuckDuckGo Instant Answer API (no API key required).
    """

    def __init__(self):
        self.base_url = "https://api.duckduckgo.com/"
        self.timeout = 10

    async def search(self, query: str, max_results: int = 5) -> Dict[str, Any]:
        """
        Search the web for information.
        
        Args:
            query: Search query
            max_results: Maximum number of results to return
            
        Returns:
            Dict with 'success', 'results', 'error'
        """
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    self.base_url,
                    params={
                        'q': query,
                        'format': 'json',
                        'no_html': 1,
                        'skip_disambig': 1
                    }
                )
                response.raise_for_status()
                data = response.json()
                
                results = []
                
                # Abstract (main answer)
                if data.get('Abstract'):
                    results.append({
                        'type': 'abstract',
                        'title': data.get('Heading', ''),
                        'content': data.get('Abstract', ''),
                        'url': data.get('AbstractURL', ''),
                        'source': data.get('AbstractSource', '')
                    })
                
                # Related topics
                for topic in data.get('RelatedTopics', [])[:max_results]:
                    if isinstance(topic, dict) and 'Text' in topic:
                        results.append({
                            'type': 'related',
                            'title': topic.get('Text', '').split(' - ')[0] if ' - ' in topic.get('Text', '') else '',
                            'content': topic.get('Text', ''),
                            'url': topic.get('FirstURL', '')
                        })
                
                return {
                    'success': True,
                    'results': results[:max_results],
                    'query': query,
                    'error': None
                }
                
        except Exception as e:
            return {
                'success': False,
                'results': [],
                'query': query,
                'error': str(e)
            }

    async def search_documentation(self, technology: str, topic: str) -> Dict[str, Any]:
        """
        Search for documentation on a specific technology.
        
        Args:
            technology: Technology name (e.g., 'FastAPI', 'React')
            topic: Specific topic (e.g., 'authentication', 'hooks')
            
        Returns:
            Search results focused on documentation
        """
        query = f"{technology} {topic} documentation"
        return await self.search(query)


# Global instance
web_search_tool = WebSearchTool()
