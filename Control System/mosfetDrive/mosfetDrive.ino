
int gate = 6;
int pot = A0;
int voltage = 0;

void setup() {
Serial.begin(9600);
pinMode(gate, OUTPUT);
pinMode(pot, INPUT);

}

void loop() {
voltage = analogRead(pot);
Serial.println(voltage);

analogWrite(gate, voltage);

}
