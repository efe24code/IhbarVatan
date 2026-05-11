# VA-ATAN SİBER GÜVENLİK ARACI | 22 MODÜL | M.K. ATATÜRK ANISINA
import os, sys, time, subprocess, json, random
from colorama import Fore, Back, Style, init
init(autoreset=True)

# FORUM BAĞLANTISI
FORUM_LINK = "https://www.turkhackteam.org/konular/ay-yildiz-siber-guvenlik-tool-u.2082661/"
ATATURK_SOZLERI = [
    "Yurtta sulh, cihanda sulh.",
    "Beni Türk doktorlarına emanet ediniz.",
    "Hayatta en hakiki mürşit ilimdir.",
    "Egemenlik verilmez, alınır.",
    "Milletimiz için, dava uğruna, her şeye katlanmaya hazırım.",
    "Türk milletinin karakteri, yüksek Türk karakteridir.",
    "Bir millet, savaş meydanlarında ne kadar zafer kazanırsa kazansın, o zaferin sürekli sonuçlar doğurabilmesi için, kültür meydanlarında da zafer kazanılması gerekir.",
    "Umutsuz durumlar yoktur, umutsuz insanlar vardır."
]

print(f"\n{Fore.YELLOW}[!] VA-ATAN SİBER GÜVENLİK ARACI açılıyor...{Style.RESET_ALL}")
print(f"\n{Fore.CYAN}M.K. ATATÜRK: {random.choice(ATATURK_SOZLERI)}{Style.RESET_ALL}")
time.sleep(1)

# ================================================
VERSIYON = "1.0.1"
GITHUB_USER = "efe24code"
GITHUB_URL = "https://github.com/" + GITHUB_USER + "/IhbarVatan"
GUNCELLEME_URL = "https://raw.githubusercontent.com/" + GITHUB_USER + "/IhbarVatan/main/version.json"


ANA_LOGO = f"""{Fore.CYAN}{Style.BRIGHT}
        ▄▀█ █ █ █▀█ █▄ █ █▀█   █▄ █ █▀█ █▄█ █▄█ █ █ █
        █ █ █ █ █▀▀ █ ▀█ █▄█   █ ▀█ █▄█ █ █ █ █ █▀█

              ██   ██    ██████  ███    ██  ███    ██
              ███ ███    ██   ██ ████   ██  ████   ██
              ███████    ██████  ██ ██  ██  ██ ██  ██
              ██ █ ██    ██   ██ ██  ██ ██  ██  ██ ██
              ██   ██    ██████  ██   ████  ██   ████

        ████████████████████████████████████████████
              VA-ATAN SİBER GÜVENLİK ARACI
              "YURTTA SULH, CİHANDA SULH"
        ████████████████████████████████████████████
{Style.RESET_ALL}"""

ATATURK_IMZASI = f"""{Fore.WHITE}
              "MUSTAFA KEMAL ATATÜRK"
              1881 - 1938
{Style.RESET_ALL}"""

