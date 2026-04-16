import json
import re

def categorize_words(words):
    categories = {
        "Nombres y Siglas": [],
        "Neologismos y Tecnicismos": [],
        "Terminología en Inglés": [],
        "Dialectal / Coloquial (Rioplatense)": [],
        "Artefactos de Formatos / Sintaxis": [],
        "Otros / Posibles Errores": []
    }
    
    # Known lists
    neologisms = {
        "ciberdiscurso", "extimidad", "affordances", "netnografía", "glocalidad", 
        "multimodalidad", "videoblog", "vlog", "vlogs", "ciberlenguaje", 
        "cibergéneros", "extimacy", "glocality", "cibercomunidad", "ciberdiscursivo"
    }
    english = {
        "frame", "setup", "storytime", "engagement", "backstage", "frontstage", 
        "jump-cuts", "thumbnail", "unboxing", "shippear", "collab", "shoutout", 
        "lifestyle", "gamer", "gameplay", "gameplays", "feedback", "vlogger", "youtuber",
        "youtubers", "tags", "tag", "timestamp", "outro", "intro"
    }
    rioplatense_traits = [r'.*ás$', r'.*és$', r'.*ís$', r'aca$', r'chabón', r'decile', r'tenes']
    
    for word in words:
        word_clean = word.strip().strip('"').strip("'")
        if not word_clean: continue
        
        # Artifacts
        if len(word_clean) <= 2 or any(c in word_clean for c in "$%&()[]{}<>_=*/|"):
            categories["Artefactos de Formatos / Sintaxis"].append(word)
            continue
            
        # Neologisms / Known
        if word_clean.lower() in neologisms:
            categories["Neologismos y Tecnicismos"].append(word)
            continue
            
        # English
        if word_clean.lower() in english:
            categories["Terminología en Inglés"].append(word)
            continue
            
        # Names (Capitalized, not first word usually)
        if word_clean[0].isupper() and word_clean[1:].islower():
            # Check if it's a common name or known youtuber
            categories["Nombres y Siglas"].append(word)
            continue
            
        if word_clean.isupper():
            categories["Nombres y Siglas"].append(word)
            continue

        # Dialectal
        is_dialectal = False
        for trait in rioplatense_traits:
            if re.match(trait, word_clean.lower()):
                is_dialectal = True
                break
        if is_dialectal:
            categories["Dialectal / Coloquial (Rioplatense)"].append(word)
            continue
            
        # Default
        categories["Otros / Posibles Errores"].append(word)
        
    return categories

def main():
    with open('artifacts/suspected_neologisms.json', 'r') as f:
        words = json.load(f)
    
    categorized = categorize_words(words)
    
    with open('artifacts/categorized_whitelist_candidates.json', 'w') as out:
        json.dump(categorized, out, indent=2)
    
    # Print summary
    for cat, items in categorized.items():
        print(f"{cat}: {len(items)}")

if __name__ == "__main__":
    main()
