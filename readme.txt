All this codes are made with python 3.

To run the code to analyze the images:

You need to specify the path to the files and images to analyze in the code where "path" is asked.

Run the code named W_and_R_cells_determination.py. Here you need to save the resulting images in a folder (this is done by the code, just need to define the directory to save the images) to further analyze them with the particle analysis of Image J software, in the particle analysis tool set the size parameter to be above 50 (we quantified that in average 50 pixels formed the cell’s nucleus), the circularity parameter between 0 and 1 to admit different nuclei shapes and the holes between nuclei are also stained. After obtaining the mask of the image, you need to save it in another folder with the number that correspond to the disc (for example "1.png","2.png",etc.) as the files obtained from the fisrt code (Do it for all the discs). We attached one image after this analysis named "mask_image.png" to run the next code.

Next, run the code named Quantification_of_W_and_R_cells_after_particle_analysis.py to obtain a Data Frame with the total number of R and W pixels and cells, also with the distance of the wing pouch in the Dorsal Ventral axis and the wing pouch area for each disc. 

*The codes would last long, depending on your computer capacity. 

For specific questions of the code send an email to luis.nava@cinvestav.mx

