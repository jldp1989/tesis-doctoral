# Materiales de investigación — Tesis doctoral

> **Autor:** José Luis De Piero  
> **Título:** *El videoblog como espacio social practicado: discursos, narrativas e identidades juveniles en YouTube Argentina (2012–2016)*  
> **Directora:** Dra. María Gabriela Palazzo  
> **Institución:** Universidad Nacional de Tucumán — Facultad de Filosofía y Letras

---

## Contenido de esta carpeta

Esta carpeta contiene los datos de investigación, los archivos de red y los scripts de visualización utilizados en el análisis de la tesis. Los materiales se publican con fines de transparencia, reproducibilidad y consulta académica.

### 1. Matriz de análisis (`matriz_analisis.csv`)

Matriz de codificación completa del corpus. Cada fila = un video (80 videos, 8 youtubers × 10 videos). Cada columna = una variable de análisis (144 variables totales).

**Grupos de variables:**
- **Metadatos** (cols 1–8): VID, autor, título, link, vistas, fecha, duración, descripción.
- **Funciones textuales – Heinemann & Viehweger** (cols 9–10): función Griffith y función predominante.
- **Tipos de procedimiento** (cols 11–20): narrativo, descriptivo, expositivo, argumentativo, dialogal (presencia y saturación).
- **Superestructura** (cols 21–30): pre-roll, intro, saludo, presentación, core, despedida, outro, post-roll + tipo de progresión temática y subgénero.
- **Temas** (cols 31–50): 18 categorías temáticas + estructura temática global.
- **Pragmática y sociolingüística** (cols 51–70): deícticos, actos de habla, coloquialismos, variación dialectal, léxico web, mención de plataformas.
- **Escenarios y espacios** (cols 71–82): privado/público, dormitorio, sala, baño, exteriores, tipo de fondo.
- **Vestimenta y cuerpo** (cols 83–89): indumentaria, accesorios, cambios.
- **Planos y cámara** (cols 90–96): primer plano, plano general, primerísimo PP, plano detalle, ángulos.
- **Audio y montaje** (cols 97–102): música de fondo, audios enlatados, clips insertados, silencio.
- **Gestualidad y corporalidad** (cols 103–111): expresividad facial, gestos, corporalidad, violencia, contacto físico, estado emocional.
- **Identidad — Giddens** (cols 112–122): 10 dimensiones de la identidad moderna (yo-nosotros, reflexividad, autenticidad, centralidad del cuerpo, etc.).
- **Dicotomías** (cols 123–126): global/local, joven/adulto, comunicación en redes/masas, obedecer/distinguirse.
- **Backstage — Meyrowitz** (cols 127–138): 12 rasgos del backstage (nombres de pila, faltas de respeto, sexualidad, exhibición corporal, etc.).
- **Índices compuestos** (cols 139–144): IGL (glocalidad), ICP (cercanía parasocial), IMP (modulación pasional), IEX (extimidad), IAP (autenticidad performativa).

**Separador:** punto y coma (`;`). **Codificación:** UTF-8.

### 2. Índices por youtuber (`indices_promedios.csv`)

Promedios de los 5 índices compuestos por youtuber. Sintetiza las 144 variables en 5 dimensiones analíticas.

| Columna | Descripción |
|:--|:--|
| IGL | Índice de Glocalidad (−2 a +2) |
| ICP | Índice de Cercanía Parasocial (1–10) |
| IMP | Índice de Modulación Pasional (1–10) |
| IEX | Índice de Extimidad (1–10) |
| IAP | Índice de Autenticidad Performativa (1–10) |

### 3. Datos de red — Análisis de Redes Sociales

Archivos preparados para Gephi u otro software de análisis de redes.

- **`red_nodos.csv`** — 59 nodos (8 youtubers del corpus nuclear + 16 colaboradores + nodos temáticos). Columnas: ID, Label, Type.
- **`red_aristas.csv`** — 668 aristas ponderadas de colaboración y co-ocurrencia temática. Columnas: Source, Target, Weight.
- **`red_aristas_tematicas.csv`** — 375 aristas de co-ocurrencia entre youtubers y temas. Columnas: Source, Target, Type, Weight.
- **`red_nodos_tematicos.csv`** — 26 nodos del grafo temático (8 youtubers + 18 categorías temáticas).

- **`viz_all.py`** — Script principal de generación de las 24 visualizaciones de la tesis (histogramas, heatmaps, scatter plots, tablas estilizadas). Requiere: Python 3.8+, pandas, matplotlib, seaborn, numpy.
- **`viz_giddens_tabla.py`** — Script de generación de la tabla de dimensiones identitarias según Giddens.
- **`topic_modeling.py`** — Script de modelado de tópicos (LDA) sobre el corpus de transcripciones. Genera los 10 tópicos latentes y su distribución por youtuber.

### 5. Transcripciones y Matrices adicionales

- **`transcripciones.csv`** — Corpus textual procesado: 80 transcripciones limpias listas para procesamiento computacional.
- **`matriz_indices.csv`** — Matriz refinada con los cálculos de los 5 índices (IGL, ICP, IMP, IEX, IAP) por video.

Las transcripciones completas (80 videos, ~96.000 palabras, con marcas temporales) están disponibles en el Anexo E de la versión web.

---

## Licencia y citación

Estos materiales se publican bajo licencia [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/). Para citar:

> De Piero, J. L. (2026). *El videoblog como espacio social practicado: discursos, narrativas e identidades juveniles en YouTube Argentina (2012–2016)* [Tesis doctoral, Universidad Nacional de Tucumán]. Materiales de investigación.

Para consultas: joseluisdepiero@gmail.com
