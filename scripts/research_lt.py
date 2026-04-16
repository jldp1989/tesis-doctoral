import json
import requests
import sys
import re

def check_text(text, lang='es'):
    url = "https://api.languagetool.org/v2/check"
    data = {
        'text': text,
        'language': lang,
    }
    response = requests.post(url, data=data)
    return response.json()

def main(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Strip frontmatter and code blocks to avoid noise
    # (Simple regex for research purposes)
    clean_text = re.sub(r'---.*?---', '', content, flags=re.DOTALL)
    clean_text = re.sub(r'```.*?```', '', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'{{<.*?>}}', '', clean_text)
    
    results = check_text(clean_text)
    
    if 'matches' in results:
        for match in results['matches']:
            msg = match['message']
            context = match['context']['text']
            offset = match['context']['offset']
            length = match['context']['length']
            word = context[offset:offset+length]
            replacements = ", ".join([r['value'] for r in match['replacements'][:3]])
            
            print(f"Word: {word}")
            print(f"Context: {context}")
            print(f"Message: {msg}")
            print(f"Suggestions: {replacements}")
            print("-" * 40)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
