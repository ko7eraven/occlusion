

%path='300/h1-10/';
path='./';


BASE=15;
BASE=15;

f=fopen([path,'s2.bin'],'rb')
a=fread(f,'float32');
fclose(f);
tm=a(1:3:end);
pwm=a(2:3:end);
O=a(3:3:end)-BASE;
pwms=zeros(size(pwm));

F=ones(300, 1)*0.0;

F=[F; [1:18]'/18];

F=F-mean(F)

G=ones(150,1)*0.0;
G=[G; [1:9]'/9];
G=G-mean(G);
%F=F/sum(F);

C=zeros(length(pwm),4);

Z=zeros(size(pwm));
N=length(F)
for i=2:(length(Z)-N)
  
   Z(i+N-2)=F'*pwm(i:i+N-1); 
endfor

if(1)
A=zeros(4,318); % row 1 is cos, row 2 is sin
n=0:317;
A(1,:)=cos(2*pi*n/70);
A(2,:)=sin(2*pi*n/70);
A(3,:)=ones(size(A(3,:)));
A(4,301:318)=[1:18];

B=zeros(3,length(pwm));
n2=[0:length(pwm)-1];
B(1,:)=cos(2*pi*n2/70);
B(2,:)=sin(2*pi*n2/70);
B(3,:)=ones(size(B(3,:)));
B=B.';
else
A=zeros(4,318); % row 1 is cos, row 2 is sin
n=0:317;
A(1,:)=cos(2*pi*n/70);
A(2,:)=sin(2*pi*n/70);
A(3,:)=ones(size(A(3,:)));
A(4,:)=F;
endif
A=A.';

YY=B\pwm;


ZZ=zeros(size(pwm));
N=length(F);
for i=2:(length(Z)-N)
   x=A(1:300,1:2)\pwm(i:i+300-1);
   %pwm2=A(:,1:4)*x;
   pwm2=A(:,1:2)*x;
   pwm2=pwm(i+N-1)-pwm2;
   ZZ(i+N-2)=(pwm2(N)-22);
   C(i+N-2,1:2)=x; 
   %ZZ(i+N-1)=x(4)*100; 
   %ZZ(i+N-1)=pwm(i+N-1)-pwm2(N);
endfor



f=fopen([path,'p2.bin'],'rb')
b=fread(f,'float32');
fclose(f);



tp=b(1:2:end);
p=b(2:2:end);


%ind15=min(find(p>=15.0))
%t15=tp(ind15);
%lim15=15*ones(size(pwm));
%ind15b=min(find(tm>=t15));
%lim15(1:ind15b)=zeros(ind15b,1);


figure
plot(tp,p,'r');
hold on
plot(tm,(pwm-BASE)*10);
%plot(tm,lim15, 'k');
%plot(tm,Z,'m')
plot(tm, O, 'g')
%plot(tm,ZZ,'c')
xlabel('time(s)')
ylabel('psi + others')
title('h1-1 downstream occlusion')
legend('pressure', 'pwm', 'occlusion');

maxp=max(p)
