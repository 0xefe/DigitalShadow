# 📱 Digital Shadow - APK Yapım Rehberi

## 🎯 YÖNTEM: Kivy + Buildozer

### Neden Kivy?
✅ Python kullanırsın (mevcut kod)
✅ Android + iOS desteği
✅ Tek komutla APK oluşturma
⚠️ UI biraz basit (ama çalışır)

---

## 🚀 ADIM ADIM KURULUM

### 1. Kivy Kurulumu

```bash
# Kivy'yi yükle
pip install kivy

# Buildozer'ı yükle (APK için)
pip install buildozer

# Cython yükle (gerekli)
pip install cython
```

### 2. Mobil UI Oluştur

Yeni dosya: `mobile_app.py`

```python
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

# Mevcut kodunu import et
from analyzer import TextAnalyzer
from real_social_scanner import real_scanner

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        layout.add_widget(Label(text='Digital Shadow', font_size=32))
        
        self.username_input = TextInput(hint_text='Kullanıcı Adı', multiline=False)
        layout.add_widget(self.username_input)
        
        login_btn = Button(text='Giriş Yap', size_hint_y=0.2)
        login_btn.bind(on_press=self.login)
        layout.add_widget(login_btn)
        
        self.add_widget(layout)
    
    def login(self, instance):
        username = self.username_input.text
        if username:
            self.manager.current = 'dashboard'

class DashboardScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        layout.add_widget(Label(text='Dashboard', font_size=24))
        
        analysis_btn = Button(text='📝 Metin Analizi')
        analysis_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'analysis'))
        layout.add_widget(analysis_btn)
        
        scan_btn = Button(text='🔍 Sosyal Medya Tara')
        scan_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'scan'))
        layout.add_widget(scan_btn)
        
        self.add_widget(layout)

class AnalysisScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        layout.add_widget(Label(text='Metin Analizi', font_size=24))
        
        self.text_input = TextInput(hint_text='Metninizi buraya yazın...', size_hint_y=0.5)
        layout.add_widget(self.text_input)
        
        analyze_btn = Button(text='Analiz Et', size_hint_y=0.2)
        analyze_btn.bind(on_press=self.analyze)
        layout.add_widget(analyze_btn)
        
        self.result_label = Label(text='', size_hint_y=0.3)
        layout.add_widget(self.result_label)
        
        back_btn = Button(text='⬅️ Geri', size_hint_y=0.2)
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'dashboard'))
        layout.add_widget(back_btn)
        
        self.add_widget(layout)
    
    def analyze(self, instance):
        text = self.text_input.text
        if text:
            analyzer = TextAnalyzer()
            result = analyzer.analyze_text([text])
            self.result_label.text = f"Risk: {result['risk_score']:.2f}"

class ScanScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        layout.add_widget(Label(text='Sosyal Medya Tarama', font_size=24))
        
        self.username_input = TextInput(hint_text='Kullanıcı adı...', multiline=False)
        layout.add_widget(self.username_input)
        
        scan_btn = Button(text='Tara', size_hint_y=0.2)
        scan_btn.bind(on_press=self.scan)
        layout.add_widget(scan_btn)
        
        self.result_label = Label(text='', size_hint_y=0.5)
        layout.add_widget(self.result_label)
        
        back_btn = Button(text='⬅️ Geri', size_hint_y=0.2)
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'dashboard'))
        layout.add_widget(back_btn)
        
        self.add_widget(layout)
    
    def scan(self, instance):
        username = self.username_input.text
        if username:
            # Basit tarama (sadece birkaç platform)
            platforms = ['Instagram', 'GitHub', 'Twitter']
            results = []
            for platform in platforms:
                try:
                    result = real_scanner.check_username(platform, username)
                    if result['found']:
                        results.append(f"✅ {platform}")
                    else:
                        results.append(f"❌ {platform}")
                except:
                    results.append(f"⚠️ {platform}")
            
            self.result_label.text = '\n'.join(results)

class DigitalShadowApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(DashboardScreen(name='dashboard'))
        sm.add_widget(AnalysisScreen(name='analysis'))
        sm.add_widget(ScanScreen(name='scan'))
        return sm

if __name__ == '__main__':
    DigitalShadowApp().run()
```

### 3. Buildozer Yapılandırması

```bash
# buildozer.spec dosyası oluştur
buildozer init
```

`buildozer.spec` dosyasını düzenle:

```ini
[app]
title = Digital Shadow
package.name = digitalshadow
package.domain = com.digitalshadow

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 1.0

requirements = python3,kivy,requests,beautifulsoup4,scikit-learn

orientation = portrait
fullscreen = 0

android.permissions = INTERNET,ACCESS_NETWORK_STATE
android.api = 31
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
```

### 4. APK Oluştur

```bash
# Android APK oluştur
buildozer android debug

# İlk çalıştırmada SDK/NDK indirecek (30-60 dakika)
# Sonraki çalıştırmalarda 5-10 dakika

# APK konumu:
# bin/digitalshadow-1.0-debug.apk
```

---

## ⚠️ ÖNEMLİ NOTLAR

### Windows'ta APK Oluşturma:
```
❌ Buildozer Windows'ta çalışmaz!
✅ Çözümler:
   1. WSL2 (Windows Subsystem for Linux) kullan
   2. Ubuntu VM kullan
   3. GitHub Actions kullan (otomatik)
   4. Online servis kullan (Replit, Colab)
```

### WSL2 Kurulumu (Önerilen):
```bash
# PowerShell'de (Admin):
wsl --install

# Ubuntu başlat
# Sonra:
sudo apt update
sudo apt install -y python3-pip git zip unzip openjdk-11-jdk
pip3 install buildozer cython
```

---

## 🚀 DAHA KOLAY YÖNTEM: React Native

### Neden React Native?
✅ Windows'ta çalışır
✅ Daha güzel UI
✅ Daha hızlı
✅ Expo ile çok kolay

### Hızlı Başlangıç:
```bash
# Node.js yükle (nodejs.org)

# Expo CLI yükle
npm install -g expo-cli

# Yeni proje oluştur
expo init DigitalShadowMobile
cd DigitalShadowMobile

# Çalıştır
expo start

# APK oluştur
expo build:android
```

---

## 💡 BENİM ÖNERİM

### Şimdi:
1. ✅ EXE'yi test et (hazır!)
2. ✅ Desktop versiyonu yayınla
3. ✅ İlk kullanıcıları bul

### Sonra (2-3 hafta):
1. 🌐 Web app yap (FastAPI + React)
2. 📱 React Native ile mobil app
3. 🚀 Hepsini birlikte yayınla

---

## 📊 ZAMAN TAHMİNİ

| Yöntem | Süre | Zorluk | Sonuç |
|--------|------|--------|-------|
| Kivy + Buildozer | 1 hafta | Orta | Çalışır ama basit UI |
| React Native + Expo | 2 hafta | Orta | Profesyonel UI |
| Flutter | 2 hafta | Orta | Çok hızlı, güzel UI |
| Native (Swift/Kotlin) | 6 hafta | Zor | En iyi performans |

---

## 🎯 SONUÇ

**ŞİMDİ NE YAPALIM?**

1. EXE'yi test et (dist/DigitalShadow.exe)
2. Mobil için React Native öğren
3. 2 hafta sonra APK hazır!

**APK yapmak istiyorsan, React Native ile başla!**
