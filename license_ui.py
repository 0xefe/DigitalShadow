"""
Digital Shadow - License UI Components
Lisans yönetimi için UI bileşenleri
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QLineEdit, QMessageBox, QGroupBox,
                             QProgressBar, QTextEdit)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import config


class LicenseDialog(QDialog):
    """Lisans yönetimi dialog'u"""
    
    def __init__(self, parent, license_manager, user_id):
        super().__init__(parent)
        self.license_manager = license_manager
        self.user_id = user_id
        self.init_ui()
    
    def init_ui(self):
        """UI'ı başlat"""
        self.setWindowTitle("🔑 Lisans Yönetimi")
        self.setMinimumWidth(600)
        self.setMinimumHeight(500)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        
        # Başlık
        title = QLabel("Digital Shadow - Lisans Yönetimi")
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Mevcut lisans bilgisi
        self.create_current_license_section(layout)
        
        # Kullanım istatistikleri
        self.create_usage_stats_section(layout)
        
        # Lisans aktivasyon
        self.create_activation_section(layout)
        
        # Upgrade butonları
        self.create_upgrade_section(layout)
        
        # Kapat butonu
        close_btn = QPushButton("Kapat")
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)
    
    def create_current_license_section(self, layout):
        """Mevcut lisans bilgisi"""
        group = QGroupBox("📋 Mevcut Lisansınız")
        group_layout = QVBoxLayout(group)
        
        license_info = self.license_manager.get_user_license(self.user_id)
        
        # Lisans tipi
        license_type = license_info["license_type"].upper()
        type_label = QLabel(f"<h2>🎯 {license_type}</h2>")
        type_label.setStyleSheet(f"color: {config.COLORS['primary']};")
        group_layout.addWidget(type_label)
        
        # Lisans anahtarı
        key_label = QLabel(f"🔑 Anahtar: {license_info['license_key']}")
        group_layout.addWidget(key_label)
        
        # Bitiş tarihi
        if license_info["end_date"]:
            end_label = QLabel(f"📅 Bitiş: {license_info['end_date'][:10]}")
            group_layout.addWidget(end_label)
        else:
            lifetime_label = QLabel("♾️ Ömür Boyu Lisans")
            lifetime_label.setStyleSheet("color: #10b981; font-weight: bold;")
            group_layout.addWidget(lifetime_label)
        
        layout.addWidget(group)
    
    def create_usage_stats_section(self, layout):
        """Kullanım istatistikleri"""
        group = QGroupBox("📊 Bugünkü Kullanım")
        group_layout = QVBoxLayout(group)
        
        remaining = self.license_manager.get_remaining_limits(self.user_id)
        license_info = self.license_manager.get_user_license(self.user_id)
        limits = license_info["limits"]
        
        # Günlük analiz
        if limits["daily_analysis"] == -1:
            analysis_text = "Analiz: ♾️ Sınırsız"
        else:
            analysis_text = f"Analiz: {remaining['daily_analysis']}/{limits['daily_analysis']} kaldı"
        
        analysis_label = QLabel(analysis_text)
        group_layout.addWidget(analysis_label)
        
        if limits["daily_analysis"] != -1:
            progress = QProgressBar()
            used = limits["daily_analysis"] - remaining["daily_analysis"]
            progress.setMaximum(limits["daily_analysis"])
            progress.setValue(used)
            group_layout.addWidget(progress)
        
        # PDF raporlar
        if limits["pdf_reports"] == -1:
            pdf_text = "PDF Rapor: ♾️ Sınırsız"
        else:
            pdf_text = f"PDF Rapor: {remaining['pdf_reports']}/{limits['pdf_reports']} kaldı"
        
        pdf_label = QLabel(pdf_text)
        group_layout.addWidget(pdf_label)
        
        # Platform sayısı
        platform_label = QLabel(f"Platform: {remaining['platforms']} platform taranabilir")
        group_layout.addWidget(platform_label)
        
        layout.addWidget(group)
    
    def create_activation_section(self, layout):
        """Lisans aktivasyon bölümü"""
        group = QGroupBox("🔓 Lisans Anahtarı Aktive Et")
        group_layout = QVBoxLayout(group)
        
        info_label = QLabel("Satın aldığınız lisans anahtarını buraya girin:")
        group_layout.addWidget(info_label)
        
        input_layout = QHBoxLayout()
        self.license_input = QLineEdit()
        self.license_input.setPlaceholderText("PROF-XXXX-XXXX-XXXX-XXXX")
        input_layout.addWidget(self.license_input)
        
        activate_btn = QPushButton("Aktive Et")
        activate_btn.clicked.connect(self.activate_license)
        input_layout.addWidget(activate_btn)
        
        group_layout.addLayout(input_layout)
        layout.addWidget(group)
    
    def create_upgrade_section(self, layout):
        """Upgrade butonları"""
        group = QGroupBox("⬆️ Planınızı Yükseltin")
        group_layout = QVBoxLayout(group)
        
        plans_text = QTextEdit()
        plans_text.setReadOnly(True)
        plans_text.setMaximumHeight(200)
        plans_text.setHtml("""
        <h3>💎 Starter - $4.99/ay</h3>
        <ul>
            <li>10 analiz/gün</li>
            <li>15 platform tarama</li>
            <li>10 PDF rapor/gün</li>
            <li>90 gün geçmiş</li>
        </ul>
        
        <h3>🚀 Professional - $9.99/ay</h3>
        <ul>
            <li>♾️ Sınırsız analiz</li>
            <li>28 platform tarama</li>
            <li>♾️ Sınırsız PDF rapor</li>
            <li>♾️ Sınırsız geçmiş</li>
            <li>API erişimi</li>
            <li>Öncelikli destek</li>
        </ul>
        
        <h3>💼 Business - $99/ay</h3>
        <ul>
            <li>Professional +</li>
            <li>10 kullanıcı</li>
            <li>Takım özellikleri</li>
            <li>Özel eğitim</li>
        </ul>
        
        <h3>♾️ Lifetime - $299 (Tek Seferlik)</h3>
        <ul>
            <li>Tüm özellikler</li>
            <li>Ömür boyu erişim</li>
            <li>Tüm güncellemeler</li>
        </ul>
        """)
        group_layout.addWidget(plans_text)
        
        btn_layout = QHBoxLayout()
        
        starter_btn = QPushButton("💎 Starter Satın Al")
        starter_btn.clicked.connect(lambda: self.show_purchase_info("Starter", 4.99))
        btn_layout.addWidget(starter_btn)
        
        pro_btn = QPushButton("🚀 Professional Satın Al")
        pro_btn.setStyleSheet(f"background-color: {config.COLORS['success']};")
        pro_btn.clicked.connect(lambda: self.show_purchase_info("Professional", 9.99))
        btn_layout.addWidget(pro_btn)
        
        business_btn = QPushButton("💼 Business Satın Al")
        business_btn.clicked.connect(lambda: self.show_purchase_info("Business", 99.00))
        btn_layout.addWidget(business_btn)
        
        lifetime_btn = QPushButton("♾️ Lifetime Satın Al")
        lifetime_btn.clicked.connect(lambda: self.show_purchase_info("Lifetime", 299.00))
        btn_layout.addWidget(lifetime_btn)
        
        group_layout.addLayout(btn_layout)
        layout.addWidget(group)
    
    def activate_license(self):
        """Lisans anahtarını aktive et"""
        license_key = self.license_input.text().strip().upper()
        
        if not license_key:
            QMessageBox.warning(self, "Hata", "Lütfen lisans anahtarını girin!")
            return
        
        success = self.license_manager.activate_license(self.user_id, license_key)
        
        if success:
            QMessageBox.information(self, "Başarılı", "Lisans başarıyla aktive edildi!")
            self.close()
            # Dialog'u yeniden aç
            new_dialog = LicenseDialog(self.parent(), self.license_manager, self.user_id)
            new_dialog.exec_()
        else:
            QMessageBox.warning(self, "Hata", "Geçersiz lisans anahtarı!")
    
    def show_purchase_info(self, plan_name, price):
        """Satın alma bilgisi göster"""
        msg = QMessageBox(self)
        msg.setWindowTitle(f"{plan_name} Satın Al")
        msg.setText(f"""
        <h2>{plan_name} Planı</h2>
        <p><b>Fiyat:</b> ${price}/ay</p>
        <p>Satın almak için:</p>
        <ol>
            <li>digitalshadow.app adresine gidin</li>
            <li>"{plan_name}" planını seçin</li>
            <li>Ödeme yapın</li>
            <li>Lisans anahtarınızı alın</li>
            <li>Buradan aktive edin</li>
        </ol>
        <p><b>Demo için:</b> Test lisansı oluşturulacak (7 gün)</p>
        """)
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.button(QMessageBox.Ok).setText("Demo Oluştur")
        msg.button(QMessageBox.Cancel).setText("İptal")
        
        if msg.exec_() == QMessageBox.Ok:
            # Demo lisans oluştur
            self.create_demo_license(plan_name.lower())
    
    def create_demo_license(self, plan_type):
        """Demo lisans oluştur"""
        license_key = self.license_manager.create_license(self.user_id, plan_type, duration_days=7)
        
        QMessageBox.information(self, "Demo Lisans Oluşturuldu", 
                               f"7 günlük demo lisansınız oluşturuldu!\n\n"
                               f"Lisans Anahtarı: {license_key}\n\n"
                               f"Bu anahtarı kaydedin!")
        
        self.close()
        # Dialog'u yeniden aç
        new_dialog = LicenseDialog(self.parent(), self.license_manager, self.user_id)
        new_dialog.exec_()
