import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

fig, ax = plt.subplots(figsize=(6, 9))
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis('off')
fig.patch.set_facecolor('#FAFAFA')

colors = {
    'ocr':    '#4A90D9',
    'orch':   '#7B68EE',
    'store':  '#2ECC71',
    'rag':    '#E67E22',
    'ui':     '#E74C3C',
    'arrow':  '#555555',
    'header': '#2C3E50',
}

def draw_layer(ax, y, height, color, label, sublabel):
    # Background fill
    ax.add_patch(FancyBboxPatch((0.3, y), 9.4, height,
                                boxstyle="round,pad=0.05",
                                linewidth=2, edgecolor=color,
                                facecolor=color, alpha=0.12, zorder=2))
    # Left accent bar
    ax.add_patch(FancyBboxPatch((0.3, y), 0.28, height,
                                boxstyle="square,pad=0",
                                linewidth=0, facecolor=color, alpha=0.85, zorder=3))
    ax.text(0.75, y + height / 2 + 0.17, label,
            fontsize=12, fontweight='bold', va='center', color=color, zorder=4)
    ax.text(0.75, y + height / 2 - 0.22, sublabel,
            fontsize=9, va='center', color='#444444', zorder=4)

def draw_arrow(ax, x, y_from, y_to):
    ax.annotate('', xy=(x, y_to + 0.02), xytext=(x, y_from - 0.02),
                arrowprops=dict(arrowstyle='->', color=colors['arrow'],
                                lw=2.0, mutation_scale=16))

layers = [
    (8.1, 1.4, colors['ocr'],   'Katman 1 — Veri Alımı (OCR)',
     'PDF / DOCX  →  Tesseract / AWS Textract  →  Ham Metin'),
    (6.2, 1.5, colors['orch'],  'Katman 2 — Orkestrasyon (LangGraph)',
     'Clause Agent   |   Risk Agent   |   Negotiation Agent'),
    (4.3, 1.5, colors['store'], 'Katman 3 — Anlamsal Depolama',
     'PostgreSQL 15 + pgvector   |   Playbook Kuralları   |   Sözleşme Arşivi'),
    (2.4, 1.5, colors['rag'],   'Katman 4 — Akıllı Analiz (RAG)',
     'Embedding  →  Cosine Similarity  →  Risk Skoru (Düşük / Orta / Yüksek)'),
    (0.4, 1.6, colors['ui'],    'Katman 5 — Görselleştirme (UI)',
     'Redline / Diff Modülü   |   Onay Akışı   |   Audit Log Ekranı'),
]

for (y, h, c, lbl, sub) in layers:
    draw_layer(ax, y, h, c, lbl, sub)

arrow_x = 5.0
for i in range(len(layers) - 1):
    y_from = layers[i][0]
    y_to   = layers[i+1][0] + layers[i+1][1]
    draw_arrow(ax, arrow_x, y_from, y_to)

ax.text(5.0, 9.8, 'Lagent — Sistem Mimarisi',
        fontsize=15, fontweight='bold', ha='center', va='top', color=colors['header'])
ax.text(5.0, 9.45, 'Test kapsamındaki bileşenler ve katmanlar arası veri akışı',
        fontsize=9.5, ha='center', va='top', color='#666666')

plt.tight_layout(pad=0.2)
plt.savefig('figures/fig_system_architecture.png', dpi=180,
            bbox_inches='tight', facecolor='#FAFAFA')
print('Saved.')
