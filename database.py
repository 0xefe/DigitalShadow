"""
Digital Shadow - Database Module
Veritabanı yönetimi ve CRUD işlemleri
"""

import sqlite3
from typing import Optional, List, Dict, Any
from datetime import datetime
import config
import utils


class Database:
    """Veritabanı yönetim sınıfı"""
    
    def __init__(self, db_path: str = config.DB_PATH):
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self._connect()
        self._create_tables()
    
    def _connect(self):
        """Veritabanına bağlan"""
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
    
    def _create_tables(self):
        """Tabloları oluştur"""
        
        # Kullanıcılar tablosu
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT,
            email TEXT,
            created_at TEXT NOT NULL,
            last_login TEXT
        )
        """)
        
        # Analizler tablosu
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS analyses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            aggression REAL NOT NULL,
            positivity REAL NOT NULL,
            risk REAL NOT NULL,
            privacy_score REAL,
            dominant_trait TEXT,
            ai_comment TEXT,
            analyzed_text TEXT,
            created_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        """)
        
        # Sosyal medya taramaları
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS social_scans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            platform TEXT NOT NULL,
            username TEXT NOT NULL,
            found BOOLEAN,
            risk_score REAL,
            details TEXT,
            scanned_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        """)
        
        # Ayarlar tablosu
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            key TEXT NOT NULL,
            value TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id),
            UNIQUE(user_id, key)
        )
        """)
        
        self.conn.commit()
    
    # ==================== USER OPERATIONS ====================
    
    def create_user(self, username: str, password: str = "", email: str = "") -> Optional[int]:
        """Yeni kullanıcı oluştur"""
        try:
            password_hash = utils.hash_password(password) if password else ""
            created_at = utils.get_current_datetime()
            
            self.cursor.execute("""
            INSERT INTO users (username, password_hash, email, created_at)
            VALUES (?, ?, ?, ?)
            """, (username, password_hash, email, created_at))
            
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.IntegrityError:
            return None
    
    def get_user(self, username: str) -> Optional[Dict[str, Any]]:
        """Kullanıcı bilgilerini getir"""
        self.cursor.execute("""
        SELECT id, username, email, created_at, last_login
        FROM users WHERE username = ?
        """, (username,))
        
        row = self.cursor.fetchone()
        if row:
            return {
                "id": row[0],
                "username": row[1],
                "email": row[2],
                "created_at": row[3],
                "last_login": row[4]
            }
        return None
    
    def verify_user(self, username: str, password: str) -> bool:
        """Kullanıcı doğrulama"""
        password_hash = utils.hash_password(password)
        self.cursor.execute("""
        SELECT id FROM users 
        WHERE username = ? AND password_hash = ?
        """, (username, password_hash))
        
        return self.cursor.fetchone() is not None
    
    def update_last_login(self, user_id: int):
        """Son giriş zamanını güncelle"""
        self.cursor.execute("""
        UPDATE users SET last_login = ? WHERE id = ?
        """, (utils.get_current_datetime(), user_id))
        self.conn.commit()
    
    # ==================== ANALYSIS OPERATIONS ====================
    
    def save_analysis(self, user_id: int, aggression: float, positivity: float, 
                     risk: float, dominant_trait: str, ai_comment: str,
                     analyzed_text: str = "") -> int:
        """Analiz sonucunu kaydet"""
        privacy_score = utils.calculate_privacy_score(aggression, positivity, risk)
        created_at = utils.get_current_datetime()
        
        self.cursor.execute("""
        INSERT INTO analyses 
        (user_id, aggression, positivity, risk, privacy_score, 
         dominant_trait, ai_comment, analyzed_text, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (user_id, aggression, positivity, risk, privacy_score,
              dominant_trait, ai_comment, analyzed_text, created_at))
        
        self.conn.commit()
        return self.cursor.lastrowid
    
    def get_user_analyses(self, user_id: int, limit: int = 50) -> List[Dict[str, Any]]:
        """Kullanıcının analizlerini getir"""
        self.cursor.execute("""
        SELECT id, aggression, positivity, risk, privacy_score,
               dominant_trait, ai_comment, created_at
        FROM analyses 
        WHERE user_id = ?
        ORDER BY created_at DESC
        LIMIT ?
        """, (user_id, limit))
        
        results = []
        for row in self.cursor.fetchall():
            results.append({
                "id": row[0],
                "aggression": row[1],
                "positivity": row[2],
                "risk": row[3],
                "privacy_score": row[4],
                "dominant_trait": row[5],
                "ai_comment": row[6],
                "created_at": row[7]
            })
        
        return results
    
    def get_analysis_stats(self, user_id: int) -> Dict[str, Any]:
        """Kullanıcının analiz istatistiklerini getir"""
        self.cursor.execute("""
        SELECT 
            COUNT(*) as total,
            AVG(aggression) as avg_aggression,
            AVG(positivity) as avg_positivity,
            AVG(risk) as avg_risk,
            AVG(privacy_score) as avg_privacy
        FROM analyses
        WHERE user_id = ?
        """, (user_id,))
        
        row = self.cursor.fetchone()
        return {
            "total_analyses": row[0] or 0,
            "avg_aggression": round(row[1] or 0, 2),
            "avg_positivity": round(row[2] or 0, 2),
            "avg_risk": round(row[3] or 0, 2),
            "avg_privacy_score": round(row[4] or 0, 1)
        }
    
    # ==================== SOCIAL SCAN OPERATIONS ====================
    
    def save_social_scan(self, user_id: int, platform: str, username: str,
                        found: bool, risk_score: float, details: str = "") -> int:
        """Sosyal medya tarama sonucunu kaydet"""
        scanned_at = utils.get_current_datetime()
        
        self.cursor.execute("""
        INSERT INTO social_scans
        (user_id, platform, username, found, risk_score, details, scanned_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (user_id, platform, username, found, risk_score, details, scanned_at))
        
        self.conn.commit()
        return self.cursor.lastrowid
    
    def get_social_scans(self, user_id: int) -> List[Dict[str, Any]]:
        """Kullanıcının sosyal medya taramalarını getir"""
        self.cursor.execute("""
        SELECT platform, username, found, risk_score, details, scanned_at
        FROM social_scans
        WHERE user_id = ?
        ORDER BY scanned_at DESC
        """, (user_id,))
        
        results = []
        for row in self.cursor.fetchall():
            results.append({
                "platform": row[0],
                "username": row[1],
                "found": bool(row[2]),
                "risk_score": row[3],
                "details": row[4],
                "scanned_at": row[5]
            })
        
        return results
    
    # ==================== SETTINGS OPERATIONS ====================
    
    def save_setting(self, user_id: int, key: str, value: str):
        """Ayar kaydet"""
        self.cursor.execute("""
        INSERT OR REPLACE INTO settings (user_id, key, value)
        VALUES (?, ?, ?)
        """, (user_id, key, value))
        self.conn.commit()
    
    def get_setting(self, user_id: int, key: str, default: str = "") -> str:
        """Ayar getir"""
        self.cursor.execute("""
        SELECT value FROM settings
        WHERE user_id = ? AND key = ?
        """, (user_id, key))
        
        row = self.cursor.fetchone()
        return row[0] if row else default
    
    def close(self):
        """Veritabanı bağlantısını kapat"""
        if self.conn:
            self.conn.close()


# Global database instance
db = Database()
