build:
	hugo --cleanDestinationDir

run: build
	hugo server -D --disableFastRender
