# CV bullet

- Led a 3-person course project on LiDAR point-density vs. 3D detection accuracy. Built the down/upsampling pipeline (random, voxel-grid, Gaussian jitter, voxel interpolation) and evaluated a pretrained PointPillars on nuScenes-mini (2 frames). Found that detection is more sensitive to the sampling method than to raw point count: voxel-grid sampling to 21% of points held mAP at 0.229 (full density 0.234), while random sampling to 50% dropped it to 0.216.

Source for every number: `results/NUMBERS.md` §1 (N = 2 frames, 1 run per condition).
