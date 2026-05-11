# VA-ATAN SİBER GÜVENLİK - Geliştirme Raporu v2.0

## Özet
VA-ATAN (IhbarVatan) siber güvenlik aracı, AY-YILDIZ SİBER KALKAN'dan fork'lanarak tam kullanılabilir hale getirildi ve **OTOMATİK SAHTE SİTE TARAMA MODU** eklendi.
- **Geliştirici:** efe24code  
**İlham:** Mustafa Kemal Atatürk (1881-1938)  
**Fork Kaynağı:** AY-YILDIZ SİBER KALKAN (ThT0AltayHR)  
- **GitHub:** https://github.com/efe24code/IhbarVatan

## 🚀 YENİ ÖZELLİKLER

### Otomatik Tarama Modu (MODÜL 22)
- **URL İSTEMEZ, KENDİ BULUR:** Kullanıcıdan URL girişi gerekmez
- **Çok Kaynaklı URL Keşfi:**
  - USOM kara listesi (ilk 100 URL)
  - Yerel kara liste
  - Olası phishing domainleri (banka + uzantı kombinasyonları)
  - Government institution variations
  - Bilinen phishing pattern'leri (login-, -secure, verify-, vb.)
- **Multi-Thread Hızlı Tarama:** 20 thread ile paralel tarama
- **Otomatik Raporlama:** Sonuçları raporlar/oto_tarama_raporu.txt dosyasına kaydeder
- **İlerleme Göstergesi:** Yüzde (%) bazlı ilerleme gösterimi

### Ana Menü Entegrasyonu
- **[A] Seçeneği:** Ana menüde en üstte "🚀 OTOMATİK TARAMA MODU" seçeneği eklendi
- Tek tuşla otomatik tarama başlatılabilir
- URL girişi gerekmez, sistem otomatik bulur

## Yapılan İyileştirmeler

### 1. Ana Menü (ana_menu.py)
- **Sorun:** `time` kütüphanesi iki kez import edilmişti
- **Çözüm:** Duplicate import kaldırıldı
- **Sorun:** Araç dosya isimleri ARACLAR sözlüğünde gerçek dosyalarla eşleşmiyordu
- **Çözüm:** Dosya isimleri düzeltildi:
  - 07: `07_guven_damgasi.py` → `07_favicon_hash.py`
  - 08: `08_form_tuzagi.py` → `08_ekran_goruntusu.py`
  - 09: `09_favicon_kontrol.py` → `09_link_ici_analiz.py`
- **Sorun:** 3 saniye zorunlu bekleme süresi kullanıcı deneyimini olumsuz etkiliyordu
- **Çözüm:** Bekleme süresi 1 saniyeye indirildi
- **İyileştirme:** `bagimlilik_kontrol()` fonksiyonu eklendi
- **YENİ:** Otomatik tarama modu için [A] seçeneği eklendi
- **YENİ:** Araç sayısı 22'ye çıkarıldı

### 2. Yapılandırma Sistemi (config.json)
- Yeni `config.json` dosyası oluşturuldu
- Tüm ayarlar merkezi olarak yönetilebilir hale getirildi
- Şu ayarlar yapılandırılabilir:
  - USOM URL
  - PhishTank API URL
  - SSL uyarı/kritik gün sayıları
  - Domain yaş uyarı/kritik gün sayıları
  - Şüpheli ülkeler listesi
  - Güvenilir CA listesi

### 3. USOM Kontrol Modülü (araclar/01_usom_kontrol.py)
- **İyileştirme:** Config dosyasından USOM URL'si yüklenir
- **Hata:** Config dosyası bulunamazsa varsayılan URL kullanılır
- **Sonuç:** Ayarları dinamik olarak değiştirilebilir

### 4. SSL Sertifika Modülü (araclar/04_ssl_sertifika.py)
- **İyileştirme:** Config dosyasından güvenilir CA listesi yüklenir
- **İyileştirme:** Config dosyasından SSL uyarı/kritik gün sayıları yüklenir
- **Sonuç:** Güvenilir CA listesi ve eşik değerleri yapılandırılabilir

### 5. Domain/Whois Modülü (araclar/05_domain_yas_whois.py)
- **İyileştirme:** Config dosyasından şüpheli ülkeler listesi yüklenir
- **İyileştirme:** Config dosyasından domain yaş eşik değerleri yüklenir
- **Sonuç:** Ülkeler ve eşik değerleri yapılandırılabilir

### 6. Sahte e-Devlet Tespiti (araclar/03_sahte_edevlet.py) - TAM FONKSİYONEL
- .gov.tr uzantısı kontrolü
- Resmi gov.tr domain'leri listesi
- Typo kontrolü
- HTTPS kontrolü
- HTML içerik kontrolü
- Toplu URL analizi

### 7. Typosquatting Tespiti (araclar/15_typosquatting.py) - TAM FONKSİYONEL
- Karakter değişimi (q→g, 0→o, 1→l, vb.)
- Karakter ekleme
- Karakter silme
- Benzerlik skoru hesaplama
- Otomatik tarama modu
- Hedef domain listesi (Türk bankalar ve kurumlar)

### 8. Toplu Tarama Modülü (araclar/11_toplu_tarama.py) - TAM FONKSİYONEL
- Manuel URL girişi
- Dosyadan okuma
- USOM listesi ile tarama
- 30 thread multi-scanning
- HTTPS kontrolü
- URL uzunluk kontrolü
- Otomatik raporlama

