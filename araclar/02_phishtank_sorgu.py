import os, sys, time, requests
from colorama import init, Fore, Style
init(autoreset=True)

VERSIYON = "5.2.2"
API_URL = "https://checkurl.phishtank.com/checkurl/"

def ekran_temizle():
    os.system('clear' if os.name == 'posix' else 'cls')

def logo():
    ekran_temizle()
    print(f"{Fore.CYAN}{'='*80}")
    print(f"{Fore.WHITE} PHISHTANK SORGU MODÜLÜ v{VERSIYON}")
    print(f"{Fore.CYAN} AY-YILDIZ SİBER KALKAN | 8M+ Phishing Sitesi Veritabanı")
    print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}")

def phishtank_sorgula(url):
    print(f"\n{Fore.YELLOW}[+] PhishTank veritabanında sorgulanıyor: {url}{Style.RESET_ALL}")
    
    try:
        payload = {
            'url': url,
            'format': 'json',
            'app_key': ''  # PhishTank API key gerekebilir
        }
        
        headers = {
            'User-Agent': 'AY-YILDIZ-SIBER-KALKAN/5.2.2'
        }
        
        r = requests.post(API_URL, data=payload, headers=headers, timeout=10)
        
        if r.status_code == 200:
            data = r.json()
            if data.get('in_database'):
                print(f"\n{Fore.RED}[!] TEHLİKE: Phishing sitesi tespit edildi!{Style.RESET_ALL}")
                print(f"{Fore.RED}[X] URL: {data.get('url', url)}{Style.RESET_ALL}")
                print(f"{Fore.RED}[X] PhishTank ID: {data.get('phish_id', 'N/A')}{Style.RESET_ALL}")
                return True
            else:
                print(f"\n{Fore.GREEN}[✓] Güvenli: Phishing veritabanında bulunamadı.{Style.RESET_ALL}")
                return False
        else:
            print(f"{Fore.YELLOW}[!] API hatası: {r.status_code}{Style.RESET_ALL}")
            return None
    except Exception as e:
        print(f"{Fore.RED}[X] Sorgu hatası: {e}{Style.RESET_ALL}")
        return None

def main():
    logo()
    
    while True:
        print(f"\n{Fore.CYAN}[1]{Fore.WHITE} URL Sorgula")
        print(f"{Fore.CYAN}[Q]{Fore.WHITE} Ana Menüye Dön")
        print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
        
        secim = input(f"{Fore.WHITE}Seçim: {Style.RESET_ALL}").strip().lower()
        
        if secim == '1':
            url = input(f"{Fore.WHITE}URL: {Style.RESET_ALL}").strip()
            if url:
                phishtank_sorgula(url)
        elif secim == 'q':
            break
        else:
            print(f"{Fore.RED}Geçersiz seçim!{Style.RESET_ALL}")
        
        input(f"\n{Fore.YELLOW}Devam için Enter...{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
