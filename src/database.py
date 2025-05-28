import sqlite3
import json
from datetime import datetime
import os

class ContentDatabase:
    def __init__(self, db_path="data/content_generator.db"):
        """Initialize database connection"""
        # Create data directory if it doesn't exist
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize database tables"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS content_history (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        topic TEXT NOT NULL,
                        platform TEXT NOT NULL,
                        content TEXT NOT NULL,
                        metadata TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                conn.commit()
        except Exception as e:
            print(f"Database initialization error: {e}")
    
    def store_content(self, topic, platform, content, metadata=None):
        """Store generated content"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO content_history (topic, platform, content, metadata)
                    VALUES (?, ?, ?, ?)
                ''', (topic, platform, content, json.dumps(metadata) if metadata else None))
                conn.commit()
                return True
        except Exception as e:
            print(f"Error storing content: {e}")
            return False
    
    def get_content_history(self, limit=50):
        """Get recent content history"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT topic, platform, content, metadata, created_at
                    FROM content_history
                    ORDER BY created_at DESC
                    LIMIT ?
                ''', (limit,))
                return cursor.fetchall()
        except Exception as e:
            print(f"Error fetching content history: {e}")
            return []
