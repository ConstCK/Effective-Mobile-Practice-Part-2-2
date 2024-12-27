import asyncio

from config import MAIN_URL
from services.initial_tasks import create_tables
from services.parser import Parser


my_service = Parser(MAIN_URL)


async def main():
    # запуск функции с созданием всех таблиц в БД
    await create_tables()
    await my_service.get_xls_urls(2024)
    await my_service.get_xls_data()
    result = await my_service.get_xls_data()
    print(result)



if __name__ == '__main__':
    try:
        asyncio.run(main())
    except Exception:
        print('There are some problems running application...exiting program...')
    # my_service.get_xls_urls(2024)
    # my_service.get_xls_data()
