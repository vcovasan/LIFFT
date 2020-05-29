
gate = 'D6';
pot = 'A0';
%voltage = 0;

% setup
% Serial.begin(9600);
%pinMode(gate, OUTPUT);
%pinMode(pot, INPUT);



while(1)
    
voltage = readVoltage(uno, pot);
%Serial.println(voltage);

writePWMVoltage(uno, gate,voltage)
%analogWrite(gate, voltage);

end
