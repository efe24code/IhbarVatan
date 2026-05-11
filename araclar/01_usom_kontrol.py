import os, sys, time, requests, json
from colorama import init, Fore, Style
init(autoreset=True)

# Load config
CONFIG = {}
try:
    with open("config.json", "r", encoding="utf-8") as f:
        CONFIG = json.load(f)
except:
    CONFIG = {
        "usom_url": "https://www.usom.gov.tr/url-list.txt"
    }

USOM_URL = CONFIG.get("usom_url", "https://www.usom.gov.tr/url-list.txt")
YEREL_LISTE = "data/usom_cache.txt"
VERSIYON = "5.2.2"

BAYRAK = f"""{Fore.RED}
████████████████████████████████████████████████
████████████████████████████████████████████████
████████████████████████████████████████████████████████████████████████████████
████████████████████████████████████████████████
████████████████████████████████████████████████
████████████████████████████████████████████████
████████████████████████████████████████████████████████████████████████████████
████████████████████████████████████████████████
████████████████████████████████████████████████
████████████████████████████████████████████████
████████████████████████████████████████████████████████████████████████████████
██████████████████████████████████████████████{Fore.WHITE}▒▒▒▒▒▒{Fore.RED}████████████████████████████████████████
██████████████████████████████████████████{Fore.WHITE}▒▒▒▒▒▒▒▒{Fore.RED}████████████████████████████████████
██████████████████████████████████████{Fore.WHITE}▒▒▒▒▒▒{Fore.RED}████████████████████████████████
██████████████████████████████████{Fore.WHITE}▒▒▒▒{Fore.RED}████████████████████████████
██████████████████████████████{Fore.WHITE}▒▒▒▒▒▒▒▒▒▒{Fore.RED}████████████████████████
██████████████████████████{Fore.WHITE}▒▒▒▒{Fore.RED}████████████████████
██████████████████████{Fore.WHITE}▒▒▒▒▒▒{Fore.RED}████████████████
██████████████████{Fore.WHITE}▒▒▒▒{Fore.RED}████████████
██████████████{Fore.WHITE}▒▒▒▒▒▒{Fore.RED}████████
██████████{Fore.WHITE}▒▒▒▒{Fore.RED}████
██████{Fore.WHITE}▒▒▒▒▒▒▒▒▒▒{Fore.RED}
██{Fore.WHITE}▒▒▒▒{Fore.RED}
{Fore.WHITE}▒▒▒▒▒▒{Fore.RED}
{Fore.WHITE}▒▒▒▒▒▒{Fore.RED}
██{Fore.WHITE}▒▒▒▒▒▒▒▒{Fore.RED}
██████{Fore.WHITE}▒▒▒▒▒▒{Fore.RED}
██████████{Fore.WHITE}▒▒▒▒▒▒▒▒▒▒{Fore.RED}████
██████████████{Fore.WHITE}▒▒▒▒▒▒▒▒▒▒{Fore.RED}████████
██████████████████{Fore.WHITE}▒▒▒▒▒▒▒▒{Fore.RED}████████████
██████████████████████{Fore.WHITE}▒▒▒▒▒▒▒▒▒▒{Fore.RED}████████████████
██████████████████████████{Fore.WHITE}▒▒▒▒{Fore.RED}████████████████████
██████████████████████████████{Fore.WHITE}▒▒▒▒▒▒▒▒▒▒{Fore.RED}████████████████████████
██████████████████████████████████{Fore.WHITE}▒▒▒▒▒▒▒▒{Fore.RED}████████████████████████████
██████████████████████████████████████{Fore.WHITE}▒▒▒▒▒▒▒▒▒▒{Fore.RED}████████████████████████████████
██████████████████████████████████████████{Fore.WHITE}▒▒▒▒{Fore.RED}████████████████████████████████████
██████████████████████████████████████████████{Fore.WHITE}▒▒▒▒▒▒{Fore.RED}████████████████████████████████████████
████████████████████████████████████████████████████████████████████████████████
████████████████████████████████████████████████
████████████████████████████████████████████████
████████████████████████████████████████████████
████████████████████████████████████████████████████████████████████████████████
████████████████████████████████████████████████
████████████████████████████████████████████████
{Style.RESET_ALL}"""

