"""
Test Suite for Refactored Pipeline
Coverage: Happy paths, boundary failures, edge cases

Run: pytest test_pipeline.py -v --tb=short
"""

import json
import os
import sqlite3
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import pytest

# Import the refactored modules
import sys
sys.path.insert(0, str(Path(__file__).parent / "architecture"))

from refactored_pipeline import (
    RawUser, TransformedUser, APIDataFetcher, JSONFileFetcher,
    NamingTransformer, SQLiteStorage, PipelineOrchestrator
)


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def sample_users():
    """Sample raw user data for testing"""
    return [
        RawUser(id=1, name="John Doe", email="JOHN@EXAMPLE.COM", age=25, active=True),
        RawUser(id=2, name="Jane Smith", email="jane@test.org", age=17, active=False),
        RawUser(id=3, name="Bob", email="bob@example.com", age=45, active=True),
    ]


@pytest.fixture
def temp_db():
    """Create temporary database for testing"""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = f.name
    yield db_path
    # Cleanup
    if os.path.exists(db_path):
        os.unlink(db_path)


@pytest.fixture
def sample_json_file():
    """Create temporary JSON file for testing"""
    data = {
        "users": [
            {"id": 1, "name": "Alice Johnson", "email": "alice@example.com", "age": 30, "active": True},
            {"id": 2, "name": "Bob", "email": "bob@test.org", "age": 22, "active": True}
        ]
    }
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(data, f)
        path = f.name
    yield path
    if os.path.exists(path):
        os.unlink(path)


# ============================================================================
# Data Model Tests
# ============================================================================

class TestRawUser:
    def test_create_raw_user(self):
        user = RawUser(id=1, name="Test User", email="test@example.com", age=25)
        assert user.id == 1
        assert user.name == "Test User"
        assert user.age == 25
    
    def test_raw_user_default_active(self):
        user = RawUser(id=1, name="Test", email="test@example.com", age=20)
        assert user.active is True


class TestTransformedUser:
    def test_create_transformed_user(self):
        user = TransformedUser(
            id=1, first_name="John", last_name="Doe",
            email="john@example.com", age=25,
            is_adult=True, category="adult",
            processed_at="2024-01-01T00:00:00"
        )
        assert user.id == 1
        assert user.is_adult is True
        assert user.category == "adult"


# ============================================================================
# APIDataFetcher Tests
# ============================================================================

