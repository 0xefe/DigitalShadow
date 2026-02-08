"""
Digital Shadow - Utility Functions
Yardımcı fonksiyonlar ve araçlar
"""

import re
import hashlib
from datetime import datetime
from typing import Optional
from cryptography.fernet import Fernet
import config

# Şifreleme anahtarı (gerçek uygulamada güvenli bir yerde saklanmalı)
ENCRYPTION_KEY = b'xQR5vK8nL2mP9wB3jF6hD4sA7tY1uE0oI5rT8qW2cX4='
cipher_suite = Fernet(ENCRYPTION_KEY)


def validate_username(username: str) -> tuple[bool, str]:
    """
    Kullanıcı adı doğrulama
    Returns: (is_valid, error_message)
    """
    if not username:
        return False, "Kullanıcı adı boş olamaz"
    
    if len(username) < 3:
        return False, "Kullanıcı adı en az 3 karakter olmalı"
    
    if len(username) > 30:
        return False, "Kullanıcı adı en fazla 30 karakter olabilir"
    
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return False, "Kullanıcı adı sadece harf, rakam ve alt çizgi içerebilir"
    
    return True, ""


def validate_text(text: str) -> tuple[bool, str]:
    """
    Analiz metni doğrulama
    Returns: (is_valid, error_message)
    """
    if not text or not text.strip():
        return False, "Metin boş olamaz"
    
    if len(text) < config.MIN_TEXT_LENGTH:
        return False, f"Metin en az {config.MIN_TEXT_LENGTH} karakter olmalı"
    
    if len(text) > config.MAX_TEXT_LENGTH:
        return False, f"Metin en fazla {config.MAX_TEXT_LENGTH} karakter olabilir"
    
    return True, ""


def hash_password(password: str) -> str:
    """Şifre hash'leme (basit örnek)"""
    return hashlib.sha256(password.encode()).hexdigest()


def encrypt_data(data: str) -> str:
    """Veri şifreleme"""
    try:
        encrypted = cipher_suite.encrypt(data.encode())
        return encrypted.decode()
    except Exception as e:
        print(f"Encryption error: {e}")
        return data


def decrypt_data(encrypted_data: str) -> str:
    """Veri şifre çözme"""
    try:
        decrypted = cipher_suite.decrypt(encrypted_data.encode())
        return decrypted.decode()
    except Exception as e:
        print(f"Decryption error: {e}")
        return encrypted_data


def format_datetime(dt_string: str) -> str:
    """
    ISO datetime string'i okunabilir formata çevirir
    """
    try:
        dt = datetime.fromisoformat(dt_string)
        return dt.strftime("%d.%m.%Y %H:%M")
    except:
        return dt_string


def get_current_datetime() -> str:
    """Şu anki tarih-saat (ISO format)"""
    return datetime.now().isoformat()


def calculate_privacy_score(aggression: float, positivity: float, risk: float) -> float:
    """
    Gizlilik skoru hesaplama
    Düşük skor = daha iyi gizlilik
    """
    score = (
        aggression * config.PRIVACY_WEIGHTS["aggression"] +
        risk * config.PRIVACY_WEIGHTS["risk"] +
        positivity * config.PRIVACY_WEIGHTS["positivity"]
    )
    
    # 0-100 arası normalize et
    normalized = max(0, min(100, score * 100))
    return round(normalized, 1)


def get_risk_level(score: float) -> dict:
    """
    Risk seviyesi belirleme
    Returns: {"level": "low/medium/high", "color": "#...", "label": "..."}
    """
    for level, data in config.RISK_LEVELS.items():
        if score <= data["threshold"]:
            return {
                "level": level,
                "color": data["color"],
                "label": data["label"]
            }
    
    return {
        "level": "high",
        "color": config.RISK_LEVELS["high"]["color"],
        "label": config.RISK_LEVELS["high"]["label"]
    }


def truncate_text(text: str, max_length: int = 100) -> str:
    """Metni kısalt"""
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."


def sanitize_filename(filename: str) -> str:
    """Dosya adını güvenli hale getir"""
    # Özel karakterleri kaldır
    safe = re.sub(r'[<>:"/\\|?*]', '_', filename)
    return safe.strip()


def format_number(number: float, decimals: int = 2) -> str:
    """Sayıyı formatla"""
    return f"{number:.{decimals}f}"


def percentage(value: float) -> str:
    """Float değeri yüzde olarak formatla"""
    return f"{value * 100:.1f}%"