ARACLAR = {
    "1": {"ad": "USOM Kontrol", "dosya": "01_usom_kontrol.py", "aciklama": "USOM kara liste sorgusu"},
    "2": {"ad": "PhishTank Sorgu", "dosya": "02_phishtank_sorgu.py", "aciklama": "PhishTank veritabanı"},
    "3": {"ad": "Sahte e-Devlet", "dosya": "03_sahte_edevlet.py", "aciklama": "gov.tr taklit tespiti"},
    "4": {"ad": "SSL Sertifika", "dosya": "04_ssl_sertifika.py", "aciklama": "SSL güvenlik analizi"},
    "5": {"ad": "Domain Yaş/Whois", "dosya": "05_domain_yas_whois.py", "aciklama": "Domain yaş kontrolü"},
    "6": {"ad": "Kara Liste Skor", "dosya": "06_kara_liste_skor.py", "aciklama": "Toplam risk skoru"},
    "7": {"ad": "Favicon Hash", "dosya": "07_favicon_hash.py", "aciklama": "Favicon hash karşılaştırma"},
    "8": {"ad": "Ekran Görüntüsü", "dosya": "08_ekran_goruntusu.py", "aciklama": "Site ekran görüntüsü alma"},
    "9": {"ad": "Link Analizi", "dosya": "09_link_ici_analiz.py", "aciklama": "Site link analizi"},
    "10": {"ad": "JS Obfuscation", "dosya": "10_js_obfuscation.py", "aciklama": "eval(atob( tespiti"},
    "11": {"ad": "Toplu Tarama", "dosya": "11_toplu_tarama.py", "aciklama": "100+ link bulk scan"},
    "12": {"ad": "Yerel Kara Liste", "dosya": "12_yerel_karaliste.py", "aciklama": "Özel engelleme listesi"},
    "13": {"ad": "USOM İhbar", "dosya": "13_usom_ihbar.py", "aciklama": "Otomatik ihbar hazırla"},
    "14": {"ad": "Telegram Bot", "dosya": "14_telegram_bot.py", "aciklama": "Telegram alarm sistemi"},
    "15": {"ad": "Typosquatting", "dosya": "15_typosquatting.py", "aciklama": "garanti vs garanıti"},
    "16": {"ad": "IP Geolocation", "dosya": "16_ip_geolocation.py", "aciklama": "TR site + Nijerya IP"},
    "17": {"ad": "Emniyet Siber", "dosya": "17_emniyet_siber.py", "aciklama": "EGM ihbar formu"},
    "18": {"ad": "Fidye Kontrol", "dosya": "18_fidye_kontrol.py", "aciklama": "Fidye link tespiti"},
    "19": {"ad": "DNS Takip", "dosya": "19_dns_takip.py", "aciklama": "DNS geçmiş takibi"},
    "20": {"ad": "Telegram Komut", "dosya": "20_telegram_komut.py", "aciklama": "/tara komut botu"},
    "21": {"ad": "Siber Savunma", "dosya": "21_savunma_merkezi.py", "aciklama": "USOM/BTK Uyumlu Araçlar"},
    "22": {"ad": "Oto Tarama", "dosya": "22_oto_tarama.py", "aciklama": "Otomatik sahte site taraması"},
}

def zaman_damgasi():
    return time.strftime("%Y-%m-%d %H:%M:%S")

def bagimlilik_kontrol():
    """Gerekli kütüphanelerin kurulu olup olmadığını kontrol eder."""
    gerekli_kutuphaneler = ['requests', 'colorama', 'whois', 'beautifulsoup4', 'selenium', 'pillow', 'dnspython']
    eksik = []
    
    for kutuphane in gerekli_kutuphaneler:
        try:
            if kutuphane == 'beautifulsoup4':
                __import__('bs4')
            elif kutuphane == 'python-whois':
                __import__('whois')
            else:
                __import__(kutuphane)
        except ImportError:
            eksik.append(kutuphane)
    
    if eksik:
        print(f"\n{Fore.YELLOW}[!] Eksik kütüphaneler tespit edildi:{Style.RESET_ALL}")
        for kutuphane in eksik:
            print(f"{Fore.RED}  - {kutuphane}{Style.RESET_ALL}")
        print(f"\n{Fore.CYAN}[i] Kurulum için: pip install -r requirements.txt{Style.RESET_ALL}")
        input(f"\n{Fore.YELLOW}Devam etmek için Enter...{Style.RESET_ALL}")
    else:
        print(f"{Fore.GREEN}[+] Tüm kütüphaneler kurulu.{Style.RESET_ALL}")

def acilis_animasyonu():
    """Profesyonel açılış animasyonu - satır satır."""
    os.system('clear' if os.name == 'posix' else 'cls')

    for satir in ANA_LOGO.split('\n'):
        print(satir)
        time.sleep(0.05)

    time.sleep(0.3)

    for satir in ATATURK_IMZASI.split('\n'):
        print(satir)
        time.sleep(0.08)

    time.sleep(0.3)

    soz = random.choice(ATATURK_SOZLERI)
    bilgiler = [
        f"{Fore.CYAN}{'='*70}",
        f"{Fore.WHITE} SÜRÜM: {Fore.GREEN}v{VERSIYON} STABLE",
        f"{Fore.WHITE} GELİŞTİRİCİ: {Fore.YELLOW}efe24code",
        f"{Fore.WHITE} ARAÇ SAYISI: {Fore.GREEN}22 MODÜL ENTEGRE",
        f"{Fore.WHITE} GITHUB: {Fore.CYAN}{GITHUB_URL}",
        f"{Fore.YELLOW} ATATÜRK: \"{soz}\"",
        f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}"
    ]

    for bilgi in bilgiler:
        print(bilgi)
        time.sleep(0.1)

    time.sleep(0.5)
    print(f"\n{Fore.GREEN}[+] Sistem hazır! Vatanı korumaya başlayalım.{Style.RESET_ALL}")
    time.sleep(1)

