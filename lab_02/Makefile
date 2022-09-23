config.txt: 
	python3 make_config.py config.txt 3 256
input.bin: config.txt
	python3 gen_binary.py input.bin

encode: output.bin

decode: check.bin

output.bin: input.bin
	python3 enigma.py config.txt input.bin output.bin

check.bin: output.bin
	python3 enigma.py config.txt output.bin check.bin 

check: input.bin output.bin check.bin
	hexdump -c input.bin
	hexdump -c output.bin
	hexdump -c check.bin
clean:
	rm *.bin *.txt