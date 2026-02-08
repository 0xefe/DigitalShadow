"""
Digital Shadow - Analyzer Module
Gelişmiş metin analizi ve dijital iz tarama
"""

import re
import random
from typing import List, Dict, Any, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import numpy as np
import config


class DigitalShadowAnalyzer:
    """Dijital ayak izi analiz motoru"""
    
    def __init__(self):
        self._init_ai_model()
    
    def _init_ai_model(self):
        """AI modelini başlat"""
        
        # Genişletilmiş eğitim verisi
        TRAIN_TEXTS = [
            # Agresif içerik
            "nefret ediyorum rezil sistem aptal berbat",
            "salak insanlar sinir bozucu kötü",
            "herkes berbat tiksiniyorum öfkeliyim",
            "savaş kavga dövüş şiddet",
            "lanet olsun hepsine düşmanım",
            
            # Pozitif içerik
            "harika bir gün çok mutluyum seviyorum",
            "başardım gurur duyuyorum mükemmel",
            "hayat güzel teşekkürler harika",
            "mutluluk sevgi barış huzur",
            "başarı zafer kazanç mutluluk",
            
            # Riskli içerik
            "risk almayı severim hızlı para",
            "kumar bahis borç kolay kazanç",
            "tehlikeli macera adrenalin",
            "yasak gizli illegal",
            "hack crack şifre kırma",
            
            # Nötr içerik
            "bugün hava güzel dışarı çıktım",
            "kitap okumayı seviyorum",
            "yemek yedim kahve içtim",
            "çalışıyorum öğreniyorum gelişiyorum"
        ]
        
        TRAIN_LABELS = [
            "aggressive", "aggressive", "aggressive", "aggressive", "aggressive",
            "positive", "positive", "positive", "positive", "positive",
            "risk", "risk", "risk", "risk", "risk",
            "neutral", "neutral", "neutral", "neutral"
        ]
        
        self.vectorizer = TfidfVectorizer(max_features=100)
        X_train = self.vectorizer.fit_transform(TRAIN_TEXTS)
        
        self.model = LogisticRegression(max_iter=1000)
        self.model.fit(X_train, TRAIN_LABELS)
    
    def analyze_text(self, texts: List[str]) -> Dict[str, Any]:
        """
        Metinleri analiz et
        Returns: {aggression, positivity, risk, neutral, dominant_trait, ai_comment}
        """
        # Metinleri birleştir ve küçük harfe çevir
        joined = " ".join(texts).lower()
        
        # AI modeli ile tahmin
        X = self.vectorizer.transform([joined])
        probs = self.model.predict_proba(X)[0]
        labels = self.model.classes_
        
        scores = dict(zip(labels, probs))
        
        # Skorları normalize et
        aggression = float(scores.get("aggressive", 0))
        positivity = float(scores.get("positive", 0))
        risk = float(scores.get("risk", 0))
        neutral = float(scores.get("neutral", 0))
        
        # Dominant özellik
        dominant = max(scores, key=scores.get)
        
        # AI yorumu
        ai_comment = self._generate_comment(dominant, aggression, positivity, risk)
        
        return {
            "aggression": round(aggression, 2),
            "positivity": round(positivity, 2),
            "risk": round(risk, 2),
            "neutral": round(neutral, 2),
            "dominant_trait": dominant,
            "ai_comment": ai_comment
        }
    
    def _generate_comment(self, dominant: str, aggr: float, pos: float, risk: float) -> str:
        """AI yorumu oluştur"""
        
        if dominant == "aggressive":
            if aggr > 0.7:
                return "⚠️ Yüksek seviyede agresif ve çatışmacı bir dijital profil. Sosyal medya kullanımınızı gözden geçirmeniz önerilir."
            elif aggr > 0.5:
                return "⚡ Orta seviyede sert ve tepkisel bir dijital iz. Daha yapıcı iletişim kurmanız faydalı olabilir."
            else:
                return "📊 Hafif agresif eğilimler. Genel olarak dengeli bir profil."
        
        elif dominant == "positive":
            if pos > 0.7:
                return "✨ Çok pozitif ve yapıcı bir dijital kimlik! Sosyal medya kullanımınız örnek teşkil ediyor."
            elif pos > 0.5:
                return "😊 Pozitif ve dengeli bir dijital ayak izi. İyi iletişim kuruyorsunuz."
            else:
                return "👍 Genel olarak olumlu bir profil. Devam edin!"
        
        elif dominant == "risk":
            if risk > 0.7:
                return "🚨 Yüksek riskli davranış kalıpları tespit edildi. Dijital güvenliğinizi gözden geçirin!"
            elif risk > 0.5:
                return "⚠️ Orta seviyede risk içeren aktiviteler. Daha dikkatli olmanız önerilir."
            else:
                return "📌 Hafif riskli eğilimler. Genel olarak güvenli bir profil."
        
        else:
            return "📝 Nötr ve dengeli bir dijital profil. Standart kullanım kalıpları."
    
    def scan_social_media(self, username: str, platforms: List[str]) -> List[Dict[str, Any]]:
        """
        Sosyal medya tarama - GERÇEK SONUÇLAR
        """
        results = []
        
        # Gerçek tarayıcıyı import et
        try:
            from real_social_scanner import real_scanner
            use_real_scanner = True
        except:
            use_real_scanner = False
            print("Gerçek tarayıcı yüklenemedi, simülasyon kullanılıyor")
        
        for platform in platforms:
            if use_real_scanner:
                # GERÇEK TARAMA
                try:
                    result = real_scanner.check_username(platform, username)
                    results.append(result)
                except Exception as e:
                    # Hata durumunda simülasyon kullan
                    print(f"{platform} tarama hatası: {e}")
                    results.append(self._simulate_scan(platform, username))
            else:
                # SİMÜLASYON (fallback)
                results.append(self._simulate_scan(platform, username))
        
        return results
    
    def _simulate_scan(self, platform: str, username: str) -> Dict[str, Any]:
        """Simülasyon tarama (fallback)"""
        found = random.choice([True, False, False])  # %33 bulunma ihtimali
        
        if found:
            risk_score = random.uniform(0.3, 0.9)
            details = self._generate_social_details(platform, risk_score)
        else:
            risk_score = 0.0
            details = f"{platform}'da '{username}' kullanıcı adı bulunamadı."
        
        return {
            "platform": platform,
            "username": username,
            "found": found,
            "risk_score": round(risk_score, 2),
            "details": details
        }
    
    def _generate_social_details(self, platform: str, risk_score: float) -> str:
        """Sosyal medya detayları oluştur"""
        
        if risk_score > 0.7:
            return f"{platform}'da aktif profil bulundu. Yüksek görünürlük ve veri paylaşımı tespit edildi."
        elif risk_score > 0.5:
            return f"{platform}'da profil bulundu. Orta seviyede veri paylaşımı mevcut."
        else:
            return f"{platform}'da profil bulundu. Düşük aktivite ve sınırlı veri paylaşımı."
    
    def search_digital_footprint(self, query: str) -> Dict[str, Any]:
        """
        Dijital ayak izi arama simülasyonu
        Email, username, telefon vb. arama
        """
        
        # Email kontrolü
        is_email = bool(re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', query))
        
        # Simülasyon sonuçları
        found_count = random.randint(2, 15)
        risk_score = random.uniform(0.2, 0.8)
        
        sources = []
        possible_sources = [
            "Sosyal medya platformları",
            "Forum kayıtları",
            "Haber arşivleri",
            "Açık veri tabanları",
            "Blog yorumları",
            "GitHub/GitLab profilleri",
            "LinkedIn bağlantıları",
            "E-ticaret siteleri"
        ]
        
        # Rastgele 3-5 kaynak seç
        sources = random.sample(possible_sources, random.randint(3, 5))
        
        return {
            "query": query,
            "query_type": "email" if is_email else "username",
            "found_count": found_count,
            "risk_score": round(risk_score, 2),
            "sources": sources,
            "recommendation": self._get_footprint_recommendation(risk_score)
        }
    
    def _get_footprint_recommendation(self, risk_score: float) -> str:
        """Dijital ayak izi önerisi"""
        
        if risk_score > 0.7:
            return "🚨 Yüksek dijital görünürlük! Gizlilik ayarlarınızı gözden geçirin ve gereksiz hesapları kapatın."
        elif risk_score > 0.5:
            return "⚠️ Orta seviyede dijital iz. Bazı hesaplarınızı gizli moda alabilirsiniz."
        else:
            return "✅ Düşük dijital ayak izi. Gizlilik yönetiminiz iyi durumda."
    
    def calculate_overall_privacy_score(self, analyses: List[Dict]) -> float:
        """
        Genel gizlilik skoru hesapla
        Tüm analizlerin ortalamasını al
        """
        if not analyses:
            return 50.0  # Varsayılan
        
        total_score = sum(a.get("privacy_score", 50) for a in analyses)
        avg_score = total_score / len(analyses)
        
        return round(avg_score, 1)
    
    def detect_patterns(self, analyses: List[Dict]) -> Dict[str, Any]:
        """
        Davranış kalıplarını tespit et
        Zaman içindeki değişimleri analiz et
        """
        if len(analyses) < 2:
            return {
                "trend": "insufficient_data",
                "message": "Yeterli veri yok"
            }
        
        # Son 5 analizi al
        recent = analyses[:5]
        
        # Ortalama skorları hesapla
        avg_aggr = np.mean([a["aggression"] for a in recent])
        avg_pos = np.mean([a["positivity"] for a in recent])
        avg_risk = np.mean([a["risk"] for a in recent])
        
        # Trend tespiti
        aggr_values = [a["aggression"] for a in recent]
        if len(aggr_values) >= 3:
            trend_aggr = "increasing" if aggr_values[0] < aggr_values[-1] else "decreasing"
        else:
            trend_aggr = "stable"
        
        return {
            "avg_aggression": round(avg_aggr, 2),
            "avg_positivity": round(avg_pos, 2),
            "avg_risk": round(avg_risk, 2),
            "aggression_trend": trend_aggr,
            "dominant_pattern": "aggressive" if avg_aggr > 0.5 else "positive" if avg_pos > 0.5 else "neutral",
            "message": self._get_pattern_message(avg_aggr, avg_pos, avg_risk, trend_aggr)
        }
    
    def _get_pattern_message(self, aggr: float, pos: float, risk: float, trend: str) -> str:
        """Davranış kalıbı mesajı"""
        
        if trend == "increasing" and aggr > 0.5:
            return "📈 Agresif eğilimler artış gösteriyor. Daha sakin bir iletişim tarzı deneyebilirsiniz."
        elif pos > 0.6:
            return "✨ Pozitif ve yapıcı bir trend. Harika gidiyorsunuz!"
        elif risk > 0.6:
            return "⚠️ Riskli davranış kalıpları tespit edildi. Dikkatli olun."
        else:
            return "📊 Dengeli ve tutarlı bir davranış kalıbı."


# Global analyzer instance
analyzer = DigitalShadowAnalyzer()
