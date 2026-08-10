import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(6, 9))
fig.patch.set_facecolor('#FAFAFA')
ax.set_facecolor('#FAFAFA')
ax.set_aspect('equal')

labels  = ['Yüksek (Major)', 'Orta (Medium)', 'Düşük (Minor)']
sizes   = [2, 3, 7]
colors  = ['#E74C3C', '#E67E22', '#3498DB']
explode = (0.05, 0.05, 0.05)

wedges, texts, autotexts = ax.pie(
    sizes,
    labels=None,
    autopct='%1.0f%%',
    startangle=140,
    colors=colors,
    explode=explode,
    pctdistance=0.72,
    wedgeprops=dict(linewidth=2, edgecolor='white'),
)

for at in autotexts:
    at.set_fontsize(13)
    at.set_fontweight('bold')
    at.set_color('white')

# Legend with counts
legend_labels = [f'{l}  ({s} hata)' for l, s in zip(labels, sizes)]
ax.legend(wedges, legend_labels,
          loc='lower center',
          bbox_to_anchor=(0.5, -0.18),
          fontsize=11,
          framealpha=0.7,
          edgecolor='#CCCCCC')

# Center annotation
ax.text(0, 0, '12\nhata', ha='center', va='center',
        fontsize=14, fontweight='bold', color='#2C3E50')

ax.set_title('Hata Kritiklik Seviyelerine Göre Dağılım\n(Blocker: 0  —  Tüm Kritik Hatalar Giderildi)',
             fontsize=12, fontweight='bold', color='#2C3E50', pad=18)

plt.tight_layout(pad=1.5)
plt.savefig('figures/fig_bug_distribution.png', dpi=180,
            bbox_inches='tight', facecolor='#FAFAFA')
print('Saved.')
