//this function checks the ultrasonic module and if there is nothing 
//in front of the robot it allow the robot to do its move

void print_servo(double Servo_1, double Servo_2) {
while(1){
    if (ultrasonic() == 0){
    degreePos_1(Servo_1);
    degreePos_2(Servo_2);
    degreePos_1(0);
    degreePos_2(0);
    Serial.println(100*count);
    break;
      }
    }
}

    
    

 

