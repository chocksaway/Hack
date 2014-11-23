#include "mbed.h"
#include <iostream>
#include <string>
#include <stdio.h>
#include <time.h>

Serial pc(USBTX, USBRX); // tx, rx

DigitalOut myled(LED1);
DigitalIn pb(p8);
// SPST Pushbutton demo using internal PullUp function
// no external PullUp resistor needed
// Pushbutton from P8 to GND.


int counter=0;
bool pushed = false;

const string currentDateTime() {
    time_t     now = time(0);
    struct tm  tstruct;
    char       buf[80];
    tstruct = *localtime(&now);
    // Visit http://en.cppreference.com/w/cpp/chrono/c/strftime
    // for more information about date/time format
    strftime(buf, sizeof(buf), "%Y-%m-%d.%X", &tstruct);

    return buf;
}


int main() {
    pb.mode(PullUp);
    while(1) {
        myled = pb;
        if (!pb) {
            pushed = true;
            pc.printf("Button pushed\r\n"); //Print each on each line
        }

        if (pb && pushed) {
            pushed = false;
            pc.printf("Button NOT pushed\r\n"); //Print each on each line
        }
    }
}