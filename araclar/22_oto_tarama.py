# OTOMATİK SAHTE SİTE TARAMA MODÜLÜ
import os, sys, time, requests, json, threading
from colorama import init, Fore, Style
init(autoreset=True)

import random

ATATURK_SOZLERI = [
    "Yurtta sulh, cihanda sulh.",
    "Hayatta en hakiki mürşit ilimdir.",
    "Egemenlik verilmez, alınır.",
    "Türk milletinin karakteri, yüksek Türk karakteridir.",
    "Umutsuz durumlar yoktur, umutsuz insanlar vardır."
]

VERSIYON = "1.0.0"
ARAC_ADI = "OTOMATİK SAHTE SİTE TARAMASI"

# Load config
CONFIG = {}
try:
    with open("config.json", "r", encoding="utf-8") as f:
        CONFIG = json.load(f)
except:
    CONFIG = {}

USOM_URL = CONFIG.get("usom_url", "https://www.usom.gov.tr/url-list.txt")
PHISHTANK_API = CONFIG.get("phishtank_api", "https://checkurl.phishtank.com/checkurl/")
YEREL_LISTE = "data/usom_cache.txt"
RAPOR_DOSYASI = "raporlar/oto_tarama_raporu.txt"

# Arama keyword'leri (Türkçe)
ARAMA_KEYWORDLERI = [
    "banka", "e-devlet", "gib", "sgk", "emekli", "ptt", "ziraat", "halkbank",
    "vakifbank", "isbank", "akbank", "garanti", "yapikredi", "finansbank",
    "tcmb", "btk", "usom", "emniyet", "jandarma", "savunma", "askeri",
    "milli", "egitim", "saglik", "corona", "covac", "asi"
]

def ekran_temizle():
    os.system('clear' if os.name == 'posix' else 'cls')

def logo():
    print(f"{Fore.CYAN}{'='*80}")
    print(f"{Fore.WHITE} {ARAC_ADI} v{VERSIYON}")
    print(f"{Fore.CYAN} VA-ATAN SİBER GÜVENLİK | OTOMATİK TEHDİT KEŞFİ")
    print(f"{Fore.YELLOW} \"{random.choice(ATATURK_SOZLERI)}\" {Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}")

def usom_listesi_indir():
    """USOM kara listesini indirir."""
    print(f"\n{Fore.YELLOW}[+] USOM kara listesi indiriliyor...{Style.RESET_ALL}")
    try:
        headers = {'User-Agent': 'VA-ATAN-SIBER-GUVENLIK/1.0.0'}
        r = requests.get(USOM_URL, timeout=30, headers=headers)
        r.raise_for_status()
        os.makedirs("data", exist_ok=True)
        with open(YEREL_LISTE, "w", encoding="utf-8") as f:
            f.write(r.text)
        print(f"{Fore.GREEN}[✓] USOM listesi indirildi.{Style.RESET_ALL}")
        return r.text.splitlines()
    except Exception as e:
        print(f"{Fore.RED}[X] USOM indirme hatası: {e}{Style.RESET_ALL}")
        if os.path.exists(YEREL_LISTE):
            with open(YEREL_LISTE, "r", encoding="utf-8") as f:
                return f.read().splitlines()
        return []

