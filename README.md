# Docs

## Install dependencies

```sh
uv python install 3.12
uv init --python=3.13.0 isbn
uv add  "numpy==1.26.4" "pandas==2.2.2" "scrapy==2.11.2" "python-dotenv==1.0.1"
```

## Activate env

```sh
# activate env
source .venv/bin/activate

# deactivate env
deactivate
```

## Create spider

```sh
scrapy startproject isbnchile # Create new Scrapy project
cd isbnchile
scrapy genspider books isbnchile # create spider 
```

## Run the spider passing arguments

```sh
cd isbnchile
scrapy crawl books -a day="YY-MM-DD"
```

## Scrapy Shell dev commands

```sh
scrapy shell <URL>
scrapy shell ; fetch(<URL>)
```

## Docker Container commands

```sh
docker build -t isbn_image .

docker run --rm \
    --name isbn_container \
    -v ~/Desktop/salida:/app/output \
    isbn_image \
    --day="2024-04-05"

docker exec -it isbn_container /bin/bash

docker rm -f $(docker ps -aq) # Eliminar todos los contenedores parados y en ejecución

docker run -it --rm \
            --name isbn_container \
            -v ~/Desktop/salida:/app/output \
            --entrypoint=bash \
            isbn_image
```
