"""
Script: topic_modeling.py
Propósito: Modelado de tópicos (LDA) sobre el corpus de 80 transcripciones
           de vlogs argentinos (2012–2016). Genera la tabla de tópicos latentes
           utilizada como andamio heurístico para la construcción del codebook temático.

Uso: python3 topic_modeling.py
Requiere: scikit-learn, numpy
"""

import csv
import re
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

# ─── Configuración ────────────────────────────────────────────────────────────

DATA_PATH  = "../transcripciones.csv" # Ruta relativa corregida para materiales/
N_TOPICS   = 10
N_TOP_WORDS = 12
RANDOM_STATE = 42

# Stopwords adaptadas al español coloquial rioplatense
STOPWORDS = [
    'que','de','en','a','la','el','los','las','un','una','y','es','se','no','si','lo',
    'le','me','te','su','ser','sus','más','por','con','esto','esta','este','para','pero',
    'como','porque','qué','cuando','al','del','hay','también','ya','muy','así','hasta',
    'ahora','después','antes','bueno','bien','acá','eso','esa','ese','todo','todos','toda',
    'todas','tengo','tiene','voy','vamos','ver','hacer','hago','hice','soy','era','fue',
    'han','he','había','estoy','están','estaba','pues','puede','sí','ni','son','está',
    'mi','tu','vos','yo','él','ella','nosotros','ellos','ustedes','les','nos','algo',
    'nada','poco','mucho','tipo','igual','nunca','siempre','solo','sólo','va','ir',
    'otro','otra','día','vez','ahí','acá','allá','parte','dije','digo','quiero',
    'quería','tenés','tenía','entonces','creo','pasa','pasó','fueron','siendo',
    'vas','va','van','vio','puede','podés','podía','tener','orador','muchas','gracias',
    'hola','chicos','gente','video','videos','canal','youtube','comentarios','like',
    'cosa','cosas','dale','sea','sé','eh','ah','ay','osea','ahi','asi','aca','mas',
    'cómo','chau','estás','estamos','gusta','verdad','serio','boludo','puta','carajo',
    'culo','loco','hijo','pelotudo','mirá','sos','mis','mí','alguien','quien',
]

# Etiquetas interpretadas del investigador para cada tópico
TOPIC_LABELS = [
    "Marcos culturales y referencias globales",
    "Humor, transgresión y cuerpo",
    "Juegos, retos y performance colaborativa",
    "Interacción con la audiencia (Q&A)",
    "Viajes, aventura y dinero",
    "Amistad, cotidianidad y grupo de pares",
    "Emociones, vulnerabilidad y reflexión personal",
    "Narrativa biográfica y trayectoria",
    "Localidad, Argentina e identidad territorial",
    "Gustos personales, cultura pop e identidad",
]


# ─── Funciones ────────────────────────────────────────────────────────────────

def clean_text(text):
    """Elimina timestamps, etiquetas de hablante y puntuación."""
    text = re.sub(r'\(\d+:\d+\)', ' ', text)   # timestamps
    text = re.sub(r'Orador \d+', ' ', text)     # etiquetas de hablante
    text = re.sub(r'[^\w\sáéíóúüñÁÉÍÓÚÜÑ]', ' ', text)
    return text.lower()


def load_corpus(path):
    """Carga el CSV de transcripciones y devuelve listas de textos y metadatos."""
    with open(path, 'r', errors='replace') as f:
        reader = csv.reader(f, delimiter=';')
        headers = next(reader)
        rows = list(reader)
    tidx = headers.index('Transcript')
    aidx = headers.index('Autor')
    vidx = 0
    docs    = [clean_text(r[tidx]) for r in rows]
    authors = [r[aidx] for r in rows]
    vids    = [r[vidx] for r in rows]
    return docs, authors, vids


# ─── Pipeline principal ───────────────────────────────────────────────────────

def main():
    print("Cargando corpus...")
    docs, authors, vids = load_corpus(DATA_PATH)
    print(f"  {len(docs)} documentos cargados.")

    print("Vectorizando...")
    vectorizer = CountVectorizer(
        max_df=0.80,
        min_df=4,
        stop_words=STOPWORDS,
        max_features=600,
        ngram_range=(1, 1)
    )
    dtm = vectorizer.fit_transform(docs)
    feature_names = vectorizer.get_feature_names_out()
    print(f"  Vocabulario: {len(feature_names)} términos.")

    print(f"Ajustando LDA ({N_TOPICS} tópicos)...")
    lda = LatentDirichletAllocation(
        n_components=N_TOPICS,
        random_state=RANDOM_STATE,
        max_iter=50,
        learning_method='batch'
    )
    lda.fit(dtm)

    # ─── Tópicos y palabras clave
    print("\n" + "="*70)
    print("TÓPICOS LATENTES — CORPUS VLOGS ARGENTINOS (2012–2016)")
    print("="*70 + "\n")
    for i, topic in enumerate(lda.components_):
        top_idx   = topic.argsort()[-N_TOP_WORDS:][::-1]
        top_words = [feature_names[j] for j in top_idx]
        print(f"Tópico {i+1:2d} — {TOPIC_LABELS[i]}")
        print(f"  Palabras: {', '.join(top_words)}\n")

    # ─── Distribución por youtuber
    topic_dist = lda.transform(dtm)
    author_agg = {}
    for i, author in enumerate(authors):
        if author not in author_agg:
            author_agg[author] = np.zeros(N_TOPICS)
        author_agg[author] += topic_dist[i]

    print("="*70)
    print("DISTRIBUCIÓN TEMÁTICA POR YOUTUBER (top 3 tópicos)")
    print("="*70 + "\n")
    for author, dist in sorted(author_agg.items()):
        norm  = dist / dist.sum()
        top3  = norm.argsort()[-3:][::-1]
        parts = [f"T{t+1} {TOPIC_LABELS[t][:30]} ({norm[t]:.0%})" for t in top3]
        print(f"{author[:20]:20s}: {' | '.join(parts)}")

    print("\nListo. Los resultados pueden exportarse para incorporar en la tesis.")


if __name__ == "__main__":
    main()
