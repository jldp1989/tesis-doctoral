import json
import requests
import re
import os
import time

def check_text(text, lang='es'):
    url = "https://api.languagetool.org/v2/check"
    data = {
        'text': text,
        'language': lang,
    }
    response = requests.post(url, data=data)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error calling API: {response.status_code}")
        return {}

def clean_qmd(content):
    # Mask certain parts rather than deleting to maintain offsets? 
    # Actually, for the report, we just need the info.
    # We'll use the same cleaning as the whitelist phase for consistency.
    content = re.sub(r'---.*?---', '', content, flags=re.DOTALL)
    content = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
    content = re.sub(r'(^|\n)>\s?.*', '', content)
    content = re.sub(r'{{<.*?>}}', ' ', content)
    content = re.sub(r'\[?@[\w:-]+\]?', ' ', content)
    content = re.sub(r':::.*?:::', '', content, flags=re.DOTALL)
    return content

def main():
    # Load whitelist
    whitelist_path = 'artifacts/suspected_neologisms.json'
    with open(whitelist_path, 'r') as f:
        whitelist = set(json.load(f))
    
    qmd_files = sorted([f for f in os.listdir('.') if re.match(r'0[1-8].*\.qmd', f)])
    
    report = "# Reporte de Hallazgos Gramaticales y Ortográficos (Filtrado)\n\n"
    report += "Este reporte contiene únicamente los problemas detectados en los capítulos 01-08, ignorando los 559 términos de la whitelist aprobada.\n\n"
    
    for filename in qmd_files:
        print(f"Analizando {filename}...")
        report += f"## {filename}\n\n"
        
        with open(filename, 'r') as f:
            content = f.read()
        
        clean_text = clean_qmd(content)
        chunks = [clean_text[i:i+15000] for i in range(0, len(clean_text), 15000)]
        
        found_any = False
        for chunk in chunks:
            results = check_text(chunk)
            if 'matches' in results:
                for match in results['matches']:
                    offset = match['offset']
                    length = match['length']
                    word = chunk[offset:offset+length]
                    
                    # Skip if word is in whitelist and it's a spelling rule
                    if match['rule']['id'] == 'MORFOLOGIK_RULE_ES' and word in whitelist:
                        continue
                        
                    # Also skip some very common noisy rules if needed
                    # (e.g. WHITESPACE_RULE)
                    
                    found_any = True
                    msg = match['message']
                    repls = ", ".join([r['value'] for r in match['replacements'][:3]])
                    context = match['context']['text']
                    
                    report += f"- **Hallazgo:** {msg}\n"
                    report += f"  - **Palabra/Segmento:** `{word}`\n"
                    report += f"  - **Contexto:** `...{context}...`\n"
                    if repls:
                        report += f"  - **Sugerencias:** {repls}\n"
                    report += "\n"
            time.sleep(1)
            
        if not found_any:
            report += "No se encontraron errores significativos en este capítulo.\n\n"
            
        report += "---\n\n"

    with open('artifacts/grammar_report.md', 'w') as out:
        out.write(report)
    
    print("Reporte generado en artifacts/grammar_report.md")

if __name__ == "__main__":
    main()
