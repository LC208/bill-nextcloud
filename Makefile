XML_DIR = /usr/local/mgr5/etc/xml/
EXEC_DIR = /usr/local/mgr5/processing/
LOGO_DIR = /usr/local/mgr5/skins/common/plugin-logo

all: dependencies install

dependencies:
	apt install python3-pip
	apt install billmanager-plugin-python-libs
	pip install -r ./config/requirements.txt

install:
	# xml
	cp ./config/billmgr_mod_nextcloud.xml  $(XML_DIR)
	# main exec
	ln -snf $(shell pwd)/src/nextcloud.py $(EXEC_DIR)nextcloud
	chmod 775 $(EXEC_DIR)nextcloud
	cp ./assets/billmanager-plugin-nextcloud.png  $(LOGO_DIR)
	/usr/local/mgr5/sbin/mgrctl -m billmgr -R
