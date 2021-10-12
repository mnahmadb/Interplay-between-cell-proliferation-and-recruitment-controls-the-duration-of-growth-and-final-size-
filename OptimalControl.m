%ODE system optimization
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
load('RhoSubset.mat.mat'); load('EndTimes.mat'); F=EndTimes;


%See materials and methods of the original manuscript
%and figure 4C to understand the process.

%Extraction of wild types values
for i=1:length(F);
    if F(i,3) == 0.0014;
       pr(i,1:4) = [F(i,1) F(i,2) F(i,3) F(i,4)];
    end 
end
pr1=find(pr(:,1));
pares = [pr(pr1,1) pr(pr1,2) pr(pr1,3) pr(pr1,4)];

%Logarithmic fit of the system with the wild types values
for i=1:length(pares); 
    k=pares(i,1); p=pares(i,2); q=pares(i,3);
    [T,Z] = ode45(@ODE_system,[0: 0.1 :5000],[225 169]);
    zv=log(Z(:,1)); t1=T/60;
ajuste = polyfit(t1,zv,1);
pol = polyval(ajuste,t1);
coef(i,1:2) = [ajuste(1,1) ajuste(1,2)]; 
end
gammawt = [(coef(:,1)/60)-0.0014];

%Logarithmic fit of the system with the values ??of the perturbstions
for i=1:length(F);
    k=F(i,1); p=F(i,2); q=F(i,3);
    [T,Z] = ode45(@ec_kqdn,[0: 0.1 :5000],[225 169]);
    zv=log(Z(:,1)); t1=T/60;
ajuste2 = polyfit(t1,zv,1);
pol = polyval(ajuste2,t1);
coef2(i,1:2) = [ajuste2(1,1) ajuste2(1,2)]; 
gamma(i,1) = [abs((coef2(i,1)/60)-F(i,3))];
end

%obtaining the polynomial tf
j=1; alpha=[0.0010:0.0001:0.0018]';
for i=1:length(pares);
    A(i) = pares(i,4)*(0.0014+gammawt(i));
    vet(i,1:9) = [A(i)./(alpha+gamma(j:j+8))];
    j=j+9;
end

%minimization of the distance between the points of the polynomials tf 
%and that obtained by disturbing the system (EndTimes.m)
%and obtaining the optimal polynomial
h=0; g=0; j=1;
for i=9:9:length(F);
    h=h+1; 
    yv=F(j:i,4)';
    suma = sum((yv-vet(h,:)).^2); 
    sigma=sqrt(suma/(9-1));
    S(h,1:5) = [suma sigma F(i,1) F(i,2) F(i,3)];
    j=j+9;
end
[v ps] = sort(S); 

%pmin := parameters of optimal polynomial
pmin=F((ps(1,2)*9)-8:ps(1,2)*9,:); vetmin=vet(ps(1,2),:);
pmax=F((ps(end,2)*9)-8:ps(end,2)*9,:); vetmax=vet(ps(end,2),:); 
pm=length(ps)/2; pmed=F((ps(pm,2)*9)-8:ps(pm,2)*9,:); vetmed=vet(ps(pm,2),:);

%To generate the graphs of figure 4D-4G.
hold on
plot(alpha,pmin(:,4),':sr',alpha,vetmin,'-sr','LineWidth',4)
plot(alpha,pmed(:,4),':ok',alpha,vetmed,'-ok','LineWidth',4)
plot(alpha,pmax(:,4),':dg',alpha,vetmax,'-dg','LineWidth',4)

%To generate supplementary figure 2
x=S(:,3);
y=S(:,4);
z=S(:,2);
stem3(x,y,z)
hold on
x=(S(1,3)); 
y=(S(1,4));
z=S(1,2);
stem3(x,y,z,'r','LineWidth',2)