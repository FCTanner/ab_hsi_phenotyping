import cv2
import os
import numpy as np
from stackImages import stackImages

import sys
sys.path.append("") # Add path containing "appf_toolbox": https://github.com/Harwis/appf_toolbox
from appf_toolbox.hyper_processing.envi_funs import read_hyper_data, calibrate_hyper_data

# This is what the program should do:
# 1. Load original SWIR pngs (this will be used later to check how segmentation worked)
# 2. Load masked SWIR pngs
# 2.1 Extract mask from masked
# 3. Load SWIR data
# 4. Extract foreground and background pixels
# 4.1. Apply binary masks to SWIR data
# 4.2. Extract foreground pixels from SWIR data
# 4.3. Extract random sample of background pixels from SWIR data
# 4.4. Create outfile for visualization + training


swir_png_base_dir = "training_data/SWIR/Original" 
swir_foreground_masks_base_dir = "training_data/SWIR/Foreground masks"
swir_background_masks_base_dir = "training_data/SWIR/Background masks"
swir_data_base_dir = "" # Set base directory of SWIR data


swir_pngs = os.listdir(swir_png_base_dir)
swir_foreground_masks = os.listdir(swir_foreground_masks_base_dir)
swir_background_masks = os.listdir(swir_background_masks_base_dir)


# Get list of the SWIR folder names that overlap with masks
list_of_SWIR_folders = []
for png_name in swir_pngs:
    path = os.path.splitext(png_name)[0]
    list_of_SWIR_folders.append(path)

print("swir_pngs")
print(swir_pngs)
print("Foreground masks")
print(swir_foreground_masks)
print("background masks")
print(swir_background_masks)
print("List of SWIR folders")
print(list_of_SWIR_folders)


# Initialize something to store data:
# Get wavelengths
raw_data, meta_plant = read_hyper_data(swir_data_base_dir, list_of_SWIR_folders[0])
ncols = meta_plant.ncols
nrows = meta_plant.nrows
nbands = meta_plant.nbands
wavelengths = np.zeros((meta_plant.metadata['Wavelength'].__len__(), ))
for i in range(wavelengths.size):
    wavelengths[i] = float(meta_plant.metadata['Wavelength'][i])
print("Wavelengths = ", wavelengths)
print("Wavelengths shape= ", wavelengths.shape)

foreground_out = np.reshape(wavelengths, (1,288))
print("foreground_out shape = ", foreground_out)
background_out = np.reshape(wavelengths, (1,288))

# Foreground
for png, foreground_mask, background_mask, swir_folder in zip(swir_pngs, swir_foreground_masks, swir_background_masks, list_of_SWIR_folders):
    # 1. + 2. Show input masks
    img_png = cv2.imread(os.path.join(swir_png_base_dir, png))
    print("Shape of png ", img_png.shape)
    img_foreground_mask = cv2.imread(os.path.join(swir_foreground_masks_base_dir, foreground_mask))
    img_background_mask = cv2.imread(os.path.join(swir_background_masks_base_dir, background_mask))
    print("Shape of mask ", img_foreground_mask.shape)
    img_foreground_binary = cv2.inRange(img_foreground_mask, (0, 0, 0), (1, 1, 1)) # binarizing mask
    img_background_binary = cv2.inRange(img_background_mask, (0, 0, 0), (1, 1, 1)) # binarizing mask
    print("Shape of binary image ", img_foreground_binary.shape)
    img_foreground_inverted = 255 - img_foreground_binary # inverting image so that foreground == 1
    img_background_inverted = 255 - img_background_binary
    print("Shape of inverted image ", img_foreground_inverted.shape)
    print(type(img_foreground_inverted))
    img_stack = stackImages(1, ([img_png, img_foreground_mask, img_foreground_inverted],
                                [img_png, img_background_mask, img_background_inverted]))
    cv2.imshow("Input", img_stack)
    cv2.waitKey(1000)

    # 3. Load hyperspec data
    SWIR_dict, meta_plant_dat = read_hyper_data(swir_data_base_dir, swir_folder)
    print("Type of output from read_hyper_data() ", type(SWIR_dict))
    print(meta_plant_dat)
    out = calibrate_hyper_data(white=SWIR_dict["white"],
                               dark=SWIR_dict["dark"],
                               plant=SWIR_dict["plant"])
    print("Type of output from calibrate_hyper_data() ", type(out))
    print("Shape of output from calibrate_hyper_data() ", out.shape)
    # Show false color image
    false_color = out[:, :, (50, 150, 250)]
    cv2.imshow("False color image", false_color)
    cv2.waitKey(1000)


    # 4. Extract foreground and background pixels

    # 4.1. Apply binary masks to SWIR data
    foreground = cv2.bitwise_and(out, out, mask=img_foreground_inverted)
    background = cv2.bitwise_and(out, out, mask=img_background_inverted)
    width_by_height_hc = foreground.shape[0] * foreground.shape[1]
    depth_hc = foreground.shape[2]
    print("Width by height hc = ", width_by_height_hc)
    print("Depth hc = ", depth_hc)
    print("background.shape", background.shape)


    # 4.2. Extract foreground pixels from SWIR data
    foreground_2d = np.reshape(foreground, (width_by_height_hc, depth_hc))
    background_2d = np.reshape(background, (width_by_height_hc, depth_hc))
    print("Shape of foreground = ", foreground.shape)
    print("Shape of foreground_2d = ", foreground_2d.shape)
    # print("Example of foreground_2d = ", foreground_2d[100,:])
    foreground_pixels = foreground_2d[np.any(foreground_2d > 0, axis=1), :]
    print("Foreground_pixels shape = ", foreground_pixels.shape)
    # print("Sample foreground pixel ", foreground_pixels[10,:])
    n_foreground_pixels = foreground_pixels.shape[0]

    print("Number of foreground pixels = ", n_foreground_pixels)

    # 4.3. Extract random sample of background pixels from SWIR data
    background_pixels_all = background_2d[np.any(background_2d > 0, axis=1), :]
    n_background_pixels = background_pixels_all.shape[0]
    print("Number of background pixels = ", n_background_pixels)

    np.random.seed(33)
    # background_pixels = background_pixels_all[np.random.choice(background_pixels_all.shape[0], n_foreground_pixels, replace=False)]
    # print("background_pixels.shape = ", background_pixels.shape)
    foreground_out = np.append(foreground_out, foreground_pixels, axis = 0)
    background_out = np.append(background_out, background_pixels_all, axis = 0)

print("Foreground out shape = ", foreground_out.shape)
print("Background out shape = ", background_out.shape)
np.savetxt("training_data/SWIR/pixel_values/swir_foreground_pixels.csv", foreground_out, delimiter=",")
np.savetxt("training_data/SWIR/pixel_values/swir_background_pixels.csv", background_out, delimiter=",")




# Visualize reflectance of random background pixels vs foreground pixels
# do this in R...
