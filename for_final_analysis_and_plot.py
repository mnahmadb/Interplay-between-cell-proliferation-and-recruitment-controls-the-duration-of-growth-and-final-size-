### Code from Luis Manuel Muñoz Nava
### email: luis.nava@cinvestav.mx

###### This code divides the discs in groups, makes the statistics and the plot for the W and R cells within the wing pouch ######  

### Import the required packages ###
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as scp

### The code runs here ###

## Define the root for the files with the masks images obtained from the particle analysis (for example: "/home/my_computer/Documents/for_paper/")
df_r_w_cells = pd.read_csv("/home/my_computer/Documents/for_paper/masks.csv")

## Obtain the mean and standard deviation of the Ellipse to group de discs depending on their size
df_r_w_cells = df_r_w_cells.sort_values(by=["Ellipse Area"], axis=0)
ellipse_area_mean = np.mean(df_r_w_cells["Ellipse Area"])
ellipse_area_std = np.std(df_r_w_cells["Ellipse Area"])

## Take out discs very big or too small
df_r_w_cells_new = df_r_w_cells[df_r_w_cells["Ellipse Area"] >= (ellipse_area_mean - 2*ellipse_area_std)]
df_r_w_cells_new = df_r_w_cells_new[df_r_w_cells_new["Ellipse Area"] <= (ellipse_area_mean + 2*ellipse_area_std)]

## We obrained the total number of groups with the square root of the total number of discs less 1 (to obtain the higher number of discs per group)
numb_groups = int(np.sqrt(len(df_r_w_cells_new["Ellipse Area"]))) -1

## We looked for the min and max area of the ellipses and divided the range between them in the number of groups
area_min = np.min(df_r_w_cells_new["Ellipse Area"])
area_max = np.max(df_r_w_cells_new["Ellipse Area"])
range_area = (area_max - area_min) / numb_groups 

groups_area_df = []
range_area_groups = []

### Define the groups of discs
l = 1
k= 0
for i in range(numb_groups):
	range_for_areas = ((area_min + range_area*k), (area_min + range_area*(k+1)))
	df = df_r_w_cells_new[df_r_w_cells_new["Ellipse Area"] < (area_min + range_area*l)]
	df = df[df["Ellipse Area"] > (area_min + range_area*(l-1))]
	groups_area_df.append(df)
	range_area_groups.append(range_for_areas)
	l += 1
	k += 1

## Obtain some descriptive statistics from the groups and append in lists
mean_r_pixels_list = []
mean_w_pixels_list = []
mean_r_cells_list = []
mean_w_cells_list = []
sem_r_pixels_list = []
sem_w_pixels_list = []
length_of_groups = []
r_pixels_group = []
w_pixels_group = []

for i in groups_area_df:
	mean_r_cells = np.mean(i["R cells"])
	mean_w_cells = np.mean(i["W cells"])
	mean_r_pixels = np.mean(i["R pixels"])
	mean_w_pixels = np.mean(i["W pixels"])
	mean_r_cells_list.append(mean_r_cells)
	mean_w_cells_list.append(mean_w_cells)
	mean_r_pixels_list.append(mean_r_pixels)
	mean_w_pixels_list.append(mean_w_pixels)
	sem_r_pixels = scp.sem(i["R pixels"])
	sem_w_pixels = scp.sem(i["W pixels"])
	sem_r_pixels_list.append(sem_r_pixels)
	sem_w_pixels_list.append(sem_w_pixels)
	r_pixels_group.append(list(i["R pixels"]))
	w_pixels_group.append(list(i["W pixels"]))
	length_of_groups.append(len(i))

### To make the R pixels plot ###
x = []
for i in range(len(mean_r_pixels_list)):
	x.append(i+1)
y = mean_r_pixels_list
e = sem_r_pixels_list
for k in range(len(mean_r_pixels_list)):
	plt.errorbar(x[k],y[k],e[k], marker="o", linestyle="None", linewidth=3, markersize=8, capsize=8, capthick=3)
plt.show()

### To make the W pixels plot ###
x = []
for i in range(len(mean_w_pixels_list)):
	x.append(i+1)
y = mean_w_pixels_list
e = sem_w_pixels_list
for k in range(len(mean_r_pixels_list)):
	plt.errorbar(x[k],y[k],e[k], marker="o", linestyle="None", linewidth=3, markersize=8, capsize=8, capthick=3)
plt.show()

### Obtain the ANOVA test for the W pixels
ANOVA_W_pixels = scp.f_oneway(w_pixels_group[0],w_pixels_group[1],w_pixels_group[2],w_pixels_group[3],w_pixels_group[4])

### Obtain the ANOVA test for the R pixels
ANOVA_R_pixels = scp.f_oneway(r_pixels_group[0],r_pixels_group[1],r_pixels_group[2],w_pixels_group[3],w_pixels_group[4])
