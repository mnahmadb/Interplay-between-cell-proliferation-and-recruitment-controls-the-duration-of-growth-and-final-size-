### Code from Luis Manuel Muñoz Nava
### email: luis.nava@cinvestav.mx

###### This code finds the positive and negative pixels for Vestigial (Vg) in the wing pouch of the Drosophila wing disc ######  

### Import the required packages ###
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from PIL import Image, ImageOps
from pathlib import Path

### Functions ###
def x_y_coor_min_max(x_y_coor):
	"""This function returns the x and y ranges coordinates of the region of interest"""
	x_range = [np.min(x_y_coor["X"]),np.max(x_y_coor["X"])]
	y_range = [np.min(x_y_coor["Y"]),np.max(x_y_coor["Y"])]
	return x_range, y_range


def tuple_of_x_y_coor(xy_coor):
	"""This function returns a list of tuples with all the x and y coordinates of the region of interest"""
	list_of_tuple_x_y = []
	l = 0
	for i in xy_coor["Y"]:
		tuple_x_y = (i,xy_coor["X"][l])
		list_of_tuple_x_y.append(tuple_x_y)
		l += 1
	return list_of_tuple_x_y


def rescale_images_0_1(image):
	"""This function rescales between 0 to 1 all the values in the selected image"""
	image_rescaled = (image - image.min()) / (image.max() - image.min())
	return image_rescaled


def region_of_image(image,x_range,y_range):
	"""This function select a region of interest from an image depending on x and y coordinates given"""
	region = np.zeros((len(range(y_range[0],y_range[1]+1)),len(range(x_range[0],x_range[1]+1)))) # makes the region array
	l = 0
	for i in range(1024): # loop in all y coordinates of the image
		if i in range(y_range[0],y_range[1]+1): # localize region in y coor
			c = 0
			for f in range(1024): # loop in all x coordinates of the image
				if f in range(x_range[0],x_range[1]+1): # localize region in x coor
					region[l][c] = image[i][f]
					c += 1
			l += 1    
	return region


def region_of_image_only_pouch(image,x_range,y_range,xy_coor,list_tuple_x_y):
	"""This function select a region of interest from an image depending on x and y given coordinates and if it is in the ellipse defining the pouch"""
	region = np.zeros((len(range(y_range[0],y_range[1]+1)),len(range(x_range[0],x_range[1]+1)))) # makes the region array
	l = 0
	for i in range(1024): # loop in all y coordinates of the image
		if i in range(y_range[0],y_range[1]+1): # localize region in y coor
			c = 0
			for f in range(1024): # loop in all x coordinates of the image
				if f in range(x_range[0],x_range[1]+1): # localize region in x coor
					if (i,f) in list_tuple_x_y:
						region[l][c] = image[i][f]
						c += 1
					else:
						region[l][c] = 0
						c += 1
			l += 1    
	return region


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

	## Obtain the list and append the last value, also generate a dictionary and a Data Frame
	list_of_pixels.append(for_last_y)
	dict_list_of_pixels = {"list_pixels" : list_of_pixels}
	df_list_of_pixels = pd.DataFrame(dict_list_of_pixels)

	return list_of_pixels, df_list_of_pixels


def divide_in_groups(image,n_groups):
	"""This function divides all the positive pixels for a marker in a region in n number of groups depending in their intensity"""
	
	### Unsupervised Machine Learning algorithm from SK Learn to find n number of groups
	region_values_reshaped = image.reshape(-1,1)
	## Declaring Model
	model = KMeans(n_clusters=n_groups)
	## Fitting Model
	model.fit(region_values_reshaped)
	## Prediction on the data
	prediction_data = model.predict(region_values_reshaped)
	prediction_data_list = list(prediction_data)

	## To append in a list in an ordered manner from 1 to 6 the groups obtained 
	groups = []
	for i in range(6):
		group = []
		groups.append(group)

	group_1 = []
	group_2 = []
	group_3 = []
	group_4 = []
	group_5 = []
	group_6 = []

	n = 0
	for i in prediction_data_list:
		if i == 0:    
			group_1.append(region_values_reshaped[n][0])
		elif i == 1:
			group_2.append(region_values_reshaped[n][0])
		elif i == 2:
			group_3.append(region_values_reshaped[n][0])
		elif i == 3:
			group_4.append(region_values_reshaped[n][0])
		elif i == 4:
			group_5.append(region_values_reshaped[n][0])
		elif i == 5:
			group_6.append(region_values_reshaped[n][0])
		n += 1
    

	cluster_groups = [group_1, group_2, group_3,group_4,group_5,group_6]
	mean_groups = [np.mean(group_1),np.mean(group_2),np.mean(group_3),np.mean(group_4),np.mean(group_5),np.mean(group_6)]

	return cluster_groups, mean_groups


