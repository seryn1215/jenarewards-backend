include env.secure
.PHONY: start-development
start-development: ## Start the development docker container.
	echo $(development) | base64 --decode > .env
	docker compose -f docker-compose.yml down
	docker compose -f docker-compose.yml up
create-base: ## Start the development docker container.
	echo $(development) | base64 --decode > .env
	docker compose -f docker-compose-base.yml up