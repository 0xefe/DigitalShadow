"""
Digital Shadow - Advanced Features Module
Gelişmiş özellikler: Threading, Logging, Notifications, Animations
"""

import logging
from typing import Callable, Any
from PyQt5.QtCore import QThread, pyqtSignal, QPropertyAnimation, QEasingCurve, QTimer
from PyQt5.QtWidgets import QWidget, QGraphicsOpacityEffect
import time


# ==================== LOGGING SETUP ====================

class Logger:
    """Gelişmiş logging sistemi"""
    
    def __init__(self, name: str = "DigitalShadow"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # File handler
        file_handler = logging.FileHandler('digital_shadow.log', encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)
        
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)
    
    def info(self, message: str):
        self.logger.info(message)
    
    def error(self, message: str):
        self.logger.error(message)
    
    def warning(self, message: str):
        self.logger.warning(message)
    
    def debug(self, message: str):
        self.logger.debug(message)


# ==================== THREADING ====================

class AnalysisWorker(QThread):
    """Analiz işlemlerini arka planda çalıştır"""
    
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)
    progress = pyqtSignal(int)
    
    def __init__(self, analyzer, text: str):
        super().__init__()
        self.analyzer = analyzer
        self.text = text
    
    def run(self):
        """Analiz işlemini çalıştır"""
        try:
            self.progress.emit(20)
            time.sleep(0.1)  # Simüle edilmiş işlem
            
            result = self.analyzer.analyze_text([self.text])
            
            self.progress.emit(60)
            time.sleep(0.1)
            
            self.progress.emit(100)
            self.finished.emit(result)
            
        except Exception as e:
            self.error.emit(str(e))


class SocialScanWorker(QThread):
    """Sosyal medya taramasını arka planda çalıştır"""
    
    finished = pyqtSignal(list)
    error = pyqtSignal(str)
    progress = pyqtSignal(int, str)  # progress, platform_name
    
    def __init__(self, analyzer, username: str, platforms: list):
        super().__init__()
        self.analyzer = analyzer
        self.username = username
        self.platforms = platforms
    
    def run(self):
        """Tarama işlemini çalıştır"""
        try:
            results = []
            total = len(self.platforms)
            
            for i, platform in enumerate(self.platforms):
                self.progress.emit(int((i / total) * 100), platform)
                
                # Platform taraması
                result = self.analyzer.scan_social_media(self.username, [platform])
                results.extend(result)
                
                time.sleep(0.2)  # Rate limiting
            
            self.progress.emit(100, "Tamamlandı")
            self.finished.emit(results)
            
        except Exception as e:
            self.error.emit(str(e))


class DataExportWorker(QThread):
    """Veri export işlemini arka planda çalıştır"""
    
    finished = pyqtSignal(str)
    error = pyqtSignal(str)
    progress = pyqtSignal(int)
    
    def __init__(self, export_func: Callable, *args, **kwargs):
        super().__init__()
        self.export_func = export_func
        self.args = args
        self.kwargs = kwargs
    
    def run(self):
        """Export işlemini çalıştır"""
        try:
            self.progress.emit(30)
            result = self.export_func(*self.args, **self.kwargs)
            self.progress.emit(100)
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))


# ==================== ANIMATIONS ====================

class AnimationHelper:
    """Widget animasyonları için yardımcı sınıf"""
    
    @staticmethod
    def fade_in(widget: QWidget, duration: int = 300):
        """Widget'ı fade-in efekti ile göster"""
        effect = QGraphicsOpacityEffect(widget)
        widget.setGraphicsEffect(effect)
        
        animation = QPropertyAnimation(effect, b"opacity")
        animation.setDuration(duration)
        animation.setStartValue(0.0)
        animation.setEndValue(1.0)
        animation.setEasingCurve(QEasingCurve.InOutQuad)
        animation.start()
        
        # Animasyonu widget'a bağla (garbage collection'dan koru)
        widget._fade_animation = animation
    
    @staticmethod
    def fade_out(widget: QWidget, duration: int = 300, callback: Callable = None):
        """Widget'ı fade-out efekti ile gizle"""
        effect = QGraphicsOpacityEffect(widget)
        widget.setGraphicsEffect(effect)
        
        animation = QPropertyAnimation(effect, b"opacity")
        animation.setDuration(duration)
        animation.setStartValue(1.0)
        animation.setEndValue(0.0)
        animation.setEasingCurve(QEasingCurve.InOutQuad)
        
        if callback:
            animation.finished.connect(callback)
        
        animation.start()
        widget._fade_animation = animation
    
    @staticmethod
    def slide_in(widget: QWidget, direction: str = "left", duration: int = 400):
        """Widget'ı slide efekti ile göster"""
        from PyQt5.QtCore import QRect
        
        # Başlangıç ve bitiş pozisyonları
        end_geometry = widget.geometry()
        start_geometry = QRect(end_geometry)
        
        if direction == "left":
            start_geometry.moveLeft(-widget.width())
        elif direction == "right":
            start_geometry.moveLeft(widget.parent().width())
        elif direction == "top":
            start_geometry.moveTop(-widget.height())
        elif direction == "bottom":
            start_geometry.moveTop(widget.parent().height())
        
        widget.setGeometry(start_geometry)
        
        animation = QPropertyAnimation(widget, b"geometry")
        animation.setDuration(duration)
        animation.setStartValue(start_geometry)
        animation.setEndValue(end_geometry)
        animation.setEasingCurve(QEasingCurve.OutCubic)
        animation.start()
        
        widget._slide_animation = animation


