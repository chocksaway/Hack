#include "mbed.h"
 
Serial pc(USBTX, USBRX); // tx, rx
 
DigitalOut myled(LED1);
DigitalIn pb(p8);
// SPST Pushbutton demo using internal PullUp function
// no external PullUp resistor needed
// Pushbutton from P8 to GND.

int main() {
    pb.mode(PullUp);
    while(1) {
        myled = pb;
        if (!pb) {
            pc.printf("Drawer Open\r\n"); //Print each on each line
        } else {
            pc.printf("Drawer NOT Open\r\n"); //Print each on each line 
        } 
    }
}