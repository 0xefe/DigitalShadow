# Digital Shadow - Executable Builder
# PyInstaller ile .exe oluşturma

# 1. PyInstaller'ı yükle
pip install pyinstaller

# 2. Executable oluştur
pyinstaller --name="DigitalShadow" ^
            --onefile ^
            --windowed ^
            --icon=icon.ico ^
            --add-data "digital_shadow.db;." ^
            gui_app.py

# 3. Sonuç
# dist/DigitalShadow.exe dosyası oluşacak

# VEYA Basit Versiyon:
pyinstaller --onefile --windowed --name="DigitalShadow" gui_app.py
