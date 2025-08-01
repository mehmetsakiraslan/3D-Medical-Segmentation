#!/usr/bin/env python3

import os
import argparse
import nibabel as nib
import numpy as np

def crop_center_memmap(img, target_shape):
    """
    Crop the center of the volume using memory-mapped access.
    """
    full_shape = img.shape
    target_shape = np.array(target_shape)

    if np.any(target_shape > full_shape):
        raise ValueError(f"Target shape {target_shape} is larger than original shape {full_shape}.")

    start = ((np.array(full_shape) - target_shape) // 2).astype(int)
    end = start + target_shape

    # Access image data as memory-mapped array
    dataobj = img.dataobj  # memmap-like object
    cropped = np.zeros(target_shape, dtype=img.get_data_dtype())

    for z in range(start[2], end[2]):
        slice_z = dataobj[start[0]:end[0], start[1]:end[1], z]
        cropped[:, :, z - start[2]] = slice_z

    return cropped

def crop_volume_memmap(input_nii, output_nii, target_shape):
    """
    Load using memmap, crop, and save the NIfTI file.
    """
    print(f"Loading (memmap): {input_nii}")
    img = nib.load(input_nii)

    cropped_data = crop_center_memmap(img, target_shape)
    cropped_img = nib.Nifti1Image(cropped_data, affine=img.affine, header=img.header)
    nib.save(cropped_img, output_nii)
    print(f"✓ Cropped volume saved: {output_nii} (shape = {cropped_data.shape})")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Crop a 3D NIfTI volume to the specified shape using memory-mapped access.")
    parser.add_argument("--input_nii", type=str, required=True, help="Path to input .nii.gz file")
    parser.add_argument("--output_nii", type=str, required=True, help="Path to output .nii.gz file")
    parser.add_argument("--shape", type=int, nargs=3, required=True, help="Target shape: X Y Z (e.g., 1000 1000 451)")

    args = parser.parse_args()
    crop_volume_memmap(args.input_nii, args.output_nii, args.shape)
