key:
	python3 gen_key.py key.txt
file:
	python3 gen_binary.py in.bin
encode: 
	python3 main.py key.txt in.bin out.bin e
decode:
	python3 main.py key.txt out.bin check.bin d
encode_zip:
	python3 main.py key.txt test.zip out.bin e
decode_zip:
	python3 main.py key.txt out.bin check.zip d
check:
	hexdump -c in.bin
	hexdump -c out.bin
	hexdump -c check.bin	
clean:
	rm *.bin *.zip 