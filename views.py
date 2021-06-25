from datetime import datetime
from json import dumps

from aiohttp.web import View, Response
from sqlalchemy import func, extract as ext

from constants import COUNTIES, CURRENCIES, COUNTRY_NAME_API, CUR_NAME_API, AMOUNT_NAME_API, DATE_NAME_API, \
    DATE_FORMAT_API
from models import Limit, Transfer, session


class LimitsView(View):
    @staticmethod
    def get_limit(d):
        return session.query(Limit).filter(Limit.country == d[COUNTRY_NAME_API], Limit.cur == d[CUR_NAME_API]).first()

    async def get(self):
        return Response(text=dumps([limit.to_json for limit in session.query(Limit).all()]))

    async def post(self):
        # пройдёмся по всем данным в запросе
        for limit_data in await self.request.json():
            # если API правильный, то есть имеются нужные значения
            if COUNTRY_NAME_API in limit_data and CUR_NAME_API in limit_data and AMOUNT_NAME_API in limit_data:
                # если названия страны и курса подходит
                if limit_data[COUNTRY_NAME_API] in COUNTIES and limit_data[CUR_NAME_API] in CURRENCIES:
                    # проверяем на наличие такого элемента. если нет, то создаём, если есть, то изменение с помощью PUT
                    if not LimitsView.get_limit(limit_data):
                        session.add(Limit(
                            country=limit_data[COUNTRY_NAME_API],
                            cur=limit_data[CUR_NAME_API],
                            amount=limit_data[AMOUNT_NAME_API]
                        ))
                    else:
                        return Response(text=dumps({"status": 705, "text": "Has object with params"}))
                else:
                    return Response(text=dumps({"status": 702, "text": "Bad value of country or cur"}))
            else:
                return Response(text=dumps({"status": 701, "text": "API error"}))

        # сохраняем данные в БД
        session.commit()
        return Response(text=dumps({"status": 200, "text": "OK"}))

    async def put(self):
        for limit_data in await self.request.json():
            if COUNTRY_NAME_API in limit_data and CUR_NAME_API in limit_data:
                # для запроса на изменение пропускаем проверку на корректность написания страны и курса,
                # так как в базе не должно быть плохих значение, а в этом запросе мы только изменяем максимальную сумму.
                # это эе относится и к удалению
                limit_object = LimitsView.get_limit(limit_data)
                if limit_object:
                    limit_object.amount = limit_data[AMOUNT_NAME_API]
                    session.add(limit_object)
                else:
                    return Response(text=dumps({"status": 706, "text": "No object with params"}))
            else:
                return Response(text=dumps({"status": 701, "text": "API error"}))

        session.commit()
        return Response(text=dumps({"status": 200, "text": "OK"}))

    async def delete(self):
        for limit_data in await self.request.json():
            if COUNTRY_NAME_API in limit_data and CUR_NAME_API in limit_data:
                limit_object = LimitsView.get_limit(limit_data)
                if limit_object:
                    session.delete(limit_object)
            else:
                return Response(text=dumps({"status": 701, "text": "API error"}))

        session.commit()
        return Response(text=dumps({"status": 200, "text": "OK"}))


class TransferView(View):
    async def post(self):
        for transfer_data in await self.request.json():
            if COUNTRY_NAME_API in transfer_data and CUR_NAME_API in transfer_data and AMOUNT_NAME_API in transfer_data:
                if transfer_data[COUNTRY_NAME_API] in COUNTIES and transfer_data[CUR_NAME_API] in CURRENCIES:
                    # проверяем правильность занесённой даты и времени
                    try:
                        date = datetime.strptime(transfer_data[DATE_NAME_API], DATE_FORMAT_API)
                    except:
                        return Response(text=dumps({"status": 702, "text": "Bad value of country or cur"}))

                    # в базе ищем подходящие значения транзакций и складываем их
                    current_sum = session.query(func.sum(Transfer.amount).label("sum_amount")) \
                        .group_by(Transfer.country, Transfer.cur) \
                        .filter(ext('month', Transfer.date) == date.month, ext('year', Transfer.date) == date.year) \
                        .filter(Transfer.country == transfer_data[COUNTRY_NAME_API],
                                Transfer.cur == transfer_data[CUR_NAME_API]) \
                        .all()

                    # обработка отсутствия транзакций
                    current_sum = current_sum[0][0] if current_sum else 0

                    # берём максимальную сумму в месяц для этих параметров
                    max_sum = LimitsView.get_limit(transfer_data).amount

                    # если значения ещё не выходят за лимиты, добавляем транзакцию в БД
                    if max_sum >= current_sum + transfer_data[AMOUNT_NAME_API]:
                        session.add(Transfer(
                            date=date,
                            country=transfer_data[COUNTRY_NAME_API],
                            cur=transfer_data[CUR_NAME_API],
                            amount=transfer_data[AMOUNT_NAME_API]
                        ))
                    else:
                        return Response(text=dumps({"status": 707, "text": "Summary transfers bigger then limits"}))
                else:
                    return Response(text=dumps({"status": 702, "text": "Bad value of country or cur"}))
            else:
                return Response(text=dumps({"status": 701, "text": "API error"}))

        session.commit()
        return Response(text=dumps({"status": 200, "text": "OK"}))
