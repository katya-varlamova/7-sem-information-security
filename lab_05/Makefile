key:
	python3 main.py -g
file:
	python3 gen_binary.py in.bin
	python3 gen_binary.py check.bin

sig: 
	python3 main.py -s in.bin signature.sig
check:
	python3 main.py -c in.bin signature.sig
check2:
	python3 main.py -c check.bin signature.sig
dump:
	hexdump -c in.bin
	hexdump -c check.bin	
sig_zip:
	python3 main.py -s in.zip signature_zip.sig
check_zip:
	python3 main.py -c in.zip signature_zip.sig
check_zip2:
	python3 main.py -c check.zip signature_zip.sig
clean:
	rm *.bin *.sig *.pub *.pri