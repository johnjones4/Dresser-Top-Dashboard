OUTPUT_FILE := "/tmp/dashboard.bmp"
PLATFORM := $(shell uname)

packages:
ifeq ($(PLATFORM),Linux)
	apt-get install python3 libopenjp2-7 libjbig0 libwebp6 libtiff5 icu-devtools libicu-dev libxml2-dev libxslt1.1 libxslt1-dev
endif

bcm2835:
ifeq ($(PLATFORM),Linux)
	wget http://www.airspayce.com/mikem/bcm2835/bcm2835-1.60.tar.gz
	tar zxf bcm2835-1.60.tar.gz
	rm bcm2835-1.60.tar.gz
	cd bcm2835-1.60
	#TODO install dependencies
	./configure
	make
	sudo make check
	sudo make install
endif

IT8951:
ifeq ($(PLATFORM),Linux)
	wget https://www.waveshare.com/w/upload/1/15/IT8951.tar.gz
	tar zxf IT8951.tar.gz
	rm IT8951.tar.gz
	cd IT8951
	make IT8951
endif

open-sans:
	wget https://github.com/googlefonts/opensans/archive/master.zip
	unzip master.zip
	rm master.zip

pip:
	pip3 install -r requirements.txt

install: clean open-sans packages bcm2835 IT8951 pip

setup: install
	cp config.sample.yaml config.yaml

clean:
	rm -rf opensans-master || true
ifeq ($(PLATFORM),Linux)
	rm -rf bcm2835 || true
	rm -rf IT8951 || true
endif

generate: 
	python3 main.py $(OUTPUT_FILE)

display: generate
ifeq ($(PLATFORM),Darwin)
	open $(OUTPUT_FILE)
else
ifeq ($(PLATFORM),Linux)
	./IT8951/IT8951 0 0 $(OUTPUT_FILE)
endif
endif
