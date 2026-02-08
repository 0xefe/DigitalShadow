# 🚀 Digital Shadow - Kullanım Kılavuzu

## Hızlı Başlangıç

### 1. Kurulum ve İlk Çalıştırma

```bash
# Bağımlılıkları yükleyin
pip install -r requirements.txt

# Uygulamayı başlatın
python gui_app.py
```

### 2. Kullanıcı Kaydı ve Giriş

1. Uygulama açıldığında login ekranını göreceksiniz
2. **İlk kez kullanıyorsanız:**
   - Kullanıcı adı girin (en az 3 karakter)
   - "Kayıt Ol" butonuna tıklayın
3. **Daha önce kayıt olduysanız:**
   - Kullanıcı adınızı girin
   - "Giriş Yap" butonuna tıklayın

## 📊 Ana Özellikler

### Dashboard
Dashboard'da şunları görebilirsiniz:
- **Toplam Analiz Sayısı**: Yaptığınız tüm analizler
- **Ortalama Gizlilik Skoru**: Genel gizlilik durumunuz
- **Ortalama Risk**: Risk seviyeniz
- **Son Aktiviteler**: Son 5 analiziniz
- **Trend Grafiği**: Zaman içindeki değişimler

**Klavye Kısayolları:**
- `F5`: Dashboard'u yenile
- `Ctrl+N`: Yeni analiz
- `Ctrl+,`: Ayarlar

### Metin Analizi

1. Dashboard'dan "📝 Yeni Analiz" butonuna tıklayın
2. Analiz etmek istediğiniz metni yazın veya yapıştırın
3. "🔍 Analiz Et" butonuna basın
4. Sonuçları inceleyin:
   - **Agresiflik**: Metninizin sertlik seviyesi
   - **Pozitiflik**: Olumlu içerik oranı
   - **Risk**: Dijital güvenlik riski
   - **AI Yorumu**: Akıllı değerlendirme

**Klavye Kısayolları:**
- `Ctrl+N`: Yeni analiz sayfası
- `Ctrl+S`: Rapor kaydet

### Sosyal Medya Tarama

1. "🔍 Sosyal Medya Tara" sekmesine gidin
2. Aramak istediğiniz kullanıcı adını girin
3. "🔍 Tara" butonuna basın
4. Sonuçları platform bazında görüntüleyin

**Taranan Platformlar:**
- Twitter/X
- Instagram
- Facebook
- LinkedIn
- TikTok
- Reddit
- GitHub

### Analiz Geçmişi

1. "📜 Geçmiş" butonuna tıklayın
2. Tüm analizlerinizi listede görün
3. "📄 PDF Rapor Oluştur" ile son analizinizi PDF olarak kaydedin
4. "🔄 Yenile" ile listeyi güncelleyin

### Analiz Karşılaştırma

1. Dashboard'dan "🔍 Detaylı Karşılaştırma" butonuna tıklayın
2. "🔍 Son 5 Analizi Karşılaştır" butonuna basın
3. Trend analizini inceleyin:
   - Ortalama skorlar
   - Agresiflik trendi
   - Dominant kalıp
   - Grafik görselleştirme

## ⚙️ Ayarlar

### Genel Ayarlar
- **Tema**: Dark Mode / Light Mode (yakında)
- **Grafik Tipi**: Varsayılan grafik türünü seçin

### Veri Yönetimi

**Dışa Aktar (Export):**
1. Ayarlar > Veri Yönetimi
2. "📤 Verileri Dışa Aktar (JSON)" butonuna tıklayın
3. Dosya konumunu seçin
4. Tüm verileriniz JSON formatında kaydedilir

**İçe Aktar (Import):**
1. Ayarlar > Veri Yönetimi
2. "📥 Verileri İçe Aktar (JSON)" butonuna tıklayın
3. JSON dosyasını seçin
4. Onaylayın

**Veri Temizleme:**
- "🗑️ Tüm Verileri Temizle" ile tüm analizleri silebilirsiniz
- ⚠️ Bu işlem geri alınamaz!

## 🎯 Gelişmiş Özellikler

### Klavye Kısayolları

| Kısayol | Açıklama |
|---------|----------|
| `Ctrl+N` | Yeni analiz |
| `Ctrl+S` | Rapor kaydet |
| `Ctrl+E` | Veri export |
| `F5` | Dashboard yenile |
| `Ctrl+,` | Ayarlar |
| `Ctrl+Q` | Uygulamadan çık |
| `F1` | Yardım |

### Otomatik Yenileme
- Dashboard her 30 saniyede bir otomatik yenilenir
- Giriş yaptığınızda otomatik başlar
- Çıkış yaptığınızda durur

### PDF Rapor Özellikleri

