int trig = 32;
int echo = 35;

int readings[5]; // array of readings 
int currentIndex = 0; // index of the current reading
int total = 0; 
int average = 0; 

void setup() {
    pinMode(trig, OUTPUT); 
    pinMode(echo, INPUT);
    Serial.begin(115200);
    for (int i = 0; i < 5; i++) {
      readings[i] = 0; // initialize all readings to 0
    }
}
 
void loop() { 
    // subtract the last reading
    total = total - readings[currentIndex];
    // read distance from the sensor
    readings[currentIndex] = readDistance();
    total = total + readings[currentIndex];
    if (currentIndex >= 5) {
      currentIndex = 0;
    }
    average = total / 5;
    Serial.println(average);
    delay(1);
}

int readDistance() {
    long unsigned duration = 0;
    int distance = 0;

    digitalWrite(trig, LOW);
    delayMicroseconds(5);
    digitalWrite(trig, HIGH);
    delayMicroseconds(20);
    digitalWrite(trig, LOW);
    
    duration = pulseIn(echo, HIGH);
    distance = (duration * 0.034)/2;
    return distance;
}
