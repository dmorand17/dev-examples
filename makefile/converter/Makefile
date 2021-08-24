JPEG=$(wildcard images/*.jpg images/*.jpeg) ## Has .jpeg and .jpg files

## Convert jpeg to jpg
JPG=$(JPEG:.jpeg=.jpg)						

## Convert jpg to png
PNG=$(JPG:.jpg=.png)

## .SUFFIXES: declaration. This tells make about all of the suffixes we will use in file suffixes
.SUFFIXES: .jpg .jpeg .png

# $< is the current dependency e.g. file.jpg
# $@ is the current target e.g. file.png

debug: 
	@echo "done!"
	@echo "JPEG values: $(JPEG)"
	@echo "JPG values: $(JPG)"
	@echo "PNG values: $(PNG)"

clean:
ifneq ("$(wildcard images/*.png)", "")	
	@rm images/*.png
	@echo "png images cleaned"
endif

webify: convert resize

convert: $(PNG)

resize: $(PNG)
	@echo "resizing file"
	## resize any images larger than 500px wide
	@mogrify -resize '500>' images/*.png
	@echo resizing is complete!

.jpeg.png .jpg.png:
	@echo "converting $< to $@ using ImageMagick..."
	convert $< $@
	@echo "conversion to $@ successful!"
