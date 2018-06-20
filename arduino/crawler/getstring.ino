//get the string which is coming form the Serial port (USB)
//which is the connection between arduino and python
void getstring(){
  double S1_double , S2_double = 0;
  while(1){
  if (Serial.available()){
    count = 0;
      String a = "", S1="", S2="";

      // get the string from the usb and then slice it into the usefull numbers
      // in this case the numbers are being trasmitted using the utf-8 protocol
      // and the body of the string is like this number&number exp : 25&67
      
      a = Serial.readString();
      Serial.flush();
      int j ;
      
      //slice the string into the 2 groups
      
      for (int i=0 ; i < a.length()-2;i++){
        if (a[i] == '&'){
          j = i ;
        }
      }
      
      // use the substrings
      
      S1 = a.substring(0, j);

      //if using arduino: S2 = a.substring(j+1, a.length()-1);
      //if using python: S2 = a.substring(j+1);
      
      S2 = a.substring(j+1);
      
      S1_double = string_to_double(S1);
      S2_double = string_to_double(S2);
      
      break;
    }
  }
  print_servo(S1_double, S2_double);
}
