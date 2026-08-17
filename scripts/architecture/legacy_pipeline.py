#!/usr/bin/env python3
"""
LEGACY MONOLITHIC PIPELINE - BEFORE REFACTORING
This is intentionally monolithic for demonstration purposes.
All functionality in a single function - hard to test, hard to maintain.
"""

import json
import sqlite3
import requests
from datetime import datetime
from typing import Dict, List, Any

def process_user_data():
    """Monolithic function doing everything - fetches, transforms, stores"""
    
    # 1. Fetch data (hardcoded URL)
    try:
        response = requests.get("https://api.example.com/users", timeout=30)
        response.raise_for_status()
        raw_data = response.json()
    except Exception as e:
        print(f"Fetch error: {e}")
        return None
    
    # 2. Transform data (inline, no separation)
    processed = []
    for user in raw_data.get("users", []):
        # Direct transformations inline
        email = user.get("email", "").lower().strip()
        name_parts = user.get("name", "").split()
        first_name = name_parts[0] if name_parts else ""
        last_name = name_parts[-1] if len(name_parts) > 1 else ""
        
        # Calculate derived fields inline
        age = user.get("age", 0)
        is_adult = age >= 18
        category = "adult" if is_adult else "minor"
        
        processed.append({
            "id": user.get("id"),
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "age": age,
            "category": category,
            "processed_at": datetime.now().isoformat()
        })
    
    # 3. Store data (direct SQL, no abstraction)
    try:
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        
        # Inline SQL - no query abstraction
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                first_name TEXT,
                last_name TEXT,
                email TEXT,
                age INTEGER,
                category TEXT,
                processed_at TEXT
            )
        """)
        
        for user in processed:
            cursor.execute("""
                INSERT INTO users (id, first_name, last_name, email, age, category, processed_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                user["id"],
                user["first_name"],
                user["last_name"],
                user["email"],
                user["age"],
                user["category"],
                user["processed_at"]
            ))
        
        conn.commit()
        conn.close()
        
    except Exception as e:
        print(f"Storage error: {e}")
        return None
    
    print(f"Processed {len(processed)} users")
    return processed


if __name__ == "__main__":
    process_user_data()