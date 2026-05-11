import urllib.request
import urllib.error
import os

os.makedirs('araclar', exist_ok=True)

tools = [
    '01_usom_kontrol.py',
    '02_phishtank_sorgu.py',
    '03_sahte_edevlet.py',
    '04_ssl_sertifika.py',
    '05_domain_yas_whois.py',
    '06_kara_liste_skor.py',
    '07_favicon_hash.py',
    '08_ekran_goruntusu.py',
    '09_link_ici_analiz.py',
    '10_js_obfuscation.py',
    '11_toplu_tarama.py',
    '12_yerel_karaliste.py',
    '13_usom_ihbar.py',
    '14_telegram_bot.py',
    '15_typosquatting.py',
    '16_ip_geolocation.py',
    '17_emniyet_siber.py',
    '18_fidye_kontrol.py',
    '19_dns_takip.py',
    '20_telegram_komut.py',
    '21_savunma_merkezi.py'
]

base_url = 'https://raw.githubusercontent.com/ThT0AltayHR/AY-YILDIZ-S-BER-VATAN-ARACI-/main/araclar/'

for tool in tools:
    url = base_url + tool
    dest = os.path.join('araclar', tool)
    try:
        print(f'Downloading {tool}...')
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0')
        with urllib.request.urlopen(req) as response:
            with open(dest, 'wb') as f:
                f.write(response.read())
        print(f'✓ Downloaded {tool}')
    except Exception as e:
        print(f'✗ Failed {tool}: {e}')

print('\nDownload complete!')
