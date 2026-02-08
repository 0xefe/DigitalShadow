"""
Digital Shadow - Main GUI Application
Modern PyQt5 masaüstü uygulaması
"""

import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from datetime import datetime
import json

# Modülleri import et
import config
import utils
from database import db
from analyzer import analyzer
from visualizer import visualizer
from report_generator import report_generator
from advanced_features import (
    logger, AnimationHelper, ShortcutManager,
    AnalysisWorker, SocialScanWorker, AutoRefreshManager,
    notification_manager, performance_monitor
)


class DigitalShadowApp(QMainWindow):
    """Ana uygulama penceresi"""
    
    def __init__(self):
        super().__init__()
        self.current_user = None
        self.current_user_id = None
        self.analysis_worker = None
        self.scan_worker = None
        
        # Auto refresh manager
        self.auto_refresh = AutoRefreshManager(self.refresh_dashboard, interval=30000)
        
        logger.info("Digital Shadow uygulaması başlatıldı")
        self.init_ui()
        self.setup_shortcuts()
    
    def init_ui(self):
        """UI'ı başlat"""
        self.setWindowTitle(f"{config.APP_NAME} v{config.APP_VERSION}")
        self.setGeometry(100, 100, config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
        self.setMinimumSize(config.WINDOW_MIN_WIDTH, config.WINDOW_MIN_HEIGHT)
        
        # İkon ayarla
        icon_path = os.path.join(os.path.dirname(__file__), "assets", "logo.svg")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        # Stil uygula
        self.apply_stylesheet()
        
        # Ana widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Ana layout
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        # Stacked widget (sayfa geçişleri için)
        self.stacked_widget = QStackedWidget()
        self.main_layout.addWidget(self.stacked_widget)
        
        # Sayfaları oluştur
        self.create_login_page()
        self.create_dashboard_page()
        self.create_analysis_page()
        self.create_history_page()
        self.create_social_scan_page()
        self.create_settings_page()
        self.create_comparison_page()
        
        # Login sayfasını göster
        self.stacked_widget.setCurrentIndex(0)
        
        # Status bar
        self.statusBar().showMessage("Hazır")
        
        logger.info("UI başarıyla oluşturuldu")
    
    def apply_stylesheet(self):
        """Dark theme stylesheet"""
        style = f"""
        QMainWindow {{
            background-color: {config.COLORS['bg_dark']};
        }}
        QWidget {{
            background-color: {config.COLORS['bg_dark']};
            color: {config.COLORS['text_primary']};
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 11pt;
        }}
        QPushButton {{
            background-color: {config.COLORS['primary']};
            color: white;
            border: none;
            border-radius: 8px;
            padding: 12px 24px;
            font-weight: bold;
            font-size: 11pt;
        }}
        QPushButton:hover {{
            background-color: {config.COLORS['secondary']};
        }}
        QPushButton:pressed {{
            background-color: #7c3aed;
        }}
        QLineEdit, QTextEdit {{
            background-color: {config.COLORS['bg_medium']};
            color: {config.COLORS['text_primary']};
            border: 2px solid {config.COLORS['border']};
            border-radius: 8px;
            padding: 10px;
            font-size: 11pt;
        }}
        QLineEdit:focus, QTextEdit:focus {{
            border: 2px solid {config.COLORS['primary']};
        }}
        QLabel {{
            color: {config.COLORS['text_primary']};
        }}
        QTabWidget::pane {{
            border: 1px solid {config.COLORS['border']};
            background-color: {config.COLORS['bg_medium']};
            border-radius: 8px;
        }}
        QTabBar::tab {{
            background-color: {config.COLORS['bg_light']};
            color: {config.COLORS['text_secondary']};
            padding: 10px 20px;
            margin-right: 2px;
            border-top-left-radius: 8px;
            border-top-right-radius: 8px;
        }}
        QTabBar::tab:selected {{
            background-color: {config.COLORS['primary']};
            color: white;
        }}
        QScrollBar:vertical {{
            background-color: {config.COLORS['bg_medium']};
            width: 12px;
            border-radius: 6px;
        }}
        QScrollBar::handle:vertical {{
            background-color: {config.COLORS['border']};
            border-radius: 6px;
        }}
        """
        self.setStyleSheet(style)
    
    # ==================== LOGIN PAGE ====================
    
    def create_login_page(self):
        """Login/Register sayfası"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setAlignment(Qt.AlignCenter)
        
        # Logo ve başlık
        title = QLabel("🔒 Digital Shadow")
        title.setStyleSheet(f"font-size: 32pt; font-weight: bold; color: {config.COLORS['primary']};")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        subtitle = QLabel("Dijital Ayak İzinizi Keşfedin")
        subtitle.setStyleSheet(f"font-size: 14pt; color: {config.COLORS['text_secondary']}; margin-bottom: 30px;")
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)
        
        # Form container
        form_container = QWidget()
        form_container.setMaximumWidth(400)
        form_container.setStyleSheet(f"""
            background-color: {config.COLORS['bg_medium']};
            border-radius: 12px;
            padding: 30px;
        """)
        form_layout = QVBoxLayout(form_container)
        
        # Username
        username_label = QLabel("Kullanıcı Adı")
        username_label.setStyleSheet("font-weight: bold; margin-bottom: 5px;")
        form_layout.addWidget(username_label)
        
        self.login_username = QLineEdit()
        self.login_username.setPlaceholderText("kullanici_adi")
        form_layout.addWidget(self.login_username)
        
        form_layout.addSpacing(20)
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        login_btn = QPushButton("Giriş Yap")
        login_btn.clicked.connect(self.handle_login)
        btn_layout.addWidget(login_btn)
        
        register_btn = QPushButton("Kayıt Ol")
        register_btn.setStyleSheet(f"background-color: {config.COLORS['secondary']};")
        register_btn.clicked.connect(self.handle_register)
        btn_layout.addWidget(register_btn)
        
        form_layout.addLayout(btn_layout)
        
        layout.addWidget(form_container, alignment=Qt.AlignCenter)
        
        # Version info
        version_label = QLabel(f"v{config.APP_VERSION}")
        version_label.setStyleSheet(f"color: {config.COLORS['text_muted']}; margin-top: 20px;")
        version_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(version_label)
        
        self.stacked_widget.addWidget(page)
    
    def handle_login(self):
        """Giriş işlemi"""
        username = self.login_username.text().strip()
        
        # Validasyon
        is_valid, error = utils.validate_username(username)
        if not is_valid:
            QMessageBox.warning(self, "Hata", error)
            return
        
        # Kullanıcıyı kontrol et
        user = db.get_user(username)
        if not user:
            QMessageBox.warning(self, "Hata", "Kullanıcı bulunamadı! Önce kayıt olun.")
            return
        
        # Giriş başarılı
        self.current_user = username
        self.current_user_id = user['id']
        db.update_last_login(self.current_user_id)
        
        logger.info(f"Kullanıcı girişi: {username}")
        notification_manager.add_notification(
            "Hoş Geldiniz",
            f"Merhaba {username}!",
            "success"
        )
        
        # Dashboard'a geç
        self.load_dashboard()
        self.stacked_widget.setCurrentIndex(1)
        
        # Auto refresh başlat
        self.auto_refresh.start()
        self.statusBar().showMessage(f"Giriş yapıldı: {username}")
    
    def handle_register(self):
        """Kayıt işlemi"""
        username = self.login_username.text().strip()
        
        # Validasyon
        is_valid, error = utils.validate_username(username)
        if not is_valid:
            QMessageBox.warning(self, "Hata", error)
            return
        
        # Kullanıcı oluştur
        user_id = db.create_user(username, "", "")
        if not user_id:
            QMessageBox.warning(self, "Hata", "Bu kullanıcı adı zaten kullanılıyor!")
            return
        
        # Başarılı
        QMessageBox.information(self, "Başarılı", f"Hoş geldiniz {username}! Şimdi giriş yapabilirsiniz.")
        self.login_username.clear()
    
    # ==================== DASHBOARD PAGE ====================
    
    def create_dashboard_page(self):
        """Dashboard sayfası"""
        page = QWidget()
        layout = QVBoxLayout(page)
        
        # Header
        header = self.create_header("📊 Dashboard")
        layout.addWidget(header)
        
        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none;")
        
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        
        # Stats cards
        stats_layout = QHBoxLayout()
        
        self.stat_total_analyses = self.create_stat_card("Toplam Analiz", "0", config.COLORS['primary'])
        self.stat_avg_privacy = self.create_stat_card("Ort. Gizlilik", "0", config.COLORS['warning'])
        self.stat_avg_risk = self.create_stat_card("Ort. Risk", "0", config.COLORS['danger'])
        
        stats_layout.addWidget(self.stat_total_analyses)
        stats_layout.addWidget(self.stat_avg_privacy)
        stats_layout.addWidget(self.stat_avg_risk)
        
        scroll_layout.addLayout(stats_layout)
        
        # Quick actions
        actions_label = QLabel("⚡ Hızlı İşlemler")
        actions_label.setStyleSheet("font-size: 16pt; font-weight: bold; margin-top: 20px;")
        scroll_layout.addWidget(actions_label)
        
        actions_layout = QHBoxLayout()
        
        analyze_btn = QPushButton("📝 Yeni Analiz")
        analyze_btn.setMinimumHeight(60)
        analyze_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        actions_layout.addWidget(analyze_btn)
        
        history_btn = QPushButton("📜 Geçmiş")
        history_btn.setMinimumHeight(60)
        history_btn.clicked.connect(lambda: self.show_history())
        actions_layout.addWidget(history_btn)
        
        social_btn = QPushButton("🔍 Sosyal Medya Tara")
        social_btn.setMinimumHeight(60)
        social_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(4))
        actions_layout.addWidget(social_btn)
        
        settings_btn = QPushButton("⚙️ Ayarlar")
        settings_btn.setMinimumHeight(60)
        settings_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(5))
        actions_layout.addWidget(settings_btn)
        
        scroll_layout.addLayout(actions_layout)
        
        # Recent activity
        recent_label = QLabel("📌 Son Aktiviteler")
        recent_label.setStyleSheet("font-size: 16pt; font-weight: bold; margin-top: 20px;")
        scroll_layout.addWidget(recent_label)
        
        self.recent_activity_list = QListWidget()
        self.recent_activity_list.setMaximumHeight(200)
        self.recent_activity_list.setStyleSheet(f"""
            background-color: {config.COLORS['bg_medium']};
            border-radius: 8px;
            padding: 10px;
        """)
        scroll_layout.addWidget(self.recent_activity_list)
        
        # Trend grafiği
        trend_label = QLabel("📈 Trend Analizi")
        trend_label.setStyleSheet("font-size: 16pt; font-weight: bold; margin-top: 20px;")
        scroll_layout.addWidget(trend_label)
        
        self.trend_chart_container = QWidget()
        self.trend_chart_layout = QVBoxLayout(self.trend_chart_container)
        self.trend_chart_layout.setContentsMargins(0, 0, 0, 0)
        scroll_layout.addWidget(self.trend_chart_container)
        
        # Hızlı karşılaştırma butonu
        quick_compare_btn = QPushButton("🔍 Detaylı Karşılaştırma")
        quick_compare_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(6))
        scroll_layout.addWidget(quick_compare_btn)
        
        scroll_layout.addStretch()
        
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)
        
        self.stacked_widget.addWidget(page)
    
    def create_header(self, title):
        """Sayfa başlığı oluştur"""
        header = QWidget()
        header.setStyleSheet(f"background-color: {config.COLORS['bg_medium']}; padding: 15px;")
        header_layout = QHBoxLayout(header)
        
        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 18pt; font-weight: bold;")
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        if self.current_user:
            user_label = QLabel(f"👤 {self.current_user}")
            user_label.setStyleSheet(f"color: {config.COLORS['text_secondary']};")
            header_layout.addWidget(user_label)
            
            logout_btn = QPushButton("Çıkış")
            logout_btn.setMaximumWidth(100)
            logout_btn.clicked.connect(self.handle_logout)
            header_layout.addWidget(logout_btn)
        
        return header
    
    def create_stat_card(self, title, value, color):
        """İstatistik kartı oluştur"""
        card = QWidget()
        card.setStyleSheet(f"""
            background-color: {config.COLORS['bg_medium']};
            border-left: 4px solid {color};
            border-radius: 8px;
            padding: 20px;
        """)
        
        layout = QVBoxLayout(card)
        
        title_label = QLabel(title)
        title_label.setStyleSheet(f"color: {config.COLORS['text_secondary']}; font-size: 10pt;")
        layout.addWidget(title_label)
        
        value_label = QLabel(value)
        value_label.setStyleSheet(f"color: {color}; font-size: 24pt; font-weight: bold;")
        value_label.setObjectName("stat_value")
        layout.addWidget(value_label)
        
        return card
    
    def load_dashboard(self):
        """Dashboard verilerini yükle"""
        if not self.current_user_id:
            return
        
        # İstatistikleri al
        stats = db.get_analysis_stats(self.current_user_id)
        
        # Kartları güncelle
        self.stat_total_analyses.findChild(QLabel, "stat_value").setText(str(stats['total_analyses']))
        self.stat_avg_privacy.findChild(QLabel, "stat_value").setText(f"{stats['avg_privacy_score']:.1f}")
        self.stat_avg_risk.findChild(QLabel, "stat_value").setText(f"{stats['avg_risk']:.2f}")
        
        # Son aktiviteleri yükle
        self.recent_activity_list.clear()
        analyses = db.get_user_analyses(self.current_user_id, limit=5)
        
        for analysis in analyses:
            date_str = utils.format_datetime(analysis['created_at'])
            item_text = f"{date_str} - {analysis['dominant_trait'].title()} (Risk: {analysis['risk']:.2f})"
            self.recent_activity_list.addItem(item_text)
        
        # Trend grafiğini yükle
        self.load_trend_chart(analyses)
    
    def handle_logout(self):
        """Çıkış işlemi"""
        self.auto_refresh.stop()
        logger.info(f"Kullanıcı çıkışı: {self.current_user}")
        
        self.current_user = None
        self.current_user_id = None
        self.login_username.clear()
        self.stacked_widget.setCurrentIndex(0)
        self.statusBar().showMessage("Çıkış yapıldı")
    
    def setup_shortcuts(self):
        """Klavye kısayollarını ayarla"""
        from PyQt5.QtWidgets import QShortcut
        from PyQt5.QtGui import QKeySequence
        
        # Yeni analiz
        new_analysis = QShortcut(QKeySequence(ShortcutManager.get_shortcut("new_analysis")), self)
        new_analysis.activated.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        
        # Rapor kaydet
        save_report = QShortcut(QKeySequence(ShortcutManager.get_shortcut("save_report")), self)
        save_report.activated.connect(self.export_latest_report)
        
        # Veri export
        export_data = QShortcut(QKeySequence(ShortcutManager.get_shortcut("export_data")), self)
        export_data.activated.connect(self.export_data)
        
        # Yenile
        refresh = QShortcut(QKeySequence(ShortcutManager.get_shortcut("refresh")), self)
        refresh.activated.connect(self.refresh_dashboard)
        
        # Ayarlar
        settings = QShortcut(QKeySequence(ShortcutManager.get_shortcut("settings")), self)
        settings.activated.connect(lambda: self.stacked_widget.setCurrentIndex(5))
        
        # Çıkış
        quit_app = QShortcut(QKeySequence(ShortcutManager.get_shortcut("quit")), self)
        quit_app.activated.connect(self.close)
        
        logger.info("Klavye kısayolları ayarlandı")
    
    def refresh_dashboard(self):
        """Dashboard'u yenile"""
        if self.current_user_id:
            self.load_dashboard()
            self.statusBar().showMessage("Dashboard yenilendi", 2000)
            logger.debug("Dashboard yenilendi")
    
    def load_trend_chart(self, analyses):
        """Trend grafiğini yükle"""
        # Önceki grafiği temizle
        for i in reversed(range(self.trend_chart_layout.count())):
            widget = self.trend_chart_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        
        if not analyses or len(analyses) < 2:
            no_data_label = QLabel("Trend analizi için en az 2 analiz gerekli")
            no_data_label.setAlignment(Qt.AlignCenter)
            no_data_label.setStyleSheet(f"color: {config.COLORS['text_muted']}; padding: 20px;")
            self.trend_chart_layout.addWidget(no_data_label)
            return
        
        try:
            # Trend grafiği oluştur
            fig = visualizer.create_history_timeline(analyses)
            canvas = FigureCanvas(fig)
            canvas.setMaximumHeight(300)
            self.trend_chart_layout.addWidget(canvas)
        except Exception as e:
            print(f"Trend chart error: {e}")
    
    # ==================== ANALYSIS PAGE ====================
    
    def create_analysis_page(self):
        """Analiz sayfası"""
        page = QWidget()
        layout = QVBoxLayout(page)
        
        # Header
        header = self.create_header("📝 Metin Analizi")
        layout.addWidget(header)
        
        # Content
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(20, 20, 20, 20)
        
        # Instruction
        instruction = QLabel("Analiz etmek istediğiniz metinleri girin (sosyal medya gönderileri, yorumlar, vb.)")
        instruction.setStyleSheet(f"color: {config.COLORS['text_secondary']}; margin-bottom: 10px;")
        content_layout.addWidget(instruction)
        
        # Text input
        self.analysis_text = QTextEdit()
        self.analysis_text.setPlaceholderText("Metninizi buraya yazın...")
        self.analysis_text.setMinimumHeight(200)
        content_layout.addWidget(self.analysis_text)
        
        # Analyze button
        analyze_btn = QPushButton("🔍 Analiz Et")
        analyze_btn.setMinimumHeight(50)
        analyze_btn.clicked.connect(self.perform_analysis)
        content_layout.addWidget(analyze_btn)
        
        # Results area
        self.analysis_results = QWidget()
        self.analysis_results_layout = QVBoxLayout(self.analysis_results)
        self.analysis_results.hide()
        
        content_layout.addWidget(self.analysis_results)
        content_layout.addStretch()
        
        layout.addWidget(content)
        
        self.stacked_widget.addWidget(page)
    
    def perform_analysis(self):
        """Analiz gerçekleştir"""
        text = self.analysis_text.toPlainText().strip()
        
        # Validasyon
        is_valid, error = utils.validate_text(text)
        if not is_valid:
            QMessageBox.warning(self, "Hata", error)
            return
        
        # Analiz yap
        try:
            result = analyzer.analyze_text([text])
            
            # Veritabanına kaydet
            db.save_analysis(
                self.current_user_id,
                result['aggression'],
                result['positivity'],
                result['risk'],
                result['dominant_trait'],
                result['ai_comment'],
                text
            )
            
            # Sonuçları göster
            self.show_analysis_results(result)
            
            # Dashboard'u güncelle
            self.load_dashboard()
            
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Analiz sırasında hata: {str(e)}")
    
    def show_analysis_results(self, result):
        """Analiz sonuçlarını göster"""
        # Önceki sonuçları temizle
        for i in reversed(range(self.analysis_results_layout.count())): 
            self.analysis_results_layout.itemAt(i).widget().setParent(None)
        
        # Başlık
        title = QLabel("✅ Analiz Tamamlandı")
        title.setStyleSheet(f"font-size: 16pt; font-weight: bold; color: {config.COLORS['success']};")
        self.analysis_results_layout.addWidget(title)
        
        # Skorlar
        scores_widget = QWidget()
        scores_layout = QGridLayout(scores_widget)
        
        scores_layout.addWidget(QLabel("Agresiflik:"), 0, 0)
        scores_layout.addWidget(QLabel(f"{result['aggression']:.2f}"), 0, 1)
        
        scores_layout.addWidget(QLabel("Pozitiflik:"), 1, 0)
        scores_layout.addWidget(QLabel(f"{result['positivity']:.2f}"), 1, 1)
        
        scores_layout.addWidget(QLabel("Risk:"), 2, 0)
        scores_layout.addWidget(QLabel(f"{result['risk']:.2f}"), 2, 1)
        
        scores_layout.addWidget(QLabel("Dominant:"), 3, 0)
        scores_layout.addWidget(QLabel(result['dominant_trait'].title()), 3, 1)
        
        self.analysis_results_layout.addWidget(scores_widget)
        
        # AI Yorumu
        comment_label = QLabel("🤖 AI Yorumu:")
        comment_label.setStyleSheet("font-weight: bold; margin-top: 15px;")
        self.analysis_results_layout.addWidget(comment_label)
        
        comment_text = QLabel(result['ai_comment'])
        comment_text.setWordWrap(True)
        comment_text.setStyleSheet(f"""
            background-color: {config.COLORS['bg_medium']};
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid {config.COLORS['primary']};
        """)
        self.analysis_results_layout.addWidget(comment_text)
        
        # Grafik göster
        try:
            fig = visualizer.create_score_chart(
                result['aggression'],
                result['positivity'],
                result['risk'],
                result.get('neutral', 0)
            )
            
            canvas = FigureCanvas(fig)
            canvas.setMaximumHeight(400)
            self.analysis_results_layout.addWidget(canvas)
        except Exception as e:
            print(f"Chart error: {e}")
        
        self.analysis_results.show()
    
    # ==================== HISTORY PAGE ====================
    
    def create_history_page(self):
        """Geçmiş sayfası"""
        page = QWidget()
        layout = QVBoxLayout(page)
        
        # Header
        header = self.create_header("📜 Analiz Geçmişi")
        layout.addWidget(header)
        
        # Content
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(20, 20, 20, 20)
        
        # History list
        self.history_list = QListWidget()
        self.history_list.setStyleSheet(f"""
            background-color: {config.COLORS['bg_medium']};
            border-radius: 8px;
            padding: 10px;
        """)
        content_layout.addWidget(self.history_list)
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        refresh_btn = QPushButton("🔄 Yenile")
        refresh_btn.clicked.connect(self.show_history)
        btn_layout.addWidget(refresh_btn)
        
        export_btn = QPushButton("📄 PDF Rapor Oluştur")
        export_btn.clicked.connect(self.export_latest_report)
        btn_layout.addWidget(export_btn)
        
        back_btn = QPushButton("⬅️ Geri")
        back_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        btn_layout.addWidget(back_btn)
        
        content_layout.addLayout(btn_layout)
        
        layout.addWidget(content)
        
        self.stacked_widget.addWidget(page)
    
    def show_history(self):
        """Geçmişi göster"""
        self.stacked_widget.setCurrentIndex(3)
        self.history_list.clear()
        
        if not self.current_user_id:
            return
        
        analyses = db.get_user_analyses(self.current_user_id, limit=50)
        
        for analysis in analyses:
            date_str = utils.format_datetime(analysis['created_at'])
            item_text = (
                f"{date_str} | "
                f"Dominant: {analysis['dominant_trait'].title()} | "
                f"Aggr: {analysis['aggression']:.2f} | "
                f"Pos: {analysis['positivity']:.2f} | "
                f"Risk: {analysis['risk']:.2f} | "
                f"Privacy: {analysis['privacy_score']:.1f}"
            )
            self.history_list.addItem(item_text)
    
    def export_latest_report(self):
        """Son analizi PDF olarak kaydet"""
        if not self.current_user_id:
            return
        
        analyses = db.get_user_analyses(self.current_user_id, limit=1)
        if not analyses:
            QMessageBox.warning(self, "Uyarı", "Henüz analiz yok!")
            return
        
        latest = analyses[0]
        
        # Dosya adı
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"digital_shadow_report_{self.current_user}_{timestamp}.pdf"
        
        # Dosya kaydetme dialogu
        filepath, _ = QFileDialog.getSaveFileName(
            self,
            "PDF Raporu Kaydet",
            filename,
            "PDF Files (*.pdf)"
        )
        
        if not filepath:
            return
        
        # Rapor oluştur
        user_data = {"username": self.current_user}
        
        success = report_generator.generate_analysis_report(
            filepath,
            user_data,
            latest
        )
        
        if success:
            QMessageBox.information(self, "Başarılı", f"Rapor kaydedildi:\n{filepath}")
        else:
            QMessageBox.critical(self, "Hata", "Rapor oluşturulamadı!")
    
    # ==================== SOCIAL SCAN PAGE ====================
    
    def create_social_scan_page(self):
        """Sosyal medya tarama sayfası"""
        page = QWidget()
        layout = QVBoxLayout(page)
        
        # Header
        header = self.create_header("🔍 Sosyal Medya Tarama")
        layout.addWidget(header)
        
        # Content
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(20, 20, 20, 20)
        
        # Instruction
        instruction = QLabel("Aramak istediğiniz kullanıcı adını girin")
        instruction.setStyleSheet(f"color: {config.COLORS['text_secondary']}; margin-bottom: 10px;")
        content_layout.addWidget(instruction)
        
        # Username input
        self.scan_username = QLineEdit()
        self.scan_username.setPlaceholderText("kullanici_adi")
        content_layout.addWidget(self.scan_username)
        
        # Scan button
        scan_btn = QPushButton("🔍 Tara")
        scan_btn.setMinimumHeight(50)
        scan_btn.clicked.connect(self.perform_social_scan)
        content_layout.addWidget(scan_btn)
        
        # Results
        self.scan_results = QTextEdit()
        self.scan_results.setReadOnly(True)
        self.scan_results.setMinimumHeight(300)
        content_layout.addWidget(self.scan_results)
        
        # Back button
        back_btn = QPushButton("⬅️ Dashboard'a Dön")
        back_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        content_layout.addWidget(back_btn)
        
        content_layout.addStretch()
        
        layout.addWidget(content)
        
        self.stacked_widget.addWidget(page)
    
    def perform_social_scan(self):
        """Sosyal medya taraması yap"""
        username = self.scan_username.text().strip()
        
        if not username:
            QMessageBox.warning(self, "Hata", "Kullanıcı adı boş olamaz!")
            return
        
        # Tarama yap
        self.scan_results.clear()
        self.scan_results.append("🔍 Tarama başlatıldı...\n")
        QApplication.processEvents()
        
        results = analyzer.scan_social_media(username, config.SOCIAL_PLATFORMS)
        
        self.scan_results.append(f"\n📊 Tarama Sonuçları ({username}):\n")
        self.scan_results.append("=" * 50 + "\n")
        
        for result in results:
            # Veritabanına kaydet
            db.save_social_scan(
                self.current_user_id,
                result['platform'],
                result['username'],
                result['found'],
                result['risk_score'],
                result['details']
            )
            
            # Sonuçları göster
            status = "✅ Bulundu" if result['found'] else "❌ Bulunamadı"
            self.scan_results.append(f"\n{result['platform']}: {status}")
            
            if result['found']:
                self.scan_results.append(f"  Risk Skoru: {result['risk_score']:.2f}")
                self.scan_results.append(f"  Detay: {result['details']}")
        
        self.scan_results.append("\n" + "=" * 50)
        self.scan_results.append("\n✅ Tarama tamamlandı!")
    
    # ==================== SETTINGS PAGE ====================
    
    def create_settings_page(self):
        """Ayarlar sayfası"""
        page = QWidget()
        layout = QVBoxLayout(page)
        
        # Header
        header = self.create_header("⚙️ Ayarlar")
        layout.addWidget(header)
        
        # Content
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(20, 20, 20, 20)
        
        # Tabs
        tabs = QTabWidget()
        
        # Genel ayarlar
        general_tab = QWidget()
        general_layout = QVBoxLayout(general_tab)
        
        general_layout.addWidget(QLabel("🎨 Tema Ayarları"))
        theme_combo = QComboBox()
        theme_combo.addItems(["Dark Mode", "Light Mode"])
        general_layout.addWidget(theme_combo)
        
        general_layout.addSpacing(20)
        general_layout.addWidget(QLabel("📊 Varsayılan Grafik Tipi"))
        chart_combo = QComboBox()
        chart_combo.addItems(["Çubuk Grafik", "Radar Grafik", "Pasta Grafik"])
        general_layout.addWidget(chart_combo)
        
        general_layout.addStretch()
        tabs.addTab(general_tab, "Genel")
        
        # Veri yönetimi
        data_tab = QWidget()
        data_layout = QVBoxLayout(data_tab)
        
        export_btn = QPushButton("📤 Verileri Dışa Aktar (JSON)")
        export_btn.clicked.connect(self.export_data)
        data_layout.addWidget(export_btn)
        
        import_btn = QPushButton("📥 Verileri İçe Aktar (JSON)")
        import_btn.clicked.connect(self.import_data)
        data_layout.addWidget(import_btn)
        
        data_layout.addSpacing(20)
        
        clear_btn = QPushButton("🗑️ Tüm Verileri Temizle")
        clear_btn.setStyleSheet(f"background-color: {config.COLORS['danger']};")
        clear_btn.clicked.connect(self.clear_all_data)
        data_layout.addWidget(clear_btn)
        
        data_layout.addStretch()
        tabs.addTab(data_tab, "Veri Yönetimi")
        
        # Hakkında
        about_tab = QWidget()
        about_layout = QVBoxLayout(about_tab)
        
        about_text = QLabel(
            f"""
            <h2>{config.APP_NAME}</h2>
            <p><b>Versiyon:</b> {config.APP_VERSION}</p>
            <p><b>Geliştirici:</b> {config.APP_AUTHOR}</p>
            <br>
            <p>Dijital ayak izinizi analiz edin ve gizliliğinizi koruyun.</p>
            <br>
            <p><i>© 2024 Digital Shadow Team</i></p>
            """
        )
        about_text.setWordWrap(True)
        about_text.setAlignment(Qt.AlignCenter)
        about_layout.addWidget(about_text)
        about_layout.addStretch()
        tabs.addTab(about_tab, "Hakkında")
        
        content_layout.addWidget(tabs)
        
        # Back button
        back_btn = QPushButton("⬅️ Dashboard'a Dön")
        back_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        content_layout.addWidget(back_btn)
        
        layout.addWidget(content)
        self.stacked_widget.addWidget(page)
    
    def export_data(self):
        """Verileri JSON olarak dışa aktar"""
        if not self.current_user_id:
            return
        
        import json
        from datetime import datetime
        
        # Dosya seç
        filename = f"digital_shadow_export_{self.current_user}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath, _ = QFileDialog.getSaveFileName(
            self,
            "Verileri Dışa Aktar",
            filename,
            "JSON Files (*.json)"
        )
        
        if not filepath:
            return
        
        try:
            # Verileri topla
            analyses = db.get_user_analyses(self.current_user_id, limit=1000)
            social_scans = db.get_social_scans(self.current_user_id)
            stats = db.get_analysis_stats(self.current_user_id)
            
            export_data = {
                "user": self.current_user,
                "export_date": datetime.now().isoformat(),
                "statistics": stats,
                "analyses": analyses,
                "social_scans": social_scans
            }
            
            # JSON'a yaz
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, ensure_ascii=False, indent=2)
            
            QMessageBox.information(self, "Başarılı", f"Veriler başarıyla dışa aktarıldı:\n{filepath}")
        
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Dışa aktarma hatası: {str(e)}")
    
    def import_data(self):
        """JSON verilerini içe aktar"""
        if not self.current_user_id:
            return
        
        import json
        
        # Dosya seç
        filepath, _ = QFileDialog.getOpenFileName(
            self,
            "Verileri İçe Aktar",
            "",
            "JSON Files (*.json)"
        )
        
        if not filepath:
            return
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                import_data = json.load(f)
            
            # Onay al
            reply = QMessageBox.question(
                self,
                "Onay",
                f"{len(import_data.get('analyses', []))} analiz içe aktarılacak. Devam edilsin mi?",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if reply == QMessageBox.No:
                return
            
            # Verileri içe aktar
            count = 0
            for analysis in import_data.get('analyses', []):
                db.save_analysis(
                    self.current_user_id,
                    analysis['aggression'],
                    analysis['positivity'],
                    analysis['risk'],
                    analysis['dominant_trait'],
                    analysis['ai_comment'],
                    ""
                )
                count += 1
            
            QMessageBox.information(self, "Başarılı", f"{count} analiz başarıyla içe aktarıldı!")
            self.load_dashboard()
        
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"İçe aktarma hatası: {str(e)}")
    
    def clear_all_data(self):
        """Tüm verileri temizle"""
        if not self.current_user_id:
            return
        
        reply = QMessageBox.warning(
            self,
            "Dikkat!",
            "Tüm analiz ve tarama verileri silinecek. Bu işlem geri alınamaz!\n\nDevam edilsin mi?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                db.cursor.execute("DELETE FROM analyses WHERE user_id = ?", (self.current_user_id,))
                db.cursor.execute("DELETE FROM social_scans WHERE user_id = ?", (self.current_user_id,))
                db.conn.commit()
                
                QMessageBox.information(self, "Başarılı", "Tüm veriler temizlendi!")
                self.load_dashboard()
            except Exception as e:
                QMessageBox.critical(self, "Hata", f"Temizleme hatası: {str(e)}")
    
    # ==================== COMPARISON PAGE ====================
    
    def create_comparison_page(self):
        """Analiz karşılaştırma sayfası"""
        page = QWidget()
        layout = QVBoxLayout(page)
        
        # Header
        header = self.create_header("📊 Analiz Karşılaştırma")
        layout.addWidget(header)
        
        # Content
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(20, 20, 20, 20)
        
        instruction = QLabel("Son analizlerinizi karşılaştırın ve trend analizi yapın")
        instruction.setStyleSheet(f"color: {config.COLORS['text_secondary']}; margin-bottom: 10px;")
        content_layout.addWidget(instruction)
        
        # Karşılaştırma butonu
        compare_btn = QPushButton("🔍 Son 5 Analizi Karşılaştır")
        compare_btn.setMinimumHeight(50)
        compare_btn.clicked.connect(self.perform_comparison)
        content_layout.addWidget(compare_btn)
        
        # Sonuç alanı
        self.comparison_results = QWidget()
        self.comparison_results_layout = QVBoxLayout(self.comparison_results)
        self.comparison_results.hide()
        content_layout.addWidget(self.comparison_results)
        
        # Back button
        back_btn = QPushButton("⬅️ Dashboard'a Dön")
        back_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        content_layout.addWidget(back_btn)
        
        content_layout.addStretch()
        layout.addWidget(content)
        
        self.stacked_widget.addWidget(page)
    
    def perform_comparison(self):
        """Analiz karşılaştırması yap"""
        if not self.current_user_id:
            return
        
        analyses = db.get_user_analyses(self.current_user_id, limit=5)
        
        if len(analyses) < 2:
            QMessageBox.warning(self, "Uyarı", "Karşılaştırma için en az 2 analiz gerekli!")
            return
        
        # Önceki sonuçları temizle
        for i in reversed(range(self.comparison_results_layout.count())):
            self.comparison_results_layout.itemAt(i).widget().setParent(None)
        
        # Trend analizi
        patterns = analyzer.detect_patterns(analyses)
        
        # Başlık
        title = QLabel("✅ Karşılaştırma Tamamlandı")
        title.setStyleSheet(f"font-size: 16pt; font-weight: bold; color: {config.COLORS['success']};")
        self.comparison_results_layout.addWidget(title)
        
        # İstatistikler
        stats_text = f"""
        <b>Ortalama Agresiflik:</b> {patterns['avg_aggression']:.2f}<br>
        <b>Ortalama Pozitiflik:</b> {patterns['avg_positivity']:.2f}<br>
        <b>Ortalama Risk:</b> {patterns['avg_risk']:.2f}<br>
        <b>Agresiflik Trendi:</b> {patterns['aggression_trend'].title()}<br>
        <b>Dominant Kalıp:</b> {patterns['dominant_pattern'].title()}<br>
        """
        
        stats_label = QLabel(stats_text)
        stats_label.setWordWrap(True)
        stats_label.setStyleSheet(f"""
            background-color: {config.COLORS['bg_medium']};
            padding: 15px;
            border-radius: 8px;
        """)
        self.comparison_results_layout.addWidget(stats_label)
        
        # AI Yorumu
        comment_label = QLabel("🤖 Trend Analizi:")
        comment_label.setStyleSheet("font-weight: bold; margin-top: 15px;")
        self.comparison_results_layout.addWidget(comment_label)
        
        comment_text = QLabel(patterns['message'])
        comment_text.setWordWrap(True)
        comment_text.setStyleSheet(f"""
            background-color: {config.COLORS['bg_medium']};
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid {config.COLORS['primary']};
        """)
        self.comparison_results_layout.addWidget(comment_text)
        
        # Grafik
        try:
            fig = visualizer.create_history_timeline(analyses)
            canvas = FigureCanvas(fig)
            canvas.setMaximumHeight(400)
            self.comparison_results_layout.addWidget(canvas)
        except Exception as e:
            print(f"Chart error: {e}")
        
        self.comparison_results.show()


def main():
    """Ana fonksiyon"""
    app = QApplication(sys.argv)
    
    # Font ayarları
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    # Ana pencereyi oluştur
    window = DigitalShadowApp()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
