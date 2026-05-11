import os, sys, time
from colorama import init, Fore, Style
init(autoreset=True)

VERSIYON = "1.0.0"
ARAC_ADI = "USOM İHBAR HAZIRLAMA"
USOM_IHBAR_URL = "https://www.usom.gov.tr/ihbar"
USOM_LISTE = "data/usom_cache.txt"
RAPOR_DOSYASI = "raporlar/usom_ihbar_raporu.txt"

def ekran_temizle():
    os.system('clear' if os.name == 'posix' else 'cls')

def logo():
    print(f"{Fore.CYAN}{'='*80}")
    print(f"{Fore.WHITE} {ARAC_ADI} v{VERSIYON}")
    print(f"{Fore.CYAN} AY-YILDIZ SİBER KALKAN | OTOMATİK İHBAR HAZIRLAMA")
    print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}")

def usom_listesini_oku():
    """USOM kara listesini okur."""
    if os.path.exists(USOM_LISTE):
        with open(USOM_LISTE, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    return []

def ihbar_formu_hazirla(url, aciklama):
    """USOM ihbar formunu hazırlar."""
    form = f"""
USOM İHBAR FORMU
{'='*80}

TARİH: {time.strftime('%d.%m.%Y %H:%M:%S')}
İHBAR EDİLEN URL: {url}
AÇIKLAMA: {aciklama}

EK BİLGİLER:
- URL zararlı içerik barındırıyor olabilir
- Phishing saldırısı olabilir
- Kötü amaçlı yazılım dağıtımı olabilir
- Sosyal mühendislik saldırısı olabilir

İHBAR EDEN: AY-YILDIZ SİBER KALKAN
OTOMATİK TESPİT: Evet

{'='*80}
USOM RESMİ İHBAR SAYFASI: {USOM_IHBAR_URL}
{'='*80}
"""
    return form

def toplu_ihbar_hazirla(url_listesi):
    """Toplu ihbar formları hazırlar."""
    os.makedirs("raporlar", exist_ok=True)
    
    with open(RAPOR_DOSYASI, "w", encoding="utf-8") as f:
        f.write(f"USOM TOPLU İHBAR RAPORU\n")
        f.write(f"TARİH: {time.strftime('%d.%m.%Y %H:%M:%S')}\n")
        f.write(f"TOPLAM URL: {len(url_listesi)}\n")
        f.write(f"{'='*80}\n\n")
        
        for i, url in enumerate(url_listesi, 1):
            f.write(f"İHBAR #{i}\n")
            f.write(f"URL: {url}\n")
            f.write(f"AÇIKLAMA: Otomatik tespit edilen şüpheli URL\n")
            f.write(f"{'-'*80}\n\n")
    
    return RAPOR_DOSYASI

def main():
    logo()
    
    while True:
        print(f"\n{Fore.CYAN}[1]{Fore.WHITE} Tek URL İhbarı Hazırla")
        print(f"{Fore.CYAN}[2]{Fore.WHITE} USOM Listesinden İhbar Hazırla")
        print(f"{Fore.CYAN}[3]{Fore.WHITE} Manuel URL Girişi")
        print(f"{Fore.CYAN}[4]{Fore.WHITE} İhbar Raporlarını Görüntüle")
        print(f"{Fore.CYAN}[Q]{Fore.WHITE} Ana Menüye Dön")
        print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
        
        secim = input(f"{Fore.WHITE}Seçim: {Style.RESET_ALL}").strip().lower()
        
        if secim == '1':
            url = input(f"{Fore.WHITE}İhbar edilecek URL: {Style.RESET_ALL}").strip()
            if url:
                aciklama = input(f"{Fore.WHITE}Açıklama: {Style.RESET_ALL}").strip()
                form = ihbar_formu_hazirla(url, aciklama or "Otomatik tespit")
                print(f"\n{Fore.CYAN}[i] İhbar Formu:{Style.RESET_ALL}")
                print(form)
                print(f"{Fore.YELLOW}[i] Bu formu kopyalayıp {USOM_IHBAR_URL} adresine gönderin.{Style.RESET_ALL}")
        elif secim == '2':
            usom_urller = usom_listesini_oku()
            if usom_urller:
                print(f"\n{Fore.YELLOW}[+] USOM listesinden {len(usom_urller)} URL için ihbar hazırlanıyor...{Style.RESET_ALL}")
                rapor_dosyasi = toplu_ihbar_hazirla(usom_urller[:50])  # İlk 50
                print(f"{Fore.GREEN}[✓] Rapor kaydedildi: {rapor_dosyasi}{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}[i] Bu raporu USOM'a iletebilirsiniz.{Style.RESET_ALL}")
            else:
                print(f"{Fore.YELLOW}[!] USOM listesi bulunamadı.{Style.RESET_ALL}")
        elif secim == '3':
            url = input(f"{Fore.WHITE}URL'leri (virgülle ayrılmış): {Style.RESET_ALL}").strip()
            if url:
                urller = [u.strip() for u in url.split(',')]
                rapor_dosyasi = toplu_ihbar_hazirla(urller)
                print(f"{Fore.GREEN}[✓] Rapor kaydedildi: {rapor_dosyasi}{Style.RESET_ALL}")
        elif secim == '4':
            if os.path.exists(RAPOR_DOSYASI):
                with open(RAPOR_DOSYASI, "r", encoding="utf-8") as f:
                    print(f"\n{Fore.CYAN}{f.read()}{Style.RESET_ALL}")
            else:
                print(f"{Fore.YELLOW}[!] Henüz ihbar raporu yok.{Style.RESET_ALL}")
        elif secim == 'q':
            break
        else:
            print(f"{Fore.RED}Geçersiz seçim!{Style.RESET_ALL}")
        
        input(f"\n{Fore.YELLOW}Devam için Enter...{Style.RESET_ALL}")

if __name__ == "__main__":
    main()

