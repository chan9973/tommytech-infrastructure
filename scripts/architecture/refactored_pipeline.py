"""
SOLID-Compliant Pipeline Architecture

Refactored from monolithic legacy_pipeline.py into modular, testable components:
- DataFetcher: Handles all data source operations (API, DB, files)
- DataTransformer: Pure transformation logic with validation
- DataStorage: Abstract storage interface with multiple implementations
- PipelineOrchestrator: Coordinates the workflow via dependency injection
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List, Dict, Any, Protocol, Optional
import json
import logging

logger = logging.getLogger(__name__)


# ============================================================================
# DOMAIN MODELS - Strongly typed data structures
# ============================================================================

@dataclass
class RawUser:
    """Raw user data from external API"""
    id: int
    name: str
    email: str
    age: int
    active: bool = True


@dataclass
class TransformedUser:
    """Processed user data with derived fields"""
    id: int
    first_name: str
    last_name: str
    email: str
    age: int
    is_adult: bool
    category: str
    processed_at: str
    metadata: Dict[str, Any] = field(default_factory=dict)


# ============================================================================
# ABSTRACTIONS - Interfaces for Dependency Inversion Principle (DIP)
# ============================================================================

class DataFetcher(Protocol):
    """Abstract data fetching capability"""
    def fetch(self) -> List[RawUser]:
        ...


class DataTransformer(Protocol):
    """Abstract data transformation capability"""
    def transform(self, raw: List[RawUser]) -> List[TransformedUser]:
        ...


class DataStorage(Protocol):
    """Abstract data storage capability"""
    def store(self, data: List[TransformedUser]) -> bool:
        ...


# ============================================================================
# IMPLEMENTATIONS - Concrete classes following SRP
# ============================================================================

class APIDataFetcher:
    """Fetches data from REST API - Single Responsibility: Data Retrieval"""
    
    def __init__(self, url: str, timeout: int = 30, session=None):
        self.url = url
        self.timeout = timeout
        self._session = session  # For injection/testing
    
    def fetch(self) -> List[RawUser]:
        """Fetch and parse users from API endpoint"""
        import requests
        
        try:
            response = requests.get(self.url, timeout=self.timeout)
            response.raise_for_status()
            raw_json = response.json()
            
            users = []
            for user_data in raw_json.get("users", []):
                users.append(RawUser(
                    id=user_data.get("id", 0),
                    name=user_data.get("name", ""),
                    email=user_data.get("email", ""),
                    age=user_data.get("age", 0),
                    active=user_data.get("active", True)
                ))
            
            logger.info(f"Fetched {len(users)} users from API")
            return users
            
        except Exception as e:
            logger.error(f"API fetch failed: {e}")
            raise


class JSONFileFetcher:
    """Fetches data from local JSON file - Test-friendly implementation"""
    
    def __init__(self, filepath: str):
        self.filepath = filepath
    
    def fetch(self) -> List[RawUser]:
        with open(self.filepath, 'r') as f:
            raw_data = json.load(f)
        
        users = []
        for user_data in raw_data.get("users", []):
            users.append(RawUser(
                id=user_data.get("id", 0),
                name=user_data.get("name", ""),
                email=user_data.get("email", ""),
                age=user_data.get("age", 0),
                active=user_data.get("active", True)
            ))
        
        return users


class NamingTransformer:
    """Transforms raw user data into structured format - Single Responsibility: Business Logic"""
    
    def transform(self, raw_users: List[RawUser]) -> List[TransformedUser]:
        """Apply business rules to transform raw data"""
        transformed = []
        
        for raw in raw_users:
            # Split name - SRP: Name parsing logic is isolated
            first_name, last_name = self._parse_name(raw.name)
            
            # Normalize email - SRP: Data normalization is isolated
            email = self._normalize_email(raw.email)
            
            # Calculate derived fields - SRP: Business rules are isolated
            is_adult = raw.age >= 18
            category = "adult" if is_adult else "minor"
            
            transformed.append(TransformedUser(
                id=raw.id,
                first_name=first_name,
                last_name=last_name,
                email=email,
                age=raw.age,
                is_adult=is_adult,
                category=category,
                processed_at=datetime.now(timezone.utc).isoformat(),
                metadata={"source": "transformation_pipeline_v1"}
            ))
        
        logger.info(f"Transformed {len(transformed)} users")
        return transformed
    
    def _parse_name(self, name: str) -> tuple:
        """Split name into first and last - can be unit tested"""
        parts = name.strip().split()
        first = parts[0] if parts else ""
        last = parts[-1] if len(parts) > 1 else ""
        return first, last
    
    def _normalize_email(self, email: str) -> str:
        """Normalize email format - can be unit tested"""
        return email.lower().strip() if email else ""


class SQLiteStorage:
    """Stores transformed data in SQLite - Single Responsibility: Persistence"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._initialize_schema()
    
    def _initialize_schema(self):
        """Create tables if they don't exist"""
        import sqlite3
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    first_name TEXT NOT NULL,
                    last_name TEXT,
                    email TEXT UNIQUE,
                    age INTEGER,
                    category TEXT,
                    is_adult INTEGER,
                    processed_at TEXT
                )
            """)
            conn.commit()
    
    def store(self, data: List[TransformedUser]) -> bool:
        """Store transformed users in database"""
        import sqlite3
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                for user in data:
                    conn.execute("""
                        INSERT OR REPLACE INTO users 
                        (id, first_name, last_name, email, age, category, is_adult, processed_at)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        user.id,
                        user.first_name,
                        user.last_name,
                        user.email,
                        user.age,
                        user.category,
                        1 if user.is_adult else 0,
                        user.processed_at
                    ))
                conn.commit()
            
            logger.info(f"Stored {len(data)} users in database")
            return True
            
        except Exception as e:
            logger.error(f"Storage failed: {e}")
            return False


