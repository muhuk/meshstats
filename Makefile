NAME = "meshstats"
VERSION = $(shell ack "^version\s*=\s*\"([\d\.]+)\"" blender_manifest.toml --output="\$$1" --nocolor)
PACKAGE_NAME = $(NAME)-$(VERSION)

SOURCE_DIR = $(NAME)
BUILD_DIR = ./release

BLENDER_CMD := "blender"


.DEFAULT_GOAL := check

.PHONY: clean build release check tag version

build:
	@mkdir -p $(BUILD_DIR)/$(PACKAGE_NAME)
	@rsync -av --exclude-from=build_excludes.txt ./$(SOURCE_DIR)/ $(BUILD_DIR)/$(PACKAGE_NAME)/$(NAME)
	@cp COPYING.txt $(BUILD_DIR)/$(PACKAGE_NAME)/$(NAME)
	@cp CHANGELOG.md $(BUILD_DIR)/$(PACKAGE_NAME)/$(NAME)
	@cp blender_manifest.toml $(BUILD_DIR)/$(PACKAGE_NAME)/$(NAME)
	@$(BLENDER_CMD) --command extension build --source-dir $(BUILD_DIR)/$(PACKAGE_NAME)/$(NAME) --output-dir $(BUILD_DIR)
	@echo "Created '$(BUILD_DIR)/$(PACKAGE_NAME).zip'"

check:
	@flake8 --show-source $(SOURCE_DIR)

clean:
	@rm -rf $(BUILD_DIR)
	@echo "Deleted $(BUILD_DIR)"

release: clean check version build tag
	@echo "Done"

tag:
	@git tag -a "v$(VERSION)" -m "Version $(VERSION)"
	@echo "Created tag 'v$(VERSION)'"
	@echo "Don't forget to run:"
	@echo
	@echo "    git push origin --tags"

version:
	@echo "Version = '$(VERSION)'"
