file:
	python3 gen_binary.py in.bin
encode: 
	python3 main.py -e in.bin out.bin
decode:
	python3 main.py -d out.bin check.bin
encode_zip:
	python3 main.py -e in.zip out.zip
decode_zip:
	python3 main.py -d out.zip check.zip
check:
	hexdump -c in.bin
	hexdump -c out.bin
	hexdump -c check.bin

clean:
	rm *.bin *.zip