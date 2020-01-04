NAME = "meshstats"
SOURCE_DIR = $(NAME)
VERSION = $(shell ack "\"version\":\s*\((\d+),\s*(\d+)\)" meshstats/__init__.py --output="\$$1.\$$2" --nocolor)
PACKAGE_NAME = $(NAME)-$(VERSION)
BUILD_DIR = ./release
ZIP_DIR = $(BUILD_DIR)/$(PACKAGE_NAME)

.DEFAULT_GOAL  := build

.PHONY: clean build relase tag version

build:
	@mkdir -p $(BUILD_DIR)/$(PACKAGE_NAME)
	@rsync -av --exclude="__pycache__" ./$(SOURCE_DIR) $(BUILD_DIR)/$(PACKAGE_NAME)
	@cp COPYING.txt $(BUILD_DIR)/$(PACKAGE_NAME)/$(SOURCE_DIR)
	@cd $(BUILD_DIR)/$(PACKAGE_NAME); zip -r "$(PACKAGE_NAME).zip" $(SOURCE_DIR)
	@mv $(BUILD_DIR)/$(PACKAGE_NAME)/$(PACKAGE_NAME).zip $(BUILD_DIR)/
	@echo "Created '$(BUILD_DIR)/$(PACKAGE_NAME)/$(PACKAGE_NAME).zip'"

clean:
	@rm -rf $(BUILD_DIR)
	@echo "Deleted $(BUILD_DIR)"

release: clean version build tag
	@echo "Done"

tag:
	@git tag -a "v$(VERSION)" -m "Version $(VERSION)"
	@echo "Created tag 'v$(VERSION)'"
	@echo "Don't forget to run:"
	@echo
	@echo "    git push origin --tags"

version:			
	@echo "Version = '$(VERSION)'"
