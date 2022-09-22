import os

with open("main.c", "w") as s:
    with open("template.c") as f:
        for line in f:
            if line == '// INSTALLATION_SERIAL\n':
                serial = os.popen("ioreg -l | awk '/IOPlatformSerialNumber/ { print $4;}' | awk -F'\"' '{ print $2; }'").read().split("\n")[0]
                s.write('#define INSTALLATION_SERIAL "{}"\n'.format(serial))
            else:
                s.write(line)
        
print(os.popen("gcc -c main.c -o main.o && gcc -L. -lapp_lib main.o -o app && rm main.c main.o && echo 'installation succeded!\n' && ./app").read())
