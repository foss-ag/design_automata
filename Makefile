PIXEL=500

all: clean generate

clean:
	rm -rf output

generate: export-svg export-png

export-svg:
	mkdir -p output
	inkscape --export-plain-svg=output/logo.svg --export-text-to-path src/base.ink.svg

export-png:
	mkdir -p output
	inkscape --export-png output/logo$(PIXEL)px.png --export-height=$(PIXEL) src/base.ink.svg

