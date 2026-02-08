# 📱 APK YAPIM TALİMATLARI

## ⚠️ ÖNEMLİ: Windows'ta Buildozer Çalışmaz!

Buildozer sadece Linux'ta çalışır. 3 seçeneğin var:

---

## SEÇENEK 1: WSL2 Kullan (Önerilen) ⭐

### Adım 1: WSL2 Kur

```powershell
# PowerShell'i Admin olarak aç
wsl --install

# Bilgisayarı yeniden başlat
# Ubuntu otomatik yüklenecek
```

### Adım 2: Ubuntu'da Kurulum

```bash
# Ubuntu terminalinde:

# Sistem güncelle
sudo apt update
sudo apt upgrade -y

# Gerekli paketleri yükle
sudo apt install -y python3-pip git zip unzip openjdk-11-jdk autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev

# Buildozer yükle
pip3 install buildozer cython

# Android SDK için yer aç (30GB gerekli!)
```

### Adım 3: Proje Dosyalarını Kopyala

```bash
# Windows dosyalarına erişim:
cd /mnt/c/Users/kids/Documents/digital_shadow

# VEYA kopyala:
cp -r /mnt/c/Users/kids/Documents/digital_shadow ~/digitalshadow
cd ~/digitalshadow
```

### Adım 4: APK Oluştur

```bash
# İlk çalıştırma (SDK/NDK indirecek - 30-60 dakika)
buildozer android debug

# APK konumu:
# bin/digitalshadow-1.0.0-debug.apk

# Windows'a kopyala:
cp bin/*.apk /mnt/c/Users/kids/Desktop/
```

---

## SEÇENEK 2: GitHub Actions (Otomatik) 🤖

### Avantajlar:
✅ Bilgisayarında hiçbir şey kurman gerekmez
✅ GitHub'da otomatik build
✅ Ücretsiz

### Adım 1: GitHub'a Yükle

```bash
cd c:\Users\kids\Documents\digital_shadow

git init
git add .
git commit -m "Initial commit"

# GitHub'da yeni repo oluştur
# Sonra:
git remote add origin https://github.com/KULLANICI_ADIN/digital-shadow.git
git push -u origin main
```

### Adım 2: GitHub Action Oluştur

`.github/workflows/build-apk.yml` dosyası oluştur:

```yaml
name: Build APK

on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install buildozer cython
    
    - name: Build APK
      run: |
        buildozer android debug
    
    - name: Upload APK
      uses: actions/upload-artifact@v3
      with:
        name: digitalshadow-apk
        path: bin/*.apk
```

### Adım 3: APK İndir

- GitHub repo'na git
- Actions sekmesi
- Son build'i aç
- APK'yı indir

---

## SEÇENEK 3: Online Servis Kullan 🌐

### Google Colab (Ücretsiz):

```python
# Colab notebook'ta:

!apt update
!apt install -y openjdk-11-jdk
!pip install buildozer cython

# Dosyaları yükle (Google Drive'dan)
from google.colab import drive
drive.mount('/content/drive')

!cd /content/drive/MyDrive/digital_shadow && buildozer android debug

# APK'yı indir
from google.colab import files
files.download('/content/drive/MyDrive/digital_shadow/bin/digitalshadow-1.0.0-debug.apk')
```

---

## SEÇENEK 4: React Native Kullan (Daha Kolay) 🚀

### Windows'ta çalışır!

```bash
# Node.js yükle (nodejs.org)

# Expo CLI yükle
npm install -g expo-cli eas-cli

# Yeni proje
expo init DigitalShadowMobile
cd DigitalShadowMobile

# Geliştir
expo start

# APK oluştur (Expo sunucularında)
eas build -p android --profile preview

# APK linkini alırsın, indir ve kur!
```

---

## 🎯 BENİM ÖNERİM

### Şimdi:
1. ✅ EXE'yi test et (dist/DigitalShadow.exe)
2. ✅ Desktop versiyonu kullan

### Mobil için (2 seçenek):

**A) Hızlı Test (Bugün):**
```bash
# Kivy'yi test et
pip install kivy
python mobile_app.py

# Bilgisayarda çalışacak, mobil UI göreceksin
```

**B) Gerçek APK (Hafta sonu):**
```bash
# WSL2 kur (1 saat)
# Buildozer ile APK yap (2 saat)
# Toplam: 3 saat
```

**C) Profesyonel Mobil (2 hafta):**
```bash
# React Native öğren
# Expo ile APK yap
# Sonuç: App Store'a yüklenebilir kalite
```

---

## 📊 KARŞILAŞTIRMA

| Yöntem | Süre | Zorluk | Sonuç |
|--------|------|--------|-------|
| WSL2 + Buildozer | 3 saat | Orta | Çalışır APK |
| GitHub Actions | 1 saat | Kolay | Otomatik APK |
| Google Colab | 30 dk | Kolay | Tek seferlik |
| React Native | 2 hafta | Orta | Profesyonel |

---

## 💡 ŞİMDİ NE YAPALIM?

### Önce Test Et:
```bash
# Mobil UI'ı bilgisayarda test et
pip install kivy
python mobile_app.py
```

### Sonra Karar Ver:
- Hızlı APK istiyorsan → WSL2 + Buildozer
- Profesyonel istiyorsan → React Native

---

## 🚀 HIZLI BAŞLANGIÇ

```bash
# 1. Kivy yükle
pip install kivy

# 2. Mobil app'i test et
python mobile_app.py

# 3. Beğendiysen APK yap (WSL2'de)
```

**Şimdi test edelim mi?**