# ==================== NOTIFICATIONS ====================

class NotificationManager:
    """Bildirim yönetimi"""
    
    def __init__(self):
        self.notifications = []
        self.max_notifications = 5
    
    def add_notification(self, title: str, message: str, type: str = "info"):
        """Yeni bildirim ekle"""
        notification = {
            "title": title,
            "message": message,
            "type": type,
            "timestamp": time.time()
        }
        
        self.notifications.insert(0, notification)
        
        # Maksimum bildirim sayısını aşma
        if len(self.notifications) > self.max_notifications:
            self.notifications = self.notifications[:self.max_notifications]
    
    def get_recent_notifications(self, count: int = 5):
        """Son bildirimleri getir"""
        return self.notifications[:count]
    
    def clear_notifications(self):
        """Tüm bildirimleri temizle"""
        self.notifications.clear()


# ==================== AUTO REFRESH ====================

class AutoRefreshManager:
    """Otomatik yenileme yöneticisi"""
    
    def __init__(self, callback: Callable, interval: int = 60000):
        """
        Args:
            callback: Çağrılacak fonksiyon
            interval: Yenileme aralığı (milisaniye)
        """
        self.timer = QTimer()
        self.timer.timeout.connect(callback)
        self.interval = interval
        self.is_running = False
    
    def start(self):
        """Otomatik yenilemeyi başlat"""
        if not self.is_running:
            self.timer.start(self.interval)
            self.is_running = True
    
    def stop(self):
        """Otomatik yenilemeyi durdur"""
        if self.is_running:
            self.timer.stop()
            self.is_running = False
    
    def set_interval(self, interval: int):
        """Yenileme aralığını değiştir"""
        self.interval = interval
        if self.is_running:
            self.stop()
            self.start()


# ==================== KEYBOARD SHORTCUTS ====================

class ShortcutManager:
    """Klavye kısayolları yöneticisi"""
    
    SHORTCUTS = {
        "new_analysis": "Ctrl+N",
        "save_report": "Ctrl+S",
        "export_data": "Ctrl+E",
        "refresh": "F5",
        "settings": "Ctrl+,",
        "quit": "Ctrl+Q",
        "search": "Ctrl+F",
        "help": "F1"
    }
    
    @classmethod
    def get_shortcut(cls, action: str) -> str:
        """Kısayol tuşunu getir"""
        return cls.SHORTCUTS.get(action, "")
    
    @classmethod
    def get_all_shortcuts(cls) -> dict:
        """Tüm kısayolları getir"""
        return cls.SHORTCUTS.copy()


# ==================== PERFORMANCE MONITOR ====================

class PerformanceMonitor:
    """Performans izleme"""
    
    def __init__(self):
        self.metrics = {}
    
    def start_timer(self, operation: str):
        """İşlem zamanlayıcısını başlat"""
        self.metrics[operation] = {"start": time.time()}
    
    def end_timer(self, operation: str):
        """İşlem zamanlayıcısını bitir"""
        if operation in self.metrics:
            elapsed = time.time() - self.metrics[operation]["start"]
            self.metrics[operation]["elapsed"] = elapsed
            return elapsed
        return 0
    
    def get_metrics(self):
        """Metrikleri getir"""
        return self.metrics.copy()
    
    def clear_metrics(self):
        """Metrikleri temizle"""
        self.metrics.clear()


# Global instances
logger = Logger()
notification_manager = NotificationManager()
performance_monitor = PerformanceMonitor()
