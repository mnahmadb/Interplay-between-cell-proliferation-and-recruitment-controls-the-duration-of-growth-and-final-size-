# Interplay-between-cell-proliferation-and-recruitment-controls-the-duration-of-growth-and-final-size-

In the article “Interplay between cell proliferation and recruitment controls the duration of growth and the final size of the Drosophila wing”, 
we model two cellular processes that are active during the morphogenesis of the wings of the fly drosophila melanogaster, 
proliferation and recruitment, using a system in differential equations (ODE) in order to optimize the system and find the parameters 
for which there is control of the size of the wings. For more details see original article. The .m files must follow the following order 
to can be run without problems.

1. ODE_system.m
Here we define the differential equations that model the two biological processes.

2. ParametricSpace.m
Exploration of the system parameters, from this script we keep the values (p,k) that are congruent with biology and store them in RhoSubset.mat

3. perturbations.m
We fix the values of the parameters (p, k) selected in the previous point and we perurb the system in the cell proliferation parameter "q", we store the data in EndTimes.mat

4. UpperBound.m
We graph the analytical solution of the upper bounds of the system, see supplementary material of the article. We also did the logarithmic fit for W (t).

5. DynamicsFunctionF.m
We explore the dynamics of the function that accompanies the proliferation and recruitment processes F (W, R).

6. OptimalControl.m
Optimization of the ODE system. See materials and methods of the original manuscript. 


contact information:

PI. Marcos Nahmad mnahmad@fisio.cinvestav.mx
PhD student Elizabeth Díaz elizabeth.diaz@fisio.cinvestav.mx
https://es.nahmadlab.com/
