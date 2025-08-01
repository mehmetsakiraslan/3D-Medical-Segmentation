#!/usr/bin/env python3

import argparse

import nibabel as nib

import numpy as np

import pandas as pd

import matplotlib.pyplot as plt
 
def main():

    p = argparse.ArgumentParser(

        description="Re-label a 3D mask to consecutive IDs, drop small objects, compute volumes, save CSV stats, and plot histogram."

    )

    p.add_argument("-i", "--input-mask",   required=True, help="Path to input .nii.gz mask")
    p.add_argument("-o", "--output-mask",  required=True, help="Path to write reordered mask (.nii.gz)")
    p.add_argument("-v", "--volumes-csv",  required=True, help="Path to write per-cell volumes CSV")
    p.add_argument("-s", "--summary-csv",  required=True, help="Path to write summary stats CSV")
    p.add_argument("-m", "--min-size",     type=int, default=400,help="Minimum voxel count to keep a cell (default: 400)")

    args = p.parse_args()
 
    # Load image & compute voxel volume

    img = nib.load(args.input_mask)

    mask = img.get_fdata().astype(np.int32)

    voxel_vol = np.prod(img.header.get_zooms())
 
    # Find and sort labels (exclude background)

    labels = np.unique(mask)

    labels = labels[labels != 0]

    labels_sorted = np.sort(labels)
 
    # Map to new consecutive IDs

    mapping = {old: new for new, old in enumerate(labels_sorted, start=1)}
 
    # Build initial relabeled mask

    temp_mask = np.zeros_like(mask)

    for old, new in mapping.items():

        temp_mask[mask == old] = new
 
    # Compute per-cell voxel counts

    counts = {new: int((temp_mask == new).sum()) for new in mapping.values()}
 
    # Filter out small objects

    keep_labels = {new for new, cnt in counts.items() if cnt >= args.min_size}
 
    # Build final mask with gaps closed (1…N)

    final_mapping = {old: idx for idx, old in enumerate(sorted(keep_labels), start=1)}

    new_mask = np.zeros_like(mask)

    records = []

    for old_label, intermediate in mapping.items():

        if intermediate not in keep_labels:

            continue

        new_label = final_mapping[intermediate]

        cnt = counts[intermediate]

        vol = cnt * voxel_vol

        new_mask[temp_mask == intermediate] = new_label

        records.append({

            "new_label":   new_label,

            "voxel_count": cnt,

            "volume":      vol

        })
 
    # Save the cleaned, relabeled mask

    nib.save(nib.Nifti1Image(new_mask, img.affine, img.header), args.output_mask)
 
    # Build DataFrame

    df = pd.DataFrame(records)
 
    # Print summary

    print(f"Kept {len(df)} cells (≥ {args.min_size} voxels).")

    print(df["volume"].describe(), "\n")
 
    # Save CSVs

    df.to_csv(args.volumes_csv, index=False)

    df["volume"].describe().to_frame().T.to_csv(args.summary_csv, index=False)
 
    # Plot histogram of volumes

    plt.figure()

    plt.hist(df["volume"], bins='auto')

    plt.xlabel("Cell Volume (voxel_units)")

    plt.ylabel("Count")

    plt.title("Histogram of Cell Volumes")

    plt.tight_layout()

    plt.savefig("cell_volume_histogram_392.png")

    print("Saved histogram to cell_volume_histogram_392.png")
 
if __name__ == "__main__":

    main()

 