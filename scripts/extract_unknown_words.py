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
    # Remove frontmatter
    content = re.sub(r'---.*?---', '', content, flags=re.DOTALL)
    # Remove code blocks
    content = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
    # Remove blockquotes (lines starting with >)
    content = re.sub(r'(^|\n)>\s?.*', '', content)
    # Remove Quarto shortcodes
    content = re.sub(r'{{<.*?>}}', ' ', content)
    # Remove URLs
    content = re.sub(r'http[s]?://\S+', ' ', content)
    # Remove citations
    content = re.sub(r'\[?@[\w:-]+\]?', ' ', content)
    # Remove pandoc ::: blocks that look like quotes or notes
    content = re.sub(r':::.*?:::', '', content, flags=re.DOTALL)
    return content

def get_unknown_words(filepath):
    print(f"Checking {filepath}...")
    with open(filepath, 'r') as f:
        content = f.read()
    
    clean_text = clean_qmd(content)
    
    # Split text into chunks of ~15000 characters to be safe with API
    chunks = [clean_text[i:i+15000] for i in range(0, len(clean_text), 15000)]
    
    unknown_words = set()
    for chunk in chunks:
        results = check_text(chunk)
        if 'matches' in results:
            for match in results['matches']:
                if match['rule']['id'] == 'MORFOLOGIK_RULE_ES':
                    offset = match['offset']
                    length = match['length']
                    word = chunk[offset:offset+length]
                    unknown_words.add(word)
        time.sleep(1) # Be nice to the API
    
    return unknown_words

def main():
    # Only process files starting with 01 to 08
    qmd_files = [f for f in os.listdir('.') if re.match(r'0[1-8].*\.qmd', f)]
    all_unknown = set()
    
    for f in qmd_files:
        words = get_unknown_words(f)
        all_unknown.update(words)
    
    # Save results
    with open('artifacts/suspected_neologisms.json', 'w') as out:
        json.dump(sorted(list(all_unknown)), out, indent=2)
    
    print(f"Found {len(all_unknown)} unique suspected words.")

if __name__ == "__main__":
    main()
