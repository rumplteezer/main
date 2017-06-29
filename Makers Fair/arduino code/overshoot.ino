#include <math.h>

// physics
int index;
float power = 0.001;
float power_o = 0.001;
float l_eff;
float tou;
float rho;

// rod positions
int pulse_posn = 1100;
int safety_posn = 340;
int shim_posn = 800;
int reg_posn = 100;

// rod controls
int pin_pwr = 13;
int pin_glow = 8;
int pin_posn = A0;
int pulse_up =52;
int pulse_down = 50;
int safety_up = 48;
int safety_down = 46;
int shim_up = 28;
int shim_down= 30;
int reg_up = 26;
int reg_down = 24;

// arrays
int i;
float powers[100];

// functions
float reg_rho(int x){
  float result;
  result = (1.11e-12)*pow(x,4)-(3.8e-9)*pow(x,3)+(3.46e-6)*pow(x,2)+(1.49e-4)*x-(4.41e-2);
  return result;
}
float shim_rho(int x){
  float result;
  result = (1.01e-12)*pow(x,4)-(6.53e-9)*pow(x,3)+(8.95e-6)*pow(x,2)-(1.42e-3)*x+(6.57e-2);
  return result;
}
float safety_rho(int x){
  float result;
  result = (1.13e-12)*pow(x,4)-(5.39e-9)*pow(x,3)+(5.95e-6)*pow(x,2)+(4.51e-5)*x-(5.38e-2);
  return result;
}
float pulse_rho(int x){
  float result;
  result = (2.9e-12)*pow(x,4)-(1.15e-8)*pow(x,3)+(1.25e-5)*pow(x,2)-(1.24e-3)*x-(2.32e-2);
  return result;
}

void setup() {
for (i=0;i<100;i++){
  powers[i] = power_o;
}
pinMode(pin_pwr,OUTPUT);
pinMode(pin_glow,OUTPUT);
pinMode(pin_posn,INPUT);
pinMode(3,OUTPUT);
pinMode(3,HIGH);
Serial.begin(9600);

}

void loop() {
if ((digitalRead(pulse_up)==LOW) and (pulse_posn<1100)){
  pulse_posn+=6;
}
if ((digitalRead(pulse_down)==LOW) and (pulse_posn>100)){
  pulse_posn-=8;
}
if ((digitalRead(safety_up)==LOW) and (safety_posn<1100)){
  safety_posn+=6;
}
if ((digitalRead(safety_down)==LOW) and (safety_posn>100)){
  safety_posn-=8;
}
if ((digitalRead(shim_up)==LOW) and (shim_posn<1100)){
  shim_posn+=6;
}
if ((digitalRead(shim_down)==LOW) and (shim_posn>100)){
  shim_posn-=8;
}
if ((digitalRead(reg_up)==LOW) and (reg_posn<1100)){
  reg_posn+=6;
}
if ((digitalRead(reg_down)==LOW) and (reg_posn>100)){
  reg_posn-=8;
}  

rho = ((pulse_rho(pulse_posn) + shim_rho(shim_posn) + safety_rho(safety_posn) + reg_rho(reg_posn))*.007-.03);

index = power/10;
if (index > 99){
  index=99;
}
if (index < 4){
  index=4;
}
p_ave = powers[(index)]+powers[(index-1)]+powers[(index-2)]+powers[(index-3)]+powers[(index-4)]

rho = rho - .0045*(powers[(index)])*.007;

if (rho < -0.0035){
  rho = -0.0035;
}

if (rho>=0.00546){
  power = 0;
  rho = 0;
}
if (rho>0){
  l_eff = 0.08;
}
if (rho<=0){
  l_eff = 0.124;
}

tou = 0.000045 / rho + (0.007 - rho)/(l_eff*rho);
power = power *exp(0.25/tou);
for (i = 0; i <99; i++){
  powers[i]=powers[i+1];
}
powers[99]=power;

if ((power < power_o) and (power != 0)){
  power = power_o;
}
if (power >=10000){
  power = 0;
}
/*  This is the driver for an analog power meter and increase light to simulate chrenkov glow.
analogWrite(pin_pwr, power*2.55);
for (i = 5; i <9; i++){
  analogWrite(i,power*255/110);
}
*/
analogWrite(pin_glow, power*255/110);
delay(250);

if (power == 0){
  tou = 0;
}
Serial.println(pulse_posn + String(",") + safety_posn + String(",") + shim_posn + String(",") + reg_posn + String(",") + power*100 + String(",") + tou + String(",") + rho/.007);
}
