"""Regenerate assets/hero.png from the numbers in results/NUMBERS.md (no model run needed).

Usage: python results/make_hero.py   (requires matplotlib)
"""
from pathlib import Path

import matplotlib.pyplot as plt

# Key-frame density (% of original points, mean of 2 frames) -> mAP. See NUMBERS.md §1.
BASELINE = 0.2342
RANDOM = [(25.0, 0.2122), (50.0, 0.2156), (100.0, BASELINE)]
VOXEL = [(21.4, 0.2293, "grid 0.4"), (34.8, 0.2397, "grid 0.2"), (66.9, 0.2341, "grid 0.05")]

SURFACE, INK, INK2, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#e4e3df"
BLUE, ORANGE = "#2a78d6", "#eb6834"

plt.rcParams.update({"font.size": 11, "axes.edgecolor": INK2, "text.color": INK,
                     "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2})
fig, ax = plt.subplots(figsize=(8, 4.6), dpi=150, facecolor=SURFACE)
ax.set_facecolor(SURFACE)

ax.axhline(BASELINE, color=INK2, lw=1, ls=(0, (4, 3)), zorder=1)
ax.text(101, BASELINE + 0.0006, f"full density  {BASELINE:.4f}", color=INK2,
        ha="right", va="bottom", fontsize=9.5)

rx, ry = zip(*RANDOM)
ax.plot(rx, ry, color=BLUE, lw=2, marker="o", ms=8, mec=SURFACE, mew=2, zorder=3)
vx, vy, vl = zip(*VOXEL)
ax.plot(vx, vy, color=ORANGE, lw=2, marker="s", ms=8, mec=SURFACE, mew=2, zorder=3)
ax.plot([vx[-1], 100], [vy[-1], BASELINE], color=ORANGE, lw=1, ls=":", zorder=2)

for x, y in RANDOM[:2]:
    ax.annotate(f"{y:.4f}", (x, y), xytext=(0, -16), textcoords="offset points",
                ha="center", color=INK, fontsize=9.5)
for x, y, lab in VOXEL:
    below = lab == "grid 0.4"
    ax.annotate(f"{y:.4f}\n{lab}", (x, y), xytext=(0, -12 if below else 10),
                textcoords="offset points", ha="center", va="top" if below else "bottom",
                color=INK, fontsize=9.5)

ax.text(72, 0.2195, "Random sampling", color=INK, fontsize=10.5, fontweight="bold")
ax.plot([69.5], [0.2199], marker="o", color=BLUE, ms=7)
ax.text(52, 0.2255, "Voxel-grid sampling", color=INK, fontsize=10.5, fontweight="bold")
ax.plot([48.5], [0.2259], marker="s", color=ORANGE, ms=7)

ax.set_xlim(15, 105)
ax.set_ylim(0.205, 0.246)
ax.set_xlabel("Key-frame points kept (% of original, mean of 2 frames)")
ax.set_ylabel("nuScenes mAP")
ax.set_title("PointPillars mAP vs. point density — sampling method matters more than point count",
             loc="left", fontsize=11.5, color=INK, pad=12)
ax.grid(axis="y", color=GRID, lw=0.8)
ax.set_axisbelow(True)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
fig.text(0.01, 0.01, "N = 2 nuScenes-mini key frames, 1 run per condition. Values: report.pdf Fig. 1.",
         color=INK2, fontsize=8.5)
fig.tight_layout(rect=(0, 0.03, 1, 1))

out = Path(__file__).resolve().parents[1] / "assets" / "hero.png"
out.parent.mkdir(exist_ok=True)
fig.savefig(out, facecolor=SURFACE)
print(out)
