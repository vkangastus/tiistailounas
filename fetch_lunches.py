import json
import re
import requests
from bs4 import BeautifulSoup

ravintolat = [
    {
        "id": "treffi",
        "nimi": "Treffi Pub & Bistro",
        "url": "https://treffipub.com/menu/lounas/"
    },
    {
        "id": "herkku",
        "nimi": "Ravintola Herkku",
        "url": "https://ravintolaherkku.fi"
    },
    {
        "id": "factory",
        "nimi": "Ravintola Factory Roihupelto",
        "url": "https://ravintolafactory.com/lounasravintolat/ravintolat/helsinki-roihupelto/"
    }
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def parsi_tiistai(text):
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    tiistai_rivit = []
    tallenna = False

    for line in lines:
        if re.search(r'tiistai|ti\s*\d+', line, re.IGNORECASE):
            tallenna = True
            tiistai_rivit.append(line)
            continue
        if tallenna and re.search(r'keskiviikko|ke\s*\d+', line, re.IGNORECASE):
            break
        if tallenna and len(line) > 3:
            tiistai_rivit.append(line)

    return tiistai_rivit if tiistai_rivit else ["Lounaslistaa ei saatu suodatettua automaattisesti."]

tulokset = []

for r in ravintolat:
    try:
        response = requests.get(r['url'], headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Poistetaan roskat
        for s in soup(['script', 'style', 'nav', 'footer', 'header']):
            s.decompose()

        text = soup.get_text(separator='\n')
        lounaat = parsi_tiistai(text)

        tulokset.append({
            "nimi": r['nimi'],
            "url": r['url'],
            "lounaat": lounaat,
            "status": "ok"
        })
    except Exception as e:
        tulokset.append({
            "nimi": r['nimi'],
            "url": r['url'],
            "lounaat": [f"Virhe haettaessa: {str(e)}"],
            "status": "error"
        })

with open('lounaat.json', 'w', encoding='utf-8') as f:
    json.dump(tulokset, f, ensure_ascii=False, indent=2)

print("lounaat.json luotu onnistuneesti.")
