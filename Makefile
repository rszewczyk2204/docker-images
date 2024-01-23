SHELL := bash
DOCKER_CONTEXT := .
DOCKER_GROUP := rszewczyk2204/docker-images
DOCKER_SITE := ghcr.io
VERSION =
DIR =

image:
	docker build --pull -f $(DOCKER_DIR)/Dockerfile -t $(DOCKER_IMAGE_FULL) $(DOCKER_CONTEXT)

docker-push:
	docker push $(DOCKER_SITE)/$(DOCKER_IMAGE_FULL)

docker-rmi:
	docker rmi -f $(DOCKER_IMAGE_FULL)

build-%:
	$(MAKE) image DOCKER_IMAGE_FULL=$(DOCKER_GROUP)/$*:$(VERSION) DOCKER_DIR=$(DIR)
push-%:
	$(MAKE) docker-push DOCKER_IMAGE_FULL=$(DOCKER_GROUP)/$*:$(VERSION) DOCKER_DIR=$(DIR)
rmi-%:
	$(MAKE) docker-rmi DOCKER_IMAGE_FULL=$(DOCKER_GROUP)/$*:$(VERSION) DOCKER_DIR=$(DIR)
