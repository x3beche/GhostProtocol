//~ 1 - GND
//~ 2 - VCC 3.3V !!! NOT 5V
//~ 3 - CE to Arduino pin 7
//~ 4 - CSN to Arduino pin 8
//~ 5 - SCK to Arduino pin 13
//~ 6 - MOSI to Arduino pin 11
//~ 7 - MISO to Arduino pin 12
//~ 8 - UNUSED

#include <printf.h>
#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>
#define CE_PIN  7
#define CSN_PIN 8
RF24 radio(CE_PIN, CSN_PIN); // Create a Radio

const uint64_t deviceID = 0xE8E8F0F0E1LL;
const byte numChars = 32;
byte ackMessgLen = 4; // NB this 4 is the number of bytes in the 2 ints that will be recieved
char  dataToSend[32];
char  dataReceived[32];
char  ackData[2] = {1,2};
char  ackMessg[2]= {1,2};
boolean newData = false;

void setup() {
    Serial.begin(115200);
    printf_begin();
    radio.begin();
    radio.setDataRate( RF24_2MBPS );
    radio.setPALevel(RF24_PA_MAX);
    radio.enableAckPayload();
    radio.openReadingPipe(1,deviceID);
    radio.startListening();
    radio.enableAckPayload();
    radio.writeAckPayload(1, ackData, sizeof(ackData));
    radio.setRetries(15,15); // delay, count
    pinMode(2, OUTPUT);
    radio.printDetails();
}

void loop() {
    serialread();
    if (newData==true) tx();
    if (radio.available()) rx();
}

void rx(){
        radio.read( dataReceived, sizeof(dataReceived) );
        for (int x = 0; x <32; x++)
        {
        radio.writeAckPayload(1, ackData, sizeof(ackData));
        Serial.print(dataReceived[x]);
        }
        Serial.println();
}

void tx() {
      radio.openWritingPipe(deviceID);
      radio.stopListening();
      bool rslt;
      rslt = radio.write( dataToSend, sizeof(dataToSend) );
      if ( radio.isAckPayloadAvailable() ) 
        {
        digitalWrite(2, HIGH);
        radio.read(ackMessg,ackMessgLen);
        Serial.println("code[200]");
        newData = false;
        digitalWrite(2, LOW);
        for( int i = 0; i < sizeof(dataToSend); ++i) dataToSend[i] = (char)0;
        }
      else {Serial.println("code[417]");}
      newData = false;
      radio.openReadingPipe(1,deviceID);
      radio.startListening();
      radio.enableAckPayload();
      radio.writeAckPayload(1, ackData, sizeof(ackData));
      }

void serialread() {
  static byte ndx = 0;
  char endMarker = '\n';
  char rc;
  while (Serial.available() > 0 && newData == false) {
    rc = Serial.read();
    if (rc != endMarker) {
      dataToSend[ndx] = rc;
      ndx++;
    if (ndx >= numChars) {
  ndx = numChars - 1; }}
  else {
  dataToSend[ndx] = '\0'; // terminate the string
  ndx = 0;
  newData = true;}}}