# ============================================================================
# ORCHESTRATOR - Uses dependency injection (OCP, ISP)
# ============================================================================

class PipelineOrchestrator:
    """
    Orchestrates the pipeline workflow using dependency injection.
    Open/Closed: New fetchers/transformers/storage can be added without modification.
    Interface Segregation: Depends on protocols, not concrete implementations.
    """
    
    def __init__(
        self,
        fetcher: DataFetcher,
        transformer: DataTransformer,
        storage: DataStorage
    ):
        self.fetcher = fetcher
        self.transformer = transformer
        self.storage = storage
    
    def run(self) -> Dict[str, Any]:
        """Execute full pipeline: fetch -> transform -> store"""
        result = {
            "success": False,
            "fetched": 0,
            "transformed": 0,
            "stored": 0,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "errors": []
        }
        
        try:
            # Stage 1: Fetch
            raw_data = self.fetcher.fetch()
            result["fetched"] = len(raw_data)
            
            # Stage 2: Transform
            transformed = self.transformer.transform(raw_data)
            result["transformed"] = len(transformed)
            
            # Stage 3: Store
            if self.storage.store(transformed):
                result["stored"] = len(transformed)
                result["success"] = True
            else:
                result["errors"].append("Storage operation failed")
                
        except Exception as e:
            result["errors"].append(str(e))
            logger.error(f"Pipeline failed: {e}")
        
        return result


# ============================================================================
# MAIN ENTRY POINT - Configurable usage
# ============================================================================

def main():
    """Example usage with real implementations"""
    
    # Configure components
    fetcher = APIDataFetcher(
        url="https://api.example.com/users",
        timeout=30
    )
    
    transformer = NamingTransformer()
    storage = SQLiteStorage(db_path="users.db")
    
    # Orchestrate
    pipeline = PipelineOrchestrator(
        fetcher=fetcher,
        transformer=transformer,
        storage=storage
    )
    
    result = pipeline.run()
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()