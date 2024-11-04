# Docs

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

## Run this spider

```sh
cd isbnchile
scrapy crawl books -o books.json 
scrapy crawl books # run spider and saving files in books directory, using pipeline class 
```

## Development commands

```sh
scrapy shell <URL>
scrapy shell ; fetch(<URL>)
```