class TestAPIDataFetcher:
    
    @patch('requests.get')
    def test_fetch_success(self, mock_get):
        """Test successful API fetch"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "users": [
                {"id": 1, "name": "John Doe", "email": "john@example.com", "age": 25}
            ]
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        fetcher = APIDataFetcher(url="https://api.example.com/users")
        users = fetcher.fetch()
        
        assert len(users) == 1
        assert users[0].id == 1
        assert users[0].name == "John Doe"
    
    @patch('requests.get')
    def test_fetch_network_error(self, mock_get):
        """Test handling of network errors"""
        mock_get.side_effect = Exception("Connection refused")
        
        fetcher = APIDataFetcher(url="https://api.example.com/users")
        
        with pytest.raises(Exception) as exc_info:
            fetcher.fetch()
        
        assert "Connection refused" in str(exc_info.value)
    
    @patch('requests.get')
    def test_fetch_timeout(self, mock_get):
        """Test timeout handling"""
        import requests
        mock_get.side_effect = requests.Timeout("Request timed out")
        
        fetcher = APIDataFetcher(url="https://api.example.com/users", timeout=5)
        
        with pytest.raises(requests.Timeout):
            fetcher.fetch()
    
    @patch('requests.get')
    def test_fetch_empty_response(self, mock_get):
        """Test handling of empty response"""
        mock_response = Mock()
        mock_response.json.return_value = {"users": []}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        fetcher = APIDataFetcher(url="https://api.example.com/users")
        users = fetcher.fetch()
        
        assert len(users) == 0


# ============================================================================
# JSONFileFetcher Tests
# ============================================================================

class TestJSONFileFetcher:
    
    def test_fetch_from_file(self, sample_json_file):
        """Test fetching from JSON file"""
        fetcher = JSONFileFetcher(filepath=sample_json_file)
        users = fetcher.fetch()
        
        assert len(users) == 2
        assert users[0].name == "Alice Johnson"
        assert users[1].name == "Bob"
    
    def test_fetch_missing_file(self):
        """Test handling of missing file"""
        fetcher = JSONFileFetcher(filepath="/nonexistent/file.json")
        
        with pytest.raises(FileNotFoundError):
            fetcher.fetch()


# ============================================================================
# NamingTransformer Tests
# ============================================================================

class TestNamingTransformer:
    
    def test_transform_basic(self, sample_users):
        """Test basic transformation"""
        transformer = NamingTransformer()
        result = transformer.transform(sample_users)
        
        assert len(result) == 3
        assert result[0].first_name == "John"
        assert result[0].last_name == "Doe"
        assert result[0].email == "john@example.com"  # normalized
        assert result[0].is_adult is True
        assert result[0].category == "adult"
    
    def test_transform_minor(self, sample_users):
        """Test adult classification"""
        transformer = NamingTransformer()
        result = transformer.transform(sample_users)
        
        # Jane is 17
        jane = [u for u in result if u.id == 2][0]
        assert jane.is_adult is False
        assert jane.category == "minor"
    
    def test_transform_single_name(self, sample_users):
        """Test name with single part"""
        transformer = NamingTransformer()
        result = transformer.transform(sample_users)
        
        # Bob has only first name
        bob = [u for u in result if u.id == 3][0]
        assert bob.first_name == "Bob"
        assert bob.last_name == ""
    
    def test_transform_normalize_email(self, sample_users):
        """Test email normalization"""
        transformer = NamingTransformer()
        result = transformer.transform(sample_users)
        
        # John's email was uppercase, should be normalized
        john = [u for u in result if u.id == 1][0]
        assert john.email == "john@example.com"
    
    def test_transform_empty_name(self):
        """Test handling of empty name"""
        transformer = NamingTransformer()
        users = [RawUser(id=999, name="", email="test@example.com", age=25)]
        
        result = transformer.transform(users)
        assert result[0].first_name == ""
        assert result[0].last_name == ""


# ============================================================================
# SQLiteStorage Tests
# ============================================================================

class TestSQLiteStorage:
    
    def test_store_users(self, temp_db, sample_users):
        """Test storing users to database"""
        transformer = NamingTransformer()
        transformed = transformer.transform(sample_users)
        
        storage = SQLiteStorage(temp_db)
        result = storage.store(transformed)
        
        assert result is True
        
        # Verify data was written
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        count = cursor.fetchone()[0]
        conn.close()
        
        assert count == 3
    
    def test_store_empty_list(self, temp_db):
        """Test storing empty list"""
        storage = SQLiteStorage(temp_db)
        result = storage.store([])
        
        assert result is True
    
    def test_store_updates_existing(self, temp_db):
        """Test that store updates existing records"""
        storage = SQLiteStorage(temp_db)
        
        # Store initial data
        user1 = TransformedUser(
            id=1, first_name="John", last_name="Doe",
            email="john@example.com", age=25, is_adult=True,
            category="adult", processed_at="2024-01-01"
        )
        storage.store([user1])
        
        # Update same record
        user1_updated = TransformedUser(
            id=1, first_name="John", last_name="Updated",
            email="john@example.com", age=26, is_adult=True,
            category="adult", processed_at="2024-01-02"
        )
        storage.store([user1_updated])
        
        # Verify update
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        cursor.execute("SELECT last_name, age FROM users WHERE id=1")
        result = cursor.fetchone()
        conn.close()
        
        assert result == ("Updated", 26)


# ============================================================================
# PipelineOrchestrator Tests
# ============================================================================

class TestPipelineOrchestrator:
    
    def test_full_pipeline_success(self):
        """Test successful end-to-end pipeline"""
        mock_fetcher = Mock()
        mock_fetcher.fetch.return_value = [
            RawUser(id=1, name="John Doe", email="john@example.com", age=25)
        ]
        
        mock_transformer = Mock()
        mock_transformer.transform.return_value = [
            TransformedUser(
                id=1, first_name="John", last_name="Doe",
                email="john@example.com", age=25, is_adult=True,
                category="adult", processed_at="2024-01-01"
            )
        ]
        
        mock_storage = Mock()
        mock_storage.store.return_value = True
        
        orchestrator = PipelineOrchestrator(
            fetcher=mock_fetcher,
            transformer=mock_transformer,
            storage=mock_storage
        )
        
        result = orchestrator.run()
        
        assert result["success"] is True
        assert result["fetched"] == 1
        assert result["transformed"] == 1
        assert result["stored"] == 1
    
    def test_pipeline_storage_failure(self):
        """Test pipeline when storage fails"""
        mock_fetcher = Mock()
        mock_fetcher.fetch.return_value = [
            RawUser(id=1, name="John", email="john@example.com", age=25)
        ]
        
        mock_transformer = Mock()
        mock_transformer.transform.return_value = [
            TransformedUser(
                id=1, first_name="John", last_name="",
                email="john@example.com", age=25, is_adult=True,
                category="adult", processed_at="2024-01-01"
            )
        ]
        
        mock_storage = Mock()
        mock_storage.store.return_value = False
        
        orchestrator = PipelineOrchestrator(
            fetcher=mock_fetcher,
            transformer=mock_transformer,
            storage=mock_storage
        )
        
        result = orchestrator.run()
        
        assert result["success"] is False
        assert "Storage operation failed" in result["errors"]
    
    def test_pipeline_fetch_error(self):
        """Test pipeline when fetch fails"""
        mock_fetcher = Mock()
        mock_fetcher.fetch.side_effect = Exception("Network error")
        
        mock_transformer = Mock()
        mock_storage = Mock()
        
        orchestrator = PipelineOrchestrator(
            fetcher=mock_fetcher,
            transformer=mock_transformer,
            storage=mock_storage
        )
        
        result = orchestrator.run()
        
        assert result["success"] is False
        assert len(result["errors"]) == 1


# ============================================================================
# Integration Tests
# ============================================================================

class TestIntegration:
    
    def test_end_to_end_with_json_file(self, sample_json_file, temp_db):
        """Full integration test using JSON file"""
        fetcher = JSONFileFetcher(filepath=sample_json_file)
        transformer = NamingTransformer()
        storage = SQLiteStorage(temp_db)
        
        orchestrator = PipelineOrchestrator(
            fetcher=fetcher,
            transformer=transformer,
            storage=storage
        )
        
        result = orchestrator.run()
        
        assert result["success"] is True
        assert result["fetched"] == 2
        
        # Verify stored data
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        count = cursor.fetchone()[0]
        conn.close()
        
        assert count == 2


# ============================================================================
# Run Tests
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])