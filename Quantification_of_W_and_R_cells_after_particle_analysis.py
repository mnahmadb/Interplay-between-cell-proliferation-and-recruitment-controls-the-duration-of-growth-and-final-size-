### Code from Luis Manuel Muñoz Nava
### email: luis.nava@cinvestav.mx

###### This code finds the W cells or Vestigial (Vg) positive cells and the R cells or Vg negative cells in the wing pouch of the Drosophila wing disc ######  

### Import the required packages ###
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageOps
from pathlib import Path

### Functions ###
def x_y_coor_min_max(x_y_coor):
	"""This function returns the x and y ranges coordinates of the region of interest"""
	x_range = [np.min(x_y_coor["X"]),np.max(x_y_coor["X"])]
	y_range = [np.min(x_y_coor["Y"]),np.max(x_y_coor["Y"])]
	return x_range, y_range

def list_of_ellipse_pixels(xy_coor):
	"""This function obtains the pixels that correspond to the ellipse defined by the wing pouch"""
	n = 0
	list_of_pixels = []
	y_pixel = xy_coor["Y"][0]
	list_for_y = []
	for_last_y = []
	x_min = np.min(xy_coor)["X"]
	## For every value in the y axis, append all the values in the x axis corresponding to the wing pouch
	for i in xy_coor["Y"]:
		if i == y_pixel:
			## Use the same x axis values for the first and the last y axis values (is an ellipse, so they must be the same)
			list_for_y.append(xy_coor["X"][n] - x_min)
			for_last_y.append(xy_coor["X"][n] - x_min)
			y_pixel = i
		else:
			list_of_pixels.append(list_for_y)
			list_for_y = [xy_coor["X"][n] - x_min]
			y_pixel = i
		n += 1

	## Obtain the list and append the last value
	list_of_pixels.append(for_last_y)
	return list_of_pixels


### The code runs here ###

# To otain the total number of R and W pixels and estimated cells
count_r_pixels = []
count_w_pixels = []
count_r_cells = []
count_w_cells = []
DV_length_list = []
ellipse_area_list = []
ellipse_area_pixels_list = []

## Binary image from the particle analysis (in RGB)
bin_image = plt.imread("/path/mask_image.png") # Write the path to the file instead of "path"

## xy_coor table for the pouch area
xy_coor = pd.read_csv("/path/xy_coor_elipse.csv") # Write the path to the file instead of "path"

## Set te min and max for the x and y coordenates for the pouch area
x_coor,y_coor = x_y_coor_min_max(xy_coor)

## Set a list of all the pixels in the ellipse area
list_of_pixels = list_of_ellipse_pixels(xy_coor)

## To count the Vg positive and negative pixels
count_vg_pos = 0
count_vg_neg = 0
non_ellipse_pixels = 0

## To obtain the W and R pixels
to_test_region = np.zeros((len(range(y_coor[0],y_coor[1]+1)),len(range(x_coor[0],x_coor[1]+1))))
l = 0
for i in bin_image:
	c = 0
	for n in i:
		if c in list_of_pixels[l]:
			## If the RGB array is white with (1,1,1), the sum is 3 and is a pixel with no Vg
			if np.sum(np.array(n)) == 3:
				to_test_region[l][c] = 0
				count_vg_neg += 1
			## All the pixels in black are Vg pixels
			else :
				to_test_region[l][c] = 1
				count_vg_pos += 1 
		else:
			non_ellipse_pixels += 1
		c += 1
	l += 1

## Append the total R pixels to a list for all the discs
r_pixels = count_vg_neg
count_r_pixels.append(r_pixels)

## Append the total W pixels to a list for all the discs
w_pixels = count_vg_pos
count_w_pixels.append(w_pixels)

## R cells are calculated to be a total of approximately 70 pixels (more than the 50 pixels estimated for a nucleus, this was calculated by hand using the ImageJ software)
r_cells = count_vg_neg / 70
## Append the total R cells to a list for all the discs
count_r_cells.append(r_cells)

## W cells calculated as for the R cells
w_cells = count_vg_pos / 70
## Append the total R cells to a list for all the discs
count_w_cells.append(w_cells)

## To obtain the total length of the wing pouch in the Dorsal Ventral axis in microns (every micron contains 5.5440 pixels in the images obtained with our microscopy) 
DV_length = (y_coor[1] - y_coor[0]) / 5.5440
## Append the Dorsal Ventral length to a list of all the discs
DV_length_list.append(DV_length)

## To obtain the ellipse area in microns
ellipse_area = (((y_coor[1] - y_coor[0])/2) / 5.5440) * (((x_coor[1] - x_coor[0])/2) / 5.5440) * np.pi
## Append the ellipse area in microns to a list of all the discs
ellipse_area_list.append(ellipse_area)

## To obtain the ellipse area in pixels
ellipse_area_pixels = ((y_coor[1] - y_coor[0])/2) * ((x_coor[1] - x_coor[0])/2)  * np.pi
## Append the ellipse area in pixels to a list of all the discs
ellipse_area_pixels_list.append(ellipse_area_pixels)

## Create a dictionary and a Data Frame of the obtained data of all the analyzed discs 
dict_data = {"DV_length" : DV_length_list, "Ellipse Area no pixels" : ellipse_area_list , "Ellipse Area" : ellipse_area_pixels_list,"W cells" : count_w_cells, "R cells" : count_r_cells, "W pixels" : count_w_pixels, "R pixels" : count_r_pixels}
data_df = pd.DataFrame(dict_data)
print(data_df)
## Save the Data Frame
# pd.DataFrame.to_csv(data_df,main_root + "r_w_pixels_and_cells.csv")