def url_bul():
    """Çeşitli kaynaklardan şüpheli URL'leri bulur."""
    print(f"\n{Fore.YELLOW}[+] Şüpheli URL'ler aranıyor...{Style.RESET_ALL}")
    
    url_listesi = []
    
    # 1. USOM listesinden
    usom_urller = usom_listesi_indir()
    url_listesi.extend(usom_urller[:100])  # İlk 100 URL
    print(f"{Fore.CYAN}[i] USOM'den {len(usom_urller[:100])} URL alındı.{Style.RESET_ALL}")
    
    # 2. Yerel kara listeden
    yerel_liste = "data/yerel_karaliste.txt"
    if os.path.exists(yerel_liste):
        with open(yerel_liste, "r", encoding="utf-8") as f:
            yerel_urller = [line.strip() for line in f if line.strip()]
            url_listesi.extend(yerel_urller)
            print(f"{Fore.CYAN}[i] Yerel listeden {len(yerel_urller)} URL alındı.{Style.RESET_ALL}")
    
    # 3. Rastgele olası phishing domainleri oluştur
    olasi_phishing = []
    bankalar = ["ziraat", "halkbank", "vakif", "isbank", "akbank", "garanti", "yapikredi", "finansbank"]
    gov_kurumlari = ["gib", "sgk", "emekli", "ptt", "meb", "saglik", "corona", "covac", "asi"]
    uzantilar = [".com", ".net", ".org", ".tk", ".ml", ".ga", ".cf", ".xyz"]
    
    for banka in bankalar:
        for uzanti in uzantilar:
            # Typo variations
            olasi_phishing.append(f"{banka}{uzanti}")
            olasi_phishing.append(f"{banka}bank{uzanti}")
            olasi_phishing.append(f"www.{banka}{uzanti}")
            olasi_phishing.append(f"{banka}-online{uzanti}")
            olasi_phishing.append(f"{banka}-login{uzanti}")
            olasi_phishing.append(f"{banka}-giris{uzanti}")
    
    for kurum in gov_kurumlari:
        for uzanti in uzantilar:
            olasi_phishing.append(f"{kurum}{uzanti}")
            olasi_phishing.append(f"{kurum}.gov{uzanti}")
            olasi_phishing.append(f"www.{kurum}{uzanti}")
            olasi_phishing.append(f"{kurum}-tr{uzanti}")
    
    url_listesi.extend(olasi_phishing)
    print(f"{Fore.CYAN}[i] Olası phishing domainleri: {len(olasi_phishing)}{Style.RESET_ALL}")
    
    # 4. Bilinen phishing pattern'leri
    phishing_patterns = [
        "login-", "-login", "-secure", "secure-", "verify-", "-verify",
        "account-", "-account", "update-", "-update", "confirm-", "-confirm"
    ]
    
    for pattern in phishing_patterns:
        for banka in bankalar[:3]:  # Sınırlı sayıda
            for uzanti in uzantilar[:3]:
                olasi_phishing.append(f"{banka}{pattern}{uzanti}")
    
    print(f"{Fore.CYAN}[i] Phishing pattern'leri: {len(phishing_patterns) * 3 * 3}{Style.RESET_ALL}")
    
    # URL'leri temizle ve benzersiz yap
    url_listesi = list(set([url.strip() for url in url_listesi if url.strip()]))
    
    print(f"{Fore.GREEN}[✓] Toplam {len(url_listesi)} URL bulundu.{Style.RESET_ALL}")
    return url_listesi

def url_tara(url, usom_listesi):
    """Tek bir URL'yi tarar."""
    try:
        # Önce USOM listesinde kontrol et
        if usom_listesi:
            if any(url.lower() in line.lower() for line in usom_listesi):
                return {"url": url, "sonuc": "TEHLİKE", "kaynak": "USOM_LİSTE", "durum": "ZATEN_LİSTEDE"}
        
        # HTTP yanıt kontrolü (curl benzeri)
        try:
            if not url.startswith('http'):
                url = 'https://' + url
            r = requests.head(url, timeout=5, allow_redirects=True)
            durum = f"HTTP {r.status_code}"
            
            if r.status_code == 200:
                return {"url": url, "sonuc": "AÇIK", "kaynak": "CURL", "durum": durum}
            elif r.status_code in [301, 302, 307, 308]:
                return {"url": url, "sonuc": "YÖNLENDİRME", "kaynak": "CURL", "durum": durum}
            elif r.status_code == 404:
                return {"url": url, "sonuc": "KAPALI", "kaynak": "CURL", "durum": durum}
            else:
                return {"url": url, "sonuc": "ŞÜPHELİ", "kaynak": "CURL", "durum": durum}
        except requests.exceptions.Timeout:
            return {"url": url, "sonuc": "ZAMAN_AŞIMI", "kaynak": "CURL", "durum": "TIMEOUT"}
        except requests.exceptions.ConnectionError:
            return {"url": url, "sonuc": "BAĞLANTI_HATASI", "kaynak": "CURL", "durum": "CONNECTION_ERROR"}
        except:
            return {"url": url, "sonuc": "ERİŞİLEMEZ", "kaynak": "CURL", "durum": "UNREACHABLE"}
            
    except:
        return {"url": url, "sonuc": "HATA", "kaynak": "KONTROL_HATASI", "durum": "ERROR"}

