init-pre-commit:
	git config --global url."https://".insteadOf git://
	pre-commit install
	pre-commit run --all-files

update-pre-commit:
	pre-commit autoupdate

nuitka-build:
	poetry install --only main
	pip install -U nuitka
	export NUITKA_CACHE_DIR=`pwd`/dist/cache
	python -m nuitka \
		--follow-imports \
		--standalone \
		--clang \
		--output-dir=dist \
		cheep_app.py
	cp .env ./dist/cheep_app.dist

build-docker-image:
	docker build \
		--platform linux/arm/v7 \
		-t cheep:latest .

docker-bash:
	docker run \
		-v `pwd`:/app \
		-it \
		--rm cheep:latest \
		bash

docker-build:
	docker run \
		--platform linux/arm/v7 \
		-v `pwd`:/app \
		--rm cheep:latest make nuitka-build

deploy:
	scp -O -oHostKeyAlgorithms=+ssh-rsa -r \
		dist/cheep_app.dist/* root@jdcloudwifi.com:/opt/apps
