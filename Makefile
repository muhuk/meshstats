NAME = "meshstats"
VERSION = $(shell ack "\"version\":\s*\((\d+),\s*(\d+)\)" meshstats/__init__.py --output="\$$1.\$$2" --nocolor)
PACKAGE_NAME = $(NAME)-$(VERSION)

SOURCE_DIR = $(NAME)
BUILD_DIR = ./release
SCRIPTS_DIR = ./scripts
ZIP_DIR = $(BUILD_DIR)/$(PACKAGE_NAME)

BLENDER_PATH = ~/lib/blender/blender-2.82a-linux64/

.DEFAULT_GOAL  := run

.PHONY: clean build relase run tag version

build:
	@mkdir -p $(BUILD_DIR)/$(PACKAGE_NAME)
	@rsync -av --exclude="__pycache__" ./$(SOURCE_DIR) $(BUILD_DIR)/$(PACKAGE_NAME)
	@cp COPYING.txt $(BUILD_DIR)/$(PACKAGE_NAME)/$(SOURCE_DIR)
	@cd $(BUILD_DIR)/$(PACKAGE_NAME); zip -r "$(PACKAGE_NAME).zip" $(SOURCE_DIR)
	@mv $(BUILD_DIR)/$(PACKAGE_NAME)/$(PACKAGE_NAME).zip $(BUILD_DIR)/
	@echo "Created '$(BUILD_DIR)/$(PACKAGE_NAME).zip'"

check:
	@flake8 --show-source $(SOURCE_DIR)

clean:
	@rm -rf $(BUILD_DIR)
	@echo "Deleted $(BUILD_DIR)"

release: clean check version build tag
	@echo "Done"

run: clean check build
	ZIP_FILE=`realpath "$(BUILD_DIR)/$(PACKAGE_NAME).zip"` \
	$(BLENDER_PATH)/blender -d \
		--debug-python \
		--factory-startup \
		-P $(SCRIPTS_DIR)/install_addon.py \
		./dev.blend
	@echo "Done"

tag:
	@git tag -a "v$(VERSION)" -m "Version $(VERSION)"
	@echo "Created tag 'v$(VERSION)'"
	@echo "Don't forget to run:"
	@echo
	@echo "    git push origin --tags"

version:			
	@echo "Version = '$(VERSION)'"
