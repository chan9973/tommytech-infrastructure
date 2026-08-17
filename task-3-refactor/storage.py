# =============================================================================
# Data Storage Module (Data Storage)
# Abstract interfaces for different storage backends
# =============================================================================

from abc import ABC, abstractmethod
from typing import List, Dict, Any


class Storage(ABC):
    """Abstract interface for all data storage backends."""
    
    @abstractmethod
    def save_all(self, records: List[Dict[str, Any]]) -> int:
        """Save multiple records.
        
        Args:
            records: List of transformed product records
            
        Returns:
            Number of records successfully saved
        """
        pass
    
    @abstractmethod
    def load(self) -> List[Dict[str, Any]]:
        """Load all records from storage."""
        pass
    
    @abstractmethod
    def name(self) -> str:
        """Return human-readable storage backend name."""
        pass


class InMemoryStorage(Storage):
    """In-memory storage for testing."""
    
    def __init__(self):
        self._records: List[Dict[str, Any]] = []
    
    def save_all(self, records: List[Dict[str, Any]]) -> int:
        self._records.extend(records)
        return len(records)
    
    def load(self) -> List[Dict[str, Any]]:
        return self._records
    
    def name(self) -> str:
        return 'InMemory'


class SQLiteStorage(Storage):
    """SQLite file-based storage."""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
    
    def save_all(self, records: List[Dict[str, Any]]) -> int:
        import sqlite3
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create table if not exists
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                category TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                processed_price REAL NOT NULL,
                discounted INTEGER NOT NULL,
                reason TEXT
            )
        ''')
        
        # Enable foreign keys
        cursor.execute('PRAGMA foreign_keys=ON')
        
        inserted = 0
        for record in records:
            try:
                cursor.execute('''
                    INSERT OR REPLACE INTO products 
                    VALUES (NULL, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    record.get('name', ''),
                    record.get('processed_price', 0),
                    record.get('processed_category', ''),
                    record.get('quantity', 0),
                    record.get('discounted', False),
                    record.get('reason', '')
                ))
                inserted += 1
            except sqlite3.IntegrityError as e:
                # Skip duplicates
                print(f"Duplicate record ID {record.get('id')}: {e}")
        
        conn.commit()
        conn.close()
        
        return inserted
    
    def load(self) -> List[Dict[str, Any]]:
        import sqlite3
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM products ORDER BY id')
        rows = cursor.fetchall()
        
        conn.close()
        return [dict(zip([desc[0] for desc in cursor.description], row)) for row in rows]
    
    def name(self) -> str:
        return f'SQLite: {self.db_path}'
