import os, sys, time
from colorama import init, Fore, Style
init(autoreset=True)

VERSIYON = "1.0.0"
ARAC_ADI = "YEREL KARA LİSTE YÖNETİMİ"
YEREL_LISTE = "data/yerel_karaliste.txt"

def ekran_temizle():
    os.system('clear' if os.name == 'posix' else 'cls')

def logo():
    print(f"{Fore.CYAN}{'='*80}")
    print(f"{Fore.WHITE} {ARAC_ADI} v{VERSIYON}")
    print(f"{Fore.CYAN} AY-YILDIZ SİBER KALKAN | ÖZEL ENGELLEME LİSTESİ")
    print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}")

def listeyi_oku():
    """Yerel kara listeyi okur."""
    os.makedirs("data", exist_ok=True)
    if os.path.exists(YEREL_LISTE):
        with open(YEREL_LISTE, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    return []

def listeye_ekle(url):
    """URL'yi kara listeye ekler."""
    liste = listeyi_oku()
    if url not in liste:
        liste.append(url)
        with open(YEREL_LISTE, "w", encoding="utf-8") as f:
            f.write("\n".join(liste))
        return True
    return False

def listeden_sil(url):
    """URL'yi kara listeden siler."""
    liste = listeyi_oku()
    if url in liste:
        liste.remove(url)
        with open(YEREL_LISTE, "w", encoding="utf-8") as f:
            f.write("\n".join(liste))
        return True
    return False

def listeyi_temizle():
    """Kara listeyi temizler."""
    if os.path.exists(YEREL_LISTE):
        os.remove(YEREL_LISTE)
        return True
    return False

def url_kontrol(url):
    """URL'nin kara listede olup olmadığını kontrol eder."""
    liste = listeyi_oku()
    return url in liste

def main():
    logo()
    
    while True:
        liste = listeyi_oku()
        print(f"\n{Fore.CYAN}[1]{Fore.WHITE} URL Ekle")
        print(f"{Fore.CYAN}[2]{Fore.WHITE} URL Sil")
        print(f"{Fore.CYAN}[3]{Fore.WHITE} Listeyi Göster ({len(liste)} URL)")
        print(f"{Fore.CYAN}[4]{Fore.WHITE} URL Kontrol Et")
        print(f"{Fore.CYAN}[5]{Fore.WHITE} Listeyi Temizle")
        print(f"{Fore.CYAN}[Q]{Fore.WHITE} Ana Menüye Dön")
        print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
        
        secim = input(f"{Fore.WHITE}Seçim: {Style.RESET_ALL}").strip().lower()
        
        if secim == '1':
            url = input(f"{Fore.WHITE}URL: {Style.RESET_ALL}").strip()
            if url:
                if listeye_ekle(url):
                    print(f"{Fore.GREEN}[✓] URL eklendi.{Style.RESET_ALL}")
                else:
                    print(f"{Fore.YELLOW}[!] URL zaten listede.{Style.RESET_ALL}")
        elif secim == '2':
            url = input(f"{Fore.WHITE}Silinecek URL: {Style.RESET_ALL}").strip()
            if url:
                if listeden_sil(url):
                    print(f"{Fore.GREEN}[✓] URL silindi.{Style.RESET_ALL}")
                else:
                    print(f"{Fore.YELLOW}[!] URL listede bulunamadı.{Style.RESET_ALL}")
        elif secim == '3':
            if liste:
                print(f"\n{Fore.CYAN}[i] Yerel Kara Liste ({len(liste)} URL):{Style.RESET_ALL}")
                for url in liste:
                    print(f"  {url}")
            else:
                print(f"{Fore.YELLOW}[!] Liste boş.{Style.RESET_ALL}")
        elif secim == '4':
            url = input(f"{Fore.WHITE}Kontrol edilecek URL: {Style.RESET_ALL}").strip()
            if url:
                if url_kontrol(url):
                    print(f"{Fore.RED}[X] URL kara listede.{Style.RESET_ALL}")
                else:
                    print(f"{Fore.GREEN}[✓] URL kara listede değil.{Style.RESET_ALL}")
        elif secim == '5':
            onay = input(f"{Fore.YELLOW}[!] Emin misiniz? (E/H): {Style.RESET_ALL}").strip().lower()
            if onay == 'e':
                if listeyi_temizle():
                    print(f"{Fore.GREEN}[✓] Liste temizlendi.{Style.RESET_ALL}")
            else:
                print(f"{Fore.YELLOW}[!] İptal edildi.{Style.RESET_ALL}")
        elif secim == 'q':
            break
        else:
            print(f"{Fore.RED}Geçersiz seçim!{Style.RESET_ALL}")
        
        input(f"\n{Fore.YELLOW}Devam için Enter...{Style.RESET_ALL}")

if __name__ == "__main__":
    main()

