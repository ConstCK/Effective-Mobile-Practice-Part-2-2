import asyncio

from services.parser import Parser
from services.services import create_tables

my_service = Parser('https://spimex.com/markets/oil_products/trades/results/')


async def main():
    #     # запуск функции с созданием всех таблиц в БД
    #     # await create_tables()
    await my_service.get_xls_urls(2024)
    await my_service.get_xls_data()
    result = await my_service.get_buffer_data()
    print(result)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except Exception:
        print('There are some problems running application...exiting program...')
    # my_service.get_xls_urls(2024)
    # my_service.get_xls_data()
