const int OPAMP_IN = A0;
const int LED_OUT = 9;

const unsigned long TX_INTERVAL = 200;
unsigned long lTxTime = 0;

void setup() {
  Serial.begin(115200);
  pinMode(OPAMP_IN, INPUT);
  pinMode(LED_OUT, OUTPUT);

  analogWrite(LED_OUT, 255);
}

void loop() {
  unsigned long cTime = millis();
  // periodic sensor sampling and transmission ardu -> py
  if(cTime-lTxTime >= TX_INTERVAL){
    int rawLight = analogRead(OPAMP_IN);
    Serial.println(rawLight);
    lTxTime = cTime;
  }
  // async command pars py -> ardu
  if(Serial.available()>0){
    char inByte = Serial.read();

    exebright(inByte);
  }
}

void exebright(char action){
  switch(action){
    case '0':
      analogWrite(LED_OUT, 0);
      break;
    case '1':
      analogWrite(LED_OUT, 64);
      break;
    case '2':
      analogWrite(LED_OUT, 128);
      break;
    case '3':
      analogWrite(LED_OUT, 191);
      break;
    case '4':
      analogWrite(LED_OUT, 255);
      break;
    default:
      break;
  }
}
