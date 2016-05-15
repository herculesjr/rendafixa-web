from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ValidationError

import re
import urllib
import os
import xlrd
import csv
import datetime
from rendafixa.models import Issuer, BoundType, Bound, BoundData


class Command(BaseCommand):
    help = 'Init data'
    issuer = None

    def handle(self, *args, **options):
        if not os.path.exists('tmp'):
            os.mkdir('tmp')
        bounds = ['LFT', 'LTN', 'NTN-C', 'NTN-B', 'NTN-B_Principal', 'NTN-F']
        bounds_description = ['Selic', 'Prefixado', 'IGPM+ com Juros Semestrais',
                              'IPCA+ com Juros Semestrais', 'IPCA+',
                              'Prefixado com Juros Semestrais']
        now = datetime.datetime.now()
        try:
            self.issuer = Issuer.objects.get(identifier='TD')
        except Issuer.DoesNotExist:
            self.issuer = Issuer(identifier='TD', name='Tesouro Direto')
            self.issuer.save()
        for bound_str in bounds:
            boundtype_identifier = re.sub('[_]', ' ', bound_str)
            try:
                bound_type = BoundType.objects.get(identifier=boundtype_identifier)
            except BoundType.DoesNotExist:
                boundtype_name = re.sub('[-]', '', boundtype_identifier)
                boundtype_description = bounds_description[bounds.index(bound_str)]
                bound_type = BoundType(identifier=boundtype_identifier,
                                       name=boundtype_name,
                                       description=boundtype_description)
                bound_type.save()
            for year in range(2002, now.year+1):
                filename = self.getFile(bound_str, year)
                self.parse_file(filename, bound_type)
                print '-----------------------------------'

    def getFile(self, bound, year):
        url = ''
        if year < 2012:
            url = 'http://www3.tesouro.gov.br/tesouro_direto/download/historico/'
            url += str(year) + '/historico'
            filename = re.sub('[-_]', '', bound)
            url += filename + '_' + str(year) + '.xls'
        else:
            url = 'http://www.tesouro.fazenda.gov.br/documents/10180/137713/'
            url += bound + '_' + str(year) + '.xls'
        filename = "tmp/%s_%s.xls" % (bound, year)
        print 'Downloading %s %s' % (bound, year),
        if not os.path.exists(filename):
            urllib.urlretrieve(url, filename)
            print ' DONE'
        else:
            print ' CACHED'
        return filename

    def parse_file(self, excel_file, bound_type):
        try:
            workbook = xlrd.open_workbook(excel_file)
        except xlrd.XLRDError:
            return
        all_worksheets = workbook.sheet_names()
        print '### Parsing file %s' % excel_file
        for worksheet_name in all_worksheets:
            print '###### Parsing worksheet %s' % worksheet_name,
            worksheet = workbook.sheet_by_name(worksheet_name)
            if worksheet.nrows == 0:
                continue

            expiration_str = ''.join(x for x in worksheet_name if x.isdigit())
            expiration = datetime.datetime.strptime(expiration_str, '%d%m%y')

            try:
                identifier = '%s %s' % (bound_type.identifier, expiration.strftime('%d/%m/%Y'))
                bound = Bound.objects.get(identifier=identifier)
            except Bound.DoesNotExist:
                crawler_name = 'Tesouro %s %s (%s)' % (bound_type.description,
                                                       expiration.strftime('%Y'),
                                                       bound_type.name[:10])
                bound = Bound(bound_type=bound_type,
                              identifier=identifier,
                              issuer=self.issuer,
                              expiration_date=expiration,
                              name=bound_type.identifier,
                              crawler_name=crawler_name)
                bound.save()
            entries = 0
            for rownum in xrange(worksheet.nrows):
                if rownum < 2:
                    continue
                entry_count = 0
                date = ''
                buy_tax = 0.0
                sell_tax = 0.0
                buy_price = 0.0
                sell_price = 0.0
                for entry in worksheet.row_values(rownum):
                    entry_str = str(entry)
                    if len(entry_str) == 0:
                        continue
                    if entry_count == 0:
                        try:
                            date = datetime.datetime.strptime(entry_str, '%d/%m/%Y')
                        except ValueError:
                            try:
                                date = datetime.datetime.strptime(entry_str, '%d/%m/%y')
                            except ValueError:
                                (year, month, day, hour, minute, nearest_second) = xlrd \
                                    .xldate_as_tuple(entry, workbook.datemode)
                                date = datetime.date(year, month, day)
                    else:
                        try:
                            entry = float(entry)
                        except ValueError:
                            entry = 0.0

                        if entry_count == 1:
                            buy_tax = entry*100
                        elif entry_count == 2:
                            sell_tax = entry*100
                        elif entry_count == 3:
                            buy_price = entry
                        elif entry_count == 4:
                            sell_price = entry
                    entry_count = entry_count+1
                if len(str(date)) == 0:
                    continue
                try:
                    bound_data = BoundData.objects.get(bound=bound, date=date)
                except BoundData.DoesNotExist:
                    bound_data = BoundData(bound=bound, date=date)

                bound_data.buy_price = buy_price
                bound_data.buy_tax = buy_tax
                bound_data.sell_price = sell_price
                bound_data.sell_tax = sell_tax
                bound_data.save()
                entries += 1
            print ' OK - %d entries' % entries
