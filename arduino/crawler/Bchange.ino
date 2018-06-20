//changes in A factor which happens if the encoder rotates in one direction

void Bchange()
{
  A = digitalRead(2);
  B = digitalRead(3);

  if ((A==HIGH)&&(B==HIGH)) state = 1;
  if ((A==HIGH)&&(B==LOW)) state = 2;
  if ((A==LOW)&&(B==LOW)) state = 3;
  if((A==LOW)&&(B==HIGH)) state = 4;
  switch (state)
  {
    case 1:
    {
      if (statep == 2) count++;
      if (statep == 4) count--;
      break;
    }
    case 2:
    {
      if (statep == 1) count--;
      if (statep == 3) count++;
      break;
    }
    case 3:
    {
      if (statep == 2) count --;
      if (statep == 4) count ++;
      break;
    }
    default:
    {
      if (statep == 1) count++;
      if (statep == 3) count--;
    }
  }
  statep = state;
}
