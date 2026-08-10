import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib.patheffects as pe

fig, ax = plt.subplots(figsize=(6, 9))
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis('off')
fig.patch.set_facecolor('#FAFAFA')

# Actors (columns)
actors = [
    (1.0,  'Kullanıcı',  '#2C3E50'),
    (3.5,  'FastAPI',    '#4A90D9'),
    (6.0,  'MinIO',      '#2ECC71'),
    (8.5,  'OCR\nMotoru','#E67E22'),
]

actor_y_top    = 9.0
actor_box_h    = 0.55
lifeline_y_bot = 0.8

# Draw actor boxes and lifelines
for x, name, color in actors:
    ax.add_patch(FancyBboxPatch((x - 0.65, actor_y_top - actor_box_h),
                                1.3, actor_box_h,
                                boxstyle="round,pad=0.06",
                                linewidth=1.8, edgecolor=color,
                                facecolor=color, alpha=0.85, zorder=3))
    ax.text(x, actor_y_top - actor_box_h / 2, name,
            fontsize=8, fontweight='bold', ha='center', va='center',
            color='white', zorder=4)
    ax.plot([x, x], [actor_y_top - actor_box_h, lifeline_y_bot],
            color=color, lw=1.2, ls='--', alpha=0.5, zorder=1)

# Messages: (from_x, to_x, y, label, is_return)
messages = [
    (1.0, 3.5, 8.1, 'POST /upload\n(PDF/DOCX)',              False),
    (3.5, 1.0, 7.3, '422 Invalid File Type\n(hatalı format)', True),
    (3.5, 6.0, 6.5, 'Dosyayı aktar\n(contracts bucket)',     False),
    (6.0, 3.5, 5.7, '200 OK\n(MinIO path)',                  True),
    (3.5, 8.5, 4.9, 'OCR isteği gönder\n(image-based PDF)',  False),
    (8.5, 3.5, 4.1, 'Ham metin döndür\n(plain text)',        True),
    (3.5, 1.0, 3.3, '200 OK\n(analiz hazır)',                True),
]

for (x1, x2, y, label, is_ret) in messages:
    color  = '#888888' if is_ret else '#2C3E50'
    ls     = '--'      if is_ret else '-'
    dx     = x2 - x1
    ax.annotate('', xy=(x2, y), xytext=(x1, y),
                arrowprops=dict(arrowstyle='->', color=color,
                                lw=1.6, mutation_scale=12,
                                linestyle=ls))
    mid_x = (x1 + x2) / 2
    offset = 0.18
    ax.text(mid_x, y + offset, label,
            fontsize=7.2, ha='center', va='bottom',
            color=color, style='italic' if is_ret else 'normal',
            zorder=5)

# Activation boxes on lifelines
activations = [
    (3.5, 7.8, 2.9, '#4A90D9'),
    (6.0, 6.8, 5.3, '#2ECC71'),
    (8.5, 5.2, 3.7, '#E67E22'),
]
for (x, y_top, y_bot, color) in activations:
    ax.add_patch(FancyBboxPatch((x - 0.12, y_bot), 0.24, y_top - y_bot,
                                boxstyle="square,pad=0",
                                linewidth=1, edgecolor=color,
                                facecolor=color, alpha=0.25, zorder=2))

# Title
ax.text(5.0, 9.72, 'Senaryo-2: Doküman Yükleme Akışı',
        fontsize=12, fontweight='bold', ha='center', va='center', color='#2C3E50')

plt.tight_layout(pad=0.2)
plt.savefig('figures/fig_upload_sequence.png', dpi=180,
            bbox_inches='tight', facecolor='#FAFAFA')
print('Saved.')
