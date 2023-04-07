#include <Arduino.h>
#include <Adafruit_NeoPixel.h>

Adafruit_NeoPixel linijka = Adafruit_NeoPixel(30, 3, NEO_GRB + NEO_KHZ800);

void setup() {
  Serial.begin(9600);
   
  linijka.begin();
  linijka.show();
  //linijka.setBrightness(120);

/*
  for (int i=0; i<15; i++) {
    linijka.setPixelColor(15+i, 30, 30, 30);
    linijka.setPixelColor(15-i, 30, 30, 30);
    linijka.show();
    delay(150);
  } 
*/

}

const int MAX_MESSAGE_LENGTH = 12;
String message;
String red;
String green;
String blue;
int ind1;
int ind2;
int ind3;

void loop() {
  if(Serial.available() > 0) {

    char input = Serial.read();

    if (input == '\n') {
      ind1 = message.indexOf(',');
      red = message.substring(0, ind1);
      ind2 = message.indexOf(',', ind1+1);
      green = message.substring(ind1+1, ind2);
      blue = message.substring(ind2+1);

      int int_red = red.toInt();
      int int_green = green.toInt();
      int int_blue = blue.toInt();

      //Serial.println(red);
      //Serial.println(green);
      //Serial.println(blue);

      for (int i=0; i<30; i++) {
        linijka.setPixelColor(i, int_red, int_green, int_blue);
        linijka.show();
      }

      message = "";
      red = "";
      green = "";
      blue = "";
    }
    else
    {
      message += input;
    }

  }
  
}

