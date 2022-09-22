#include <stdio.h>
#include <string.h>
extern int start();
// INSTALLATION_SERIAL
int main() {
    char serial_num[128];
    const char * com = "ioreg -l | awk '/IOPlatformSerialNumber/ { print $4;}' | awk -F'\"' '{ print $2; }'";
    FILE * pipe = popen(com, "r");
    fgets(serial_num, 128, pipe);
    serial_num[strlen(serial_num) - 1] = '\0';
    pclose(pipe);
    if (strcmp(serial_num, INSTALLATION_SERIAL) == 0) {

        start();
    }
    else {
        printf("access denied!");
    }

    return 0;
}
