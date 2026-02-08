"""
Digital Shadow - License Manager
Lisans yönetimi ve kullanıcı limitleri
"""

import sqlite3
import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import json


class LicenseType:
    """Lisans tipleri"""
    FREE = "free"
    STARTER = "starter"
    PROFESSIONAL = "professional"
    BUSINESS = "business"
    LIFETIME = "lifetime"


class LicenseManager:
    """Lisans yönetim sistemi"""
    
    # Lisans limitleri
    LIMITS = {
        LicenseType.FREE: {
            "daily_analysis": 5,
            "platforms": 10,
            "history_days": 30,
            "pdf_reports": 3,
            "api_access": False,
            "priority_support": False,
            "price": 0
        },
        LicenseType.STARTER: {
            "daily_analysis": 10,
            "platforms": 15,
            "history_days": 90,
            "pdf_reports": 10,
            "api_access": False,
            "priority_support": False,
            "price": 4.99
        },
        LicenseType.PROFESSIONAL: {
            "daily_analysis": -1,  # Sınırsız
            "platforms": 28,
            "history_days": -1,  # Sınırsız
            "pdf_reports": -1,  # Sınırsız
            "api_access": True,
            "priority_support": True,
            "price": 9.99
        },
        LicenseType.BUSINESS: {
            "daily_analysis": -1,
            "platforms": 28,
            "history_days": -1,
            "pdf_reports": -1,
            "api_access": True,
            "priority_support": True,
            "team_features": True,
            "max_users": 10,
            "price": 99.00
        },
        LicenseType.LIFETIME: {
            "daily_analysis": -1,
            "platforms": 28,
            "history_days": -1,
            "pdf_reports": -1,
            "api_access": True,
            "priority_support": True,
            "price": 299.00
        }
    }
    
    def __init__(self, db_path: str = "digital_shadow.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Lisans tablosunu oluştur"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS licenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                license_key TEXT UNIQUE NOT NULL,
                license_type TEXT NOT NULL,
                start_date TEXT NOT NULL,
                end_date TEXT,
                is_active INTEGER DEFAULT 1,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usage_stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                date TEXT NOT NULL,
                analysis_count INTEGER DEFAULT 0,
                scan_count INTEGER DEFAULT 0,
                pdf_count INTEGER DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES users (id),
                UNIQUE(user_id, date)
            )
        """)
        
        conn.commit()
        conn.close()
    
    def generate_license_key(self, license_type: str) -> str:
        """Lisans anahtarı oluştur"""
        prefix = {
            LicenseType.FREE: "FREE",
            LicenseType.STARTER: "STRT",
            LicenseType.PROFESSIONAL: "PROF",
            LicenseType.BUSINESS: "BUSI",
            LicenseType.LIFETIME: "LIFE"
        }.get(license_type, "UNKN")
        
        random_part = secrets.token_hex(8).upper()
        checksum = hashlib.md5(random_part.encode()).hexdigest()[:4].upper()
        
        return f"{prefix}-{random_part[:4]}-{random_part[4:8]}-{random_part[8:12]}-{checksum}"
    
    def create_license(self, user_id: int, license_type: str, duration_days: int = 30) -> str:
        """Yeni lisans oluştur"""
        license_key = self.generate_license_key(license_type)
        start_date = datetime.now()
        
        if license_type == LicenseType.LIFETIME:
            end_date = None
        else:
            end_date = start_date + timedelta(days=duration_days)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Eski lisansları deaktive et
        cursor.execute("""
            UPDATE licenses 
            SET is_active = 0 
            WHERE user_id = ? AND is_active = 1
        """, (user_id,))
        
        # Yeni lisans ekle
        cursor.execute("""
            INSERT INTO licenses (user_id, license_key, license_type, start_date, end_date)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, license_key, license_type, 
              start_date.isoformat(), 
              end_date.isoformat() if end_date else None))
        
        conn.commit()
        conn.close()
        
        return license_key
    
    def get_user_license(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Kullanıcının aktif lisansını getir"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT license_key, license_type, start_date, end_date, is_active
            FROM licenses
            WHERE user_id = ? AND is_active = 1
            ORDER BY created_at DESC
            LIMIT 1
        """, (user_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        if not result:
            # Ücretsiz lisans oluştur
            self.create_license(user_id, LicenseType.FREE, duration_days=365)
            return self.get_user_license(user_id)
        
        license_key, license_type, start_date, end_date, is_active = result
        
        # Süre kontrolü
        if end_date:
            end_dt = datetime.fromisoformat(end_date)
            if datetime.now() > end_dt:
                # Lisans süresi dolmuş, ücretsiz'e düşür
                self.create_license(user_id, LicenseType.FREE, duration_days=365)
                return self.get_user_license(user_id)
        
        return {
            "license_key": license_key,
            "license_type": license_type,
            "start_date": start_date,
            "end_date": end_date,
            "is_active": bool(is_active),
            "limits": self.LIMITS.get(license_type, self.LIMITS[LicenseType.FREE])
        }
    
    def activate_license(self, user_id: int, license_key: str) -> bool:
        """Lisans anahtarını aktive et"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Lisans anahtarını kontrol et
        cursor.execute("""
            SELECT id, license_type, end_date
            FROM licenses
            WHERE license_key = ? AND user_id = ?
        """, (license_key, user_id))
        
        result = cursor.fetchone()
        
        if not result:
            conn.close()
            return False
        
        license_id, license_type, end_date = result
        
        # Süre kontrolü
        if end_date:
            end_dt = datetime.fromisoformat(end_date)
            if datetime.now() > end_dt:
                conn.close()
                return False
        
        # Eski lisansları deaktive et
        cursor.execute("""
            UPDATE licenses 
            SET is_active = 0 
            WHERE user_id = ? AND id != ?
        """, (user_id, license_id))
        
        # Bu lisansı aktive et
        cursor.execute("""
            UPDATE licenses 
            SET is_active = 1 
            WHERE id = ?
        """, (license_id,))
        
        conn.commit()
        conn.close()
        
        return True
    
    def check_limit(self, user_id: int, limit_type: str) -> bool:
        """Limit kontrolü yap"""
        license_info = self.get_user_license(user_id)
        limits = license_info["limits"]
        
        # Sınırsız ise
        if limits.get(limit_type, 0) == -1:
            return True
        
        # Günlük limitler için
        if limit_type == "daily_analysis":
            today = datetime.now().date().isoformat()
            usage = self.get_daily_usage(user_id, today)
            return usage["analysis_count"] < limits["daily_analysis"]
        
        elif limit_type == "platforms":
            return True  # Platform limiti tarama sırasında kontrol edilir
        
        elif limit_type == "pdf_reports":
            today = datetime.now().date().isoformat()
            usage = self.get_daily_usage(user_id, today)
            return usage["pdf_count"] < limits["pdf_reports"]
        
        return limits.get(limit_type, False)
    
    def increment_usage(self, user_id: int, usage_type: str):
        """Kullanım sayacını artır"""
        today = datetime.now().date().isoformat()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Bugünkü kayıt var mı?
        cursor.execute("""
            SELECT id FROM usage_stats
            WHERE user_id = ? AND date = ?
        """, (user_id, today))
        
        if cursor.fetchone():
            # Güncelle
            cursor.execute(f"""
                UPDATE usage_stats
                SET {usage_type} = {usage_type} + 1
                WHERE user_id = ? AND date = ?
            """, (user_id, today))
        else:
            # Yeni kayıt
            cursor.execute(f"""
                INSERT INTO usage_stats (user_id, date, {usage_type})
                VALUES (?, ?, 1)
            """, (user_id, today))
        
        conn.commit()
        conn.close()
    
    def get_daily_usage(self, user_id: int, date: str) -> Dict[str, int]:
        """Günlük kullanım istatistiklerini getir"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT analysis_count, scan_count, pdf_count
            FROM usage_stats
            WHERE user_id = ? AND date = ?
        """, (user_id, date))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                "analysis_count": result[0],
                "scan_count": result[1],
                "pdf_count": result[2]
            }
        
        return {
            "analysis_count": 0,
            "scan_count": 0,
            "pdf_count": 0
        }
    
    def get_remaining_limits(self, user_id: int) -> Dict[str, Any]:
        """Kalan limitleri getir"""
        license_info = self.get_user_license(user_id)
        limits = license_info["limits"]
        today = datetime.now().date().isoformat()
        usage = self.get_daily_usage(user_id, today)
        
        remaining = {}
        
        # Günlük analiz
        if limits["daily_analysis"] == -1:
            remaining["daily_analysis"] = "Sınırsız"
        else:
            remaining["daily_analysis"] = max(0, limits["daily_analysis"] - usage["analysis_count"])
        
        # PDF raporlar
        if limits["pdf_reports"] == -1:
            remaining["pdf_reports"] = "Sınırsız"
        else:
            remaining["pdf_reports"] = max(0, limits["pdf_reports"] - usage["pdf_count"])
        
        # Platform sayısı
        remaining["platforms"] = limits["platforms"]
        
        return remaining


# Global instance
license_manager = LicenseManager()
