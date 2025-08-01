
#!/usr/bin/env python3
"""
Script to remove cell labels outside of an organ mask.

Given two NIfTI files:
 - organ_mask.nii.gz: binary (0/1) mask of the organ
 - cell_mask.nii.gz: integer labels for cells

This script sets all cell_mask voxels to zero wherever organ_mask is zero.

Usage:
    python filter_cells_by_organ.py \
        --organ organ_mask.nii.gz \
        --cells cell_mask.nii.gz \
        --output filtered_cells.nii.gz
"""
import argparse
import numpy as np
import nibabel as nib


def filter_cells(organ_path: str, cells_path: str, output_path: str) -> None:
    # Load organ mask
    organ_nii = nib.load(organ_path)
    organ_data = organ_nii.get_fdata()  # returns float64 by default
    # Binarize (in case it's not exactly 0/1)
    organ_bin = (organ_data > 0).astype(np.uint8)

    # Load cell mask
    cells_nii = nib.load(cells_path)
    # get_fdata returns float64, then convert to int32 labels
    cells_data = cells_nii.get_fdata().astype(np.int32)

    # Zero-out cells outside organ
    filtered = np.where(organ_bin, cells_data, 0).astype(cells_data.dtype)

    # Create new NIfTI and save
    filtered_nii = nib.Nifti1Image(filtered, affine=cells_nii.affine, header=cells_nii.header)
    nib.save(filtered_nii, output_path)
    print(f"Saved filtered cell mask to {output_path}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Filter a cell mask by an organ mask (remove cells outside organ)'
    )
    parser.add_argument(
        '--organ', '-o', required=True,
        help='Path to organ mask NIfTI file'
    )
    parser.add_argument(
        '--cells', '-c', required=True,
        help='Path to cell mask NIfTI file'
    )
    parser.add_argument(
        '--output', '-O', required=True,
        help='Path for output filtered cell mask NIfTI file'
    )
    args = parser.parse_args()

    filter_cells(args.organ, args.cells, args.output)


