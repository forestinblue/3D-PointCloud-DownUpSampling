
from nuscenes.nuscenes import NuScenes
import os

# 设置 nuScenes 数据集
nusc = NuScenes(version='v1.0-mini', dataroot='/mnt/ssd1/yaojunguang/WorkSpace/3d_object_detection/data/nus/v1.0-mini', verbose=False)

# 选定的 LIDAR_TOP 文件名
target_filenames = [
    'samples/LIDAR_TOP/n015-2018-07-24-11-22-45+0800__LIDAR_TOP__1532402937198682.pcd.bin',
    'samples/LIDAR_TOP/n008-2018-08-01-15-16-36-0400__LIDAR_TOP__1533151613398020.pcd.bin'
]

for filename in target_filenames:
    print(f"\n 正在检查注释文件: {filename}")

    # 查找对应的 sample_data 对象
    sample_data = next(sd for sd in nusc.sample_data if sd['filename'] == filename)
    sample_token = sample_data['sample_token']

    # 获取 sample 对象
    sample = nusc.get('sample', sample_token)

    # 获取注释（annotation）
    ann_tokens = sample['anns']
    print(f"共有 {len(ann_tokens)} 个目标对象:")

    for ann_token in ann_tokens:
        ann = nusc.get('sample_annotation', ann_token)
        name = ann['category_name']
        translation = ann['translation']
        size = ann['size']
        yaw = ann['rotation']
        print(f" 类别: {name} | 位置: {translation[:2]} | 尺寸: {size} | 旋转: {yaw}")