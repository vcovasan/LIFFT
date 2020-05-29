fig = uifigure;



gauge = uigauge(fig,'ScaleColors',{'yellow','red'},...
                 'ScaleColorLimits', [120 140; 140 150]);
gauge.Position = [200 200 120 120];

gauge.Limits = [0 150];



ENC_COUNT_REV = 245;
 
ENC_IN = 'D3';
  
encoderValue = 0;
 
interval = 1000;
 
previousMillis = 0;
currentMillis = 0;
 
rpm = 0;
 
motorPwm = 0;
 

  
  pinMode(ENC_IN, INPUT_PULLUP); 
   
  attachInterrupt(digitalPinToInterrupt(ENC_IN), updateEncoder, RISING);
  
  previousMillis = millis();

 
while(1)

  
  currentMillis = millis();
  if (currentMillis - previousMillis > interval) 
    previousMillis = currentMillis;
 
    rpm = (encoderValue * 60 / ENC_COUNT_REV);
 
    if (motorPwm > 0 || rpm > 0) 

      Serial.print('\t');
      Serial.print(" PULSES: ");
      Serial.print(encoderValue);
      Serial.print('\t');
      Serial.print(" SPEED: ");
      Serial.print(rpm);
      Serial.println(" RPM");
    end
    
    encoderValue = 0;
  end

end
function updateEncoder
  encoderValue++;
end