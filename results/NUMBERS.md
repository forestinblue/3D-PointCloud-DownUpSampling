# Numbers — source of truth for README / RESULTS.md

**Setting (applies to every number below):** PointPillars (MMDetection3D config
`pointpillars_hv_secfpn_sbn-all_8xb4-2x_nus-3d`, nuScenes-pretrained, inference only, no retraining);
nuScenes v1.0-mini; density was modified on **N = 2 LIDAR_TOP key frames**
(scene-0061 `…1532402937198682`, scene-0103 `…1533151613398020`); metric = nuScenes mAP;
**single run per condition, no seeds / repeats**. No latency or memory was measured.

## 1. Downsampling (mAP)

Source: `report.pdf` p.5, Figure 1 (embedded image; values read verbatim from bar labels).
Point counts: `3d_object_detection/downsampled_bin/*` (file size / 20 bytes = float32 × 5),
also printed in `Upsanpling_DownSampling.ipynb` cell 16. Voxel folder ↔ grid size mapping
from notebook cell 16 (`voxel_sizes = {1.0: 0.05, 0.5: 0.2, 0.25: 0.4}`).

| Condition (figure label) | Folder | Points s-0061 / s-0103 | Key-frame density (mean of 2) | mAP |
|---|---|---|---|---|
| original | `RS_100` | 34,688 / 34,752 | 100% | **0.2342** |
| RS_25 (random 25%) | `RS_25` | 8,672 / 8,688 | 25.0% | 0.2122 |
| RS_50 (random 50%) | `RS_50` | 17,344 / 17,376 | 50.0% | 0.2156 |
| Voxel_0.4 | `Voxel_25` | 7,630 / 7,228 | 21.4% | 0.2293 |
| Voxel_0.2 | `Voxel_50` | 11,675 / 12,522 | 34.8% | **0.2397** |
| Voxel_0.05 | `Voxel_100` | 22,282 / 24,160 | 66.9% | 0.2341 |

## 2. Upsampling back to 100% (mAP)

Source: `report.pdf` p.6, Figure 2 (embedded image; verbatim). Target point count 34,688 for
both frames (notebook cell 19). GJ = Gaussian jittering σ = 0.02 (cell 19 call; the cell 18 function default is 0.01);
VI = voxel interpolation, voxel 0.4 per report §3 (function default in notebook is 0.5; the
call site for RS inputs is truncated in the notebook, so 0.4 is taken from the report).

| Condition | Input | mAP |
|---|---|---|
| original | — | 0.2342 |
| RS25_to100_GJ | RS_25 (0.2122) | 0.2153 |
| RS25_to100_VI | RS_25 (0.2122) | 0.2110 |
| RS50_to100_GJ | RS_50 (0.2156) | 0.2232 |
| RS50_to100_VI | RS_50 (0.2156) | 0.2193 |

## 3. Raw evaluation logs in the repo

Source: `3d_object_detection/results/<timestamp>/<timestamp>.json` (29 run dirs, 23 with a
metrics JSON; `Programming/3d_object_detection/results/` is a duplicate copy).

| mAP | NDS | Runs | Matches figure value |
|---|---|---|---|
| 0.2342 | 0.2727 | 17 runs (20250718_213454 … 20250724_224834) | original |
| 0.2341 | 0.2726 | 20250718_144839, _193139, _195822 | original or Voxel_0.05 (ambiguous) |
| 0.2156 | 0.2487 | 20250718_195950 | RS_50 |
| 0.2284 | 0.2687 | 20250718_195912 | none (Figure 1 has Voxel_0.4 = 0.2293) |
| 0.1369 | 0.2059 | 20250724_224733 | none |

**Traceability limits — read before quoting any number:**
- Every saved config is identical and points at the stock `samples/LIDAR_TOP` +
  `nuscenes_infos_val.pkl`, so the logs do not record *which* modified point cloud a run used.
  Runs were executed on a teammate's server (`/mnt/ssd1/yaojunguang/...`).
- 0.2397 (Voxel_0.2), 0.2122, 0.2293 and all four upsampling values exist **only** in the report
  figures, not in any log in the repo.
- The eval pipeline uses `LoadPointsFromMultiSweeps(sweeps_num=10)` with the unmodified
  `sweeps/LIDAR_TOP`. If this config was used for the density runs, only the key frame was
  down/up-sampled and ~9 prior sweeps entered at full density — the *effective* input density
  change is much smaller than the key-frame % above.
- In the official v1.0-mini split, scene-0061 is in *train* and scene-0103 is in *val*;
  how the 2 frames were isolated for mAP is not recorded.
- Differences of ~0.005 mAP (e.g. 0.2397 vs 0.2342) are within what a single run on 2 frames
  can move by chance; treat them as "no measurable loss", not "improvement".
