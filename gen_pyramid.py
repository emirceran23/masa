import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
import numpy as np

fig, ax = plt.subplots(figsize=(6, 9))
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis('off')
fig.patch.set_facecolor('#FAFAFA')

# Pyramid layers: (y_bottom, y_top, color, label, count, tool)
layers = [
    (0.6, 3.2, '#4A90D9', 'Birim Testleri',      '65 vaka', 'pytest · React Testing Library'),
    (3.5, 6.1, '#E67E22', 'Entegrasyon Testleri', '12 vaka', 'LangGraph · DB · MinIO'),
    (6.4, 8.8, '#E74C3C', 'E2E / UAT',            '8 vaka',  'Playwright'),
]

total_width = 8.0
margin_left = 1.0

for i, (y_bot, y_top, color, label, count, tool) in enumerate(layers):
    # Each higher layer is narrower
    shrink = i * 1.4
    x_left  = margin_left + shrink
    x_right = margin_left + total_width - shrink

    poly = Polygon([
        [x_left,  y_bot],
        [x_right, y_bot],
        [x_right - 0.6, y_top],
        [x_left  + 0.6, y_top],
    ], closed=True)

    p = PatchCollection([poly], facecolor=color, alpha=0.18,
                        edgecolor=color, linewidth=2.5, zorder=2)
    ax.add_collection(p)

    mid_y = (y_bot + y_top) / 2
    ax.text(5.0, mid_y + 0.38, label,
            fontsize=12, fontweight='bold', ha='center', va='center',
            color=color, zorder=3)
    ax.text(5.0, mid_y - 0.10, count,
            fontsize=11, fontweight='bold', ha='center', va='center',
            color=color, alpha=0.85, zorder=3)
    ax.text(5.0, mid_y - 0.55, tool,
            fontsize=8.5, ha='center', va='center',
            color='#555555', zorder=3)

# Divider lines
for i in range(1, len(layers)):
    shrink = i * 1.4
    x_left  = margin_left + shrink
    x_right = margin_left + total_width - shrink
    ax.plot([x_left, x_right], [layers[i][0] - 0.15, layers[i][0] - 0.15],
            color='#AAAAAA', lw=1.2, ls='--', zorder=1)

# Title
ax.text(5.0, 9.5, 'Lagent — Test Piramidi',
        fontsize=14, fontweight='bold', ha='center', va='center', color='#2C3E50')
ax.text(5.0, 9.05, 'Toplam: 85 test vakası',
        fontsize=9, ha='center', va='center', color='#666666')

# Bottom label
ax.text(5.0, 0.22, 'Hız: Yüksek  ·  Maliyet: Düşük',
        fontsize=8, ha='center', va='center', color='#888888', style='italic')

plt.tight_layout(pad=0.2)
plt.savefig('figures/fig_test_pyramid.png', dpi=180,
            bbox_inches='tight', facecolor='#FAFAFA')
print('Saved.')
