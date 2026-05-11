import os, sys, time, requests, re
from colorama import init, Fore, Style
from urllib.parse import urlparse
init(autoreset=True)

VERSIYON = "1.0.0"
ARAC_ADI = "SAHTE E-DEVLET TESPİTİ"

# Resmi gov.tr domain'leri
RESMI_GOV_DOMAINLER = [
    "gib.gov.tr", "sgk.gov.tr", "emekli.gov.tr", "ptt.gov.tr",
    "meb.gov.tr", "saglik.gov.tr", "corona.gov.tr", "covid19.gov.tr",
    "e-devlet.gov.tr", "turkiye.gov.tr", "tckimlik.gov.tr", "nvi.gov.tr"
]

def ekran_temizle():
    os.system('clear' if os.name == 'posix' else 'cls')

def logo():
    print(f"{Fore.CYAN}{'='*80}")
    print(f"{Fore.WHITE} {ARAC_ADI} v{VERSIYON}")
    print(f"{Fore.CYAN} AY-YILDIZ SİBER KALKAN | .GOV.TR TAKLİT TESPİT")
    print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}")

def domain_analizi(url):
    """Domain'i analiz eder ve sahte olup olmadığını kontrol eder."""
    try:
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        
        # .gov.tr kontrolü
        if not domain.endswith('.gov.tr'):
            return {"url": url, "sonuc": "ŞÜPHELİ", "neden": "gov.tr uzantısı yok"}
        
        # Resmi domain kontrolü
        if domain in RESMI_GOV_DOMAINLER:
            return {"url": url, "sonuc": "GÜVENLİ", "neden": "Resmi gov.tr domaini"}
        
        # Typo kontrolü
        for resmi in RESMI_GOV_DOMAINLER:
            if resmi in domain or domain in resmi:
                return {"url": url, "sonuc": "ŞÜPHELİ", "neden": f"{resmi} benzeri"}
        
        return {"url": url, "sonuc": "BİLİNMEYEN", "neden": "Gov.tr ama resmi değil"}
    except:
        return {"url": url, "sonuc": "HATA", "neden": "Analiz hatası"}

def html_kontrol(url):
    """HTML içeriğini kontrol eder."""
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(url, timeout=10, headers=headers)
        
        # SSL kontrolü
        if not url.startswith('https://'):
            return {"url": url, "sonuc": "ŞÜPHELİ", "neden": "HTTPS yok"}
        
        # İçerik kontrolü
        html = r.text.lower()
        if "e-devlet" in html and "giriş" in html:
            if domain_analizi(url)["sonuc"] != "GÜVENLİ":
                return {"url": url, "sonuc": "TEHLİKE", "neden": "Sahte e-devlet sayfası"}
        
        return {"url": url, "sonuc": "ANALİZ_EDİLİYOR", "neden": "HTML kontrolü tamamlandı"}
    except:
        return {"url": url, "sonuc": "HATA", "neden": "Bağlantı hatası"}

def main():
    logo()
    
    while True:
        print(f"\n{Fore.CYAN}[1]{Fore.WHITE} URL Analizi")
        print(f"{Fore.CYAN}[2]{Fore.WHITE} Toplu URL Analizi")
        print(f"{Fore.CYAN}[Q]{Fore.WHITE} Ana Menüye Dön")
        print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
        
        secim = input(f"{Fore.WHITE}Seçim: {Style.RESET_ALL}").strip().lower()
        
        if secim == '1':
            url = input(f"{Fore.WHITE}URL: {Style.RESET_ALL}").strip()
            if url:
                if not url.startswith('http'):
                    url = 'https://' + url
                
                print(f"\n{Fore.YELLOW}[+] Analiz ediliyor...{Style.RESET_ALL}")
                sonuc = domain_analizi(url)
                
                print(f"\n{Fore.CYAN}{'='*80}")
                print(f"{Fore.WHITE} URL: {Fore.CYAN}{sonuc['url']}{Style.RESET_ALL}")
                print(f"{Fore.WHITE} Sonuç: {Fore.RED if sonuc['sonuc'] == 'TEHLİKE' or sonuc['sonuc'] == 'ŞÜPHELİ' else Fore.GREEN}{sonuc['sonuc']}{Style.RESET_ALL}")
                print(f"{Fore.WHITE} Neden: {Fore.YELLOW}{sonuc['neden']}{Style.RESET_ALL}")
                print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
        elif secim == '2':
            url = input(f"{Fore.WHITE}URL'leri (virgülle ayrılmış): {Style.RESET_ALL}").strip()
            if url:
                urller = [u.strip() for u in url.split(',')]
                print(f"\n{Fore.YELLOW}[+] {len(urller)} URL analiz ediliyor...{Style.RESET_ALL}")
                for u in urller:
                    if not u.startswith('http'):
                        u = 'https://' + u
                    sonuc = domain_analizi(u)
                    renk = Fore.RED if sonuc['sonuc'] == 'TEHLİKE' or sonuc['sonuc'] == 'ŞÜPHELİ' else Fore.GREEN
                    print(f"{renk}[{sonuc['sonuc']}] {u} - {sonuc['neden']}{Style.RESET_ALL}")
        elif secim == 'q':
            break
        else:
            print(f"{Fore.RED}Geçersiz seçim!{Style.RESET_ALL}")
        
        input(f"\n{Fore.YELLOW}Devam için Enter...{Style.RESET_ALL}")

if __name__ == "__main__":
    main()

