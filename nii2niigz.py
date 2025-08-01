import nibabel as nib

nii_path = r"C:\Users\Cheng Lab\Downloads\Daphnia_392\AAA392_Gut_segmentation130_9.16.24a_FINAL.nii\AAA392_Gut_segmentation130_9.16.24a_FINAL.nii"
img = nib.load(nii_path)
nib.save(img, nii_path + ".gz")  # Saves as .nii.gz
