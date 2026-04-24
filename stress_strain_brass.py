import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

df = pd.read_csv('LA4_brass.csv')
position = np.abs(df['Position (m) Run #1'])
force = np.abs(df['Force (N) Run #1'])

A0 = 8.553e-6
L0 = 33.5e-3
preload = force.iloc[0]

strain = (position / L0).values
stress = ((force + preload) / A0 / 1e6).values  


limit = int(len(strain) * 0.05)
coeffs = np.polyfit(strain[:limit], stress[:limit], 1)
E = coeffs[0]

offset_stress = E * (strain - 0.002)
diff = stress - offset_stress
sign_changes = np.where(np.diff(np.sign(diff)))[0]
yi = sign_changes[0]
yield_strain, yield_stress = strain[yi], stress[yi]


peak_idx = np.argmax(stress)
uts_strain, uts_stress = strain[peak_idx], stress[peak_idx]
frac_strain, frac_stress = strain[-1], stress[-1]


fig, ax = plt.subplots(figsize=(12, 7))
fig.patch.set_facecolor('#f9f9f9')
ax.set_facecolor('#f9f9f9')

ax.plot(strain, stress, color='#1a3a6b', linewidth=2.0, zorder=3)


ax.axvspan(0, yield_strain, alpha=0.15, color='#2ecc71', zorder=1)
ax.axvspan(yield_strain, uts_strain, alpha=0.15, color='#f39c12', zorder=1)
ax.axvspan(uts_strain, frac_strain, alpha=0.15, color='#e74c3c', zorder=1)


ax.plot(yield_strain, yield_stress, 'o', color='#27ae60', markersize=5, zorder=5)
ax.annotate(f'Yield Point\n({yield_strain:.4f}, {yield_stress:.1f} MPa)',
            xy=(yield_strain, yield_stress),
            xytext=(yield_strain + 0.008, yield_stress - 60),
            fontsize=9, color='#27ae60', fontweight='bold',
            arrowprops=dict(arrowstyle='->', color='#27ae60', lw=1.5))


ax.plot(uts_strain, uts_stress, 's', color='#e67e22', markersize=9, zorder=5)
ax.annotate(f'Ultimate Tensile Strength (UTS)\n({uts_strain:.4f}, {uts_stress:.1f} MPa)',
            xy=(uts_strain, uts_stress),
            xytext=(uts_strain - 0.04, uts_stress + 25),
            fontsize=9, color='#e67e22', fontweight='bold',
            arrowprops=dict(arrowstyle='->', color='#e67e22', lw=1.5))

 
ax.plot(frac_strain, frac_stress, 'X', color='#c0392b', markersize=12, zorder=5)
ax.annotate(f'Fracture Point\n({frac_strain:.4f}, {frac_stress:.1f} MPa)',
            xy=(frac_strain, frac_stress),
            xytext=(frac_strain - 0.03, frac_stress + 70),
            fontsize=9, color='#c0392b', fontweight='bold',
            arrowprops=dict(arrowstyle='->', color='#c0392b', lw=1.5))

ax.text(yield_strain / 2, stress.max() * 0.70, 'Elastic\nDeformation',
        ha='center', va='center', fontsize=9, color='#1a7a44', style='italic',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.6))

mid_sh = (yield_strain + uts_strain) / 2
ax.text(mid_sh, stress.max() * 0.30, 'Plastic Deformation\n(Strain Hardening)',
        ha='center', va='center', fontsize=9, color='#b7600a', style='italic',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.6))

mid_neck = (uts_strain + frac_strain) / 2
ax.text(mid_neck, stress.max() * 0.30, 'Plastic Deformation\n(Necking)',
        ha='center', va='center', fontsize=9, color='#922b21', style='italic',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.6))


ax.set_title('Engineering Stress–Strain Curve', fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel('Engineering Strain  ε  (dimensionless)', fontsize=12)
ax.set_ylabel('Engineering Stress  σ  (MPa)', fontsize=12)
ax.set_xlim(-0.002, frac_strain * 1.06)
ax.set_ylim(-10, stress.max() * 1.15)
ax.grid(True, linestyle=':', alpha=0.5, color='gray')
ax.axhline(0, color='black', linewidth=0.8)
ax.axvline(0, color='black', linewidth=0.8)


handles = [
    mpatches.Patch(color='#2ecc71', alpha=0.5, label='Elastic Region'),
    mpatches.Patch(color='#f39c12', alpha=0.5, label='Strain Hardening Region'),
    mpatches.Patch(color='#e74c3c', alpha=0.5, label='Necking Region'),
    plt.Line2D([0],[0], marker='o', color='w', markerfacecolor='#27ae60', markersize=9, label='Yield Point'),
    plt.Line2D([0],[0], marker='s', color='w', markerfacecolor='#e67e22', markersize=9, label='UTS'),
    plt.Line2D([0],[0], marker='X', color='w', markerfacecolor='#c0392b', markersize=9, label='Fracture Point'),
]
ax.legend(handles=handles, 
          loc='upper left', 
          bbox_to_anchor=(0.02, 0.98), 
          ncol=2,           
          fontsize=7,     
          columnspacing=0.8) 
plt.tight_layout()
plt.savefig('stress_strain_brass.png', dpi=150, bbox_inches='tight')
plt.show()
