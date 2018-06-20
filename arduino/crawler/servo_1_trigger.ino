//changes the positon of servo 1

void degreePos_1(float motorPos1) {
    Ser_M1.attach(motorPinAttach_1);
    Ser_M1.write(180 - motorPos1);
    delay(300);
    }
