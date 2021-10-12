%Upper Bound Solution
lear all; clc; close all;

%ODE system parameters
%k := Proportionality constant for half maximal contribution of R cells
%to the recruitment rate
%q := Proliferation rate 
%p := Maximum percentage of cells from the recruitment boundary that 
%will be recruited per unit of time.
global k
global q
global p 

%numerical solution
k=1; p=0.0039; q=0.0014
[t,z] = ode45(@ODE_system,[0: 0.1 :5000],[225 169]);
t1=t/60;


%Parameters for analytical solution
%See appendix 2 of the supplementary material
w0=225; r0=169; k=1; rho=0.0039; a=0.0014;
u=((sqrt(w0)+(rho*pi/a))*exp((a/2)*t)-(rho*pi/a)).^2;
u2=log(u);

%To generate figure 2A
figure; 
hold on;
plot(t1,z(:,1),'k','LineWidth',4)
x1=log(z(:,1));
plot(t1,u,'r','LineWidth',4)

%To generate figure 2B
figure; 
hold on;
plot(t1,x1,'k','LineWidth',4)
pp = polyfit(t1,x1,1)
f = polyval(pp,t1);
plot(t1,f,'g','LineWidth',4)
