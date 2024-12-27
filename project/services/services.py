import datetime
import io
import pandas


class DataService:
    def __init__(self) -> None:
        self.buffer: list[dict[str, str | int]] = list()

    @staticmethod
    def clean_table(objects: pandas.DataFrame, date: datetime.date) -> pandas.DataFrame:
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

    def get_buffer_data(self):
        return self.buffer

    @staticmethod
    def get_data_from_xls(content: bytes) -> pandas.DataFrame:
        with io.BytesIO(content) as f:
            print('Reading from excel file...')
            data = pandas.read_excel(f)

        result = pandas.DataFrame(data)
        return result

    def buffer_data(self, objects: pandas.DataFrame) -> None:
        try:
            buffer_data = objects.to_dict('records')
            self.buffer.extend(buffer_data)
        except Exception as err:
            print('Ошибка буферизации данных...', err)
