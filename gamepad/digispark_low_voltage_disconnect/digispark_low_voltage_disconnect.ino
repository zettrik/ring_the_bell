/*  Use the digispark as low voltage disconnect to prevent batteries 
 *  from deep discharge. Connect a relais, mosfet to Pin0 and the 
 *  batteries + pol to Pin5.
 *  You might also want to connect a big red LED on Pin1, if the one onboard
 *  is to small for your purpose.
 *  
 *  The LVD itself will consume 25mA @ 12V.
 *  The power indicator LED uses ca 5mA. You can disable it with careful cut.
 *  You can flash with Arduino and select the board: Digispark 1MHz
 *  This will cut down the power needings in shutdown mode to 9mA @ 12V.
 *  
 */
 
// voltages from 0 eq. 0V to 1023 eq. 5V
// safe low voltage for li-ion is 3.3V a little above eq. 680
int low_voltage = 680;

// time (in seconds) to warn before shutoff
int lvd_delay = 5;


int voltage = 0;
int seconds = 0;

void setup() {
  /*  All pins are capable of Digital output.
   *  Although P5 is 3V at HIGH instead of 5V. 
   *  Pin numbers for digitalWrite match e.g. 0 is P0, 2 is P2.
   *  Keep in mind analogWrite and analogRead use different numbers.
   *  P0, P1, and P4 are capable of hardware PWM (analogWrite)
   *  P2, P3, P4 and P5 have ADCs (analogRead)
   */
  pinMode(0, OUTPUT); // analogWrite(0, x)
  pinMode(1, OUTPUT); // analogWrite(1, x)
  pinMode(2, INPUT); // analogRead(1)
  pinMode(3, INPUT); // analogRead(3)
  pinMode(4, OUTPUT); // analogWrite(4, x)
  //pinMode(4, INPUT); // analogRead(2)
  pinMode(5, INPUT); // analogRead(0)
}

// the main loops runs round about once per second
void loop() {
  // read voltage of battery connected to Pin5
  voltage = analogRead(0);

  if (voltage <= low_voltage) {
    // warn users for 10 min with red LED switched on
    // but keep mosfet still switched on 
    if (seconds < lvd_delay) {
      seconds++;
      digitalWrite(0, 1);
      // continous red light to warn before low power shutdown
      digitalWrite(1, 1);
      delay(1000);
    }
    // after 600 seconds with low voltage switch mosfet off
    // to safe power let red LED blink shortly
    // stay in this state as long as voltage stays low
    else {
      seconds = lvd_delay;
      digitalWrite(0, 0);
      // short flash to signal shutdown mode
      digitalWrite(1, 1);
      delay(50);
      digitalWrite(1, 0);
      delay(950);
    }
  }
  
  // 0 seconds since last low voltage where measured, 
  // voltage is okay, mosfet on, LED is blinking slowly
  else {
    seconds = 0;
    digitalWrite(0, 1);
    // heartbeat
    digitalWrite(1, 0);
    delay(500);
    digitalWrite(1, 1);
    delay(500);
    digitalWrite(1, 0);
  }
}
