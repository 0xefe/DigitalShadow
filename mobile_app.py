"""
Digital Shadow - Mobile App (Kivy)
Basit mobil uygulama versiyonu
"""

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window

# Renkler
Window.clearcolor = (0.1, 0.1, 0.15, 1)


class LoginScreen(Screen):
    """Giriş ekranı"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        layout = BoxLayout(orientation='vertical', padding=40, spacing=20)
        
        # Logo/Başlık
        title = Label(
            text='[b]Digital Shadow[/b]',
            markup=True,
            font_size=36,
            size_hint_y=0.3,
            color=(0.39, 0.4, 0.95, 1)
        )
        layout.add_widget(title)
        
        subtitle = Label(
            text='Dijital Ayak İzinizi Kontrol Edin',
            font_size=16,
            size_hint_y=0.1,
            color=(0.7, 0.7, 0.7, 1)
        )
        layout.add_widget(subtitle)
        
        # Kullanıcı adı
        self.username_input = TextInput(
            hint_text='Kullanıcı Adı',
            multiline=False,
            size_hint_y=0.15,
            font_size=18,
            background_color=(0.2, 0.2, 0.25, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(0.39, 0.4, 0.95, 1)
        )
        layout.add_widget(self.username_input)
        
        # Giriş butonu
        login_btn = Button(
            text='Giriş Yap',
            size_hint_y=0.15,
            font_size=20,
            background_color=(0.39, 0.4, 0.95, 1),
            background_normal=''
        )
        login_btn.bind(on_press=self.login)
        layout.add_widget(login_btn)
        
        # Boşluk
        layout.add_widget(Label(size_hint_y=0.3))
        
        self.add_widget(layout)
    
    def login(self, instance):
        """Giriş yap"""
        username = self.username_input.text.strip()
        if username:
            # Dashboard'a geç
            self.manager.get_screen('dashboard').set_username(username)
            self.manager.current = 'dashboard'
        else:
            self.username_input.hint_text = 'Lütfen kullanıcı adı girin!'


class DashboardScreen(Screen):
    """Ana ekran"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.username = ""
        
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # Header
        self.header = Label(
            text='Dashboard',
            font_size=28,
            size_hint_y=0.15,
            color=(0.39, 0.4, 0.95, 1)
        )
        self.layout.add_widget(self.header)
        
        # Butonlar
        buttons = [
            ('📝 Metin Analizi', 'analysis', (0.16, 0.73, 0.51, 1)),
            ('🔍 Sosyal Medya Tara', 'scan', (0.95, 0.39, 0.27, 1)),
            ('📊 Geçmiş', 'history', (0.95, 0.61, 0.07, 1)),
        ]
        
        for text, screen, color in buttons:
            btn = Button(
                text=text,
                size_hint_y=0.2,
                font_size=20,
                background_color=color,
                background_normal=''
            )
            btn.bind(on_press=lambda x, s=screen: setattr(self.manager, 'current', s))
            self.layout.add_widget(btn)
        
        # Çıkış butonu
        logout_btn = Button(
            text='Çıkış',
            size_hint_y=0.15,
            font_size=18,
            background_color=(0.5, 0.5, 0.5, 1),
            background_normal=''
        )
        logout_btn.bind(on_press=self.logout)
        self.layout.add_widget(logout_btn)
        
        self.add_widget(self.layout)
    
    def set_username(self, username):
        """Kullanıcı adını ayarla"""
        self.username = username
        self.header.text = f'Merhaba, {username}!'
    
    def logout(self, instance):
        """Çıkış yap"""
        self.manager.current = 'login'


class AnalysisScreen(Screen):
    """Metin analizi ekranı"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # Başlık
        title = Label(
            text='📝 Metin Analizi',
            font_size=24,
            size_hint_y=0.1,
            color=(0.16, 0.73, 0.51, 1)
        )
        layout.add_widget(title)
        
        # Metin girişi
        self.text_input = TextInput(
            hint_text='Analiz etmek istediğiniz metni buraya yazın...',
            size_hint_y=0.4,
            font_size=16,
            background_color=(0.2, 0.2, 0.25, 1),
            foreground_color=(1, 1, 1, 1)
        )
        layout.add_widget(self.text_input)
        
        # Analiz butonu
        analyze_btn = Button(
            text='🔍 Analiz Et',
            size_hint_y=0.12,
            font_size=18,
            background_color=(0.16, 0.73, 0.51, 1),
            background_normal=''
        )
        analyze_btn.bind(on_press=self.analyze)
        layout.add_widget(analyze_btn)
        
        # Sonuç
        scroll = ScrollView(size_hint_y=0.28)
        self.result_label = Label(
            text='Sonuçlar burada görünecek...',
            size_hint_y=None,
            font_size=14,
            color=(0.9, 0.9, 0.9, 1)
        )
        self.result_label.bind(texture_size=self.result_label.setter('size'))
        scroll.add_widget(self.result_label)
        layout.add_widget(scroll)
        
        # Geri butonu
        back_btn = Button(
            text='⬅️ Geri',
            size_hint_y=0.1,
            font_size=16,
            background_color=(0.5, 0.5, 0.5, 1),
            background_normal=''
        )
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'dashboard'))
        layout.add_widget(back_btn)
        
        self.add_widget(layout)
    
    def analyze(self, instance):
        """Metni analiz et"""
        text = self.text_input.text.strip()
        
        if not text:
            self.result_label.text = '⚠️ Lütfen bir metin girin!'
            return
        
        # Basit analiz (gerçek AI yerine)
        import random
        risk_score = random.uniform(0.2, 0.8)
        sentiment = "Pozitif" if risk_score < 0.5 else "Negatif"
        
        self.result_label.text = f"""
