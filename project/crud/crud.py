from sqlalchemy import insert

from db.db import async_session
from models.models import TradingResult


class TradingExchange:
    def __init__(self) -> None:
        self.session = async_session()

    async def add_data(self, data: list[dict[str, str | int]]) -> None:
        for i in data:
            stmt = insert(TradingResult).values(
                exchange_product_id=i['exchange_product_id'],
                exchange_product_name=i['exchange_product_name'],
                oil_id=i['oil_id'],
                delivery_basis_id=i['delivery_basis_id'],
                delivery_basis_name=i['delivery_basis_name'],
                delivery_type_id=i['delivery_type_id'],
                volume=i['volume'],
                total=int(i['total']),
                count=i['count'],
                date=i['date'],
            )
            try:
                await self.session.execute(stmt)
                await self.session.commit()
            except Exception as err:
                print('Error adding data to DB...', err)
                continue
            finally:
                await self.session.close()

        print('All data are successfully added to DB...')
