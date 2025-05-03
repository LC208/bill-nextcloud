XML_DIR = /usr/local/mgr5/etc/xml/
EXEC_DIR = /usr/local/mgr5/processing/
LOGO_DIR = /usr/local/mgr5/skins/common/plugin-logo

all: detect_os dependencies install

OS := $(shell grep ^ID= /etc/os-release | cut -d= -f2 | tr -d \")

detect_os:
	@echo "Detected OS: $(OS)"

dependencies:
ifneq (,$(filter $(OS),ubuntu astra))
	sudo apt update
	@if ! dpkg -s python3-pip >/dev/null 2>&1; then \
		echo "Installing python3-pip..."; \
		sudo apt install -y python3-pip; \
	else echo "python3-pip already installed."; fi
	@if ! dpkg -s billmanager-plugin-python-libs >/dev/null 2>&1; then \
		echo "Installing billmanager-plugin-python-libs..."; \
		sudo apt install -y billmanager-plugin-python-libs; \
	else echo "billmanager-plugin-python-libs already installed."; fi
	pip3 install --upgrade pip
	pip3 install -r ./config/requirements.txt

else ifeq ($(OS),almalinux)
	@if ! rpm -q python3-pip >/dev/null 2>&1; then \
		echo "Installing python3-pip..."; \
		sudo dnf install -y python3-pip; \
	else echo "python3-pip already installed."; fi
	@if ! rpm -q billmanager-plugin-python-libs >/dev/null 2>&1; then \
		echo "Installing billmanager-plugin-python-libs..."; \
		sudo dnf install -y billmanager-plugin-python-libs; \
	else echo "billmanager-plugin-python-libs already installed."; fi
	pip3 install --upgrade pip
	pip3 install -r ./config/requirements.txt

else
	$(error Unsupported OS: $(OS))
endif

install:
	cp ./config/billmgr_mod_pmnextcloud.xml  $(XML_DIR)
	ln -snf $(shell pwd)/src/pmnextcloud.py $(EXEC_DIR)pmnextcloud
	chmod 775 $(EXEC_DIR)pmnextcloud
	cp ./assets/billmanager-plugin-pmnextcloud.png  $(LOGO_DIR)
	/usr/local/mgr5/sbin/mgrctl -m billmgr -R
