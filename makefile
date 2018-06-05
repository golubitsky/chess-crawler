APP_NAME ?= scalable-app
PORT ?= 3000
WORKERS ?= 1
THREADS ?= 1

build:
	docker build -qt $(APP_NAME) .

run: build
	docker run -v $(PWD):/usr/src/app -p $(PORT):$(PORT) -it --rm --name running-$(APP_NAME) $(APP_NAME) gunicorn \
    --threads $(THREADS) -e THREADS=$(THREADS) \
    -w $(WORKERS) -e WORKERS=$(WORKERS) \
    --worker-class gthread \
    -b 0.0.0.0:$(PORT) wsgi:app

test: build
	PYTHONDONTWRITEBYTECODE=1 # no __pycache__ files
	docker run -v $(PWD):/usr/src/app \
	--rm -it --name test-$(APP_NAME) $(APP_NAME) \
	python -Bm nose --rednose --with-watch