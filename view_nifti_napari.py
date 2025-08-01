import napari
import numpy as np
import nibabel as nib


image_path = r"C:\Users\Cheng Lab\Downloads\Daphnia_392\AAA392_bin0_image.nii.gz"
# Add more masks as needed
mask_path = r"C:\Users\Cheng Lab\Downloads\Daphnia_392\AAA392_Gut_segmentation130_9.16.24a_FINAL.nii\AAA392_Gut_segmentation130_9.16.24a_FINAL.nii.gz"
# mask_path = r""


# Load image and mask 
image_nii = nib.load(image_path)
mask_nii = nib.load(mask_path)
# mask_nii2 = nib.load(mask_path)

image = image_nii.get_fdata().astype(np.float32)
mask = mask_nii.get_fdata().astype(np.uint16)
# mask2 = mask_nii2.get_fdata().astype(np.uint16)

# Launch napari viewer
viewer = napari.Viewer()
viewer.add_image(image, name='Image', colormap='gray')
viewer.add_labels(mask, name='Mask')
# viewer.add_labels(mask2, name='Mask') 
napari.run()
