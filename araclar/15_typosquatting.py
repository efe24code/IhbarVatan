import os, sys, time
from colorama import init, Fore, Style
import difflib
import string
init(autoreset=True)

VERSIYON = "1.0.0"
ARAC_ADI = "TYPOSQUATTING TESPİTİ"

# Yaygın Türk banka ve kurum domain'leri
HEDEF_DOMAINLER = [
    "ziraatbank.com.tr", "halkbank.com.tr", "vakifbank.com.tr",
    "isbank.com.tr", "akbank.com.tr", "garanti.com.tr", "yapikredi.com.tr",
    "finansbank.com.tr", "gib.gov.tr", "sgk.gov.tr", "emekli.gov.tr",
    "ptt.gov.tr", "meb.gov.tr", "saglik.gov.tr", "e-devlet.gov.tr",
    "turkiye.gov.tr", "tckimlik.gov.tr", "nvi.gov.tr"
]

def ekran_temizle():
    os.system('clear' if os.name == 'posix' else 'cls')

def logo():
    print(f"{Fore.CYAN}{'='*80}")
    print(f"{Fore.WHITE} {ARAC_ADI} v{VERSIYON}")
    print(f"{Fore.CYAN} AY-YILDIZ SİBER KALKAN | YAZIM HATASI TESPİTİ")
    print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}")

def karakter_degisimi(domain):
    """Domain'de karakter değişimleri oluştur."""
    sonuclar = []
    domain_adi = domain.split('.')[0]
    
    # Karakter değişimi (q -> g, 0 -> o, 1 -> l, 1 -> i, vb.)
    degisimler = {
        'q': 'g', 'g': 'q', '0': 'o', 'o': '0', '1': 'l', 'l': '1',
        '1': 'i', 'i': '1', '5': 's', 's': '5', '3': 'e', 'e': '3'
    }
    
    for char, replacement in degisimler.items():
        if char in domain_adi:
            yeni_domain = domain_adi.replace(char, replacement)
            if yeni_domain != domain_adi:
                sonuclar.append(yeni_domain + '.' + '.'.join(domain.split('.')[1:]))
    
    return sonuclar

def karakter_ekleme(domain):
    """Domain'e karakter ekle."""
    sonuclar = []
    domain_adi = domain.split('.')[0]
    
    # Her pozisyona karakter ekle
    for i in range(len(domain_adi)):
        for char in string.ascii_lowercase + string.digits:
            yeni_domain = domain_adi[:i] + char + domain_adi[i:]
            if yeni_domain != domain_adi:
                sonuclar.append(yeni_domain + '.' + '.'.join(domain.split('.')[1:]))
    
    return sonuclar[:20]  # Sınırlı sayıda

def karakter_silme(domain):
    """Domain'den karakter sil."""
    sonuclar = []
    domain_adi = domain.split('.')[0]
    
    # Her pozisyondan karakter sil
    for i in range(len(domain_adi)):
        yeni_domain = domain_adi[:i] + domain_adi[i+1:]
        if yeni_domain != domain_adi and len(yeni_domain) > 2:
            sonuclar.append(yeni_domain + '.' + '.'.join(domain.split('.')[1:]))
    
    return sonuclar[:20]  # Sınırlı sayıda

def benzerlik_skoru(domain1, domain2):
    """İki domain arasındaki benzerlik skorunu hesapla."""
    return difflib.SequenceMatcher(None, domain1.lower(), domain2.lower()).ratio()

def typosquatting_tespit(domain):
    """Bir domain için olası typosquatting varyasyonlarını oluştur."""
    sonuclar = []
    
    # Karakter değişimi
    sonuclar.extend(karakter_degisimi(domain))
    
    # Karakter ekleme
    sonuclar.extend(karakter_ekleme(domain))
    
    # Karakter silme
    sonuclar.extend(karakter_silme(domain))
    
    # Benzersiz yap
    sonuclar = list(set(sonuclar))
    
    return sonuclar

def main():
    logo()
    
    while True:
        print(f"\n{Fore.CYAN}[1]{Fore.WHITE} Domain Analizi")
        print(f"{Fore.CYAN}[2]{Fore.WHITE} Hedef Domain Listesi")
        print(f"{Fore.CYAN}[3]{Fore.WHITE} Otomatik Typosquatting Taraması")
        print(f"{Fore.CYAN}[Q]{Fore.WHITE} Ana Menüye Dön")
        print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
        
        secim = input(f"{Fore.WHITE}Seçim: {Style.RESET_ALL}").strip().lower()
        
        if secim == '1':
            domain = input(f"{Fore.WHITE}Domain: {Style.RESET_ALL}").strip()
            if domain:
                print(f"\n{Fore.YELLOW}[+] Typosquatting varyasyonları oluşturuluyor...{Style.RESET_ALL}")
                varyasyonlar = typosquatting_tespit(domain)
                
                print(f"\n{Fore.CYAN}[i] {len(varyasyonlar)} varyasyon bulundu:{Style.RESET_ALL}")
                for v in varyasyonlar[:20]:
                    skor = benzerlik_skoru(domain, v)
                    renk = Fore.RED if skor > 0.8 else Fore.YELLOW
                    print(f"{renk}  - {v} (Skor: {skor:.2f}){Style.RESET_ALL}")
        elif secim == '2':
            print(f"\n{Fore.CYAN}[i] Hedef Domain Listesi:{Style.RESET_ALL}")
            for h in HEDEF_DOMAINLER:
                print(f"  {h}")
        elif secim == '3':
            print(f"\n{Fore.YELLOW}[+] Otomatik tarama başlatılıyor...{Style.RESET_ALL}")
            for hedef in HEDEF_DOMAINLER[:5]:  # İlk 5 hedef
                print(f"\n{Fore.CYAN}[i] {hedef} analiz ediliyor...{Style.RESET_ALL}")
                varyasyonlar = typosquatting_tespit(hedef)
                for v in varyasyonlar[:10]:
                    skor = benzerlik_skoru(hedef, v)
                    if skor > 0.7:
                        print(f"{Fore.RED}  [YÜKSEK RİSK] {v} (Skor: {skor:.2f}){Style.RESET_ALL}")
        elif secim == 'q':
            break
        else:
            print(f"{Fore.RED}Geçersiz seçim!{Style.RESET_ALL}")
        
        input(f"\n{Fore.YELLOW}Devam için Enter...{Style.RESET_ALL}")

if __name__ == "__main__":
    main()

