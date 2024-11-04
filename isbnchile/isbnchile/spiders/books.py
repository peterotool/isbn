import json
import logging
import os

import scrapy
from dotenv import load_dotenv
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider, Rule
from scrapy.utils.log import configure_logging

from ..items import BookDetailItem, BookItem

load_dotenv()
URL = os.getenv("URL")
DAY = os.getenv("DAY")

class BooksSpider(CrawlSpider):

    configure_logging(install_root_handler=False)
    logging.basicConfig(
        filename=f'../log_extraction_{DAY}.txt',
        format='%(levelname)s: %(message)s',
        level=logging.INFO
    )

    name = "books"
    allowed_domains = ["isbnchile.cl"]
    start_urls = [f"{URL}={DAY}"]
    rules = (
        Rule(LinkExtractor(allow=(r"pagina=\d+")), callback="parse_book",follow=True),
    )


    def clean_str(self, data:str)->str:
        if data:
            return data.strip()
        else:
            return ''

    def list_2_str(self, data:list)->str:
        if data:
            return ''.join(data)
        else:
            return ''
        
    def parse_book(self, response):

        logging.info(f"{response.url=}")
        
        isbn:list = response.xpath(".//span[@class='isbn']/text()").getall()
        titulo:list = response.xpath(".//a[@class='titulo']/text()").getall()
        fecha:list = response.css('span.textofecha::text').getall()

        for isbn,titulo, fecha in zip(isbn,titulo, fecha):
            
            items = BookItem()
            items['isbn'] = isbn
            items['titulo'] = titulo
            items['fecha']= fecha
            yield items

        next_pages =response.xpath('.//a[contains(@href,"detalle")]/@href').getall()
        if len(next_pages)>1:
            for next_page in next_pages:
                next_page= response.urljoin(next_page)
                logging.info("Querying Book Detail")
                logging.info(f"{next_page=}")
                yield  response.follow(next_page, callback=self.parse_book_detail)
    

    def parse_book_detail(self, response):

        logging.info(f"Book Detail {response.css("span.isbn::text").get().strip()}")
        logging.info(f"{response.url=}")

        autor:str = response.xpath("//span[contains(text(), 'Autor:')]/following-sibling::a[@class='texto']/text()").get()
        autor = self.clean_str(autor)

        colaborador:str = response.xpath(".//span[contains(text(), 'Colaborador:')]/following-sibling::a[@class='texto']/text()").get() # null
        colaborador = self.clean_str(colaborador)

        numero_de_paginas:str = response.xpath(".//span[contains(text(), 'Número de páginas:')]/following-sibling::span[@class='texto']/text()").get() # null
        numero_de_paginas = self.clean_str(numero_de_paginas)

        precio:str = response.xpath(".//span[contains(text(), 'Precio:')]/following-sibling::span[@class='textofecha']/text()").get() # null
        precio = self.clean_str(precio)

        formato:str = response.xpath(".//span[contains(text(), 'Formato:')]/following-sibling::span[@class='textofecha']/text()").get()
        formato = self.clean_str(formato)

        autores:list = response.xpath("//span[@class='labels' and text()='Autores:']/following-sibling::span[@class='texto'][1]//a/text()").getall() # null
        autores = self.list_2_str(autores)

        items = BookDetailItem()
        items['isbn']= response.css("span.isbn::text").get().strip()
        items['autor']= autor
        items['autores']= autores
        items['colaborador']= colaborador
        items['colaboradores']= response.xpath(".//span[contains(text(), 'Colaboradores:')]/following-sibling::span[@class='texto'][1]//a/text()").getall()
        items['editorial']= response.xpath(".//span[contains(text(), 'Editorial:')]/following-sibling::span[@class='texto'][1]//a/text()").get()
        items['materia']= response.xpath(".//span[contains(text(), 'Materia:')]/following-sibling::span[@class='texto'][1]//a/text()").get()
        items['publico_objetivo']= response.xpath(".//span[contains(text(), 'Público objetivo:')]/following-sibling::span[@class='textofecha']/a/text()").get()
        items['publicado']= response.xpath(".//span[contains(text(), 'Publicado:')]/following-sibling::span[@class='textofecha']/text()").get()
        items['numero_de_edicion']= response.xpath(".//span[contains(text(), 'Número de edición:')]/following-sibling::span[@class='textofecha']/text()").get()
        items['numero_de_paginas']= numero_de_paginas
        items['tamano']= response.xpath(".//span[contains(text(), 'Tamaño:')]/following-sibling::span[@class='textofecha']/text()").get()
        items['precio']= precio
        items['soporte']= response.xpath(".//span[contains(text(), 'Soporte:')]/following-sibling::span[@class='textofecha']/text()").get()
        items['formato']= formato
        items['idioma']= response.xpath(".//span[contains(text(), 'Idioma:')]/following-sibling::span[@class='texto']/span[@class='texto']/text()").get()
        yield items