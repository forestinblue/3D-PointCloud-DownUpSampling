import numpy as np

def read_bin_file(file_path, dim):
    point_cloud = np.fromfile(file_path, dtype=np.float32)
    point_cloud = point_cloud.reshape(-1, dim)

    return point_cloud

origin_pc = read_bin_file('/mnt/ssd1/yaojunguang/WorkSpace/3d_object_detection/data/nus/bin/original_bin/n015-2018-07-24-11-22-45+0800__LIDAR_TOP__1532402937198682.pcd.bin', 5)
voxel_pc = read_bin_file('/mnt/ssd1/yaojunguang/WorkSpace/3d_object_detection/data/nus/bin/downsampled_bin/Voxel_25/n015-2018-07-24-11-22-45+0800__LIDAR_TOP__1532402937198682.pcd.bin', 4)


def pc_concate(origin_pc, voxel_pc):
    num_pc = voxel_pc.shape[0]

    for i in range(num_pc):
        voxel_point = voxel_pc[i, :]
        print(voxel_point)
        idx = np.where(np.abs(origin_pc[:, 0] - voxel_point[0]) <= 0)

def voxel_downsample(origin_pc, r):
    x = origin_pc[:, 0]
    y = origin_pc[:, 1]
    z = origin_pc[:, 2]

    xmin, xmax = np.min(x), np.max(x)
    ymin, ymax = np.min(y), np.max(y)
    zmin, zmax = np.min(z), np.max(z)

    Dx = (xmax - xmin) / r
    Dy = (ymax - ymin) / r
    Dz = (zmax - zmin) / r
    print(Dx, Dy, Dz)
    hx = np.floor((x - xmin) / r)
    hy = np.floor((y - ymin) / r)
    hz = np.floor((z - zmin) / r)

    h = hx + hy * Dx + hz * Dx * Dy
    h_sort = np.argsort(h)
    hx_sort = np.argsort(hx)
    print(h_sort)
    print(hx_sort)



# print(origin_pc.shape, voxel_pc.shape)
# print(voxel_pc[0, :])
# print(np.where(origin_pc[:, 0] == 8.625057))
# print(origin_pc[19182, :])
voxel_downsample(origin_pc, 0.25)

