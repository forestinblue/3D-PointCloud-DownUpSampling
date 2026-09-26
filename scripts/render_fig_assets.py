"""Render the four bird's-eye-view panels for the hero figure into assets/fig_src/.

Frame: nuScenes-mini scene-0103 LIDAR_TOP key frame (…1533151613398020), one of the two
pilot frames in results/NUMBERS.md. Inputs are the stored resampled files in
3d_object_detection/downsampled_bin/. The upsampled panel is regenerated here because no
upsampled file is stored in the repo: same function as notebook cell 18, same call as
cell 19 (target 34,688 points, std=0.02), fixed seed. It is therefore a faithful re-run of
the method, not the exact file that was evaluated. PointPillars is not run.

Usage: python scripts/render_fig_assets.py   (numpy + matplotlib)
Writes only assets/fig_src/bev_*.png — never assets/hero.png.
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

ROOT = Path(__file__).resolve().parents[1]
BIN = ROOT / "3d_object_detection" / "downsampled_bin"
OUT = ROOT / "assets" / "fig_src"

EXTENT = 40.0            # metres, square window centred on the sensor (same for all panels)
Z_RANGE = (-2.0, 1.0)    # colour clip, sensor frame (ground ≈ -1.8 m)
PX = 600                 # panel size; shown at 300 px on a 1400 px canvas (2x export)
DPI = 200
POINT_SIZE = 0.35        # scatter size in pt^2, identical for all panels
LABEL_PX = 30            # 30 px here = 15 px on the 1400 px canvas
SEED = 0

GREY_TEXT = "#222222"
CMAP = LinearSegmentedColormap.from_list("grey_accent", ["#b4b4b4", "#1f4e79"])
plt.rcParams["font.family"] = ["Helvetica", "Arial", "DejaVu Sans"]


def load_bin(path):
    return np.fromfile(path, dtype=np.float32).reshape(-1, 5)


# Verbatim from Upsanpling_DownSampling.ipynb cell 18.
def upsample_gaussian_jittering(points: np.ndarray, target_num_points: int, std=0.01) -> np.ndarray:
    current_num = len(points)
    assert target_num_points > current_num, "Target must be greater than current number of points"
    dup_num = target_num_points - current_num
    dup_indices = np.random.choice(current_num, size=dup_num, replace=True)
    dup_points = points[dup_indices].copy()
    noise = np.random.normal(scale=std, size=(dup_num, 3))
    dup_points[:, :3] += noise
    upsampled = np.vstack([points, dup_points])
    return upsampled


def render(points, n_keyframe, out_path):
    fig = plt.figure(figsize=(PX / DPI, PX / DPI), dpi=DPI)
    ax = fig.add_axes([0, 0, 1, 1])
    order = np.argsort(points[:, 2])  # draw high points last so objects stay visible
    p = points[order]
    ax.scatter(p[:, 0], p[:, 1], c=np.clip(p[:, 2], *Z_RANGE), cmap=CMAP,
               vmin=Z_RANGE[0], vmax=Z_RANGE[1], s=POINT_SIZE, marker="o", linewidths=0)
    ax.set_xlim(-EXTENT, EXTENT)
    ax.set_ylim(-EXTENT, EXTENT)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ax.spines.values():
        s.set_edgecolor("#595959")
        s.set_linewidth(4 * 72 / DPI)  # 4 px here = 2 px on canvas

    fs = LABEL_PX * 72 / DPI
    in_win = (np.abs(points[:, 0]) <= EXTENT) & (np.abs(points[:, 1]) <= EXTENT)
    ax.text(0.03, 0.97, f"{len(points):,} pts", transform=ax.transAxes, ha="left", va="top",
            fontsize=fs, color=GREY_TEXT,
            bbox=dict(facecolor="white", edgecolor="none", pad=2, alpha=0.85))
    # 20 m scale bar, bottom-left
    x0, y0 = -EXTENT + 3, -EXTENT + 4
    ax.plot([x0, x0 + 20], [y0, y0], color=GREY_TEXT, linewidth=6 * 72 / DPI, solid_capstyle="butt")
    ax.text(x0 + 10, y0 + 1.2, "20 m", ha="center", va="bottom", fontsize=fs, color=GREY_TEXT)
    ax.plot(0, 0, marker="^", color=GREY_TEXT, markersize=5)  # sensor position
    fig.savefig(out_path, dpi=DPI, facecolor="white")
    plt.close(fig)
    return len(points), len(points) / n_keyframe, int(in_win.sum())


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    np.random.seed(SEED)
    original = load_bin(BIN / "RS_100" / "scene-0103_RS100.bin")
    voxel = load_bin(BIN / "Voxel_25" / "n008-2018-08-01-15-16-36-0400__LIDAR_TOP__1533151613398020.pcd.bin")
    rs50 = load_bin(BIN / "RS_50" / "scene-0103_RS50.bin")
    rs50_up = upsample_gaussian_jittering(rs50, 34688, std=0.02)  # cell 19 call

    n = len(original)
    panels = [
        ("bev_1_original.png", original),
        ("bev_2_voxel21.png", voxel),
        ("bev_3_random50.png", rs50),
        ("bev_4_random50_up.png", rs50_up),
    ]
    for name, pts in panels:
        count, frac, in_win = render(pts, n, OUT / name)
        print(f"{name:26s} {count:6,d} pts  {100 * frac:5.1f}% of keyframe points  ({in_win:,} inside ±{EXTENT:.0f} m)")


if __name__ == "__main__":
    main()
