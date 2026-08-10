import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

fig, ax = plt.subplots(figsize=(6, 9))
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis('off')
fig.patch.set_facecolor('#FAFAFA')

actors = [
    (1.0,  'Risk\nAgent',     '#E74C3C'),
    (3.5,  'Embedding\nServis', '#7B68EE'),
    (6.0,  'pgvector',        '#2ECC71'),
    (8.5,  'Playbook\nKuralları', '#E67E22'),
]

actor_y_top = 9.0
actor_box_h = 0.6
lifeline_y_bot = 0.7

for x, name, color in actors:
    ax.add_patch(FancyBboxPatch((x - 0.65, actor_y_top - actor_box_h),
                                1.3, actor_box_h,
                                boxstyle="round,pad=0.06",
                                linewidth=1.8, edgecolor=color,
                                facecolor=color, alpha=0.85, zorder=3))
    ax.text(x, actor_y_top - actor_box_h / 2, name,
            fontsize=7.5, fontweight='bold', ha='center', va='center',
            color='white', zorder=4)
    ax.plot([x, x], [actor_y_top - actor_box_h, lifeline_y_bot],
            color=color, lw=1.2, ls='--', alpha=0.5, zorder=1)

# (from_x, to_x, y, label, is_return)
messages = [
    (1.0, 3.5, 8.0, 'Madde metnini gönder',          False),
    (3.5, 1.0, 7.2, 'Vektör döndür\n(embedding)',     True),
    (1.0, 6.0, 6.4, 'Cosine similarity sorgusu\n(top-k=5)', False),
    (6.0, 8.5, 5.6, 'Eşleşen kural ID\'leri',        False),
    (8.5, 6.0, 4.8, 'Kural metinleri döndür',         True),
    (6.0, 1.0, 4.0, 'En yakın Playbook kuralları\n(similarity > 0.75)', True),
    (1.0, 1.0, 3.1, 'Risk skoru hesapla\n(Düşük / Orta / Yüksek)', False),
]

for i, (x1, x2, y, label, is_ret) in enumerate(messages):
    color = '#888888' if is_ret else '#2C3E50'
    ls    = '--'      if is_ret else '-'

    if x1 == x2:  # self-message
        ax.annotate('', xy=(x1 + 0.55, y - 0.35), xytext=(x1 + 0.55, y),
                    arrowprops=dict(arrowstyle='->', color='#4A90D9',
                                   lw=1.6, mutation_scale=12))
        ax.plot([x1, x1 + 0.55, x1 + 0.55], [y, y, y - 0.35],
                color='#4A90D9', lw=1.6)
        ax.text(x1 + 0.65, y - 0.18, label,
                fontsize=7, ha='left', va='center', color='#4A90D9', zorder=5)
    else:
        ax.annotate('', xy=(x2, y), xytext=(x1, y),
                    arrowprops=dict(arrowstyle='->', color=color,
                                   lw=1.6, mutation_scale=12,
                                   linestyle=ls))
        mid_x = (x1 + x2) / 2
        ax.text(mid_x, y + 0.17, label,
                fontsize=7, ha='center', va='bottom',
                color=color, style='italic' if is_ret else 'normal', zorder=5)

# Activation boxes
activations = [
    (1.0, 8.3, 2.7, '#E74C3C'),
    (3.5, 8.3, 6.9, '#7B68EE'),
    (6.0, 6.7, 3.7, '#2ECC71'),
    (8.5, 5.9, 4.5, '#E67E22'),
]
for (x, y_top, y_bot, color) in activations:
    ax.add_patch(FancyBboxPatch((x - 0.12, y_bot), 0.24, y_top - y_bot,
                                boxstyle="square,pad=0",
                                linewidth=1, edgecolor=color,
                                facecolor=color, alpha=0.22, zorder=2))

# Output badge
ax.add_patch(FancyBboxPatch((1.8, 1.75), 6.4, 0.85,
                             boxstyle="round,pad=0.08",
                             linewidth=2, edgecolor='#27AE60',
                             facecolor='#27AE60', alpha=0.12, zorder=2))
ax.text(5.0, 2.42, 'Risk Raporu Çıktısı',
        fontsize=8.5, ha='center', va='center', color='#2C3E50',
        fontweight='bold', zorder=3)

# Risk level dots + labels, evenly spaced
risk_items = [
    (3.0,  '#27AE60', 'Düşük'),
    (5.0,  '#E67E22', 'Orta'),
    (7.0,  '#E74C3C', 'Yüksek'),
]
for rx, col, rlabel in risk_items:
    ax.plot(rx - 0.25, 2.0, 'o', color=col, markersize=9, zorder=4)
    ax.text(rx + 0.1, 2.0, rlabel, fontsize=8, ha='left', va='center',
            color=col, fontweight='bold', zorder=4)

ax.text(5.0, 9.72, 'Senaryo-4: RAG Hattı ve Risk Analizi',
        fontsize=12, fontweight='bold', ha='center', va='center', color='#2C3E50')

plt.tight_layout(pad=0.2)
plt.savefig('figures/fig_rag_sequence.png', dpi=180,
            bbox_inches='tight', facecolor='#FAFAFA')
print('Saved.')
