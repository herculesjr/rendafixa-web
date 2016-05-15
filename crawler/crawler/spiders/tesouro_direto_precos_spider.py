import scrapy

class TesouroDiretoPrecosSpider(scrapy.Spider):
    name = "tesouro_direto_precos"
    allowed_domains = ["dmoz.org"]
    start_urls = [
        "http://www3.tesouro.gov.br/tesouro_direto/consulta_titulos_novosite/consultatitulos.asp",
    ]

    def parse(self, response):
        filename = response.url.split("/")[-2] + '.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
