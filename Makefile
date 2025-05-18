MGR = billmgr
PLUGIN = pmnextcloud

SRC=$(shell pwd)

dist-prepare: $(DISTDIR)/processing/pmnextcloud
$(DISTDIR)/processing/pmnextcloud: $(SRC)/pmnextcloud.py
	@echo "NextCloud: Copy pmnextcloud module"
	@mkdir -p $(DISTDIR)/processing && \
		ln -snf $(SRC)/src/pmnextcloud.py $(DISTDIR)/processing/pmnextcloud && \
		chmod 744 $(DISTDIR)/processing/pmnextcloud


BASE ?= /usr/local/mgr5
include $(BASE)/src/isp.mk