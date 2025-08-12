import open3d as o3d
import numpy as np


import os
import numpy as np
from open3d import *


points = np.random.rand(10000, 3)
point_cloud = PointCloud()
point_cloud.points = Vector3dVector(points)
draw_geometries([point_cloud])