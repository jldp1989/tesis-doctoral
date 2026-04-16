"""
viz_giddens_tabla.py
VIZ-20: Tabla de articulación Giddens / ciberdiscurso juvenil / marcadores en el vlog
Salida: imagenes/viz20_tabla_giddens.png
"""
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.patches as mpatches
import numpy as np
import os

DARK_BG = "#1a1a2e"; P1 = "#e94560"; P2 = "#0f3460"; P3 = "#533483"; P4 = "#00b4d8"
P5 = "#e8c46a"; WHITE = "#f0f0f0"; GRAY = "#a8a8b3"

mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["IBM Plex Sans", "DejaVu Sans"],
    "figure.facecolor": DARK_BG, "text.color": WHITE,
})

# Tabla: Giddens 1991 → Palazzo 2010 → Marcador en el vlog
rows = [
    ("Proyecto reflexivo\ndel yo",
     "Narrativa de identidad\ncontinua y coherente",
     "«Hola, soy [nombre]»; auto-presentaciones\nrecurrentes; auto-definiciones explícitas"),

    ("Reflexividad continua\ne inserción comunitaria",
     "Diálogo con la audiencia;\nconciencia de ser visto",
     "Interpelación directa; preguntas retóricas;\nconvocatoria a comentar y suscribir"),

    ("Centralidad del cuerpo\ncomo proyecto",
     "Exhibición corporal gestionada;\nauto-imagen curada",
     "Encuadre: primer plano predominante;\ngestualidad expresiva; ropa como código"),

    ("Riesgo y oportunidad:\nnarrativa de éxito",
     "Discurso de superación;\nmodelos aspiracionales",
     "Relatos de «cuando era chico»;\nmención de logros y hitos del canal"),

    ("Sinceridad y autenticidad\ncomo valor",
     "Backstage visible;\nestética de lo espontáneo",
     "Errores no editados; confesiones;\nrelatos de fracaso y vulnerabilidad"),

    ("Atemporalidad →\nactualidad situada",
     "Referencia al presente inmediato;\ncalendario juvenil",
     "«Hoy les cuento»; marcadores temporales\ninmediatos; eventos virales del momento"),

    ("Ritos de pasaje\ny transición",
     "Relatos de cambio biográfico;\ncrisis y maduración",
     "Anuncios de mudanza, fin de estudios,\nprimeras veces; reflexiones de cierre de etapas"),

    ("Tensión global/local\n(glocalidad)",
     "Mezcla de referentes globales\ny marcas locales",
     "Anglicismos + lunfardo; marcas glocales;\nreferencias a cultura local y global simultáneas"),
]

n_rows = len(rows)
fig, ax = plt.subplots(figsize=(14, n_rows * 0.75 + 1.5), facecolor=DARK_BG)
ax.set_facecolor(DARK_BG)
ax.axis('off')

col_labels = [
    "Rasgo de identidad reflexiva\n(Giddens, 1991)",
    "Característica del ciberdiscurso juvenil\n(Palazzo, 2010)",
    "Marcador discursivo en el videoblog\n(corpus: 80 vlogs, 2012-2016)",
]
col_colors = [P3, P2, P1]
x_starts = [0.01, 0.30, 0.57]
col_widths_frac = [0.28, 0.26, 0.42]

row_h = 1.0 / (n_rows + 2)

# Column headers
for j, (label, xp, cw, cc) in enumerate(zip(col_labels, x_starts, col_widths_frac, col_colors)):
    rect = mpatches.FancyBboxPatch((xp, 1 - row_h), cw - 0.01, row_h - 0.01,
                                    boxstyle='round,pad=0.01', transform=ax.transAxes,
                                    facecolor=cc, alpha=0.95, edgecolor=DARK_BG, linewidth=2)
    ax.add_patch(rect)
    ax.text(xp + cw / 2, 1 - row_h / 2, label, ha='center', va='center',
            fontsize=9, fontweight='bold', color=WHITE, transform=ax.transAxes)

# Data rows
for i, (col1, col2, col3) in enumerate(rows):
    y = 1 - (i + 2) * row_h
    bg_alpha = 0.10 if i % 2 == 0 else 0.04
    bg = mpatches.FancyBboxPatch((0.01, y), 0.98, row_h - 0.005,
                                  boxstyle='square', transform=ax.transAxes,
                                  facecolor=WHITE, alpha=bg_alpha, edgecolor='none')
    ax.add_patch(bg)
    for val, xp, cw in zip([col1, col2, col3], x_starts, col_widths_frac):
        ax.text(xp + 0.01, y + row_h / 2, val, ha='left', va='center',
                fontsize=7.5, color=WHITE, transform=ax.transAxes,
                multialignment='left', linespacing=1.3)

# Vertical dividers
for xp in x_starts[1:]:
    line = plt.Line2D([xp - 0.005, xp - 0.005], [row_h, 1],
                      transform=ax.transAxes, color=GRAY, linewidth=0.5, alpha=0.4)
    ax.add_line(line)

ax.text(0.5, 1 - row_h * 0.15,
        'Tabla 4. Articulación entre identidad reflexiva, ciberdiscurso juvenil y marcadores discursivos en el videoblog',
        ha='center', va='center', fontsize=10.5, fontweight='bold',
        color=WHITE, transform=ax.transAxes)

plt.tight_layout()
out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   'imagenes', 'viz20_tabla_giddens.png')
plt.savefig(out, dpi=150, bbox_inches='tight', facecolor=DARK_BG)
plt.close()
print(f"✅ {out}")
