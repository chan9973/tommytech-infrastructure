# =============================================================================
# Data Source Abstract Interface (Data Fetcher)
# Dependency Inversion Principle: Depend on abstractions, not concretions
# =============================================================================

from abc import ABC, abstractmethod
from typing import List, Dict, Any


class DataSource(ABC):
    """Abstract interface for all data sources."""
    
    @abstractmethod
    def fetch(self) -> List[Dict[str, Any]]:
        """Fetch raw data from the source."""
        pass
    
    @abstractmethod
    def name(self) -> str:
        """Return human-readable data source name."""
        pass


class MockNetworkData(DataSource):
    """Mock implementation for testing - no network required."""
    
    def fetch(self) -> List[Dict[str, Any]]:
        return [
            {
                'id': 1001,
                'name': 'Widget A',
                'price': 25.99,
                'category': 'electronics',
                'quantity': 50
            },
            {
                'id': 1002,
                'name': 'Gadget B',
                'price': 49.99,
                'category': 'electronics',
                'quantity': 30
            }
        ]
    
    def name(self) -> str:
        return 'NetworkAPI'


class FileDataFetcher(DataSource):
    """Fetch data from a local JSON file."""
    
    def __init__(self, filepath: str):
        self.filepath = filepath
    
    def fetch(self) -> List[Dict[str, Any]]:
        import json
        with open(self.filepath, 'r') as f:
            return json.load(f)
    
    def name(self) -> str:
        return 'FileSource: ' + self.filepath


class LiveAPI(DataSource):
    """Real network data source implementation."""
    
    def __init__(self, url: str, headers: Dict[str, str], timeout: int = 30):
        self.url = url
        self.headers = headers
        self.timeout = timeout
    
    def fetch(self) -> List[Dict[str, Any]]:
        import requests
        response = requests.get(self.url, headers=self.headers, timeout=self.timeout)
        
        if response.status_code != 200:
            raise Exception(f"HTTP {response.status_code}: {response.text}")
        
        return response.json()
    
    def name(self) -> str:
        return 'LiveAPI'