def ekran_temizle():
    os.system('clear' if os.name == 'posix' else 'cls')

def ana_menu_goster():
    ekran_temizle()
    print(ANA_LOGO)
    print(ATATURK_IMZASI)
    print(f"{Fore.CYAN}{'='*70}")
    print(f"{Fore.WHITE} VA-ATAN ANA KONTROL PANELİ v{VERSIYON} | 22 ARAÇ AKTİF {Style.RESET_ALL}")
    print(f"{Fore.YELLOW} \"{random.choice(ATATURK_SOZLERI)}\" {Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")

    print(f"{Fore.RED}[A]{Fore.WHITE} 🚀 OTOMATİK TARAMA MODU - URL İSTEMEZ, KENDİ BULUR")
    print(f"{Fore.GREEN}[1]{Fore.WHITE} VA-ATAN ARAÇ MENÜSÜ - 22 Modül")
    print(f"{Fore.GREEN}[2]{Fore.WHITE} HAKKIMIZDA - Vizyon & Misyon")
    print(f"{Fore.GREEN}[3]{Fore.WHITE} GÜNCELLEME KONTROL - Yeni Sürüm")
    print(f"{Fore.GREEN}[Q]{Fore.WHITE} ÇIKIŞ{Style.RESET_ALL}")
    print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")

def arac_menusu():
    """22 aracı listeler ve çalıştırır."""
    while True:
        ekran_temizle()
        print(ANA_LOGO)
        print(f"{Fore.CYAN}{'='*70}")
        print(f"{Fore.WHITE} VA-ATAN SİBER GÜVENLİK - 22 ARAÇ {Style.RESET_ALL}")
        print(f"{Fore.YELLOW} \"{random.choice(ATATURK_SOZLERI)}\" {Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")

        for i in range(1, 23, 2):
            sol = ARACLAR[str(i)]
            sag = ARACLAR[str(i+1)] if str(i+1) in ARACLAR else None

            sol_metin = f"{Fore.GREEN}[{i:2d}]{Fore.WHITE} {sol['ad']:<25}"
            if sag:
                sag_metin = f"{Fore.GREEN}[{i+1:2d}]{Fore.WHITE} {sag['ad']}"
                print(f"{sol_metin} {sag_metin}{Style.RESET_ALL}")
            else:
                print(f"{sol_metin}{Style.RESET_ALL}")

        print(f"\n{Fore.CYAN}{'='*70}")
        print(f"{Fore.YELLOW}[?] Araç açıklaması: 1? veya 15? yazın{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[Q] Ana menüye dön{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}")

        secim = input(f"{Fore.WHITE}AY-YILDIZ > Seçim: {Style.RESET_ALL}").strip().lower()

        if secim == 'q':
            break

        if secim.endswith('?'):
            numara = secim[:-1]
            if numara in ARACLAR:
                arac = ARACLAR[numara]
                print(f"\n{Fore.CYAN}{'='*70}")
                print(f"{Fore.WHITE} ARAÇ {numara}: {arac['ad']} {Style.RESET_ALL}")
                print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
                print(f"{Fore.WHITE}Açıklama: {Fore.YELLOW}{arac['aciklama']}{Style.RESET_ALL}")
                print(f"{Fore.WHITE}Dosya: {Fore.CYAN}araclar/{arac['dosya']}{Style.RESET_ALL}")
                print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
                input(f"\n{Fore.YELLOW}Devam için Enter...{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}Geçersiz araç numarası!{Style.RESET_ALL}")
                time.sleep(1.5)
            continue

        if secim in ARACLAR:
            arac = ARACLAR[secim]
            arac_yolu = os.path.join("araclar", arac['dosya'])

            if not os.path.exists(arac_yolu):
                print(f"{Fore.RED}[X] Araç bulunamadı: {arac_yolu}{Style.RESET_ALL}")
                time.sleep(2)
                continue

            print(f"\n{Fore.GREEN}[+] {arac['ad']} başlatılıyor...{Style.RESET_ALL}")
            time.sleep(1)

            try:
                subprocess.run([sys.executable, arac_yolu])
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}[!] Araç kullanıcı tarafından durduruldu{Style.RESET_ALL}")
            except Exception as e:
                print(f"\n{Fore.RED}[X] Araç hatası: {e}{Style.RESET_ALL}")

            input(f"\n{Fore.YELLOW}Ana menüye dönmek için Enter...{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Geçersiz seçim! 1-21 arası veya Q{Style.RESET_ALL}")
            time.sleep(1.5)

