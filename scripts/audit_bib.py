import re
import os

def get_citations(directory):
    citations = set()
    qmd_files = [f for f in os.listdir(directory) if re.match(r'0[1-8].*\.qmd', f)]
    for filename in qmd_files:
        with open(os.path.join(directory, filename), 'r') as f:
            content = f.read()
            # Match @key or [@key]
            matches = re.findall(r'@([\w:-]+)', content)
            citations.update(matches)
    return citations

def get_bib_keys(bib_path):
    keys = set()
    with open(bib_path, 'r') as f:
        for line in f:
            match = re.search(r'@\w+\{([\w:-]+),', line)
            if match:
                keys.add(match.group(1))
    return keys

def main():
    root = "."
    cite_keys = get_citations(root)
    bib_keys = get_bib_keys("bibl/tesis.bib")
    
    missing = cite_keys - bib_keys
    print(f"Total citations found: {len(cite_keys)}")
    print(f"Total keys in BIB: {len(bib_keys)}")
    print(f"Missing keys: {sorted(list(missing))}")

if __name__ == "__main__":
    main()
