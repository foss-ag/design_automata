PIXEL=500
COLOR=foss-ag_green
OUTDIR=output

clean-gen: clean generate

clean:
	rm -rf $(OUTDIR)

clean-tmp:
	rm $(OUTDIR)/tmp.svg

generate: export-svg export-png

export-svg: create-out-dir change-color
	inkscape --export-plain-svg=$(OUTDIR)/logo.svg --export-text-to-path src/base.ink.svg

export-png: create-out-dir change-color
	inkscape --export-png $(OUTDIR)/logo$(PIXEL)px_$(COLOR).png --export-height=$(PIXEL) $(OUTDIR)/tmp.svg

change-color: create-out-dir
	./changeStarColor.py $(COLOR)

.PHONY create-out-dir:
	mkdir -p $(OUTDIR)