def ekran_temizle():
    os.system('clear' if os.name == 'posix' else 'cls')

def logo():
    ekran_temizle()
    print(BAYRAK)
    print(f"{Fore.RED}{'='*80}{Style.RESET_ALL}")
    print(f"{Fore.WHITE} USOM KONTROL MODÜLÜ v{VERSIYON} | BAYRAK: 2647 KARAKTER{Style.RESET_ALL}")
    print(f"{Fore.RED} AY-YILDIZ SİBER KALKAN | T.C. ULAŞTIRMA BAKANLIĞI USOM ENTEGRASYON{Style.RESET_ALL}")
    print(f"{Fore.RED}{'='*80}{Style.RESET_ALL}")

def listeyi_guncelle():
    print(f"\n{Fore.YELLOW}[+] USOM zararlı listesi indiriliyor...{Style.RESET_ALL}")
    try:
        headers = {'User-Agent': 'AY-YILDIZ-SIBER-KALKAN/5.2.2'}
        r = requests.get(USOM_URL, timeout=30, headers=headers)
        r.raise_for_status()
        os.makedirs("data", exist_ok=True)
        with open(YEREL_LISTE, "w", encoding="utf-8") as f:
            f.write(r.text)
        kayit = len(r.text.splitlines())
        boyut = round(len(r.content)/1024, 2)
        print(f"{Fore.GREEN}[✓] Liste güncellendi.{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[i] Toplam Kayıt: {kayit} | Boyut: {boyut} KB{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[i] Tarih: {time.strftime('%d.%m.%Y %H:%M:%S')}{Style.RESET_ALL}")
        return True
    except Exception as e:
        print(f"{Fore.RED}[X] USOM bağlantı hatası: {e}{Style.RESET_ALL}")
        if os.path.exists(YEREL_LISTE):
            print(f"{Fore.YELLOW}[i] Yerel önbellek kullanılacak.{Style.RESET_ALL}")
            return True
        return False

def sorgula(domain):
    if not os.path.exists(YEREL_LISTE):
        print(f"{Fore.RED}[X] Yerel liste yok. Önce [1] ile güncelle.{Style.RESET_ALL}")
        return False
    
    try:
        with open(YEREL_LISTE, "r", encoding="utf-8") as f:
            liste = f.read().splitlines()
        
        domain = domain.strip().lower()
        if domain.startswith("http://"):
            domain = domain.replace("http://", "")
        elif domain.startswith("https://"):
            domain = domain.replace("https://", "")
        
        if domain.endswith("/"):
            domain = domain[:-1]
        
        for satir in liste:
            if satir.strip().lower() in domain or domain in satir.strip().lower():
                print(f"\n{Fore.RED}[!] TEHLİKE TESPİT EDİLDİ!{Style.RESET_ALL}")
                print(f"{Fore.RED}[X] Domain USOM kara listesinde: {satir.strip()}{Style.RESET_ALL}")
                return True
        
        print(f"\n{Fore.GREEN}[✓] Güvenli: {domain}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[i] Domain USOM kara listesinde bulunamadı.{Style.RESET_ALL}")
        return False
    except Exception as e:
        print(f"{Fore.RED}[X] Sorgu hatası: {e}{Style.RESET_ALL}")
        return False

def main():
    logo()
    
    while True:
        print(f"\n{Fore.CYAN}[1]{Fore.WHITE} USOM Listesini Güncelle")
        print(f"{Fore.CYAN}[2]{Fore.WHITE} Domain Sorgula")
        print(f"{Fore.CYAN}[Q]{Fore.WHITE} Ana Menüye Dön")
        print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
        
        secim = input(f"{Fore.WHITE}Seçim: {Style.RESET_ALL}").strip().lower()
        
        if secim == '1':
            listeyi_guncelle()
        elif secim == '2':
            domain = input(f"{Fore.WHITE}Domain: {Style.RESET_ALL}").strip()
            if domain:
                sorgula(domain)
        elif secim == 'q':
            break
        else:
            print(f"{Fore.RED}Geçersiz seçim!{Style.RESET_ALL}")
        
        input(f"\n{Fore.YELLOW}Devam için Enter...{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
