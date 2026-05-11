# OTOMATİK SAHTE SİTE TARAMA MODÜLÜ
import os, sys, time, requests, json, threading
from colorama import init, Fore, Style
init(autoreset=True)

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
    print(f"{Fore.CYAN} AY-YILDIZ SİBER KALKAN | OTOMATİK TEHDİT KEŞFİ")
    print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}")

def usom_listesi_indir():
    """USOM kara listesini indirir."""
    print(f"\n{Fore.YELLOW}[+] USOM kara listesi indiriliyor...{Style.RESET_ALL}")
    try:
        headers = {'User-Agent': 'AY-YILDIZ-SIBER-KALKAN/1.0.0'}
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

def url_tara(url):
    """Tek bir URL'yi tarar."""
    try:
        # USOM kontrolü
        if os.path.exists(YEREL_LISTE):
            with open(YEREL_LISTE, "r", encoding="utf-8") as f:
                usom_listesi = f.read().splitlines()
                if any(url.lower() in line.lower() for line in usom_listesi):
                    return {"url": url, "sonuc": "TEHLİKE", "kaynak": "USOM"}
        
        # Basit URL analizi
        if len(url) > 50:
            return {"url": url, "sonuc": "ŞÜPHELİ", "kaynak": "UZUN_URL"}
        
        if url.count(".") > 3:
            return {"url": url, "sonuc": "ŞÜPHELİ", "kaynak": "COK_NOKTA"}
        
        return {"url": url, "sonuc": "GÜVENLİ", "kaynak": "BASIT_KONTROL"}
    except:
        return {"url": url, "sonuc": "HATA", "kaynak": "KONTROL_HATASI"}

def coklu_tarama(url_listesi, max_thread=20):
    """Multi-thread ile hızlı tarama."""
    print(f"\n{Fore.YELLOW}[+] {len(url_listesi)} URL taranıyor...{Style.RESET_ALL}")
    print(f"{Fore.CYAN}[i] Thread sayısı: {max_thread}{Style.RESET_ALL}")
    
    sonuclar = []
    tamamlanan = 0
    kilit = threading.Lock()
    
    def tarama_thread(urller):
        nonlocal tamamlanan
        thread_sonuclar = []
        for url in urller:
            sonuc = url_tara(url)
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
    
    tehlikeler = [s for s in sonuclar if s["sonuc"] == "TEHLİKE"]
    supheliler = [s for s in sonuclar if s["sonuc"] == "ŞÜPHELİ"]
    guvenliler = [s for s in sonuclar if s["sonuc"] == "GÜVENLİ"]
    hatalar = [s for s in sonuclar if s["sonuc"] == "HATA"]
    
    print(f"\n{Fore.CYAN}{'='*80}")
    print(f"{Fore.WHITE} TARAMA RAPORU")
    print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
    print(f"{Fore.RED}TEHLİKE: {len(tehlikeler)}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}ŞÜPHELİ: {len(supheliler)}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}GÜVENLİ: {len(guvenliler)}{Style.RESET_ALL}")
    print(f"{Fore.WHITE}HATA: {len(hatalar)}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
    
    if tehlikeler:
        print(f"\n{Fore.RED}[!] TEHLİKELİ SİTELER:{Style.RESET_ALL}")
        for t in tehlikeler[:10]:
            print(f"{Fore.RED}  - {t['url']} ({t['kaynak']}){Style.RESET_ALL}")
    
    if supheliler:
        print(f"\n{Fore.YELLOW}[!] ŞÜPHELİ SİTELER:{Style.RESET_ALL}")
        for s in supheliler[:10]:
            print(f"{Fore.YELLOW}  - {s['url']} ({s['kaynak']}){Style.RESET_ALL}")
    
    # Dosyaya kaydet
    os.makedirs("raporlar", exist_ok=True)
    with open(RAPOR_DOSYASI, "w", encoding="utf-8") as f:
        f.write("OTOMATİK TARAMA RAPORU\n")
        f.write("="*80 + "\n\n")
        f.write(f"TEHLİKE: {len(tehlikeler)}\n")
        f.write(f"ŞÜPHELİ: {len(supheliler)}\n")
        f.write(f"GÜVENLİ: {len(guvenliler)}\n")
        f.write(f"HATA: {len(hatalar)}\n\n")
        f.write("TEHLİKELİ SİTELER:\n")
        for t in tehlikeler:
            f.write(f"  - {t['url']} ({t['kaynak']})\n")
        f.write("\nŞÜPHELİ SİTELER:\n")
        for s in supheliler:
            f.write(f"  - {s['url']} ({s['kaynak']})\n")
    
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
