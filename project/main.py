import asyncio

from config import MAIN_URL
from crud.crud import TradingExchange
from services.initial_tasks import create_tables, delete_tables
from services.parser import Parser
from services.services import DataService

my_parser = Parser(MAIN_URL)
db_service = TradingExchange()


async def main():
    await delete_tables()
    await create_tables()
    try:
        await my_parser.get_xls_urls(2023)
        await my_parser.get_xls_data()
        result = await my_parser.get_all_data()
        await db_service.add_data(result)
    except Exception as error:
        print('!!!', error)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except Exception:
        print('There are some app problems...exiting program...')
