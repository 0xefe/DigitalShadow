"""
Digital Shadow - Real Social Media Scanner
Gerçek sosyal medya API entegrasyonu ve web scraping
"""

import requests
from bs4 import BeautifulSoup
import time
from typing import Dict, List, Any
import re


class RealSocialMediaScanner:
    """Gerçek sosyal medya tarayıcı"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def check_username(self, platform: str, username: str) -> Dict[str, Any]:
        """Kullanıcı adını gerçek platformda kontrol et"""
        
        checkers = {
            "Instagram": self.check_instagram,
            "Twitter/X": self.check_twitter,
            "GitHub": self.check_github,
            "YouTube": self.check_youtube,
            "TikTok": self.check_tiktok,
            "Reddit": self.check_reddit,
            "LinkedIn": self.check_linkedin,
            "Twitch": self.check_twitch,
            "Pinterest": self.check_pinterest,
            "Medium": self.check_medium,
            "Tumblr": self.check_tumblr,
            "Spotify": self.check_spotify,
            "SoundCloud": self.check_soundcloud,
            "Vimeo": self.check_vimeo,
            "Patreon": self.check_patreon,
            "Snapchat": self.check_snapchat,
            "Telegram": self.check_telegram,
        }
        
        checker = checkers.get(platform, self.check_generic)
        return checker(username)
    
    def check_instagram(self, username: str) -> Dict[str, Any]:
        """Instagram kontrolü"""
        url = f"https://www.instagram.com/{username}/"
        try:
            response = self.session.get(url, timeout=5)
            found = response.status_code == 200 and "Page Not Found" not in response.text
            
            details = ""
            risk_score = 0.0
            
            if found:
                # Profil bilgilerini çıkar
                if '"edge_followed_by":{"count":' in response.text:
                    followers_match = re.search(r'"edge_followed_by":\{"count":(\d+)', response.text)
                    if followers_match:
                        followers = int(followers_match.group(1))
                        details = f"Takipçi: {followers:,}"
                        risk_score = min(0.9, followers / 100000)  # Her 100k takipçi = +0.1 risk
                else:
                    details = "Profil bulundu"
                    risk_score = 0.5
            else:
                details = "Profil bulunamadı"
            
            return {
                "platform": "Instagram",
                "username": username,
                "found": found,
                "risk_score": round(risk_score, 2),
                "details": details,
                "url": url if found else None
            }
        except Exception as e:
            return self.error_result("Instagram", username, str(e))
    
    def check_twitter(self, username: str) -> Dict[str, Any]:
        """Twitter/X kontrolü"""
        url = f"https://twitter.com/{username}"
        try:
            response = self.session.get(url, timeout=5)
            found = response.status_code == 200 and "This account doesn't exist" not in response.text
            
            return {
                "platform": "Twitter/X",
                "username": username,
                "found": found,
                "risk_score": 0.6 if found else 0.0,
                "details": "Hesap aktif" if found else "Hesap bulunamadı",
                "url": url if found else None
            }
        except Exception as e:
            return self.error_result("Twitter/X", username, str(e))
    
    def check_github(self, username: str) -> Dict[str, Any]:
        """GitHub kontrolü"""
        url = f"https://api.github.com/users/{username}"
        try:
            response = self.session.get(url, timeout=5)
            found = response.status_code == 200
            
            details = ""
            risk_score = 0.0
            
            if found:
                data = response.json()
                repos = data.get('public_repos', 0)
                followers = data.get('followers', 0)
                details = f"Repo: {repos}, Takipçi: {followers}"
                risk_score = min(0.8, (repos + followers) / 200)
            else:
                details = "Kullanıcı bulunamadı"
            
            return {
                "platform": "GitHub",
                "username": username,
                "found": found,
                "risk_score": round(risk_score, 2),
                "details": details,
                "url": f"https://github.com/{username}" if found else None
            }
        except Exception as e:
            return self.error_result("GitHub", username, str(e))
    
    def check_youtube(self, username: str) -> Dict[str, Any]:
        """YouTube kontrolü"""
        url = f"https://www.youtube.com/@{username}"
        try:
            response = self.session.get(url, timeout=5)
            found = response.status_code == 200 and "This page isn't available" not in response.text
            
            return {
                "platform": "YouTube",
                "username": username,
                "found": found,
                "risk_score": 0.7 if found else 0.0,
                "details": "Kanal bulundu" if found else "Kanal bulunamadı",
                "url": url if found else None
            }
        except Exception as e:
            return self.error_result("YouTube", username, str(e))
    
    def check_tiktok(self, username: str) -> Dict[str, Any]:
        """TikTok kontrolü"""
        url = f"https://www.tiktok.com/@{username}"
        try:
            response = self.session.get(url, timeout=5)
            found = response.status_code == 200 and "Couldn't find this account" not in response.text
            
            return {
                "platform": "TikTok",
                "username": username,
                "found": found,
                "risk_score": 0.65 if found else 0.0,
                "details": "Hesap aktif" if found else "Hesap bulunamadı",
                "url": url if found else None
            }
        except Exception as e:
            return self.error_result("TikTok", username, str(e))
    
    def check_reddit(self, username: str) -> Dict[str, Any]:
        """Reddit kontrolü"""
        url = f"https://www.reddit.com/user/{username}/about.json"
        try:
            response = self.session.get(url, timeout=5)
            found = response.status_code == 200
            
            details = ""
            risk_score = 0.0
            
            if found:
                data = response.json()
                if 'data' in data:
                    karma = data['data'].get('total_karma', 0)
                    details = f"Karma: {karma:,}"
                    risk_score = min(0.7, karma / 50000)
                else:
                    details = "Kullanıcı bulundu"
                    risk_score = 0.4
            else:
                details = "Kullanıcı bulunamadı"
            
            return {
                "platform": "Reddit",
                "username": username,
                "found": found,
                "risk_score": round(risk_score, 2),
                "details": details,
                "url": f"https://reddit.com/u/{username}" if found else None
            }
        except Exception as e:
            return self.error_result("Reddit", username, str(e))
    
    def check_linkedin(self, username: str) -> Dict[str, Any]:
        """LinkedIn kontrolü (sınırlı - login gerektirir)"""
        url = f"https://www.linkedin.com/in/{username}"
        try:
            response = self.session.get(url, timeout=5)
            found = response.status_code == 200
            
            return {
                "platform": "LinkedIn",
                "username": username,
                "found": found,
                "risk_score": 0.5 if found else 0.0,
                "details": "Profil var (detaylar için login gerekli)" if found else "Profil bulunamadı",
                "url": url if found else None
            }
        except Exception as e:
            return self.error_result("LinkedIn", username, str(e))
    
    def check_twitch(self, username: str) -> Dict[str, Any]:
        """Twitch kontrolü"""
        url = f"https://www.twitch.tv/{username}"
        try:
            response = self.session.get(url, timeout=5)
            found = response.status_code == 200 and "Sorry. Unless you've got a time machine" not in response.text
            
            return {
                "platform": "Twitch",
                "username": username,
                "found": found,
                "risk_score": 0.6 if found else 0.0,
                "details": "Kanal aktif" if found else "Kanal bulunamadı",
                "url": url if found else None
            }
        except Exception as e:
            return self.error_result("Twitch", username, str(e))
    
    def check_pinterest(self, username: str) -> Dict[str, Any]:
        """Pinterest kontrolü"""
        url = f"https://www.pinterest.com/{username}/"
        try:
            response = self.session.get(url, timeout=5)
            found = response.status_code == 200
            
            return {
                "platform": "Pinterest",
                "username": username,
                "found": found,
                "risk_score": 0.4 if found else 0.0,
                "details": "Profil bulundu" if found else "Profil bulunamadı",
                "url": url if found else None
            }
        except Exception as e:
            return self.error_result("Pinterest", username, str(e))
    
    def check_medium(self, username: str) -> Dict[str, Any]:
        """Medium kontrolü"""
        url = f"https://medium.com/@{username}"
        try:
            response = self.session.get(url, timeout=5)
            found = response.status_code == 200
            
            return {
                "platform": "Medium",
                "username": username,
                "found": found,
                "risk_score": 0.5 if found else 0.0,
                "details": "Yazar profili bulundu" if found else "Profil bulunamadı",
                "url": url if found else None
            }
        except Exception as e:
            return self.error_result("Medium", username, str(e))
    
    def check_tumblr(self, username: str) -> Dict[str, Any]:
        """Tumblr kontrolü"""
        url = f"https://{username}.tumblr.com"
        try:
            response = self.session.get(url, timeout=5)
            found = response.status_code == 200 and "There's nothing here" not in response.text
            
            return {
                "platform": "Tumblr",
                "username": username,
                "found": found,
                "risk_score": 0.45 if found else 0.0,
                "details": "Blog bulundu" if found else "Blog bulunamadı",
                "url": url if found else None
            }
        except Exception as e:
            return self.error_result("Tumblr", username, str(e))
    
    def check_spotify(self, username: str) -> Dict[str, Any]:
        """Spotify kontrolü (sınırlı)"""
        return self.check_generic(username, "Spotify", f"https://open.spotify.com/user/{username}")
    
    def check_soundcloud(self, username: str) -> Dict[str, Any]:
        """SoundCloud kontrolü"""
        url = f"https://soundcloud.com/{username}"
        try:
            response = self.session.get(url, timeout=5)
            found = response.status_code == 200 and "We can't find that user" not in response.text
            
            return {
                "platform": "SoundCloud",
                "username": username,
                "found": found,
                "risk_score": 0.5 if found else 0.0,
                "details": "Profil bulundu" if found else "Profil bulunamadı",
                "url": url if found else None
            }
        except Exception as e:
            return self.error_result("SoundCloud", username, str(e))
    
    def check_vimeo(self, username: str) -> Dict[str, Any]:
        """Vimeo kontrolü"""
        url = f"https://vimeo.com/{username}"
        try:
            response = self.session.get(url, timeout=5)
            found = response.status_code == 200
            
            return {
                "platform": "Vimeo",
                "username": username,
                "found": found,
                "risk_score": 0.4 if found else 0.0,
                "details": "Profil bulundu" if found else "Profil bulunamadı",
                "url": url if found else None
            }
        except Exception as e:
            return self.error_result("Vimeo", username, str(e))
    
    def check_patreon(self, username: str) -> Dict[str, Any]:
        """Patreon kontrolü"""
        url = f"https://www.patreon.com/{username}"
        try:
            response = self.session.get(url, timeout=5)
            found = response.status_code == 200
            
            return {
                "platform": "Patreon",
                "username": username,
                "found": found,
                "risk_score": 0.6 if found else 0.0,
                "details": "Sayfa bulundu" if found else "Sayfa bulunamadı",
                "url": url if found else None
            }
        except Exception as e:
            return self.error_result("Patreon", username, str(e))
    
    def check_snapchat(self, username: str) -> Dict[str, Any]:
        """Snapchat kontrolü (sınırlı - API yok)"""
        return {
            "platform": "Snapchat",
            "username": username,
            "found": None,  # Belirlenemez
            "risk_score": 0.0,
            "details": "Snapchat API erişimi yok - manuel kontrol gerekli",
            "url": f"https://snapchat.com/add/{username}"
        }
    
    def check_telegram(self, username: str) -> Dict[str, Any]:
        """Telegram kontrolü"""
        url = f"https://t.me/{username}"
        try:
            response = self.session.get(url, timeout=5)
            found = response.status_code == 200 and "If you have <strong>Telegram</strong>" in response.text
            
            return {
                "platform": "Telegram",
                "username": username,
                "found": found,
                "risk_score": 0.5 if found else 0.0,
                "details": "Kullanıcı/Kanal bulundu" if found else "Bulunamadı",
                "url": url if found else None
            }
        except Exception as e:
            return self.error_result("Telegram", username, str(e))
    
    def check_generic(self, username: str, platform: str = "Generic", url: str = None) -> Dict[str, Any]:
        """Genel kontrol"""
        if not url:
            return {
                "platform": platform,
                "username": username,
                "found": None,
                "risk_score": 0.0,
                "details": "API erişimi yok - manuel kontrol gerekli",
                "url": None
            }
        
        try:
            response = self.session.get(url, timeout=5)
            found = response.status_code == 200
            
            return {
                "platform": platform,
                "username": username,
                "found": found,
                "risk_score": 0.4 if found else 0.0,
                "details": "Sayfa bulundu" if found else "Sayfa bulunamadı",
                "url": url if found else None
            }
        except Exception as e:
            return self.error_result(platform, username, str(e))
    
    def error_result(self, platform: str, username: str, error: str) -> Dict[str, Any]:
        """Hata sonucu"""
        return {
            "platform": platform,
            "username": username,
            "found": None,
            "risk_score": 0.0,
            "details": f"Kontrol edilemedi: {error[:50]}",
            "url": None
        }


# Global instance
real_scanner = RealSocialMediaScanner()
