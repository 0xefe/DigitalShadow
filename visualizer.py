"""
Digital Shadow - Visualizer Module
Veri görselleştirme ve grafik oluşturma
"""

import matplotlib
matplotlib.use('Qt5Agg')  # PyQt5 ile uyumlu backend

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import seaborn as sns
import numpy as np
from typing import List, Dict, Any
from io import BytesIO
import config

# Stil ayarları
plt.style.use('dark_background')
sns.set_palette(config.CHART_COLORS)


class Visualizer:
    """Veri görselleştirme sınıfı"""
    
    def __init__(self):
        self.dpi = config.CHART_DPI
    
    def create_score_chart(self, aggression: float, positivity: float, 
                          risk: float, neutral: float = 0) -> Figure:
        """
        Skor çubuk grafiği oluştur
        """
        fig, ax = plt.subplots(figsize=(8, 5), dpi=self.dpi)
        
        categories = ['Agresiflik', 'Pozitiflik', 'Risk', 'Nötr']
        values = [aggression, positivity, risk, neutral]
        colors = [config.COLORS["danger"], config.COLORS["success"], 
                 config.COLORS["warning"], config.COLORS["info"]]
        
        bars = ax.barh(categories, values, color=colors, alpha=0.8)
        
        # Değerleri bar'ların üzerine yaz
        for i, (bar, value) in enumerate(zip(bars, values)):
            width = bar.get_width()
            ax.text(width + 0.02, bar.get_y() + bar.get_height()/2,
                   f'{value:.2f}',
                   ha='left', va='center', fontsize=10, fontweight='bold')
        
        ax.set_xlim(0, 1.0)
        ax.set_xlabel('Skor', fontsize=12, fontweight='bold')
        ax.set_title('Dijital Profil Analizi', fontsize=14, fontweight='bold', pad=20)
        ax.grid(axis='x', alpha=0.3, linestyle='--')
        
        plt.tight_layout()
        return fig
    
    def create_radar_chart(self, aggression: float, positivity: float, 
                          risk: float, privacy_score: float) -> Figure:
        """
        Radar (örümcek ağı) grafiği oluştur
        """
        fig, ax = plt.subplots(figsize=(7, 7), dpi=self.dpi, subplot_kw=dict(projection='polar'))
        
        categories = ['Agresiflik', 'Pozitiflik', 'Risk', 'Gizlilik\nSkoru']
        values = [aggression, positivity, risk, privacy_score / 100]
        
        # Grafiği kapat (ilk değeri sona ekle)
        values += values[:1]
        
        # Açıları hesapla
        angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
        angles += angles[:1]
        
        # Çiz
        ax.plot(angles, values, 'o-', linewidth=2, color=config.COLORS["primary"], 
               markersize=8, label='Skorlar')
        ax.fill(angles, values, alpha=0.25, color=config.COLORS["primary"])
        
        # Etiketler
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories, fontsize=10)
        ax.set_ylim(0, 1)
        ax.set_yticks([0.25, 0.5, 0.75, 1.0])
        ax.set_yticklabels(['0.25', '0.50', '0.75', '1.00'], fontsize=8)
        ax.grid(True, alpha=0.3)
        
        ax.set_title('Dijital Profil Radar Analizi', fontsize=14, 
                    fontweight='bold', pad=20)
        
        plt.tight_layout()
        return fig
    
    def create_history_timeline(self, analyses: List[Dict[str, Any]]) -> Figure:
        """
        Zaman çizelgesi grafiği oluştur
        """
        if not analyses:
            fig, ax = plt.subplots(figsize=(10, 5), dpi=self.dpi)
            ax.text(0.5, 0.5, 'Henüz analiz verisi yok', 
                   ha='center', va='center', fontsize=14)
            ax.axis('off')
            return fig
        
        fig, ax = plt.subplots(figsize=(10, 6), dpi=self.dpi)
        
        # Son 10 analizi al (ters sırada - eskiden yeniye)
        recent = analyses[:10][::-1]
        
        indices = list(range(len(recent)))
        aggr_values = [a["aggression"] for a in recent]
        pos_values = [a["positivity"] for a in recent]
        risk_values = [a["risk"] for a in recent]
        
        # Çizgiler
        ax.plot(indices, aggr_values, marker='o', linewidth=2, 
               label='Agresiflik', color=config.COLORS["danger"])
        ax.plot(indices, pos_values, marker='s', linewidth=2, 
               label='Pozitiflik', color=config.COLORS["success"])
        ax.plot(indices, risk_values, marker='^', linewidth=2, 
               label='Risk', color=config.COLORS["warning"])
        
        ax.set_xlabel('Analiz Sırası (Eski → Yeni)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Skor', fontsize=12, fontweight='bold')
        ax.set_title('Analiz Geçmişi Trendi', fontsize=14, fontweight='bold', pad=20)
        ax.set_ylim(0, 1.0)
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.legend(loc='upper left', fontsize=10)
        
        plt.tight_layout()
        return fig
    
    def create_privacy_gauge(self, privacy_score: float) -> Figure:
        """
        Gizlilik skoru göstergesi (gauge chart)
        """
        fig, ax = plt.subplots(figsize=(6, 4), dpi=self.dpi, subplot_kw=dict(projection='polar'))
        
        # Yarım daire oluştur
        theta = np.linspace(0, np.pi, 100)
        
        # Renk bölgeleri
        # 0-30: İyi (yeşil)
        # 30-60: Orta (sarı)
        # 60-100: Kötü (kırmızı)
        
        # Arka plan renkleri
        ax.barh(0, np.pi/3, left=0, height=0.3, 
               color=config.COLORS["success"], alpha=0.3)
        ax.barh(0, np.pi/3, left=np.pi/3, height=0.3, 
               color=config.COLORS["warning"], alpha=0.3)
        ax.barh(0, np.pi/3, left=2*np.pi/3, height=0.3, 
               color=config.COLORS["danger"], alpha=0.3)
        
        # İbre (skor göstergesi)
        score_angle = np.pi * (1 - privacy_score / 100)
        ax.plot([score_angle, score_angle], [0, 0.3], 
               linewidth=4, color='white', marker='o', markersize=10)
        
        # Ayarlar
        ax.set_ylim(0, 0.3)
        ax.set_xlim(0, np.pi)
        ax.set_yticks([])
        ax.set_xticks([0, np.pi/3, 2*np.pi/3, np.pi])
        ax.set_xticklabels(['100\n(Kötü)', '67', '33', '0\n(İyi)'], fontsize=9)
        ax.grid(False)
        ax.spines['polar'].set_visible(False)
        
        # Başlık ve skor
        ax.set_title(f'Gizlilik Skoru: {privacy_score:.1f}', 
                    fontsize=14, fontweight='bold', pad=20)
        
        plt.tight_layout()
        return fig
    
    def create_risk_heatmap(self, social_scans: List[Dict[str, Any]]) -> Figure:
        """
        Sosyal medya risk ısı haritası
        """
        if not social_scans:
            fig, ax = plt.subplots(figsize=(8, 5), dpi=self.dpi)
            ax.text(0.5, 0.5, 'Sosyal medya tarama verisi yok', 
                   ha='center', va='center', fontsize=14)
            ax.axis('off')
            return fig
        
        fig, ax = plt.subplots(figsize=(10, 6), dpi=self.dpi)
        
        # Veriyi hazırla
        platforms = [s["platform"] for s in social_scans]
        risk_scores = [s["risk_score"] if s["found"] else 0 for s in social_scans]
        
        # Renk haritası
        colors_map = []
        for score in risk_scores:
            if score == 0:
                colors_map.append(config.COLORS["bg_light"])
            elif score < 0.4:
                colors_map.append(config.COLORS["success"])
            elif score < 0.7:
                colors_map.append(config.COLORS["warning"])
            else:
                colors_map.append(config.COLORS["danger"])
        
        # Çubuk grafik
        bars = ax.barh(platforms, risk_scores, color=colors_map, alpha=0.8)
        
        # Değerleri yaz
        for bar, score, scan in zip(bars, risk_scores, social_scans):
            if score > 0:
                ax.text(score + 0.02, bar.get_y() + bar.get_height()/2,
                       f'{score:.2f}',
                       ha='left', va='center', fontsize=9, fontweight='bold')
            else:
                ax.text(0.02, bar.get_y() + bar.get_height()/2,
                       'Bulunamadı',
                       ha='left', va='center', fontsize=9, style='italic', alpha=0.7)
        
        ax.set_xlim(0, 1.0)
        ax.set_xlabel('Risk Skoru', fontsize=12, fontweight='bold')
        ax.set_title('Sosyal Medya Risk Haritası', fontsize=14, fontweight='bold', pad=20)
        ax.grid(axis='x', alpha=0.3, linestyle='--')
        
        plt.tight_layout()
        return fig
    
    def create_pie_chart(self, aggression: float, positivity: float, 
                        risk: float, neutral: float) -> Figure:
        """
        Pasta grafiği - profil dağılımı
        """
        fig, ax = plt.subplots(figsize=(7, 7), dpi=self.dpi)
        
        labels = ['Agresiflik', 'Pozitiflik', 'Risk', 'Nötr']
        sizes = [aggression, positivity, risk, neutral]
        colors = [config.COLORS["danger"], config.COLORS["success"], 
                 config.COLORS["warning"], config.COLORS["info"]]
        
        # Pasta grafiği
        wedges, texts, autotexts = ax.pie(sizes, labels=labels, colors=colors,
                                          autopct='%1.1f%%', startangle=90,
                                          textprops={'fontsize': 11, 'fontweight': 'bold'})
        
        # Yüzde metinlerini beyaz yap
        for autotext in autotexts:
            autotext.set_color('white')
        
        ax.set_title('Dijital Profil Dağılımı', fontsize=14, fontweight='bold', pad=20)
        
        plt.tight_layout()
        return fig
    
    def fig_to_bytes(self, fig: Figure) -> BytesIO:
        """Figure'ı byte stream'e çevir"""
        buf = BytesIO()
        fig.savefig(buf, format='png', dpi=self.dpi, bbox_inches='tight',
                   facecolor='#0f172a', edgecolor='none')
        buf.seek(0)
        plt.close(fig)
        return buf


# Global visualizer instance
visualizer = Visualizer()
