import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(figsize=(6, 9))
fig.patch.set_facecolor('#FAFAFA')
ax.set_facecolor('#FAFAFA')

categories = [
    'Birim\n(Backend)',
    'Birim\n(Frontend)',
    'Entegrasyon',
    'E2E / UAT',
]
basarili  = [43, 19, 11, 7]
basarisiz = [2,  1,  1,  1]

x     = np.arange(len(categories))
width = 0.38

bars1 = ax.bar(x - width/2, basarili,  width, label='Başarılı',  color='#2ECC71', alpha=0.85, zorder=3)
bars2 = ax.bar(x + width/2, basarisiz, width, label='Başarısız', color='#E74C3C', alpha=0.85, zorder=3)

# Value labels on bars
for bar in bars1:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.4,
            str(int(bar.get_height())),
            ha='center', va='bottom', fontsize=11, fontweight='bold', color='#2ECC71')

for bar in bars2:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.4,
            str(int(bar.get_height())),
            ha='center', va='bottom', fontsize=11, fontweight='bold', color='#E74C3C')

ax.set_xticks(x)
ax.set_xticklabels(categories, fontsize=11)
ax.set_ylabel('Test Vakası Sayısı', fontsize=11)
ax.set_ylim(0, 52)
ax.yaxis.grid(True, linestyle='--', alpha=0.5, zorder=0)
ax.set_axisbelow(True)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

ax.legend(fontsize=11, loc='upper right',
          framealpha=0.7, edgecolor='#CCCCCC')

ax.set_title('Test Seviyelerine Göre Başarı/Başarısızlık Dağılımı',
             fontsize=13, fontweight='bold', color='#2C3E50', pad=16)

# Total annotation
total_pass = sum(basarili)
total_fail = sum(basarisiz)
ax.text(0.5, -0.13,
        f'Toplam: {total_pass + total_fail} vaka  |  Başarılı: {total_pass}  |  Başarısız: {total_fail}  |  Genel Oran: %94.1',
        transform=ax.transAxes, ha='center', fontsize=9,
        color='#555555', style='italic')

plt.tight_layout(pad=1.2)
plt.savefig('figures/fig_test_results_bar.png', dpi=180,
            bbox_inches='tight', facecolor='#FAFAFA')
print('Saved.')
