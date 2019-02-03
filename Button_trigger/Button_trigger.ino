
long last_event = -1;

//#include <Adafruit_NeoPixel.h>

// constants won't change. They're used here to set pin numbers:
const int buttonPin = 2;     // the number of the pushbutton pin
const int buttonPin2 = 3;     // the number of the pushbutton pin
const int strip_pin = 7;

//Adafruit_NeoPixel strip = Adafruit_NeoPixel(5, strip_pin, NEO_RGBW);

const int ledPin =  13;      // the number of the LED pin

volatile byte state1 = LOW;
volatile byte state2 = LOW;
volatile byte state3 = LOW;



int msg = 0;

void setup() {
  Serial.begin(115200);
  // initialize the LED pin as an output:
  pinMode(ledPin, OUTPUT);
  // initialize the pushbutton pin as an input:
  pinMode(buttonPin, INPUT_PULLUP);
  pinMode(buttonPin2, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(buttonPin), blink1, FALLING); // on connection?
  attachInterrupt(digitalPinToInterrupt(buttonPin2), blink2, FALLING); // Change

//  pinMode(strip_pin, OUTPUT);
//
//  strip.begin();
//  strip.show(); // Initialize all pixels to 'off'
//  strip.setPixelColor(0, 255, 0, 0);
//  strip.show();
//  Serial.println("init");
}


int event_length = 400;

void blink1() {
  state1 = 1;
//  Serial.println("1");
msg = max(1, msg);

  long now = millis();
  long dt = now-last_event;
   
  if (dt < event_length)
  {
     return;
  } 

  last_event = now;
}

void blink2() {
  state2 = 1;
//  Serial.println("2");
msg = max(2, msg);


  long now = millis();
  long dt = now-last_event;
   
  if (dt < event_length)
  {
     return;
  } 

  last_event = now;
}

void blink3() {
  state1 = 3;
//  Serial.println("3");
msg = max(3, msg);


  long now = millis();
  long dt = now-last_event;
   
  if (dt < event_length)
  {
     return;
  } 

  last_event = now;
}


void loop() {
    // digitalWrite(ledPin, state);


//Serial.println(last_event);
//delay(20);
      

    if (last_event < 0)
      return;

    // end of event:
    int now = millis();
    int dt = now-last_event;

    if (dt > event_length)
    {
      // check who was triggered in the last event duration and send this value
      
//      Serial.write("event end");
      Serial.println(msg);
//      Serial.print(state2);
//      Serial.print(state3);
//      Serial.println(".");

      msg = 0;
      state1 = 0;
      state2 = 0;
      state3 = 0;

      last_event = -1;
    }
}
