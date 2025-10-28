import os
import shutil
from sklearn.model_selection import train_test_split

# Paths
images_dir = "datasets/images"
labels_dir = "datasets/labels"

output_base = "datasets"
train_img = os.path.join(output_base, "train/images")
train_lbl = os.path.join(output_base, "train/labels")
val_img = os.path.join(output_base, "valid/images")
val_lbl = os.path.join(output_base, "valid/labels")
test_img = os.path.join(output_base, "test/images")
test_lbl = os.path.join(output_base, "test/labels")

# Create output folders
for path in [train_img, train_lbl, val_img, val_lbl, test_img, test_lbl]:
    os.makedirs(path, exist_ok=True)

# Get all images
images = [f for f in os.listdir(images_dir) if f.endswith(('.jpg', '.png', '.jpeg'))]

# Split data
train_files, test_files = train_test_split(images, test_size=0.2, random_state=42)
val_files, test_files = train_test_split(test_files, test_size=0.5, random_state=42)

def move_files(file_list, target_img_dir, target_lbl_dir):
    for file in file_list:
        base = os.path.splitext(file)[0]
        src_img = os.path.join(images_dir, file)
        src_lbl = os.path.join(labels_dir, base + ".txt")

        if os.path.exists(src_img) and os.path.exists(src_lbl):
            shutil.copy(src_img, target_img_dir)
            shutil.copy(src_lbl, target_lbl_dir)

# Move files
move_files(train_files, train_img, train_lbl)
move_files(val_files, val_img, val_lbl)
move_files(test_files, test_img, test_lbl)

print("✅ Dataset successfully split into train/valid/test!")