[b]Analiz Sonuçları:[/b]

📊 Risk Skoru: {risk_score:.2f}
😊 Duygu: {sentiment}
📏 Kelime Sayısı: {len(text.split())}
🔤 Karakter Sayısı: {len(text)}

[b]AI Yorumu:[/b]
Bu metin {sentiment.lower()} bir ton içeriyor.
Risk seviyesi: {"Düşük" if risk_score < 0.4 else "Orta" if risk_score < 0.7 else "Yüksek"}

[i]Not: Bu demo versiyonudur.[/i]
        """


class ScanScreen(Screen):
    """Sosyal medya tarama ekranı"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # Başlık
        title = Label(
            text='🔍 Sosyal Medya Tarama',
            font_size=24,
            size_hint_y=0.1,
            color=(0.95, 0.39, 0.27, 1)
        )
        layout.add_widget(title)
        
        # Kullanıcı adı girişi
        self.username_input = TextInput(
            hint_text='Kullanıcı adı...',
            multiline=False,
            size_hint_y=0.1,
            font_size=18,
            background_color=(0.2, 0.2, 0.25, 1),
            foreground_color=(1, 1, 1, 1)
        )
        layout.add_widget(self.username_input)
        
        # Tarama butonu
        scan_btn = Button(
            text='🚀 Taramayı Başlat',
            size_hint_y=0.12,
            font_size=18,
            background_color=(0.95, 0.39, 0.27, 1),
            background_normal=''
        )
        scan_btn.bind(on_press=self.scan)
        layout.add_widget(scan_btn)
        
        # Sonuçlar
        scroll = ScrollView(size_hint_y=0.58)
        self.result_label = Label(
            text='Tarama sonuçları burada görünecek...',
            size_hint_y=None,
            font_size=14,
            color=(0.9, 0.9, 0.9, 1)
        )
        self.result_label.bind(texture_size=self.result_label.setter('size'))
        scroll.add_widget(self.result_label)
        layout.add_widget(scroll)
        
        # Geri butonu
        back_btn = Button(
            text='⬅️ Geri',
            size_hint_y=0.1,
            font_size=16,
            background_color=(0.5, 0.5, 0.5, 1),
            background_normal=''
        )
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'dashboard'))
        layout.add_widget(back_btn)
        
        self.add_widget(layout)
    
    def scan(self, instance):
        """Sosyal medya taraması yap"""
        username = self.username_input.text.strip()
        
        if not username:
            self.result_label.text = '⚠️ Lütfen bir kullanıcı adı girin!'
            return
        
        # Basit tarama (demo)
        import random
        platforms = [
            'Instagram', 'GitHub', 'Twitter', 'TikTok', 
            'YouTube', 'Reddit', 'LinkedIn', 'Facebook'
        ]
        
        results = [f"[b]Tarama Sonuçları: {username}[/b]\n"]
        found_count = 0
        
        for platform in platforms:
            found = random.choice([True, False])
            if found:
                risk = random.uniform(0.3, 0.9)
                results.append(f"✅ {platform} - Risk: {risk:.2f}")
                found_count += 1
            else:
                results.append(f"❌ {platform} - Bulunamadı")
        
        results.append(f"\n[b]Özet:[/b]")
        results.append(f"Toplam: {len(platforms)} platform tarandı")
        results.append(f"Bulundu: {found_count} hesap")
        results.append(f"\n[i]Not: Bu demo versiyonudur.[/i]")
        
        self.result_label.text = '\n'.join(results)


class HistoryScreen(Screen):
    """Geçmiş ekranı"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # Başlık
        title = Label(
            text='📊 Geçmiş',
            font_size=24,
            size_hint_y=0.1,
            color=(0.95, 0.61, 0.07, 1)
        )
        layout.add_widget(title)
        
        # İçerik
        scroll = ScrollView(size_hint_y=0.8)
        content = Label(
            text="""
[b]Son Aktiviteler:[/b]

📝 Metin Analizi - 2 saat önce
   Risk: 0.45 (Orta)

🔍 Sosyal Medya Tarama - 5 saat önce
   Kullanıcı: test123
   Bulundu: 6/10 platform

📝 Metin Analizi - Dün
   Risk: 0.72 (Yüksek)

[i]Daha fazla özellik yakında...[/i]
            """,
            size_hint_y=None,
            font_size=14,
            color=(0.9, 0.9, 0.9, 1),
            markup=True
        )
        content.bind(texture_size=content.setter('size'))
        scroll.add_widget(content)
        layout.add_widget(scroll)
        
        # Geri butonu
        back_btn = Button(
            text='⬅️ Geri',
            size_hint_y=0.1,
            font_size=16,
            background_color=(0.5, 0.5, 0.5, 1),
            background_normal=''
        )
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'dashboard'))
        layout.add_widget(back_btn)
        
        self.add_widget(layout)


class DigitalShadowApp(App):
    """Ana uygulama"""
    
    def build(self):
        """Uygulamayı oluştur"""
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(DashboardScreen(name='dashboard'))
        sm.add_widget(AnalysisScreen(name='analysis'))
        sm.add_widget(ScanScreen(name='scan'))
        sm.add_widget(HistoryScreen(name='history'))
        return sm


if __name__ == '__main__':
    DigitalShadowApp().run()
