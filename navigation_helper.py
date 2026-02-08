"""
Digital Shadow - Navigation Helper
Her sayfaya kolay navigasyon ekler
"""

from PyQt5.QtWidgets import QPushButton, QHBoxLayout, QWidget
from PyQt5.QtCore import Qt


def create_navigation_bar(parent_app, current_page=""):
    """
    Navigasyon çubuğu oluştur
    
    Args:
        parent_app: Ana uygulama referansı
        current_page: Şu anki sayfa adı
    
    Returns:
        QWidget: Navigasyon çubuğu
    """
    nav_widget = QWidget()
    nav_layout = QHBoxLayout(nav_widget)
    nav_layout.setContentsMargins(10, 10, 10, 10)
    nav_layout.setSpacing(10)
    
    # Buton stilleri
    button_style = """
        QPushButton {
            background-color: #6366f1;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 10px 20px;
            font-weight: bold;
            font-size: 10pt;
            min-width: 120px;
        }
        QPushButton:hover {
            background-color: #4f46e5;
        }
        QPushButton:pressed {
            background-color: #4338ca;
        }
    """
    
    active_style = """
        QPushButton {
            background-color: #10b981;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 10px 20px;
            font-weight: bold;
            font-size: 10pt;
            min-width: 120px;
        }
    """
    
    # Dashboard butonu
    dash_btn = QPushButton("🏠 Dashboard")
    dash_btn.setStyleSheet(active_style if current_page == "dashboard" else button_style)
    dash_btn.clicked.connect(lambda: parent_app.stacked_widget.setCurrentIndex(1))
    nav_layout.addWidget(dash_btn)
    
    # Analiz butonu
    analysis_btn = QPushButton("📝 Analiz")
    analysis_btn.setStyleSheet(active_style if current_page == "analysis" else button_style)
    analysis_btn.clicked.connect(lambda: parent_app.stacked_widget.setCurrentIndex(2))
    nav_layout.addWidget(analysis_btn)
    
    # Geçmiş butonu
    history_btn = QPushButton("📜 Geçmiş")
    history_btn.setStyleSheet(active_style if current_page == "history" else button_style)
    history_btn.clicked.connect(lambda: parent_app.stacked_widget.setCurrentIndex(3))
    nav_layout.addWidget(history_btn)
    
    # Sosyal Medya butonu
    social_btn = QPushButton("🔍 Sosyal Medya")
    social_btn.setStyleSheet(active_style if current_page == "social" else button_style)
    social_btn.clicked.connect(lambda: parent_app.stacked_widget.setCurrentIndex(4))
    nav_layout.addWidget(social_btn)
    
    # Karşılaştırma butonu
    compare_btn = QPushButton("📊 Karşılaştırma")
    compare_btn.setStyleSheet(active_style if current_page == "comparison" else button_style)
    compare_btn.clicked.connect(lambda: parent_app.stacked_widget.setCurrentIndex(6))
    nav_layout.addWidget(compare_btn)
    
    # Ayarlar butonu
    settings_btn = QPushButton("⚙️ Ayarlar")
    settings_btn.setStyleSheet(active_style if current_page == "settings" else button_style)
    settings_btn.clicked.connect(lambda: parent_app.stacked_widget.setCurrentIndex(5))
    nav_layout.addWidget(settings_btn)
    
    nav_layout.addStretch()
    
    return nav_widget


def create_quick_nav_button(parent_app, text, icon, page_index):
    """
    Hızlı navigasyon butonu oluştur
    
    Args:
        parent_app: Ana uygulama referansı
        text: Buton metni
        icon: Emoji icon
        page_index: Sayfa indeksi
    
    Returns:
        QPushButton: Navigasyon butonu
    """
    btn = QPushButton(f"{icon} {text}")
    btn.setStyleSheet("""
        QPushButton {
            background-color: #10b981;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 12px 24px;
            font-weight: bold;
            font-size: 11pt;
        }
        QPushButton:hover {
            background-color: #059669;
        }
    """)
    btn.clicked.connect(lambda: parent_app.stacked_widget.setCurrentIndex(page_index))
    return btn
