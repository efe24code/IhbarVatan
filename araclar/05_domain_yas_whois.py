# GÖREV: Domain'in kayıt tarihini, sahibini, gizli mi açık mı olduğunu tespit eder. Yeni domain = şüpheli.
import os, sys, time, datetime, re, socket, json
from colorama import Fore, Back, Style, init
init(autoreset=True)

# ================================================
VERSIYON = "4.0.1"
ARAC_ADI = "DOMAİN YAŞI + WHOİS"
RENK = Fore.BLUE
LOG_DOSYASI = "raporlar/whois_log.txt"

# Load config
CONFIG = {}
try:
    with open("config.json", "r", encoding="utf-8") as f:
        CONFIG = json.load(f)
except:
    CONFIG = {}

# ŞÜPHELİ DURUMLAR
thresholds = CONFIG.get("thresholds", {})
KRITIK_YAS_GUN = thresholds.get("domain_critical_days", 30)  # 30 günden yeni domain KRİTİK
UYARI_YAS_GUN = thresholds.get("domain_warning_days", 90)  # 90 günden yeni domain UYARI
SUPHELI_ULKELER = CONFIG.get("suspicious_countries", ["RU", "CN", "KP", "IR", "NG", "PK"])  # Yüksek phishing oranı

TR_BAYRAK = f"""{Back.RED}{Fore.WHITE}
██████████████████████████████████████████████████████
██████████████████████████████████████████████████████
███████████████████████ ████████████████████████
███████████████████████ ███ ████████████████████████
███████████████████████ ████████████████████████
██████████████████████████████████████████████████████
██████████████████████████████████████████████████████
{Style.RESET_ALL}"""

WHOIS_LOGOSU = f"""{Fore.BLUE}{Style.BRIGHT}
██╗ ██╗██╗ ██╗ ██████╗ ██╗███████╗
██║ ██║██║ ██║██╔═══██╗██║██╔════╝
██║ █╗ ██║███████║██║ ██║██║███████╗
██║███╗██║██╔══██║██║ ██║██║╚════██║
╚███╔███╔╝██║ ██║╚██████╔╝██║███████║
 ╚══╝╚══╝ ╚═╝ ╚═╝ ╚═════╝ ╚═╝╚══════╝
        D O M A I N A G E & O W N E R S H I P
              I N T E L L I G E N C E
{Style.RESET_ALL}"""

AYYILDIZ_BANNER = f"""{Fore.WHITE}
          &-_____-₺
(_____
_____) -----------)
{Style.RESET_ALL}"""

def ekran_temizle():
    os.system('clear' if os.name == 'posix' else 'cls')

def logo():
    ekran_temizle()
    print(TR_BAYRAK)
    print(WHOIS_LOGOSU)
    print(AYYILDIZ_BANNER)
    print(f"{Fore.BLUE}{'='*80}")
    print(f"{Fore.WHITE} {ARAC_ADI} v{VERSIYON}")
    print(f"{Fore.BLUE}{'='*80}{Style.RESET_ALL}")

def domain_analizi(domain):
    print(f"\n{Fore.YELLOW}[+] Domain analizi yapılıyor: {domain}{Style.RESET_ALL}")
    
    try:
        import whois
        
        print(f"\n{Fore.CYAN}[i] Whois sorgusu yapılıyor...{Style.RESET_ALL}")
        w = whois.whois(domain)
        
        print(f"\n{Fore.CYAN}[i] Domain Bilgileri:{Style.RESET_ALL}")
        
        # Kayıt tarihi
        if w.creation_date:
            if isinstance(w.creation_date, list):
                creation_date = w.creation_date[0]
            else:
                creation_date = w.creation_date
            
            yas_gun = (datetime.datetime.now() - creation_date).days
            print(f"{Fore.WHITE}  Kayıt Tarihi: {Fore.CYAN}{creation_date.strftime('%d.%m.%Y')}{Style.RESET_ALL}")
            print(f"{Fore.WHITE}  Domain Yaşı: {Fore.CYAN}{yas_gun} gün{Style.RESET_ALL}")
            
            if yas_gun <= KRITIK_YAS_GUN:
                print(f"{Fore.RED}[X] KRİTİK: Domain çok yeni ({yas_gun} gün)! Phishing riski yüksek.{Style.RESET_ALL}")
            elif yas_gun <= UYARI_YAS_GUN:
                print(f"{Fore.YELLOW}[!] UYARI: Domain yeni ({yas_gun} gün). Şüpheli.{Style.RESET_ALL}")
            else:
                print(f"{Fore.GREEN}[✓] Domain yaşı normal.{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}[!] Kayıt tarihi bulunamadı.{Style.RESET_ALL}")
        
        # Kayıtçı
        if w.registrar:
            print(f"{Fore.WHITE}  Kayıtçı: {Fore.CYAN}{w.registrar}{Style.RESET_ALL}")
        
        # Ülke
        if w.country:
            print(f"{Fore.WHITE}  Ülke: {Fore.CYAN}{w.country}{Style.RESET_ALL}")
            if w.country in SUPHELI_ULKELER:
                print(f"{Fore.RED}[X] Şüpheli ülke: {w.country}{Style.RESET_ALL}")
        
        # Gizlilik
        if w.org:
            print(f"{Fore.WHITE}  Organizasyon: {Fore.CYAN}{w.org}{Style.RESET_ALL}")
        
        privacy_keywords = ['privacy', 'whois protection', 'domains by proxy', 'redacted']
        if any(keyword in str(w).lower() for keyword in privacy_keywords):
            print(f"{Fore.YELLOW}[!] WHOIS gizlilik koruması aktif.{Style.RESET_ALL}")
        
        return True
    except Exception as e:
        print(f"{Fore.RED}[X] Whois sorgu hatası: {e}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[!] python-whois kütüphanesi kurulu olmayabilir.{Style.RESET_ALL}")
        return False

def main():
    logo()
    
    while True:
        print(f"\n{Fore.CYAN}[1]{Fore.WHITE} Domain Analizi")
        print(f"{Fore.CYAN}[Q]{Fore.WHITE} Ana Menüye Dön")
        print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
        
        secim = input(f"{Fore.WHITE}Seçim: {Style.RESET_ALL}").strip().lower()
        
        if secim == '1':
            domain = input(f"{Fore.WHITE}Domain: {Style.RESET_ALL}").strip()
            if domain:
                domain_analizi(domain)
        elif secim == 'q':
            break
        else:
            print(f"{Fore.RED}Geçersiz seçim!{Style.RESET_ALL}")
        
        input(f"\n{Fore.YELLOW}Devam için Enter...{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