def coklu_tarama(url_listesi, usom_listesi=None, max_thread=20):
    """Multi-thread ile hızlı tarama."""
    print(f"\n{Fore.YELLOW}[+] {len(url_listesi)} URL taranıyor...{Style.RESET_ALL}")
    print(f"{Fore.CYAN}[i] Thread sayısı: {max_thread}{Style.RESET_ALL}")
    
    if usom_listesi is None:
        usom_listesi = []
        if os.path.exists(YEREL_LISTE):
            with open(YEREL_LISTE, "r", encoding="utf-8") as f:
                usom_listesi = f.read().splitlines()
    
    print(f"{Fore.CYAN}[i] USOM listesi: {len(usom_listesi)} URL{Style.RESET_ALL}")
    
    sonuclar = []
    tamamlanan = 0
    kilit = threading.Lock()
    
    def tarama_thread(urller):
        nonlocal tamamlanan
        thread_sonuclar = []
        for url in urller:
            sonuc = url_tara(url, usom_listesi)
            thread_sonuclar.append(sonuc)
            with kilit:
                tamamlanan += 1
                if tamamlanan % 50 == 0:
                    print(f"{Fore.CYAN}[i] İlerleme: {tamamlanan}/{len(url_listesi)} ({int(tamamlanan/len(url_listesi)*100)}%){Style.RESET_ALL}")
        return thread_sonuclar
    
    # URL'leri thread'lere böl
    chunk_size = max(1, len(url_listesi) // max_thread)
    chunks = [url_listesi[i:i + chunk_size] for i in range(0, len(url_listesi), chunk_size)]
    
    threads = []
    for chunk in chunks:
        thread = threading.Thread(target=lambda c=chunk: thread_sonuclar.extend(tarama_thread(c)))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    print(f"{Fore.GREEN}[✓] Tarama tamamlandı.{Style.RESET_ALL}")
    return thread_sonuclar

def raporla(sonuclar):
    """Sonuçları raporlar."""
    print(f"\n{Fore.YELLOW}[+] Rapor oluşturuluyor...{Style.RESET_ALL}")
    
    usom_de = [s for s in sonuclar if s["sonuc"] == "TEHLİKE" and s["durum"] == "ZATEN_LİSTEDE"]
    acik = [s for s in sonuclar if s["sonuc"] == "AÇIK"]
    kapali = [s for s in sonuclar if s["sonuc"] == "KAPALI"]
    yonlendirme = [s for s in sonuclar if s["sonuc"] == "YÖNLENDİRME"]
    supheliler = [s for s in sonuclar if s["sonuc"] in ["ŞÜPHELİ", "ZAMAN_AŞIMI", "BAĞLANTI_HATASI", "ERİŞİLEMEZ"]]
    hatalar = [s for s in sonuclar if s["sonuc"] == "HATA"]
    
    print(f"\n{Fore.CYAN}{'='*80}")
    print(f"{Fore.WHITE} TARAMA RAPORU")
    print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
    print(f"{Fore.RED}USOM LİSTEDE: {len(usom_de)}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}AÇIK SİTELER: {len(acik)}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}KAPALI SİTELER: {len(kapali)}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}YÖNLENDİRME: {len(yonlendirme)}{Style.RESET_ALL}")
    print(f"{Fore.RED}ŞÜPHELİ: {len(supheliler)}{Style.RESET_ALL}")
    print(f"{Fore.WHITE}HATA: {len(hatalar)}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
    
    if acik:
        print(f"\n{Fore.GREEN}[+] AÇIK SİTELER (USOM'de OLMAYAN):{Style.RESET_ALL}")
        for a in acik[:20]:
            print(f"{Fore.GREEN}  - {a['url']} ({a['durum']}){Style.RESET_ALL}")
    
    if yonlendirme:
        print(f"\n{Fore.CYAN}[+] YÖNLENDİRME YAPAN SİTELER:{Style.RESET_ALL}")
        for y in yonlendirme[:10]:
            print(f"{Fore.CYAN}  - {y['url']} ({y['durum']}){Style.RESET_ALL}")
    
    if usom_de:
        print(f"\n{Fore.RED}[!] USOM LİSTEDE OLANLAR (TARANMADI):{Style.RESET_ALL}")
        for u in usom_de[:10]:
            print(f"{Fore.RED}  - {u['url']}{Style.RESET_ALL}")
    
    # Dosyaya kaydet
    os.makedirs("raporlar", exist_ok=True)
    with open(RAPOR_DOSYASI, "w", encoding="utf-8") as f:
        f.write("OTOMATİK TARAMA RAPORU\n")
        f.write("="*80 + "\n\n")
        f.write(f"USOM LİSTEDE: {len(usom_de)}\n")
        f.write(f"AÇIK SİTELER: {len(acik)}\n")
        f.write(f"KAPALI SİTELER: {len(kapali)}\n")
        f.write(f"YÖNLENDİRME: {len(yonlendirme)}\n")
        f.write(f"ŞÜPHELİ: {len(supheliler)}\n")
        f.write(f"HATA: {len(hatalar)}\n\n")
        f.write("AÇIK SİTELER (USOM'de OLMAYAN):\n")
        for a in acik:
            f.write(f"  - {a['url']} ({a['durum']})\n")
        f.write("\nYÖNLENDİRME YAPAN SİTELER:\n")
        for y in yonlendirme:
            f.write(f"  - {y['url']} ({y['durum']})\n")
        f.write("\nUSOM LİSTEDE OLANLAR:\n")
        for u in usom_de:
            f.write(f"  - {u['url']}\n")
    
    print(f"\n{Fore.GREEN}[✓] Rapor kaydedildi: {RAPOR_DOSYASI}{Style.RESET_ALL}")

def main():
    logo()
    
    while True:
        print(f"\n{Fore.CYAN}[1]{Fore.WHITE} Otomatik Tarama Başlat")
        print(f"{Fore.CYAN}[2]{Fore.WHITE} URL Listesini Göster")
        print(f"{Fore.CYAN}[3]{Fore.WHITE} Raporları Görüntüle")
        print(f"{Fore.CYAN}[Q]{Fore.WHITE} Ana Menüye Dön")
        print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
        
        secim = input(f"{Fore.WHITE}Seçim: {Style.RESET_ALL}").strip().lower()
        
        if secim == '1':
            print(f"\n{Fore.YELLOW}[!] Otomatik tarama başlatılıyor...{Style.RESET_ALL}")
            url_listesi = url_bul()
            if url_listesi:
                sonuclar = coklu_tarama(url_listesi)
                raporla(sonuclar)
        elif secim == '2':
            url_listesi = url_bul()
            print(f"\n{Fore.CYAN}[i] Bulunan URL'ler ({len(url_listesi)}):{Style.RESET_ALL}")
            for url in url_listesi[:20]:
                print(f"  {url}")
        elif secim == '3':
            if os.path.exists(RAPOR_DOSYASI):
                with open(RAPOR_DOSYASI, "r", encoding="utf-8") as f:
                    print(f"\n{Fore.CYAN}{f.read()}{Style.RESET_ALL}")
            else:
                print(f"{Fore.YELLOW}[!] Henüz rapor yok.{Style.RESET_ALL}")
        elif secim == 'q':
            break
        else:
            print(f"{Fore.RED}Geçersiz seçim!{Style.RESET_ALL}")
        
        input(f"\n{Fore.YELLOW}Devam için Enter...{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
