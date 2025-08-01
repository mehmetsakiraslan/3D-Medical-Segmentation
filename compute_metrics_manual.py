#!/usr/bin/env python3

import argparse
import nibabel as nib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def main():
    p = argparse.ArgumentParser(
        description="Compute cell volumes from a 3D mask without modifying or saving the mask."
    )

    p.add_argument("-i", "--input-mask", required=True, help="Path to input .nii.gz mask")
    p.add_argument("-m", "--min-size", type=int, default=0, help="Minimum voxel count to include in report (default: 0)")

    args = p.parse_args()

    # Load mask image
    img = nib.load(args.input_mask)
    mask = img.get_fdata().astype(np.int32)
    voxel_vol = np.prod(img.header.get_zooms())

    # Get unique non-zero labels
    labels = np.unique(mask)
    labels = labels[labels != 0]

    records = []
    for label in labels:
        cnt = np.sum(mask == label)
        if cnt < args.min_size:
            continue
        vol = cnt * voxel_vol
        records.append({
            "label": label,
            "voxel_count": cnt,
            "volume": vol
        })

    df = pd.DataFrame(records)

    print(f"Found {len(df)} cells with ≥ {args.min_size} voxels.")
    print(df["volume"].describe(), "\n")

    # Plot histogram
    plt.figure()
    plt.hist(df["volume"], bins='auto')
    plt.xlabel("Cell Volume (voxel_units)")
    plt.ylabel("Count")
    plt.title("Histogram of Cell Volumes")
    plt.tight_layout()
    plt.savefig("cell_volume_histogram.png")
    print("Saved histogram to cell_volume_histogram.png")

if __name__ == "__main__":
    main()
