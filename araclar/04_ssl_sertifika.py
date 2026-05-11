# GÖREV: Sitenin SSL sertifikasını inceler. Sahte/kısa süreli/güvensiz sertifikaları tespit eder.
import os, sys, time, datetime, ssl, socket, re, json
from colorama import Fore, Back, Style, init
init(autoreset=True)

# ================================================
VERSIYON = "4.0.1"
ARAC_ADI = "SSL SERTİFİKA ANALİZİ"
RENK = Fore.GREEN
LOG_DOSYASI = "raporlar/ssl_log.txt"

# Load config
CONFIG = {}
try:
    with open("config.json", "r", encoding="utf-8") as f:
        CONFIG = json.load(f)
except:
    CONFIG = {}

# GÜVENİLİR CA LİSTESİ
GUVENILIR_CA = CONFIG.get("trusted_ca", [
    "DigiCert", "Let's Encrypt", "GlobalSign", "Sectigo", "GoDaddy",
    "Google Trust Services", "Amazon", "Cloudflare", "Microsoft", "Apple"
])

# ŞÜPHELİ DURUMLAR
thresholds = CONFIG.get("thresholds", {})
SUPHELI_SURE_GUN = thresholds.get("ssl_warning_days", 90)  # 90 günden kısa sertifika şüpheli
KRITIK_SURE_GUN = thresholds.get("ssl_critical_days", 30)  # 30 günden kısa çok şüpheli

TR_BAYRAK = f"""{Back.RED}{Fore.WHITE}
██████████████████████████████████████████████████████
██████████████████████████████████████████████████████
███████████████████████ ████████████████████████
███████████████████████ ███ ████████████████████████
███████████████████████ ████████████████████████
██████████████████████████████████████████████████████
██████████████████████████████████████████████████████
{Style.RESET_ALL}"""

SSL_LOGOSU = f"""{Fore.GREEN}{Style.BRIGHT}
███████╗███████╗██╗░░░░░ ██████╗███████╗██████╗░████████╗
██╔════╝██╔════╝██║░░░░░  ██╔════╝██╔════╝██╔══██╗╚══██╔══╝
███████╗█████╗░░██║░░░░░  ██║░░░░░█████╗░░██████╔╝░░░██║░░░
╚════██║██╔══╝░░██║░░░░░  ██║░░░░░██╔══╝░░██╔══██╗░░░██║░░░
███████║███████╗███████╗  ╚██████╗███████╗██║░░██║░░░██║░░░
╚══════╝╚══════╝╚══════╝  ░╚═════╝╚══════╝╚═╝░░╚═╝░░░╚═╝░░░
                    C E R T I F I C A T E
                    S E C U R I T Y A N A L Y S I S
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
    print(SSL_LOGOSU)
    print(AYYILDIZ_BANNER)
    print(f"{Fore.GREEN}{'='*80}")
    print(f"{Fore.WHITE} {ARAC_ADI} v{VERSIYON}")
    print(f"{Fore.GREEN}{'='*80}{Style.RESET_ALL}")

def ssl_kontrol(domain):
    print(f"\n{Fore.YELLOW}[+] SSL sertifikası analiz ediliyor: {domain}{Style.RESET_ALL}")
    
    try:
        context = ssl.create_default_context()
        
        with socket.create_connection((domain, 443), timeout=10) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                
                print(f"\n{Fore.CYAN}[i] Sertifika Bilgileri:{Style.RESET_ALL}")
                print(f"{Fore.WHITE}  Konu: {Fore.CYAN}{cert.get('subject', [[['', '']]])[0][0][1]}{Style.RESET_ALL}")
                print(f"{Fore.WHITE}  Veren: {Fore.CYAN}{cert.get('issuer', [[['', '']]])[0][0][1]}{Style.RESET_ALL}")
                print(f"{Fore.WHITE}  Sürüm: {Fore.CYAN}{cert.get('version', 'N/A')}{Style.RESET_ALL}")
                
                # Tarih analizi
                not_before = datetime.datetime.strptime(cert['notBefore'], '%b %d %H:%M:%S %Y %Z')
                not_after = datetime.datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                kalan_gun = (not_after - datetime.datetime.utcnow()).days
                
                print(f"{Fore.WHITE}  Başlangıç: {Fore.CYAN}{not_before.strftime('%d.%m.%Y')}{Style.RESET_ALL}")
                print(f"{Fore.WHITE}  Bitiş: {Fore.CYAN}{not_after.strftime('%d.%m.%Y')}{Style.RESET_ALL}")
                print(f"{Fore.WHITE}  Kalan Gün: {Fore.CYAN}{kalan_gun}{Style.RESET_ALL}")
                
                # CA analizi
                issuer = str(cert.get('issuer', [[['', '']]])[0][0][1])
                guvenilir_ca = any(ca.lower() in issuer.lower() for ca in GUVENILIR_CA)
                
                print(f"\n{Fore.CYAN}[i] Güvenlik Analizi:{Style.RESET_ALL}")
                
                if kalan_gun <= KRITIK_SURE_GUN:
                    print(f"{Fore.RED}[X] KRİTİK: Sertifika {kalan_gun} gün içinde bitecek!{Style.RESET_ALL}")
                elif kalan_gun <= SUPHELI_SURE_GUN:
                    print(f"{Fore.YELLOW}[!] UYARI: Sertifika yakında bitecek ({kalan_gun} gün).{Style.RESET_ALL}")
                else:
                    print(f"{Fore.GREEN}[✓] Sertifika süresi uygun.{Style.RESET_ALL}")
                
                if guvenilir_ca:
                    print(f"{Fore.GREEN}[✓] Güvenilir CA: {issuer}{Style.RESET_ALL}")
                else:
                    print(f"{Fore.YELLOW}[!] Bilinmeyen CA: {issuer}{Style.RESET_ALL}")
                
                return True
    except ssl.SSLCertVerificationError:
        print(f"{Fore.RED}[X] SSL Sertifika doğrulama hatası! Sahte veya geçersiz sertifika.{Style.RESET_ALL}")
        return False
    except Exception as e:
        print(f"{Fore.RED}[X] Bağlantı hatası: {e}{Style.RESET_ALL}")
        return False

def main():
    logo()
    
    while True:
        print(f"\n{Fore.CYAN}[1]{Fore.WHITE} Domain SSL Analizi")
        print(f"{Fore.CYAN}[Q]{Fore.WHITE} Ana Menüye Dön")
        print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
        
        secim = input(f"{Fore.WHITE}Seçim: {Style.RESET_ALL}").strip().lower()
        
        if secim == '1':
            domain = input(f"{Fore.WHITE}Domain: {Style.RESET_ALL}").strip()
            if domain:
                ssl_kontrol(domain)
        elif secim == 'q':
            break
        else:
            print(f"{Fore.RED}Geçersiz seçim!{Style.RESET_ALL}")
        
        input(f"\n{Fore.YELLOW}Devam için Enter...{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
