XML_DIR = /usr/local/mgr5/etc/xml/
EXEC_DIR = /usr/local/mgr5/processing/
LOGO_DIR = /usr/local/mgr5/skins/common/plugin-logo

all: dependencies install

dependencies:
	apt install python3-pip
	apt install billmanager-plugin-python-libs
	pip install -r ./config/requirements.txt

install:
	cp ./config/billmgr_mod_pmnextcloud.xml  $(XML_DIR)
	ln -snf $(shell pwd)/src/pmnextcloud.py $(EXEC_DIR)pmnextcloud
	chmod 775 $(EXEC_DIR)pmnextcloud
	cp ./assets/billmanager-plugin-pmnextcloud.png  $(LOGO_DIR)
	/usr/local/mgr5/sbin/mgrctl -m billmgr -R
