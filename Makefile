# Build and preview this Carpentries Workbench lesson locally with Docker.
#
#   make preview   # rebuild the site, then refresh http://localhost:$(PORT)
#   make serve     # start a local web server for the built site
#   make clean     # drop the build cache (fixes stale-cache build errors)

LESSON := $(CURDIR)
IMAGE  := ghcr.io/carpentries/workbench-docker:latest
PORT   := 4321

.PHONY: preview serve clean help

preview: ## rebuild the site into site/docs
	docker run --rm --user rstudio -e DISABLE_AUTH=true \
	  -v "$(LESSON):/home/rstudio/lesson" $(IMAGE) \
	  Rscript -e 'sandpaper::build_lesson("/home/rstudio/lesson")'
	@echo "Built. Open http://localhost:$(PORT)  —  run 'make serve' if nothing is serving yet."

serve: ## serve site/docs at http://localhost:$(PORT)
	python3 -m http.server $(PORT) --bind 0.0.0.0 --directory "$(LESSON)/site/docs"

clean: ## remove the sandpaper build cache
	rm -rf "$(LESSON)/site" "$(LESSON)/.cache"

help: ## list targets
	@grep -E '^[a-z]+:.*##' $(MAKEFILE_LIST) | sed -E 's/:.*## /\t/'
