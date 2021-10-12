%Exploration of the parametric space of the ODE system
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

%Exploration of the ODE system dynamics as a function of (p,k) 
%fixing the q parameter in the wild type value. 
s=0; x=0; y=0; q=0.0014;
for j=0.25:0.001:1.5;
    k = j;    
for f=0.0000:0.0001:0.0050; 
    p = f; 
[T,Z] = ode45(@ODE_system,[0: 0.1 :5000],[225 169]); 
hold on 
T = T/60;
m1 = find(Z(:,2)>=0 & Z(:,2)<=1,1,'first');
tf = T(m1,1);
[mr mp]=max(Z(:,2));
tm = T(mp,1);
rf=Z(end,2);
ri=Z(1,2);

%We store the pairs of parameters (p,k) in which R(t) meets the criteria
%of line 24 in a time between 24 and 36 hours.
   if mr == rf;
       s = s+1;
       %plot(p/0.0014,k,'m*')%To graph the supplementary figure
       plot(T,Z(:,2),'m','LineWidth',0.7) %To graph the figure 2 panel E.
       rhom(s,1:4) = [k,q,p,tm];
   elseif ri == mr;
       x=x+1;
       %plot(p/0.0014,k,'g*')%To graph the supplementary figure
           if tf >= 24 & tf <= 36;
               rhog(x,1:4) = [k,q,p,tf];
           end
       plot(T,Z(:,2),'g','LineWidth',0.7)%To graph the figure 2 panel E.
   else 
       y=y+1;
       %plot(p/0.0014,k,'b*')%To graph the supplementary figure
          if tf >= 24 & tf <= 36;
              rhob(y,1:4) = [k,q,p,tf];
          end
       plot(T,Z(:,2),'b','LineWidth',0.7)%To graph the figure 2 panel E
   end
 
end
end

save('RhoSubset.ma','rhob');