def hakkinda():
    ekran_temizle()
    print(ANA_LOGO)
    print(f"{Fore.CYAN}{'='*70}")
    print(f"{Fore.WHITE} HAKKIMIZDA - VA-ATAN SİBER GÜVENLİK {Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")
    print(f"{Fore.WHITE}VA-ATAN, Türk milletinin siber güvenliğini korumak için")
    print(f"{Fore.WHITE}geliştirilmiş %100 yerli ve milli bir siber güvenlik aracıdır.")
    print(f"{Fore.WHITE}Mustafa Kemal Atatürk'ün 'Yurtta sulh, cihanda sulh' ilkesiyle,")
    print(f"{Fore.WHITE}vatanımızı dijital tehditlere karşı korumayı hedefler.")
    print(f"\n{Fore.WHITE}Geliştirici: {Fore.YELLOW}efe24code")
    print(f"{Fore.WHITE}İlham: {Fore.YELLOW}Mustafa Kemal Atatürk")
    print(f"{Fore.WHITE}Forum: {Fore.CYAN}{FORUM_LINK}")
    print(f"{Fore.WHITE}GitHub: {Fore.CYAN}{GITHUB_URL}")
    print(f"\n{Fore.YELLOW}\"Hayatta en hakiki mürşit ilimdir.\" - M.K. Atatürk{Style.RESET_ALL}")
    print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
    input(f"\n{Fore.YELLOW}Ana menüye dönmek için Enter...{Style.RESET_ALL}")

def guncelleme_kontrol():
    try:
        import requests
        print(f"\n{Fore.CYAN}[+] Güncelleme kontrol ediliyor...{Style.RESET_ALL}")
        response = requests.get(GUNCELLEME_URL, timeout=5)
        if response.status_code == 200:
            data = response.json()
            surum = data.get('version', VERSIYON)
            if surum != VERSIYON:
                print(f"{Fore.YELLOW}[!] Yeni sürüm mevcut: v{surum}{Style.RESET_ALL}")
                print(f"{Fore.WHITE}Şu anki sürüm: v{VERSIYON}{Style.RESET_ALL}")
            else:
                print(f"{Fore.GREEN}[+] Güncel sürüm kullanıyorsunuz.{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}[!] Güncelleme kontrolü başarısız.{Style.RESET_ALL}")
    except:
        print(f"{Fore.YELLOW}[!] İnternet bağlantısı yok.{Style.RESET_ALL}")
    
    input(f"\n{Fore.YELLOW}Devam için Enter...{Style.RESET_ALL}")

def main():
    acilis_animasyonu()
    bagimlilik_kontrol()
    
    while True:
        ana_menu_goster()
        secim = input(f"{Fore.WHITE}Seçim: {Style.RESET_ALL}").strip().lower()
        
        if secim == 'a':
            # Otomatik tarama modu
            arac_yolu = os.path.join("araclar", "22_oto_tarama.py")
            if os.path.exists(arac_yolu):
                print(f"\n{Fore.GREEN}[+] Otomatik tarama başlatılıyor...{Style.RESET_ALL}")
                time.sleep(1)
                try:
                    subprocess.run([sys.executable, arac_yolu])
                except KeyboardInterrupt:
                    print(f"\n{Fore.YELLOW}[!] Tarama kullanıcı tarafından durduruldu{Style.RESET_ALL}")
                except Exception as e:
                    print(f"\n{Fore.RED}[X] Tarama hatası: {e}{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}[X] Otomatik tarama modülü bulunamadı.{Style.RESET_ALL}")
        elif secim == '1':
            arac_menusu()
        elif secim == '2':
            hakkinda()
        elif secim == '3':
            guncelleme_kontrol()
        elif secim == 'q':
            print(f"\n{Fore.YELLOW}[!] VA-ATAN kapatılıyor...{Style.RESET_ALL}")
            print(f"{Fore.CYAN}\"Egemenlik verilmez, alınır.\" - M.K. Atatürk{Style.RESET_ALL}")
            time.sleep(1)
            break
        else:
            print(f"{Fore.RED}Geçersiz seçim!{Style.RESET_ALL}")
            time.sleep(1)

if __name__ == "__main__":
    main()
