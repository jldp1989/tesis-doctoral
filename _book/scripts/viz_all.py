"""
viz_all.py — Generador de todas las visualizaciones autónomas de la tesis
Autor: J.L. De Piero
Genera: VIZ02, VIZ03, VIZ05, VIZ10, VIZ11, VIZ18, VIZ19, VIZ21, VIZ22
Salidas: imagenes/viz*.png
"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib as mpl
import numpy as np
import networkx as nx
import os, warnings
warnings.filterwarnings('ignore')

# ─── Paleta visual unificada ────────────────────────────────────────────────
DARK_BG = "#1a1a2e"
P1 = "#e94560"   # rojo-coral
P2 = "#0f3460"   # azul oscuro  
P3 = "#533483"   # violeta
P4 = "#00b4d8"   # cyan
P5 = "#e8c46a"   # dorado
GRAY = "#a8a8b3"
WHITE = "#f0f0f0"
PALETTE = [P1, P4, P3, P5, P2, "#2dc653", "#ff9f1c", "#c9f0ff"]

mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["IBM Plex Sans", "DejaVu Sans", "Liberation Sans"],
    "axes.facecolor": DARK_BG,
    "figure.facecolor": DARK_BG,
    "text.color": WHITE,
    "axes.labelcolor": WHITE,
    "xtick.color": GRAY,
    "ytick.color": WHITE,
    "axes.edgecolor": "#3a3a5a",
    "grid.color": "#2a2a4a",
    "grid.linestyle": "--",
    "grid.alpha": 0.6,
    "axes.titlecolor": WHITE,
})

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT  = os.path.join(BASE, 'imagenes')
DATA = os.path.join(BASE, 'data')

def savefig(name, fig):
    path = os.path.join(OUT, name)
    fig.savefig(path, dpi=150, bbox_inches='tight', facecolor=DARK_BG)
    plt.close(fig)
    print(f"  ✅ {name}")

# ─── Cargar datos ────────────────────────────────────────────────────────────
df = pd.read_csv(os.path.join(DATA, 'MATRIZ_FINAL_RESTAURADA.csv'),
                 sep=';', encoding='utf-8', on_bad_lines='skip', low_memory=False)
tp = pd.read_csv(os.path.join(DATA, 'TABLA_PROMEDIOS_TESIS.csv'),
                 sep=';', on_bad_lines='skip', encoding='utf-8')
N = len(df)  # 80
print(f"Corpus cargado: {N} videos\n")

# ═══════════════════════════════════════════════════════════════════════════════
# VIZ-02: Network Graph del corpus (8 youtubers × 10 videos)
# ═══════════════════════════════════════════════════════════════════════════════
print("→ VIZ-02 Network Graph corpus...")
G = nx.Graph()
youtubers = df['Autor'].unique()
subs = {
    'Lucas Castel': 2.5, 'Julián Serrano': 2.2, 'Gonzalo Fonseca': 1.8,
    'Lionel Ferro': 1.6, 'Mariano Bondar': 1.4, 'Gonzalo Goette': 1.23,
    'Elchuiuical': 1.15, 'Mica Suárez': 1.08
}

for _, row in df.iterrows():
    autor = row['Autor']
    vid_id = f"v{int(row['VID'])}"
    titulo = str(row['Título'])[:25] + '…' if len(str(row['Título'])) > 25 else str(row['Título'])
    G.add_node(autor, type='youtuber', subs=subs.get(autor, 1.0))
    G.add_node(vid_id, type='video', label=titulo, autor=autor)
    G.add_edge(autor, vid_id)

fig, ax = plt.subplots(figsize=(13, 10), facecolor=DARK_BG)
ax.set_facecolor(DARK_BG)

yt_nodes = [n for n, d in G.nodes(data=True) if d.get('type') == 'youtuber']
vid_nodes = [n for n, d in G.nodes(data=True) if d.get('type') == 'video']

pos = {}
n_yt = len(yt_nodes)
for i, yt in enumerate(yt_nodes):
    angle = 2 * np.pi * i / n_yt
    pos[yt] = (np.cos(angle) * 3, np.sin(angle) * 3)
    vid_list = [v for v in G.neighbors(yt)]
    for j, vid in enumerate(vid_list):
        sub_angle = angle + (j - 4.5) * 0.18
        r = 5.2 + np.random.uniform(-0.2, 0.2)
        pos[vid] = (np.cos(sub_angle) * r, np.sin(sub_angle) * r)

nx.draw_networkx_edges(G, pos, ax=ax, alpha=0.18, edge_color=GRAY, width=0.6)
node_sizes_yt = [subs.get(yt, 1) * 1200 for yt in yt_nodes]
nx.draw_networkx_nodes(G, pos, nodelist=yt_nodes, node_color=PALETTE[:n_yt],
                       node_size=node_sizes_yt, ax=ax)
nx.draw_networkx_nodes(G, pos, nodelist=vid_nodes, node_color=GRAY,
                       node_size=35, ax=ax, alpha=0.7)
nx.draw_networkx_labels(G, pos, labels={n: n for n in yt_nodes},
                        ax=ax, font_size=8, font_color=WHITE,
                        font_weight='bold', verticalalignment='bottom')

ax.set_title('Estructura del corpus: 8 youtubers (nodos centrales) × 80 videoblogs',
             fontsize=13, weight='bold', pad=15)
ax.axis('off')
leg_els = [mpatches.Patch(color=PALETTE[i], label=yt) for i, yt in enumerate(yt_nodes)]
leg_els.append(mpatches.Patch(color=GRAY, label='Videos del corpus (n=80)'))
ax.legend(handles=leg_els, loc='lower left', fontsize=8,
          facecolor='#2a2a4a', edgecolor=GRAY, labelcolor=WHITE, framealpha=0.85)

savefig('viz02_corpus_network.png', fig)

# ═══════════════════════════════════════════════════════════════════════════════
# VIZ-03: Diagrama de Venn — Tres ejes teóricos
# ═══════════════════════════════════════════════════════════════════════════════
print("→ VIZ-03 Venn tres ejes...")
from matplotlib.patches import Ellipse
fig, ax = plt.subplots(figsize=(9, 7), facecolor=DARK_BG)
ax.set_facecolor(DARK_BG)

circles = [
    (0.0,  0.7, P1,  "Análisis del\nDiscurso"),
    (-0.6, -0.4, P4, "Estudios de\nJuventudes"),
    (0.6, -0.4, P3,  "Internet como\nEspacio Social"),
]
for (cx, cy, color, label) in circles:
    e = Ellipse((cx, cy), width=1.9, height=1.5, alpha=0.35, color=color, zorder=1)
    ax.add_patch(e)
    # Label outside
    ax.text(cx * 1.75, cy * 1.6, label, ha='center', va='center',
            fontsize=11, color=WHITE, fontweight='bold', zorder=5,
            bbox=dict(boxstyle='round,pad=0.3', facecolor=color, alpha=0.75, edgecolor='none'))

# Center: the vlog
ax.text(0, 0.12, 'El\nVIDEOBLOG', ha='center', va='center',
        fontsize=13, fontweight='bold', color=WHITE, zorder=6,
        bbox=dict(boxstyle='round,pad=0.5', facecolor='#1a1a2e', edgecolor=P5, linewidth=2))

# Intersection labels  
ax.text(0, 0.55,     'Discurso\njuvenil digital', ha='center', fontsize=8, color=GRAY, zorder=4)
ax.text(-0.45, -0.05, 'Cultura\njuvenil', ha='center', fontsize=8, color=GRAY, zorder=4)
ax.text(0.45, -0.05,  'Prácticas\nen red', ha='center', fontsize=8, color=GRAY, zorder=4)

ax.set_xlim(-2.2, 2.2)
ax.set_ylim(-1.9, 2.2)
ax.set_title('Marco teórico integrado: intersección de los tres ejes\nde la investigación', 
             fontsize=13, weight='bold', pad=12)
ax.axis('off')
savefig('viz03_venn_ejes.png', fig)

# ═══════════════════════════════════════════════════════════════════════════════
# VIZ-05: Barras horizontales — Suscriptores (2016)
# ═══════════════════════════════════════════════════════════════════════════════
print("→ VIZ-05 Suscriptores...")
subs_ordered = {k: v for k, v in sorted(subs.items(), key=lambda x: x[1])}
yt_names = list(subs_ordered.keys())
sub_vals = list(subs_ordered.values())
colors_bar = [PALETTE[i % len(PALETTE)] for i in range(len(yt_names))]

fig, ax = plt.subplots(figsize=(9, 5), facecolor=DARK_BG)
bars = ax.barh(yt_names, sub_vals, color=colors_bar, height=0.6)
for bar, val in zip(bars, sub_vals):
    ax.text(bar.get_width() + 0.03, bar.get_y() + bar.get_height()/2,
            f'{val:.2f}M', va='center', ha='left', fontsize=9.5, color=WHITE)
ax.axvline(1.0, color=P5, linewidth=1, linestyle=':', alpha=0.7, label='Criterio mínimo: 1M suscriptores')
ax.set_xlabel('Suscriptores (millones, dic. 2016)')
ax.set_title('Youtubers del corpus según número de suscriptores\n(corte: diciembre 2016)', 
             fontsize=12, weight='bold', pad=10)
ax.set_xlim(0, 3.1)
ax.grid(axis='x', zorder=0)
ax.spines[['top','right']].set_visible(False)
ax.legend(facecolor='#2a2a4a', edgecolor=GRAY, labelcolor=WHITE, fontsize=9)
savefig('viz05_suscriptores.png', fig)

# ═══════════════════════════════════════════════════════════════════════════════
# VIZ-09+10: Escenarios y Secuencias
# ═══════════════════════════════════════════════════════════════════════════════
print("→ VIZ-09 Escenarios...")
# Simplify escenarios (take first listed)
esc_simple = df['Escenarios'].fillna('NC')
esc_map = {
    'Dormitorio': 'Dormitorio', 'Sala del Hogar': 'Sala del hogar',
    'Exteriores viajes': 'Exteriores / viajes', 'Interior': 'Interior (otro)',
    'Exterior': 'Exterior (otro)'
}
esc_first = esc_simple.str.split(',').str[0].str.strip()
esc_counts = esc_first.value_counts()

fig, ax = plt.subplots(figsize=(9, 5), facecolor=DARK_BG)
esc_labels = [e[:30] for e in esc_counts.index]
esc_vals = list(esc_counts.values)
bars = ax.barh(esc_labels, esc_vals, color=PALETTE[:len(esc_labels)], height=0.55)
for bar, val in zip(bars, esc_vals):
    pct = val/N*100
    ax.text(bar.get_width() + 0.2, bar.get_y() + bar.get_height()/2,
            f'{val} ({pct:.0f}%)', va='center', fontsize=9, color=WHITE)
ax.set_xlabel('Número de videos')
ax.set_title('Escenarios predominantes en el corpus\n(escenario principal por video, n=80)',
             fontsize=12, weight='bold', pad=10)
ax.set_xlim(0, 32)
ax.grid(axis='x', zorder=0)
ax.spines[['top','right']].set_visible(False)
ax.invert_yaxis()
savefig('viz09_escenarios.png', fig)

print("→ VIZ-10 Secuencias TP...")
tp_data = {
    'Narrativa\n(TP-Nar)': (df['TP-Nar'].astype(str).str.upper() == 'VERDADERO').sum(),
    'Dialógica\n(TP-dia)': (df['TP-dia'].astype(str).str.upper() == 'VERDADERO').sum(),
    'Argumentativa\n(TP-Ar)': (df['TP-Ar'].astype(str).str.upper() == 'VERDADERO').sum(),
    'Expositiva\n(TP-Ex)': (df['TP-Ex'].astype(str).str.upper() == 'VERDADERO').sum(),
    'Descriptiva\n(TP-Des)': (df['TP-Des'].astype(str).str.upper() == 'VERDADERO').sum(),
}
explode = (0.04, 0.02, 0.02, 0.02, 0.02)
fig, ax = plt.subplots(figsize=(8, 7), facecolor=DARK_BG)
wedges, texts, autotexts = ax.pie(list(tp_data.values()), labels=None,
                                   autopct='%1.1f%%', colors=PALETTE[:5],
                                   startangle=140, explode=explode,
                                   pctdistance=0.78, textprops={'color': WHITE})
for at in autotexts:
    at.set_fontsize(11)
    at.set_fontweight('bold')
ax.legend(wedges, [f'{k.replace(chr(10), " ")} ({v})'
                   for k, v in tp_data.items()],
          loc='lower center', bbox_to_anchor=(0.5, -0.12), ncol=2,
          fontsize=9, facecolor='#2a2a4a', edgecolor=GRAY, labelcolor=WHITE)
ax.set_title('Distribución de secuencias discursivas dominantes\nen el corpus de vlogs (n=80)',
             fontsize=12, weight='bold', pad=15)
savefig('viz10_secuencias.png', fig)

# ═══════════════════════════════════════════════════════════════════════════════
# VIZ-11: Superestructura
# ═══════════════════════════════════════════════════════════════════════════════
print("→ VIZ-11 Superestructura...")
sup = df['Superestructura'].fillna('')
comp = {
    'Pre-vid\n(anticipación)':  sup.str.contains('Pre-vid', case=False, na=False).sum(),
    'Intro':                    (sup.str.contains(r'Intro', case=False, na=False) & 
                                 ~sup.str.contains('INTROSALUDO', na=False)).sum(),
    'Saludo /\nIntroSaludo':    sup.str.contains('Saludo|INTROSALUDO', case=False, na=False).sum(),
    'Presentación\ndel tema':   sup.str.contains('Presentación del tema', case=False, na=False).sum(),
    'Núcleo\ntemático':         N,
    'Despedida':                sup.str.contains('Despedida', case=False, na=False).sum(),
    'Outro':                    sup.str.contains('Outro', case=False, na=False).sum(),
    'Post-vid':                 sup.str.contains('Postvid', case=False, na=False).sum(),
}
c_labels = list(comp.keys())
c_vals = [v / N * 100 for v in comp.values()]
c_counts = list(comp.values())
bar_colors = [P3, P3, P1, P1, P4, P1, P2, P2]

fig, ax = plt.subplots(figsize=(10, 5.5), facecolor=DARK_BG)
bars = ax.barh(c_labels, c_vals, color=bar_colors, height=0.6)
for bar, val, cnt in zip(bars, c_vals, c_counts):
    ax.text(bar.get_width() + 0.8, bar.get_y() + bar.get_height()/2,
            f'{val:.1f}%  ({cnt}/{N})', va='center', ha='left', fontsize=9, color=WHITE)
ax.set_xlim(0, 120)
ax.set_xlabel('% de videos del corpus')
ax.set_title('Frecuencia de componentes superestructurales del vlog\n(corpus: 80 videos, 8 youtubers)',
             fontsize=12, weight='bold', pad=10)
ax.axvline(100, color=P1, linewidth=0.8, linestyle=':', alpha=0.6)
ax.grid(axis='x', zorder=0)
ax.invert_yaxis()
ax.spines[['top','right']].set_visible(False)
leg = [mpatches.Patch(color=P1, label='Componente frecuente (>60%)'),
       mpatches.Patch(color=P2, label='Componente opcional (<50%)'),
       mpatches.Patch(color=P4, label='Componente universal (100%)'),
       mpatches.Patch(color=P3, label='Componente periférico (<42%)')]
ax.legend(handles=leg, loc='lower right', fontsize=8,
          facecolor='#2a2a4a', edgecolor=GRAY, labelcolor=WHITE)
savefig('viz11_superestructura.png', fig)

# ═══════════════════════════════════════════════════════════════════════════════
# VIZ-18: Torta ICP — Distribución del índice de cercanía parasocial
# ═══════════════════════════════════════════════════════════════════════════════
print("→ VIZ-18 Torta ICP...")
icp = df['ICP']
# Real distribution using tercile cuts matching data
low  = (icp <= 3.38).sum()
mid  = ((icp > 3.38) & (icp <= 5.62)).sum()
high = (icp > 5.62).sum()

fig, ax = plt.subplots(figsize=(7, 6.5), facecolor=DARK_BG)
sizes = [low, mid, high]
labels_pie = [f'Cercanía baja\n(ICP ≤ 3.38)\nn={low} ({low/N*100:.1f}%)',
              f'Cercanía media\n(3.38 < ICP ≤ 5.62)\nn={mid} ({mid/N*100:.1f}%)',
              f'Cercanía alta\n(ICP > 5.62)\nn={high} ({high/N*100:.1f}%)']
wedges, texts = ax.pie(sizes, labels=None, colors=[P2, P3, P1],
                       startangle=120, explode=(0.03, 0.02, 0.05),
                       wedgeprops={'linewidth': 1.5, 'edgecolor': DARK_BG})
ax.legend(wedges, labels_pie, loc='lower center', bbox_to_anchor=(0.5, -0.15),
          fontsize=9.5, facecolor='#2a2a4a', edgecolor=GRAY, labelcolor=WHITE)
ax.set_title('Distribución del Índice de Cercanía Parasocial (ICP)\nen el corpus (n=80, escala 0-10)',
             fontsize=12, weight='bold', pad=12)
savefig('viz18_icp_torta.png', fig)

# ═══════════════════════════════════════════════════════════════════════════════
# VIZ-19: Diagrama modelo analítico 3 niveles
# ═══════════════════════════════════════════════════════════════════════════════
print("→ VIZ-19 Modelo 3 niveles...")
fig, ax = plt.subplots(figsize=(10, 7), facecolor=DARK_BG)
ax.set_facecolor(DARK_BG)
ax.set_xlim(0, 10)
ax.set_ylim(0, 8)
ax.axis('off')

levels = [
    (5, 6.5, P3, 'NIVEL 1: Representaciones sociales',
     'Marcos estructurantes que delimitan\nlo pensable, decible y mostrable sobre juventud\n[Feixa, Reguillo, Bonvillani]'),
    (5, 4.2, P2, 'NIVEL 2: Subjetividades',
     'Posiciones disponibles para los sujetos\ndentro de los marcos representacionales\n[Giddens, Palazzo, Bonvillani]'),
    (5, 1.9, P1, 'NIVEL 3: Identidades juveniles digitales',
     'Construcciones performativas, reflexivas\ny situadas en la interacción concreta\n[Proyecto reflexivo del yo — Giddens 1991]'),
]
for (cx, cy, color, title, subtitle) in levels:
    rect = mpatches.FancyBboxPatch((cx-4.3, cy-0.65), 8.6, 1.5,
                                    boxstyle="round,pad=0.15",
                                    facecolor=color, alpha=0.8, edgecolor=WHITE,
                                    linewidth=1.2)
    ax.add_patch(rect)
    ax.text(cx, cy + 0.42, title, ha='center', va='center',
            fontsize=11, fontweight='bold', color=WHITE, zorder=4)
    ax.text(cx, cy - 0.12, subtitle, ha='center', va='center',
            fontsize=8, color=WHITE, alpha=0.9, zorder=4)

# Arrows between levels
for y_top, y_bot in [(5.65, 5.35), (3.35, 3.05)]:
    ax.annotate('', xy=(5, y_bot), xytext=(5, y_top),
                arrowprops=dict(arrowstyle='->', color=P5, lw=2))

# The vlog in center connecting
vlog_box = mpatches.FancyBboxPatch((3.5, 2.9), 3, 0.95,
                                    boxstyle="round,pad=0.12",
                                    facecolor=P5, alpha=0.9, edgecolor=WHITE,
                                    linewidth=1.5, zorder=5)
ax.add_patch(vlog_box)
ax.text(5, 3.38, 'el VIDEOBLOG\ncomo arena de negociación', ha='center', va='center',
        fontsize=9.5, fontweight='bold', color=DARK_BG, zorder=6)

ax.set_title('Modelo analítico integrado: tres niveles de análisis\nde las identidades juveniles digitales',
             fontsize=13, weight='bold', pad=12, color=WHITE)
savefig('viz19_modelo_niveles.png', fig)

# ═══════════════════════════════════════════════════════════════════════════════
# VIZ-21: Tabla 2 — Índices promedio por youtuber (heatmap tabla)
# ═══════════════════════════════════════════════════════════════════════════════
print("→ VIZ-21 Tabla índices...")
tp_sorted = tp.set_index('Autor').sort_values('IAP', ascending=False)
indices = ['IGL', 'ICP', 'IMP', 'IEX', 'IAP']
index_labels = {'IGL': 'Glocalidad\n(IGL)', 'ICP': 'Cercanía\nParasocial (ICP)',
                'IMP': 'Modulación\nPasional (IMP)', 'IEX': 'Extimidad\n(IEX)',
                'IAP': 'Autenticidad\nPerformativa (IAP)'}

fig, ax = plt.subplots(figsize=(11, 5), facecolor=DARK_BG)
ax.set_facecolor(DARK_BG)

data_matrix = tp_sorted[indices].values.astype(float)
n_yt, n_idx = data_matrix.shape

# Normalize per column for color intensity
normed = np.zeros_like(data_matrix)
for j in range(n_idx):
    col = data_matrix[:, j]
    cmin, cmax = col.min(), col.max()
    normed[:, j] = (col - cmin) / (cmax - cmin + 1e-9)

from matplotlib.colors import LinearSegmentedColormap
cmap = LinearSegmentedColormap.from_list('tesis', [P2, P3, P1])

for i, yt in enumerate(tp_sorted.index):
    for j, idx in enumerate(indices):
        val = data_matrix[i, j]
        intensity = normed[i, j]
        color = cmap(intensity)
        rect = mpatches.FancyBboxPatch((j, n_yt - i - 1), 1, 1,
                                        boxstyle="round,pad=0.05",
                                        facecolor=color, alpha=0.88,
                                        edgecolor=DARK_BG, linewidth=2)
        ax.add_patch(rect)
        fmt = f'{val:+.2f}' if idx == 'IGL' else f'{val:.2f}'
        ax.text(j + 0.5, n_yt - i - 0.5, fmt,
                ha='center', va='center', fontsize=10.5, fontweight='bold',
                color=WHITE if intensity > 0.4 else GRAY)

ax.set_xlim(0, n_idx)
ax.set_ylim(0, n_yt)
ax.set_xticks([j + 0.5 for j in range(n_idx)])
ax.set_xticklabels([index_labels[i] for i in indices], fontsize=9, color=WHITE)
ax.set_yticks([n_yt - i - 0.5 for i in range(n_yt)])
ax.set_yticklabels(tp_sorted.index, fontsize=9.5, color=WHITE)
ax.xaxis.set_ticks_position('top')
ax.xaxis.set_label_position('top')
ax.spines[:].set_visible(False)
ax.tick_params(length=0)

# Color scale note
sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(0, 1))
sm.set_array([])
cbar = plt.colorbar(sm, ax=ax, orientation='vertical', fraction=0.03, pad=0.02)
cbar.set_label('Intensidad relativa\n(normalizada por índice)', fontsize=8, color=WHITE)
cbar.ax.yaxis.set_tick_params(color=WHITE)
plt.setp(cbar.ax.yaxis.get_ticklabels(), color=WHITE, fontsize=7)

ax.set_title('Índices ponderados promedio por youtuber\n(IGL ∈ ℝ; ICP, IMP, IEX, IAP ∈ [0,10])',
             fontsize=12, weight='bold', pad=30)

plt.tight_layout()
savefig('viz21_tabla_indices.png', fig)

# ═══════════════════════════════════════════════════════════════════════════════
# VIZ-22: Tabla dialectal (from existing table in 07_lenguaje.qmd)
# Already exists as markdown table — generate a formatted PNG version
# ═══════════════════════════════════════════════════════════════════════════════
print("→ VIZ-22 Tabla dialectal...")
dial_data = {
    'Youtuber':       ['Lucas Castel', 'Julián Serrano', 'Gonzalo Fonseca', 'Lionel Ferro',
                       'Mariano Bondar', 'Gonzalo Goette', 'Elchuiuical', 'Mica Suárez'],
    'Origen':         ['Buenos Aires', 'Entre Ríos', 'Buenos Aires', 'Córdoba',
                       'Buenos Aires', 'Santa Fe', 'Buenos Aires', 'Buenos Aires'],
    'Variedad':       ['Rioplatense', 'Litoral/Riopl. (conv.)', 'Rioplatense', 'Cordobesa (conv.)',
                       'Rioplatense', 'Santafesina (conv.)', 'Rioplatense', 'Rioplatense'],
    'Videos':         [10]*8,
    'Suscriptores':   ['~2.5M', '~2.2M', '~1.8M', '~1.6M', '~1.4M', '~1.23M', '~1.15M', '~1.08M'],
}
dial_df = pd.DataFrame(dial_data)

fig, ax = plt.subplots(figsize=(12, 4), facecolor=DARK_BG)
ax.set_facecolor(DARK_BG)
ax.axis('off')

col_widths = [0.16, 0.14, 0.25, 0.07, 0.13]
col_headers = ['Youtuber', 'Origen geográfico', 'Variedad dialectal', 'Videos', 'Suscriptores (2016)']
colors_row = [PALETTE[i % len(PALETTE)] for i in range(8)]

y_start = 0.85
row_h = 0.10
x_pos = [0.01, 0.20, 0.36, 0.64, 0.73]

# Header
for j, (hdr, xp) in enumerate(zip(col_headers, x_pos)):
    ax.text(xp, y_start + 0.04, hdr, transform=ax.transAxes,
            fontsize=9, fontweight='bold', color=P5, va='center')

ax.axhline(y=y_start - 0.01, xmin=0.01, xmax=0.97, color=P5, linewidth=1.5, transform=ax.transAxes)

for i, row in dial_df.iterrows():
    y = y_start - (i + 1) * row_h
    # Row background alternating
    bg = mpatches.FancyBboxPatch((0.01, y - 0.03), 0.96, row_h - 0.01,
                                  boxstyle='square', transform=ax.transAxes,
                                  facecolor=colors_row[i], alpha=0.12,
                                  edgecolor='none', zorder=1)
    ax.add_patch(bg)
    for j, (col, xp) in enumerate(zip(dial_data.keys(), x_pos)):
        val = str(row[col])
        ax.text(xp, y + 0.02, val, transform=ax.transAxes,
                fontsize=9, color=WHITE, va='center')
    # Color dot for origin
    if 'conv' in row['Variedad']:
        ax.text(0.91, y + 0.02, '⟳', transform=ax.transAxes, fontsize=10,
                color=P5, va='center', ha='center')

ax.set_title('Tabla 1. Youtubers del corpus: origen geográfico y variedad dialectal',
             fontsize=11, weight='bold', pad=8, color=WHITE, x=0.5, y=1.02,
             transform=ax.transAxes)
ax.text(0.93, y_start + 0.04, '⟳ = convergencia', transform=ax.transAxes,
        fontsize=7.5, color=P5, va='center')

savefig('viz22_tabla_dialectal.png', fig)

print("\n✅ Todas las visualizaciones generadas:")
for f in sorted(os.listdir(OUT)):
    if f.startswith('viz'):
        print(f"  {f}")