def vg_image_without_noise(image_rescaled,mean_vg_min,x_range,y_range,list_of_pixels):
	"""This function returns the rescaled image region (wing pouch) with only the positive Vg pixels """
    

	no_max_no_min_region = np.zeros((len(range(y_range[0],y_range[1]+1)),len(range(x_range[0],x_range[1]+1))))
	bin_image = np.zeros((len(range(y_range[0],y_range[1]+1)),len(range(x_range[0],x_range[1]+1))), "uint8")
	bin_image_no_vg_noise = np.zeros((len(range(y_range[0],y_range[1]+1)),len(range(x_range[0],x_range[1]+1))), "uint8")

	## Clutser the pixels in 6 different groups depending on their intensity
	cluster_groups,mean_groups = divide_in_groups(image_rescaled,6)

	## Obtain the group with the maximum intensities
	mean_max = np.max(mean_groups)

	## Obtain the all the pixels values of the maximum instensities group
	max_group = []    
	n = 0
	for i in mean_groups:	
		if i == mean_max:
			max_group = cluster_groups[n]
		n += 1

	## Obtain the minimum value of the maximium intensities group
	min_of_max_group = np.min(max_group)

	## To obtain the positive Vg pixels (the pixels below a threshold and the pixels in the maximum intensities gruop will be excluded to take out the noise)
	count_vg_pos = 0
	count_vg_neg = 0
	l = 0
	for i in image_rescaled:
		c = 0
		for n in i:
			if n <= mean_vg_min or n >= min_of_max_group:
				no_max_no_min_region[l][c] = 0
				bin_image[l][c] = 0
				if n <= mean_vg_min:
					count_vg_neg += 1
			else:
				no_max_no_min_region[l][c] = n
				bin_image[l][c] = 255
				count_vg_pos += 1
    		## If the pixels are outside the pouch, give them a value of 0
			if c not in list_of_pixels[-l]:
				no_max_no_min_region[l][c] = 0
				bin_image[l][c] = 0
				#if n <= max_of_min_list:
				#	count_vg_neg -= 1
			c += 1
		l += 1

    
	return no_max_no_min_region, bin_image, count_vg_pos, count_vg_neg



### The code runs here ###

## Define the main root for the files (for example: "/home/my_computer/Documents/for_paper/")
main_root = "/home/my_computer/Documents/for_paper/"

## Obtain all the files names list to work with
rootdir_xy_coor = Path(main_root + "xy_coor_elipse")
file_list_xy_coor = [f for f in rootdir_xy_coor.glob("**/*.csv") if f.is_file()]

### for every disc in the file of all the discs, obtain the Vg positive image in the pouch
for disc in range(1,(len(file_list_xy_coor)+1)):
	## Vg image
	vg_image = plt.imread(main_root + "vg_images/" + str(disc) + ".png")

	## rescale Vg images between 0 and 1
	vg_rescaled = rescale_images_0_1(vg_image)

	## xy_coor table for the pouch area
	xy_coor = pd.read_csv(main_root + "xy_coor_elipse/" + str(disc) + ".csv")

	## xy_coor table for vg minimum values (area outside the pouch to obtain the background noise in the image)
	xy_min = pd.read_csv(main_root + "xy_coor_vgmin/" + str(disc) + ".csv")

	## Set te min and max for the x and y coordenates for the pouch area
	x_coor,y_coor = x_y_coor_min_max(xy_coor)

	## Set the min and max for the x and y coordenates for vg min area
	x_coor_min, y_coor_min = x_y_coor_min_max(xy_min)

	## Set and show the region of the pouch in the vg image
	vg_region = region_of_image(vg_rescaled,x_coor,y_coor)
	#plt.imshow(vg_region)
	#plt.show()

	## Set and show the region of the min in the vg image
	vg_min = region_of_image(vg_rescaled,x_coor_min,y_coor_min)
	#plt.imshow(vg_min)
	#plt.show()

	## Set the mean and Std of the intensities of the vg min region
	mean_vg_min = np.mean(vg_min)
	std_dev_vg_min = np.std(vg_min)

	## Set the background noise value with the intensity mean plus two standard deviation data of the vg min intensities
	mean_plus_two_std = mean_vg_min + (std_dev_vg_min*2)

	## Set a list of all the pixels in the ellipse area
	list_of_pixels, df_list_of_pixels = list_of_ellipse_pixels(xy_coor)

	# Do all the quantifications and obtain the vg image without noise and a binary image with or without vg 
	image_no_min_no_max, bin_image, count_vg_pos, count_vg_neg = vg_image_without_noise(vg_region,mean_plus_two_std,x_coor,y_coor,list_of_pixels)

	## Display the Vg image in the wing pouch without noise
	plt.imshow(image_no_min_no_max)
	plt.axis("off")
	plt.show()

	## Display the binary Vg image in the wing pouch without noise
	plt.imshow(bin_image)
	plt.axis("off")
	plt.show()

	## Save the bin image of vg in the wing pouch for further analysis
	# bin_image_no_vg_noise = Image.fromarray(bin_image,"L")
	# bin_image_no_vg_noise.save(main_root + "bin_images_01/" + str(disc) + ".png")






