%dynamics of the ODE system under perturbations in the proliferation rate
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

%We perturb the system in the parameter q 
%around the wild value reported in the literature, and we store 
%the data of Wf, tf, k, p y q defined in the original manuscript.
s=0; x=0; y=0; load('RhoSubset.mat');
F=find(RhoSubset(:,4));  
M = [RhoSubset(F,1) RhoSubset(F,2) RhoSubset(F,3) RhoSubset(F,4)];
for j=1:length(M); 
    k = M(j,1);     
    p = M(j,4);
for f=0.0010:0.0001:0.0018; 
    q = f; 
[T,Z] = ode45(@ODE_system,[0: 0.1 :5000],[225 169]); 
hold on
T = T/60;
m1 = find(Z(:,2)>=0 & Z(:,2)<=1,1,'first');
tf = T(m1,1);
[mr mp]=max(Z(:,2)); 
tm = T(mp,1);
rf=Z(end,2); ri=Z(1,2); wf=Z(m1,1);
   if mr == rf;
       s = s+1;
       rhom(s,1:3) = [k,q,tm];
   elseif ri == mr;
       x=x+1;
       rhog(x,1:3) = [k,q,p];
           if tf >= 24 & tf <= 36;
               rhog(x,1:3) = [k,q,tf];
           end
   else 
       y=y+1;
          if tf <= 60;
              rhob(y,1:4) = [k,p,q,tf];
          end
   end
end
end
save('EndTimes.mat','rhob');

