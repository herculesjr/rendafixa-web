from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ValidationError

import lxml.html
import datetime
import re

from rendafixa.models import Issuer, BoundType, Bound, BoundData


class Command(BaseCommand):
    help = 'Init data'
    issuer = None

    URL_TO_PARSE = 'http://www3.tesouro.gov.br/tesouro_direto/consulta_titulos_novosite/consultatitulos.asp'

    def handle(self, *args, **options):
        site = lxml.html.parse(self.URL_TO_PARSE)
        xpath_table = '//table/tr/td/table/tr/td/center/table/tr'
        table = site.xpath(xpath_table)
        xpath_update = '%s//td[@class="listing2"]/b' % xpath_table
        last_update = site.xpath(xpath_update)[0].text.strip()

        print last_update

        for item in table:
            children = item.getchildren()
            entry = 0
            crawler_name = ''
            expiration_date = None
            tax_sell = None
            tax_buy = None
            price_sell = None
            price_buy = None
            for td in children:
                if not td.tag == 'td':
                    continue
                if 'colspan' not in td.attrib:
                        text = td.text
                        if text is not None:
                            text = text.strip()
                            text = re.sub('[R$%.]', '', text)
                            text = re.sub('[,]', '.', text)
                        if entry == 0:
                            crawler_name = text
                            if len(crawler_name) == 0:
                                break
                        elif entry == 1:
                            expiration_date = datetime.datetime.strptime(text, '%d/%m/%Y')
                        elif entry == 2:
                            if text is not None:
                                tax_buy = float(text)/100
                        elif entry == 3:
                            if text is not None:
                                tax_sell = float(text)/100
                        elif entry == 4:
                            if text is not None:
                                price_buy = float(text)
                        elif entry == 5:
                            if text is not None:
                                price_sell = float(text)
                        entry += 1
            if len(crawler_name) == 0:
                continue
            print '%s - %s - %s %s %s %s' % (crawler_name, expiration_date, tax_buy, tax_sell, price_buy, price_sell)
