DESTDIR ?=
PREFIX ?= /usr

EXTSCHEMAS := $(wildcard schema/*.extschema)
SANE_OVSSCHEMAS := $(patsubst %.extschema,%.ovsschema,$(EXTSCHEMAS))
EXTXMLS := $(wildcard schema/*.xml)
SANE_OVSXMLS := $(patsubst %.xml,%.xml.untag,$(EXTXMLS))

.PHONY: all compile install clean

all: compile

%.ovsschema: %.extschema
	if [ -f $(TOPDIR)/.ops-config ]; \
	then \
		${PYTHON} schema/schemaprune_json.py -i $< -o $<.untag -f ${BUILD_ROOT}/images/image_features -l $<.schemaprune.log -L INFO -S FALSE; \
	else \
		${PYTHON} schema/schemaprune_json.py -i $< -o $<.untag -f ${BUILD_ROOT}/images/image_features -l $<.schemaprune.log.$< -L INFO -S TRUE; \
	fi ; \
	schema/sanitize.py $<.untag $@

%.xml.untag: %.xml
	if [ -f $(TOPDIR)/.ops-config ]; \
	then \
		${PYTHON} schema/schemaprune_xml.py -i $< -o $@ -f ${BUILD_ROOT}/images/image_features -l $<.schemaprune.log -L INFO -S FALSE; \
	else \
		${PYTHON} schema/schemaprune_xml.py -i $< -o $@ -f ${BUILD_ROOT}/images/image_features -l $<.schemaprune.log -L INFO -S TRUE; \
	fi ; \

compile: $(SANE_OVSSCHEMAS) $(SANE_OVSXMLS)
	touch schema/vswitch.xml

install:
	install -d $(DESTDIR)/$(PREFIX)/share/openvswitch
	set -e; cd schema; for f in *.extschema *.ovsschema; do \
	    install -m 0644 $$f $(DESTDIR)/$(PREFIX)/share/openvswitch/$$f; \
	done; \
	install -m 0644 vswitch.xml.untag $(DESTDIR)/$(PREFIX)/share/openvswitch/vswitch.xml; \
	install -m 0644 dhcp_leases.xml.untag $(DESTDIR)/$(PREFIX)/share/openvswitch/dhcp_leases.xml; \
	install -m 0644 vtep.xml.untag $(DESTDIR)/$(PREFIX)/share/openvswitch/vtep.xml

clean:
	rm -rf $(SANE_OVSSCHEMAS) $(SANE_OVSXMLS) schema/*.log

