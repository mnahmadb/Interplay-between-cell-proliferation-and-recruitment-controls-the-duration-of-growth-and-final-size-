%dynamics of the function F (W, R)
clear all; clc; close all;

%ODE system parameters
%k := Proportionality constant for half maximal contribution of R cells
%to the recruitment rate
%q := Proliferation rate 
%p := Maximum percentage of cells from the recruitment boundary that 
%will be recruited per unit of time.
global k
global q
global p


s=0; x=0; y=0; load('EndTimes.mat.mat');  
M = [EndTimes];
for j=length(M):length(M); 
    k = M(j,1)           
    p = M(j,2);
for i=0.0010:0.0001:0.0018; 
    q = i; 
[T,Z] = ode45(@ODE_system,[0: 0.1 :5000],[225 169]); 
T = T/60;
f = pi*p*sqrt(Z(:,1)).*((d+Z(:,2))./(k*pi*sqrt(Z(:,1))+Z(:,2)))*60;
%To graph figure 4A
hold on
colorbar 
if q < 0.0014
    plot(T,f,'b','LineWidth',1.5);
else
    plot(T,f,'r','LineWidth',1.5);
end
end
end
