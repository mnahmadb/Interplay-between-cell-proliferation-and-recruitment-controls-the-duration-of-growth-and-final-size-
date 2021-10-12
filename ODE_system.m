%ODE system that considers cell proliferation and recruitment. 

function dz = ODE_system(T,z)
global k 
global q
global p
dz=zeros(2,1);

dz (1) = q*z(1)+pi*p*sqrt(z(1))*((z(2))/(k*pi*sqrt(z(1))+z(2))); 
dz (2) = 0.0014*z(2)-pi*p*sqrt(z(1))*((z(2))/(k*pi*sqrt(z(1))+z(2)));


end