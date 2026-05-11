import os, sys, time, threading
from colorama import init, Fore, Style
import requests
init(autoreset=True)

VERSIYON = "1.0.0"
ARAC_ADI = "TOPLU TARAMA MODÜLÜ"

def ekran_temizle():
    os.system('clear' if os.name == 'posix' else 'cls')

def logo():
    print(f"{Fore.CYAN}{'='*80}")
    print(f"{Fore.WHITE} {ARAC_ADI} v{VERSIYON}")
    print(f"{Fore.CYAN} AY-YILDIZ SİBER KALKAN | 100+ LİNK BULK SCAN")
    print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}")

def url_tekil_tara(url):
    """Tek URL'yi hızlı tarama."""
    try:
        # Basit kontroller
        if not url.startswith('http'):
            url = 'https://' + url
        
        # Uzunluk kontrolü
        if len(url) > 100:
            return {"url": url, "sonuc": "ŞÜPHELİ", "neden": "Çok uzun URL"}
        
        # HTTPS kontrolü
        if not url.startswith('https://'):
            return {"url": url, "sonuc": "ŞÜPHELİ", "neden": "HTTPS yok"}
        
        # Domain karakter kontrolü
        domain = url.split('/')[2]
        if len(domain) > 50:
            return {"url": url, "sonuc": "ŞÜPHELİ", "neden": "Uzun domain"}
        
        # Bağlantı denemesi (timeout kısa)
        try:
            requests.head(url, timeout=3)
            return {"url": url, "sonuc": "GÜVENLİ", "neden": "Erişilebilir"}
        except:
            return {"url": url, "sonuc": "ŞÜPHELİ", "neden": "Erişilemez"}
            
    except:
        return {"url": url, "sonuc": "HATA", "neden": "Tarama hatası"}

def coklu_tarama(url_listesi, max_thread=30):
    """Multi-thread ile hızlı toplu tarama."""
    print(f"\n{Fore.YELLOW}[+] {len(url_listesi)} URL taranıyor...{Style.RESET_ALL}")
    print(f"{Fore.CYAN}[i] Thread sayısı: {max_thread}{Style.RESET_ALL}")
    
    sonuclar = []
    tamamlanan = 0
    kilit = threading.Lock()
    
    def tarama_thread(urller):
        nonlocal tamamlanan
        thread_sonuclar = []
        for url in urller:
            sonuc = url_tekil_tara(url)
            thread_sonuclar.append(sonuc)
            with kilit:
                tamamlanan += 1
                if tamamlanan % 20 == 0:
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
    tehlikeler = [s for s in sonuclar if s["sonuc"] == "ŞÜPHELİ" or s["sonuc"] == "TEHLİKE"]
    guvenliler = [s for s in sonuclar if s["sonuc"] == "GÜVENLİ"]
    hatalar = [s for s in sonuclar if s["sonuc"] == "HATA"]
    
    print(f"\n{Fore.CYAN}{'='*80}")
    print(f"{Fore.WHITE} TARAMA RAPORU")
    print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
    print(f"{Fore.RED}ŞÜPHELİ/TEHLİKE: {len(tehlikeler)}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}GÜVENLİ: {len(guvenliler)}{Style.RESET_ALL}")
    print(f"{Fore.WHITE}HATA: {len(hatalar)}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
    
    if tehlikeler:
        print(f"\n{Fore.RED}[!] ŞÜPHELİ URL'LER:{Style.RESET_ALL}")
        for t in tehlikeler[:20]:
            print(f"{Fore.RED}  - {t['url']} ({t['neden']}){Style.RESET_ALL}")

def dosyadan_oku(dosya_yolu):
    """Dosyadan URL'leri okur."""
    try:
        with open(dosya_yolu, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except:
        return []

def main():
    logo()
    
    while True:
        print(f"\n{Fore.CYAN}[1]{Fore.WHITE} Manuel URL Girişi")
        print(f"{Fore.CYAN}[2]{Fore.WHITE} Dosyadan Oku")
        print(f"{Fore.CYAN}[3]{Fore.WHITE} USOM Listesi ile Tarama")
        print(f"{Fore.CYAN}[Q]{Fore.WHITE} Ana Menüye Dön")
        print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
        
        secim = input(f"{Fore.WHITE}Seçim: {Style.RESET_ALL}").strip().lower()
        
        if secim == '1':
            url = input(f"{Fore.WHITE}URL'leri (virgülle ayrılmış): {Style.RESET_ALL}").strip()
            if url:
                urller = [u.strip() for u in url.split(',')]
                sonuclar = coklu_tarama(urller)
                raporla(sonuclar)
        elif secim == '2':
            dosya = input(f"{Fore.WHITE}Dosya yolu: {Style.RESET_ALL}").strip()
            if dosya and os.path.exists(dosya):
                urller = dosyadan_oku(dosya)
                if urller:
                    sonuclar = coklu_tarama(urller)
                    raporla(sonuclar)
                else:
                    print(f"{Fore.YELLOW}[!] Dosya boş veya okunamadı.{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}[!] Dosya bulunamadı.{Style.RESET_ALL}")
        elif secim == '3':
            usom_dosya = "data/usom_cache.txt"
            if os.path.exists(usom_dosya):
                urller = dosyadan_oku(usom_dosya)
                if urller:
                    print(f"{Fore.CYAN}[i] USOM listesinden {len(urller)} URL taranacak.{Style.RESET_ALL}")
                    input(f"{Fore.YELLOW}Devam için Enter...{Style.RESET_ALL}")
                    sonuclar = coklu_tarama(urller[:100])  # İlk 100
                    raporla(sonuclar)
                else:
                    print(f"{Fore.YELLOW}[!] USOM listesi boş.{Style.RESET_ALL}")
            else:
                print(f"{Fore.YELLOW}[!] USOM listesi bulunamadı. Önce USOM Kontrol ile indirin.{Style.RESET_ALL}")
        elif secim == 'q':
            break
        else:
            print(f"{Fore.RED}Geçersiz seçim!{Style.RESET_ALL}")
        
        input(f"\n{Fore.YELLOW}Devam için Enter...{Style.RESET_ALL}")

if __name__ == "__main__":
    main()

