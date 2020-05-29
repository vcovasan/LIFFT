close all
clear all

% screwTroque;
% screwTorque1 = 2;
% screwTorque = ScrewTorque1;

uno = arduino('/dev/cu.usbmodem14101','Uno','Libraries','RotaryEncoder')

encFile = fopen('encoderStep.txt','w');

fig1 = uifigure('Position',[100 100 700 700]);


slider = uislider(fig1);
slider.Limits = [0 5];
slider.Position = [175 250 300 300];
button = uibutton(fig1,'state');

button.Position = [300 150 80 30];

button.Text = "STOP"


gauge = uigauge(fig1,'ScaleColors',{'yellow','red'},...
                 'ScaleColorLimits', [800 900; 900 1000]);
gauge.Position = [50 450 160 160];
gauge.Limits = [0 1000];

ax1 = uiaxes(fig1,'Position',[275 350 400 320]);
ax1.YLim = [0 1500];   
ax1.GridLineStyle = '-'
%set(ax,'Color','k')
% ax2 = uiaxes(fig1,'Position',[275 350 300 300]);
% ax2.YLim = [0 10]; 

gate = 'D6';
chA = 'D2';
chB = 'D3';


encoder = rotaryEncoder(uno,chA,chB, 378*48/7)
x=0;
i = 0;
y=0;
current = 0;
tic
while(i<20)
    if(i>5)    
    writePWMVoltage(uno, gate, 5);
    end
current = readVoltage(uno,'A4');
rpm = readSpeed(encoder)
%gauge.Value = rpm;
fprintf(encFile,'%d\n',rpm);
x = [x,rpm];
y = [y, current];
plot(x)
%plot(y./10);
%plot(ax1,abs(fft(x)))
drawnow
i=i+1;
end
toc
writePWMVoltage(uno, gate, 0);
fclose(encFile);
% 
% x=0;
% grid on 
% while(1)
% writePWMVoltage(uno, gate, slider.Value);
% rpm = readSpeed(encoder)
% gauge.Value = rpm;
% x=[x,rpm];
% plot(x)
% drawnow
% end
% 


%close(fig)

%  count = readCount(encoder);
%        pos = mod(count,48);
%        fprintf('Current knob position: %d\n',pos);