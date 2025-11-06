"""
filename: split_plantvillage_dataset.py

    function:
        - This script is used to split the PlantVillage dataset into training, validation, and test sets.
        - The split is going to be 80% training, 10% validation, and 10% test.
"""

import os
import shutil
import random
from pathlib import Path

SRC_COLOR = Path("PlantVillage/color")
SRC_SEG = Path("PlantVillage/segmented")
DEST = Path("data")
SPLITS = ["train", "valid", "test"]
RATIOS = [0.8, 0.1, 0.1]
random.seed(42)

def create_dir_structure(base, classes):
    for split in SPLITS:
        for cls in classes:
            (base / "color" / split / cls).mkdir(parents=True, exist_ok=True)
            (base / "segmented" / split / cls).mkdir(parents=True, exist_ok=True)

def split_dataset():
    classes = [d.name for d in SRC_COLOR.iterdir() if d.is_dir()]
    create_dir_structure(DEST, classes)

    for cls in classes:
        color_files = list((SRC_COLOR / cls).glob("*.jpg"))
        random.shuffle(color_files)

        n = len(color_files)
        n_train = int(n * RATIOS[0])
        n_valid = int(n * RATIOS[1])

        splits = {
            "train": color_files[:n_train],
            "valid": color_files[n_train:n_train + n_valid],
            "test": color_files[n_train + n_valid:],
        }

        for split_name, files in splits.items():
            for f in files:
                seg_file = SRC_SEG / cls / f.name
                if not seg_file.exists():
                    continue  # skip missing pair

                shutil.copy2(f, DEST / "color" / split_name / cls / f.name)
                shutil.copy2(seg_file, DEST / "segmented" / split_name / cls / f.name)

        print(f"{cls}: {n} images split.")

if __name__ == "__main__":
    split_dataset()
    print("✅ Dataset split complete.")