### 9. Yerel Kara Liste (araclar/12_yerel_karaliste.py) - TAM FONKSİYONEL
- URL ekleme
- URL silme
- Listeyi görüntüleme
- URL kontrolü
- Listeyi temizleme
- Dosya tabanlı depolama

### 10. USOM İhbar Hazırlama (araclar/13_usom_ihbar.py) - TAM FONKSİYONEL
- Tek URL ihbar formu
- USOM listesinden toplu ihbar
- Manuel URL girişi
- Rapor görüntüleme
- Otomatik rapor kaydetme

## Oluşturulan Dosyalar

### Ana Dosyalar
- `ana_menu.py` - Ana menü (iyileştirildi + otomatik tarama)
- `requirements.txt` - Python bağımlılıkları
- `config.json` - Yapılandırma dosyası (yeni)
- `README.md` - Proje belgesi
- `GELISTIRME_RAPORU.md` - Bu rapor

### Araç Modülleri (araclar/) - 22 ARAÇ
- `01_usom_kontrol.py` - USOM kara liste sorgusu (iyileştirildi)
- `02_phishtank_sorgu.py` - PhishTank sorgusu
- `03_sahte_edevlet.py` - Sahte e-Devlet tespiti (TAM FONKSİYONEL)
- `04_ssl_sertifika.py` - SSL analiz (iyileştirildi)
- `05_domain_yas_whois.py` - Domain/Whois (iyileştirildi)
- `06_kara_liste_skor.py` - Kara liste skor (placeholder)
- `07_favicon_hash.py` - Favicon hash (placeholder)
- `08_ekran_goruntusu.py` - Ekran görüntüsü (placeholder)
- `09_link_ici_analiz.py` - Link analizi (placeholder)
- `10_js_obfuscation.py` - JS deobfuscation (placeholder)
- `11_toplu_tarama.py` - Toplu tarama (TAM FONKSİYONEL)
- `12_yerel_karaliste.py` - Yerel kara liste (TAM FONKSİYONEL)
- `13_usom_ihbar.py` - USOM ihbar (TAM FONKSİYONEL)
- `14_telegram_bot.py` - Telegram bot (placeholder)
- `15_typosquatting.py` - Typosquatting (TAM FONKSİYONEL)
- `16_ip_geolocation.py` - IP geolocation (placeholder)
- `17_emniyet_siber.py` - Emniyet siber (placeholder)
- `18_fidye_kontrol.py` - Fidye kontrol (placeholder)
- `19_dns_takip.py` - DNS takip (placeholder)
- `20_telegram_komut.py` - Telegram komut (placeholder)
- `21_savunma_merkezi.py` - Siber savunma (placeholder)
- `22_oto_tarama.py` - OTOMATİK TARAMA (YENİ - TAM FONKSİYONEL)

### Dizinler
- `data/` - Veri dosyaları için
- `raporlar/` - Rapor dosyaları için
- `assets/` - Varlık dosyaları için

## Kullanım

### Otomatik Tarama Modu
```bash
python ana_menu.py
# Ana menüde [A] seçeneğini seçin
# URL girmenize gerek yok, sistem otomatik bulur ve tarar
```

### Manuel Araç Kullanımı
```bash
python ana_menu.py
# [1] SİBER KALKAN SUITE - Araç Menüsü
# İstediğiniz aracı seçin
```

## Tam Fonksiyonel Modüller (8/22)
1. ✅ USOM Kontrol (01)
2. ✅ Sahte e-Devlet Tespiti (03)
3. ✅ SSL Sertifika Analizi (04)
4. ✅ Domain Yaş/Whois (05)
5. ✅ Toplu Tarama (11)
6. ✅ Yerel Kara Liste (12)
7. ✅ USOM İhbar (13)
8. ✅ Typosquatting (15)
9. ✅ Otomatik Tarama (22) - YENİ

## Placeholder Modüller (13/22)
- PhishTank Sorgu (02)
- Kara Liste Skor (06)
- Favicon Hash (07)
- Ekran Görüntüsü (08)
- Link Analizi (09)
- JS Obfuscation (10)
- Telegram Bot (14)
- IP Geolocation (16)
- Emniyet Siber (17)
- Fidye Kontrol (18)
- DNS Takip (19)
- Telegram Komut (20)
- Siber Savunma (21)

## Önerilen Sonraki Adımlar

1. **Placeholder Modülleri Tamamlama**
   - 02, 06-10, 14, 16-21 numaralı modüllerin tam fonksiyonellik eklenmesi

2. **Hata Yönetimi İyileştirmesi**
   - Daha detaylı hata mesajları
   - Loglama sistemi ekleme

3. **Test Süreci**
   - Birim testleri yazma
   - Entegrasyon testleri

4. **Performans İyileştirmeleri**
   - Önbellekleme mekanizması
   - Asenkron işlemler

## Kurulum

```bash
# Bağımlılıkları yükle
pip install -r requirements.txt

# Aracı çalıştır
python ana_menu.py
```

## Notlar
- Tüm iyileştirmeler geriye uyumludur
- Config dosyası opsiyoneldir, yoksa varsayılan değerler kullanılır
- Otomatik tarama modu URL girişi gerektirmez
- 8 modül tam fonksiyonel, 13 modül placeholder durumda
