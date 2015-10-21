/* 
 * Arm_Controller.ino
 * SIUC Robotics Programming Team
 * ATMAE Conference 2015
 * October 21, 2015
 */

int basePin = A0;
int shoulderPin = A1;
int elbowPin = A2;
int clawPin = A3;

int baseIn = 0;
int shoulderIn = 0;
int elbowIn = 0;
int clawIn = 0;

char dataToSend[13];

int i = 0;

void setup() {
  pinMode(basePin, INPUT);
  pinMode(shoulderPin, INPUT);
  pinMode(elbowPin, INPUT);
  pinMode(clawPin, INPUT);
  Serial.begin(115200);
  delay(500);
}

void loop() {
  baseIn = (analogRead(basePin) / 4); // reading of ~[0-1024] divided by 1024, times 256 --> range * (256/1024) --> range / 4, range is now ~[0-255]
  shoulderIn = (analogRead(shoulderPin) / 4);
  elbowIn = (analogRead(elbowPin) / 4);
  clawIn = (analogRead(clawPin) / 4);

  for (i = 0; i < 13; i++)
    if (i != 12)
      dataToSend[i] = '0';
    else
      dataToSend[i] = '\0';

  updateData(baseIn, 0);
  updateData(shoulderIn, 3);
  updateData(elbowIn, 6);
  updateData(clawIn, 9);
  
  Serial.write(dataToSend, 12); // write the data string to serial
  Serial.write('\n');  // terminate serial with newline
}

void updateData(int val, int place) {
  char temp[4];
  itoa(val, temp, 10);
  
  if (val > 99) {
    dataToSend[place] = temp[0];
    dataToSend[place + 1] = temp[1];
    dataToSend[place + 2] = temp[2];
  } else if (val > 99) {
    dataToSend[place] = '0';
    dataToSend[place + 1] = temp[0];
    dataToSend[place + 2] = temp[1];
  } else {
    dataToSend[place] = '0';
    dataToSend[place + 1] = '0';
    dataToSend[place + 2] = temp[0];
  }
}
