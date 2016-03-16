PYTHON ?= $(shell /usr/bin/env python)
DESTDIR ?=
PREFIX ?= /usr

EXTSCHEMAS := $(wildcard schema/*.extschema)
SANE_OVSSCHEMAS := $(patsubst %.extschema,%.ovsschema,$(EXTSCHEMAS))

.PHONY: all compile install clean

all: compile

%.ovsschema: %.extschema
	$(PYTHON) schema/sanitize.py $< $@

compile: $(SANE_OVSSCHEMAS)
	touch schema/vswitch.xml

install:
	install -d $(DESTDIR)/$(PREFIX)/share/openvswitch
	set -e; cd schema; for f in *.extschema *.ovsschema *.xml; do \
	    install -m 0644 $$f $(DESTDIR)/$(PREFIX)/share/openvswitch/$$f; \
	done

clean:
	rm -rf $(SANE_OVSSCHEMAS)

