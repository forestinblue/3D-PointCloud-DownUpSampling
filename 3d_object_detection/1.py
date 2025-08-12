from nuscenes.nuscenes import NuScenes
nusc = NuScenes(version='v1.0-trainval', dataroot='/mnt/ssd1/yaojunguang/WorkSpace/3d_object_detection/data/nuscenes/')

# 根据时间戳找到样本
sample_token = nusc.field2token('sample', 'timestamp', 1532402937198682)[0]
# sample_token = nusc.field2token('sample', 'timestamp', 1533151613398020)[0]
sample = nusc.get('sample', sample_token)

# 获取标注
ann_tokens = sample['anns']
print(ann_tokens)
targets = [nusc.get('sample_annotation', t) for t in ann_tokens]
valid_targets = [t for t in targets if t['num_lidar_pts'] > 0]
# valid_targets = [t for t in targets]
print(valid_targets)
print(f"有效目标数量: {len(valid_targets)}")  # 输出 23