PIXEL=500

all: clean generate

clean:
	rm -rf output

generate: export-svg export-png

export-svg:
	inkscape --export-plain-svg --export-text-to-path

export-png:
	mkdir output
	inkscape --export-png output/logo$(PIXEL)px.png --export-height=$(PIXEL) src/base.ink.svg

