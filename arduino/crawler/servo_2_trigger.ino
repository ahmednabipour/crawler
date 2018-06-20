//changes the positon of servo 2

  void degreePos_2(float motorPos2) {
    Ser_M2.attach(motorPinAttach_2);
    Ser_M2.write(150 - motorPos2);
    delay(300);

  
  }
