# 3D-PointCloud-DownUpSampling

Exploring the impact of **point cloud density** on **3D object detection performance** using various **downsampling** and **upsampling** techniques.

---

## 📌 Overview
This project investigates how adjusting LiDAR point cloud density influences the accuracy and efficiency of 3D object detection models.  
We implemented and compared multiple **downsampling** and **upsampling** algorithms, and evaluated their effect on the **PointPillars** model using the **nuScenes v1.0-mini** dataset.

The findings provide practical insights for real-time autonomous driving, robotics, and AI vision applications.

---

## 🎯 Objectives
- Analyze the trade-off between **detection accuracy (mAP)** and **processing efficiency**.
- Compare different **downsampling** methods:
  - Random Sampling
  - Voxel Grid Downsampling
- Compare different **upsampling** methods:
  - Gaussian Jittering
  - Voxel Interpolation
- Identify optimal parameters (e.g., voxel size) for performance gains.

---

## 🛠 Methods

### **1. Downsampling**
- **Random Sampling**: Uniform random selection of points.
- **Voxel Grid Downsampling**: Group points into voxels and keep one representative point per voxel.

### **2. Upsampling**
- **Gaussian Jittering**: Duplicate points and add Gaussian noise.
- **Voxel Interpolation**: Generate new points as the mean of points within the same voxel.

---

## 📊 Experiments
- **Model**: PointPillars (pretrained on nuScenes)
- **Dataset**: nuScenes v1.0-mini (2 selected scenes)
- **Metrics**: mAP (mean Average Precision)

### **Results Summary**
| Method                  | Key Parameter | mAP    | Notes |
|-------------------------|--------------|--------|-------|
| Full density (baseline) | -            | 0.2342 | -     |
| Voxel Downsampling      | voxel=0.2    | 0.2397 | Improved accuracy |
| Random Downsampling     | 50% ratio    | ↓      | Performance drop |
| Gaussian Jittering      | std=0.01     | ↓      | Partial recovery |
| Voxel Interpolation     | voxel=0.4    | ↓      | Performance drop |

---
## 📂 Repository Structure
3D-PointCloud-DownUpSampling/
│
├── 3d_object_detection/ # Core implementation & configs
├── Programming/ # Additional scripts & notebooks
├── Upsampling_DownSampling.ipynb # Jupyter notebook for testing
├── Readme.pdf # Setup & usage instructions
├── report.pdf # Final project report
├── .gitignore
└── README.md

---

## 🚀 Getting Started

### **1. Clone the repository**
```bash
git clone https://github.com/forestinblue/3D-PointCloud-DownUpSampling.git
cd 3D-PointCloud-DownUpSampling
```
### **2. Install dependencies
Follow the MMDetection3D installation guide
Example:
```bash

conda create -n mmdet3d python=3.8 -y
conda activate mmdet3d
pip install -r requirements.txt
```

### **3. Prepare dataset
Download nuScenes v1.0-mini
Update dataset paths in scripts as described in Readme.pdf
### **4. Run evaluation
python tools/test.py configs/pointpillars_nuscenes.py \
    checkpoints/pointpillars_nuscenes.pth \
    --eval mAP
## 👤 Author & Contribution
Jun Seok Kim – Team Leader, Research Lead, Data Processing Pipeline Developer
Responsibilities:

Proposed research topic and led project planning.
Implemented all downsampling and upsampling algorithms.
Managed dataset preparation and preprocessing.
Co-authored report and delivered presentation.
## 📄 License
This project is released under the MIT License.
## 📚 References
MMDetection3D
Caesar, H., et al. nuScenes: A multimodal dataset for autonomous driving.
Lang, A. H., et al. PointPillars: Fast encoders for object detection from point clouds.