PDF raporlarınızda:
- ✅ Detaylı analiz özeti
- ✅ Görsel grafikler
- ✅ AI değerlendirmesi
- ✅ Öneriler
- ✅ Tarih ve kullanıcı bilgisi

### Performans İzleme
- Tüm işlemler log dosyasına kaydedilir
- `digital_shadow.log` dosyasından takip edebilirsiniz

## 📈 Metrikleri Anlama

### Agresiflik (0.0 - 1.0)
- **0.0 - 0.3**: Düşük - Sakin ve yapıcı
- **0.3 - 0.6**: Orta - Bazen sert ifadeler
- **0.6 - 1.0**: Yüksek - Çatışmacı ve agresif

### Pozitiflik (0.0 - 1.0)
- **0.0 - 0.3**: Düşük - Olumsuz içerik ağırlıklı
- **0.3 - 0.6**: Orta - Dengeli
- **0.6 - 1.0**: Yüksek - Çok pozitif ve destekleyici

### Risk (0.0 - 1.0)
- **0.0 - 0.3**: Düşük Risk - Güvenli profil
- **0.3 - 0.6**: Orta Risk - Dikkatli olun
- **0.6 - 1.0**: Yüksek Risk - Acil önlem gerekli

### Gizlilik Skoru (0 - 100)
- **0 - 30**: İyi - Gizliliğiniz korunuyor
- **30 - 60**: Orta - İyileştirme yapılabilir
- **60 - 100**: Kötü - Acil önlem alın

## 🔐 Güvenlik İpuçları

1. **Düzenli Analiz Yapın**: Haftada en az bir kez profilinizi analiz edin
2. **Trend Takibi**: Davranış kalıplarınızdaki değişimleri izleyin
3. **Yedekleme**: Verilerinizi düzenli olarak export edin
4. **Gizlilik Ayarları**: Sosyal medya hesaplarınızın gizlilik ayarlarını kontrol edin
5. **Risk Azaltma**: Yüksek risk skorunda önerileri dikkate alın

## 🐛 Sorun Giderme

### Uygulama Açılmıyor
```bash
# Bağımlılıkları tekrar yükleyin
pip install --upgrade -r requirements.txt

# Python versiyonunu kontrol edin (3.8+)
python --version
```

### Analiz Hatası
- Metin uzunluğunu kontrol edin (10-5000 karakter)
- İnternet bağlantınızı kontrol edin (sosyal medya tarama için)
- Log dosyasını inceleyin: `digital_shadow.log`

### Veritabanı Hatası
- `digital_shadow.db` dosyasının yazma izni olduğundan emin olun
- Gerekirse dosyayı silin, otomatik yeniden oluşturulur

### Grafik Görünmüyor
```bash
# Matplotlib'i yeniden yükleyin
pip install --upgrade matplotlib seaborn
```

## 💡 İpuçları ve Püf Noktaları

1. **Toplu Analiz**: Birden fazla metni tek seferde analiz etmek için metinleri alt alta yazın
2. **Karşılaştırma**: Farklı zamanlarda aynı metni analiz ederek değişimi görün
3. **Export Kullanımı**: Önemli analizlerinizi JSON olarak yedekleyin
4. **PDF Raporları**: Profesyonel sunumlar için PDF raporları kullanın
5. **Klavye Kısayolları**: Hızlı çalışma için kısayolları öğrenin

## 📞 Destek

### Sık Sorulan Sorular

**S: Verilerim güvende mi?**
C: Evet, tüm veriler yerel olarak saklanır. İnternet bağlantısı sadece sosyal medya tarama için gereklidir.

**S: Kaç kullanıcı oluşturabilirim?**
C: Sınırsız kullanıcı oluşturabilirsiniz.

**S: Analizler ne kadar sürer?**
C: Ortalama 1-2 saniye içinde tamamlanır.

**S: PDF raporları nereye kaydedilir?**
C: Sizin seçtiğiniz konuma kaydedilir.

**S: Veritabanı ne kadar yer kaplar?**
C: Ortalama 100 analiz yaklaşık 1 MB yer kaplar.

### İletişim
- **GitHub**: Issues bölümünden bildirebilirsiniz
- **Email**: info@digitalshadow.com
- **Log Dosyası**: `digital_shadow.log` dosyasını paylaşın

## 🎓 Öğrenme Kaynakları

### Video Eğitimler (Yakında)
- Temel kullanım
- Gelişmiş özellikler
- Veri analizi ipuçları

### Blog Yazıları (Yakında)
- Dijital gizlilik rehberi
- Sosyal medya güvenliği
- AI analiz teknikleri

---

**Digital Shadow** ile dijital ayak izinizi kontrol altına alın! 🚀

*Son Güncelleme: 2024*
*Versiyon: 2.0.0*
