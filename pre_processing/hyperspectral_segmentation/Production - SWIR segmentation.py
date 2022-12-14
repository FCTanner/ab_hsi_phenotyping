#!/usr/bin/env python
# coding: utf-8

import pickle
import os
import numpy as np
import time
import cv2

import sys
sys.path.append("") # Add path containing "appf_toolbox": https://github.com/Harwis/appf_toolbox
from appf_toolbox.hyper_processing.envi_funs import read_hyper_data, calibrate_hyper_data

results_dir = "" # Set output results directory
masks_out_dir = "" # Set output directory for binary masks
swir_data_base_dir = "" # Set base directory for SWIR data

swir_data = os.listdir(swir_data_base_dir)

pixel_results_list = os.listdir(results_dir)
pixel_results_list = [x[:-4] for x in pixel_results_list]
print(pixel_results_list)

raw_data, meta_plant = read_hyper_data(swir_data_base_dir, swir_data[5])
ncols = meta_plant.ncols
nrows = meta_plant.nrows
nbands = meta_plant.nbands
wavelengths = np.zeros((meta_plant.metadata['Wavelength'].__len__(), ))
for i in range(wavelengths.size):
    wavelengths[i] = float(meta_plant.metadata['Wavelength'][i])

with open("training_data/SWIR/classifier/study_08_SWIR_SVM_pixel_classifier.pkl", "rb") as f:
    clf = pickle.load(f)

# Some things to print progress
left_to_do = len(swir_data) - len(pixel_results_list)
done = 0
duration_list = []


for swir_folder in swir_data:
    result_path = os.path.join(results_dir, swir_folder) + ".csv"
    if os.path.exists(result_path):
        pass
    else:
        try:
            print("#############################################################################")
            print(swir_folder)
            start = time.time()
            # 2. Load SWIR data
            SWIR_dict, meta_plant_dat = read_hyper_data(swir_data_base_dir, swir_folder)
            hyper = calibrate_hyper_data(white=SWIR_dict["white"],
                                         dark=SWIR_dict["dark"],
                                         plant=SWIR_dict["plant"])

            # 3. Reshape to 2d np-array
            width_hc = hyper.shape[1]
            height_hc = hyper.shape[0]
            depth_hc = hyper.shape[2]
            hyper_2d = np.reshape(hyper, (width_hc * height_hc, depth_hc))

            # 4. Apply pixel classifier
            pixel_predict = clf.predict(hyper_2d)
            foreground_pixels = hyper_2d[pixel_predict == 1]

            # 5. Saving foreground pixels
            foreground_out = np.reshape(wavelengths, (1, 288))
            foreground_out = np.append(foreground_out, foreground_pixels, axis=0)
            np.savetxt(os.path.join(results_dir, "{to_save}.csv".format(to_save = swir_folder)),  foreground_out, delimiter=",")

            # 6. Outputting masks
            png_path = os.path.join(swir_data_base_dir, swir_folder, "{to_save}.png".format(to_save = swir_folder))
            if os.path.isfile(png_path): # check whether png exists
                # 6.1 Load original SWIR png
                SWIR_png = cv2.imread(png_path)
                # cv2.imshow("swir_png", SWIR_png)
                # cv2.waitKey(1000)

                # 6.2 Turning mask into color image
                predict_mask = np.reshape(pixel_predict, (height_hc, width_hc))
                predict_mask_img = np.array(predict_mask * 255).astype('uint8')
                color_predict_mask = cv2.cvtColor(predict_mask_img, cv2.COLOR_GRAY2BGR)
                color_predict_mask[predict_mask_img > 0] = (0, 255, 0)

                # 6.3 Overlay predicted mask and SWIR png
                overlay_predict_mask = cv2.addWeighted(src1=SWIR_png, alpha=1, src2=color_predict_mask, beta=1, gamma=0)
                title = swir_folder.format()
                # 6.4. Output those images somewhere
                cv2.imwrite(filename=os.path.join(masks_out_dir, "{to_save}.png".format(to_save=swir_folder)), img=overlay_predict_mask)
            else:
                print("Png does not exist")
            # Printing status report to console
            left_to_do = left_to_do - 1
            done += 1
            print(foreground_pixels.shape[0], "foreground pixels found in", swir_folder)
            print(done, "segmentations are done, ", left_to_do, "iterations left to do ")
            stop = time.time()
            duration = stop - start
            duration_list.append(duration)
            print("Pixel classification took", round(duration), "seconds")
            average_duration = sum(duration_list) / len(duration_list)
            print("Approximate time left =", round((left_to_do * average_duration) / 60), "minutes")
        except:
            print("####################################")
            print(swir_folder)
            print("EOF error")