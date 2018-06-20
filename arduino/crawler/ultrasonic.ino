//checks to see if anything is in front of the robot

int ultrasonic(){                                       // Clears the trigPin
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);                                // Sets the trigPin on HIGH state for 10 micro seconds
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);                        // Reads the echoPin, returns the sound wave travel time in microseconds
  duration = pulseIn(echoPin, HIGH);                // Calculating the distance
  distance= duration*0.034/2;
  if (abs(distance - distance0) > 20){
    int iter = distance;
    distance = distance0;
    distance0 = iter;
  }
  if (distance <= 15 && distance>=0.5){
    stoop=1;
  }
  else{
    stoop=0;
    }
   return stoop;
}
