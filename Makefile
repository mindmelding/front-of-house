.PHONY: build check test all
build:
	python3 scripts/build_adapters.py
check:
	python3 scripts/fohcheck.py --repo
	python3 scripts/build_adapters.py --check
test: check
all: build check
