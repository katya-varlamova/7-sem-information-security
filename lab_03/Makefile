key:
	python3 gen_key.py key.txt
file:
	python3 gen_binary.py in.bin
encode: 
	python3 main.py key.txt in.bin out.bin e
decode:
	python3 main.py key.txt out.bin check.bin d
check:
	hexdump -c in.bin
	hexdump -c out.bin
	hexdump -c check.bin	
clean:
	rm *.bin