PIXEL=500
COLOR=foss-ag_green

all: clean generate

clean:
	rm -rf output

generate: export-svg export-png

export-svg: change-color 
	inkscape --export-plain-svg=output/logo.svg --export-text-to-path src/base.ink.svg

export-png: change-color
	inkscape --export-png output/logo$(PIXEL)px_$(COLOR).png --export-height=$(PIXEL) output/tmp.svg
change-color:
	mkdir -p output
	./changeStarColor.py $(COLOR)
