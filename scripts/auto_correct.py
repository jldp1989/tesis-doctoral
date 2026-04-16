import re
import os

def apply_safe_corrections(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    
    original = content
    
    # 1. Typos Manuales Confirmados
    content = content.replace("re-codificación", "recodificación")
    content = content.replace("espontaneo", "espontáneo")
    content = content.replace("onceptuales", "conceptuales") # Por si acaso
    
    # 2. Puntuación: Comas antes de 'pero' y 'sino'
    # Solo si están precedidos por una palabra y NO por una coma o puntuación.
    # Evitamos casos como "Pero..." al inicio de párrafo.
    content = re.sub(r'(\w)\s+sino\b', r'\1, sino', content)
    content = re.sub(r'(\w)\s+pero\b', r'\1, pero', content)
    
    # 3. Limpieza de dobles puntuaciones (artefactos de edición previa)
    content = re.sub(r'\s*;\s*;\s*', '; ', content)
    content = re.sub(r'\s*,\s*,\s*', ', ', content)
    
    if content != original:
        with open(filepath, 'w') as f:
            f.write(content)
        return True
    return False

def main():
    files = [f for f in os.listdir('.') if re.match(r'0[1-8].*\.qmd', f)]
    for f in files:
        changed = apply_safe_corrections(f)
        if changed:
            print(f"Correcciones aplicadas en {f}")

if __name__ == "__main__":
    main()
