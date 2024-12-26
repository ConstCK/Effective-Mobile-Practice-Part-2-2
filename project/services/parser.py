import datetime
import io

import pandas
import requests
from bs4 import BeautifulSoup


class Parser:
    def __init__(self, url: str) -> None:
        self.url = url
        self.xls_urls: list[dict[str, str]] = list()
        self.buffer: list[dict[str, str | int]] = list()

    async def get_xls_urls(self, limit: int) -> list[dict[str, str]]:
        """Получение всех маршрутов (с указанного года) с Excel файлами с данными для БД"""
        page = 0
        data_year = datetime.datetime.now().year
        print('Receiving data files urls...')
        while limit <= data_year:
            page += 1
            r = requests.get(f'{self.url}?page=page-{page}')
            soup = BeautifulSoup(r.content, 'html.parser')

            raw_data = soup.find_all('a',
                                           class_='accordeon-inner__item-title link xls')[:10]
            data = [x['href'] for x in raw_data]

            for i in data:
                data_year = int(i[32:36])
                if data_year < limit:
                    break
                self.xls_urls.append({i[32:40]: i})

        return self.xls_urls

    async def get_xls_data(self):
        """Сохранение данных в локальный буфер"""
        print('Adding data to local storage... ')
        for item in self.xls_urls:
            for key, value in item.items():
                current_date = datetime.date.fromisoformat(f'{key[:4]}-{key[4:6]}-{key[6:]}')

                current_url = f'https://spimex.com{value}'
                print(current_url)
                r = requests.get(current_url)

                with io.BytesIO(r.content) as f:
                    print('Reading from excel file...')
                    data = pandas.read_excel(f)

                objects = pandas.DataFrame(data)
                try:
                    objects = self._clean_table(objects, current_date)
                except Exception as err:
                    print('Table refactoring error...', err)
                try:
                    buffer_data = objects.to_dict('records')
                    self.buffer.extend(buffer_data)
                except Exception as err:
                    print('2', err)

        return self.buffer

    @staticmethod
    def _clean_table(objects: pandas.DataFrame, date: datetime.date) -> pandas.DataFrame:
        objects.columns = [x for x in range(15)]
        objects = objects[[1, 2, 3, 4, 5, 14]][objects[14] != '-'].dropna()
        objects[15] = date
        objects = objects.drop(objects[objects[1].str.len() != 11].index)
        objects[16] = objects[1].str[:4]
        objects[17] = objects[1].str[4:7]
        objects[18] = objects[1].str[-1]
        objects = objects.astype({4: 'int64', 5: 'int64', 14: 'int16'}, errors='ignore')
        objects.columns = [
            'exchange_product_id',
            'exchange_product_name',
            'delivery_basis_name',
            'volume',
            'total',
            'count',
            'date',
            'oil_id',
            'delivery_basis_id',
            'delivery_type_id',
        ]
        return objects

    async def get_buffer_data(self):
        return self.buffer[:10]
