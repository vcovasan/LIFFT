// Motor encoder output pulse per rotation (change as required)
#define ENC_COUNT_REV 245
 
// Encoder output to Arduino Interrupt pin
#define ENC_IN 3 
  
// Pulse count from encoder
volatile long encoderValue = 0;
 
// One-second interval for measurements
int interval = 1000;
 
// Counters for milliseconds during interval
long previousMillis = 0;
long currentMillis = 0;
 long motorTiming = 0;
 long timeNow = 0;
// Variable for RPM measuerment
int rpm = 0;
 
// Variable for PWM motor speed output
int motorPwm = 0;
 
void setup()
{
  // Setup Serial Monitor
  Serial.begin(9600); 
  
  // Set encoder as input with internal pullup  
  pinMode(ENC_IN, INPUT_PULLUP); 
   
  // Attach interrupt 
  attachInterrupt(digitalPinToInterrupt(ENC_IN), updateEncoder, RISING);
  
  // Setup initial values for timer
  previousMillis = millis();
  motorTiming = millis();
}
 
void loop()
{
timeNow = millis();
while(round((timeNow-motorTiming)/1000)%5==0){
analogWrite(6,255);
rpm = getRpm();  
 }
rpm = getRpm();


}

int getRpm(){
 // Update RPM value every second
  currentMillis = millis();
  if (currentMillis - previousMillis > interval) {
    previousMillis = currentMillis;
 
 
    // Calculate RPM
    rpm = (float)(encoderValue * 60 / ENC_COUNT_REV);
 
    // Only update display when there is a reading
    Serial.println(rpm);
    
    encoderValue = 0;
  }
  return rpm;
  
}
 void runMotor(){
  delay(1000);
    analogWrite(6,0);
    delay(1000);
      analogWrite(6,255);

  }
void updateEncoder()
{
  // Increment value for each pulse from encoder
  encoderValue++;
}
