"""
Digital Shadow - Configuration Module
Uygulama ayarları ve sabitler
"""

import os

# Uygulama Bilgileri
APP_NAME = "Digital Shadow"
APP_VERSION = "2.0.0"
APP_AUTHOR = "Digital Shadow Team"

# Veritabanı
DB_NAME = "digital_shadow.db"
DB_PATH = os.path.join(os.path.dirname(__file__), DB_NAME)

# API Ayarları
API_HOST = "127.0.0.1"
API_PORT = 8000
API_BASE_URL = f"http://{API_HOST}:{API_PORT}"

# GUI Ayarları
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
WINDOW_MIN_WIDTH = 900
WINDOW_MIN_HEIGHT = 600

# Tema Renkleri (Dark Mode)
COLORS = {
    "primary": "#6366f1",      # Indigo
    "secondary": "#8b5cf6",    # Purple
    "success": "#10b981",      # Green
    "warning": "#f59e0b",      # Amber
    "danger": "#ef4444",       # Red
    "info": "#3b82f6",         # Blue
    
    "bg_dark": "#0f172a",      # Slate 900
    "bg_medium": "#1e293b",    # Slate 800
    "bg_light": "#334155",     # Slate 700
    
    "text_primary": "#f1f5f9",   # Slate 100
    "text_secondary": "#cbd5e1", # Slate 300
    "text_muted": "#94a3b8",     # Slate 400
    
    "border": "#475569",       # Slate 600
    "shadow": "rgba(0, 0, 0, 0.3)"
}

# Risk Seviyeleri
RISK_LEVELS = {
    "low": {"threshold": 0.3, "color": COLORS["success"], "label": "Düşük Risk"},
    "medium": {"threshold": 0.6, "color": COLORS["warning"], "label": "Orta Risk"},
    "high": {"threshold": 1.0, "color": COLORS["danger"], "label": "Yüksek Risk"}
}

# Gizlilik Skorları
PRIVACY_WEIGHTS = {
    "aggression": 0.3,
    "risk": 0.5,
    "positivity": -0.2  # Pozitiflik gizlilik riskini azaltır
}

# Chart Ayarları
CHART_STYLE = "dark_background"
CHART_DPI = 100
CHART_COLORS = ["#6366f1", "#8b5cf6", "#ec4899", "#f59e0b", "#10b981"]

# Analiz Ayarları
MIN_TEXT_LENGTH = 10
MAX_TEXT_LENGTH = 5000
ANALYSIS_TIMEOUT = 30  # saniye

# Sosyal Medya Platformları (Genişletilmiş)
SOCIAL_PLATFORMS = [
    "Twitter/X",
    "Instagram", 
    "Facebook",
    "LinkedIn",
    "TikTok",
    "YouTube",
    "Reddit",
    "GitHub",
    "Twitch",
    "Discord",
    "Telegram",
    "WhatsApp",
    "Snapchat",
    "Pinterest",
    "Tumblr",
    "Medium",
    "Quora",
    "Stack Overflow",
    "Spotify",
    "SoundCloud",
    "Vimeo",
    "Dailymotion",
    "Patreon",
    "OnlyFans",
    "Clubhouse",
    "BeReal",
    "Mastodon",
    "Threads"
]

# Platform kategorileri
PLATFORM_CATEGORIES = {
    "social": ["Twitter/X", "Instagram", "Facebook", "LinkedIn", "Threads", "Mastodon", "BeReal"],
    "video": ["YouTube", "TikTok", "Twitch", "Vimeo", "Dailymotion"],
    "messaging": ["Discord", "Telegram", "WhatsApp", "Snapchat"],
    "professional": ["LinkedIn", "GitHub", "Stack Overflow", "Medium"],
    "creative": ["Pinterest", "Tumblr", "Medium", "Patreon", "OnlyFans"],
    "audio": ["Spotify", "SoundCloud", "Clubhouse"],
    "forum": ["Reddit", "Quora"]
}

# Platform URL şablonları
PLATFORM_URLS = {
    "Twitter/X": "https://twitter.com/{username}",
    "Instagram": "https://instagram.com/{username}",
    "Facebook": "https://facebook.com/{username}",
    "LinkedIn": "https://linkedin.com/in/{username}",
    "TikTok": "https://tiktok.com/@{username}",
    "YouTube": "https://youtube.com/@{username}",
    "Reddit": "https://reddit.com/u/{username}",
    "GitHub": "https://github.com/{username}",
    "Twitch": "https://twitch.tv/{username}",
    "Discord": "Discord: {username}",
    "Telegram": "https://t.me/{username}",
    "WhatsApp": "WhatsApp: {username}",
    "Snapchat": "https://snapchat.com/add/{username}",
    "Pinterest": "https://pinterest.com/{username}",
    "Tumblr": "https://{username}.tumblr.com",
    "Medium": "https://medium.com/@{username}",
    "Quora": "https://quora.com/profile/{username}",
    "Stack Overflow": "https://stackoverflow.com/users/{username}",
    "Spotify": "https://open.spotify.com/user/{username}",
    "SoundCloud": "https://soundcloud.com/{username}",
    "Vimeo": "https://vimeo.com/{username}",
    "Dailymotion": "https://dailymotion.com/{username}",
    "Patreon": "https://patreon.com/{username}",
    "OnlyFans": "https://onlyfans.com/{username}",
    "Clubhouse": "Clubhouse: @{username}",
    "BeReal": "BeReal: {username}",
    "Mastodon": "https://mastodon.social/@{username}",
    "Threads": "https://threads.net/@{username}"
}

# Rapor Ayarları
REPORT_TITLE = "Digital Shadow Analiz Raporu"
REPORT_AUTHOR = APP_AUTHOR
REPORT_SUBJECT = "Dijital Ayak İzi Analizi"
