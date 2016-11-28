from decentralized_etl import Eff
from decentralized_etl import EffPipeline
from decentralized_etl import EventTypes as E


@EffPipeline.handle(E.Buy)
@EffPipeline.handle(E.Sell)
def handle_transaction(ticker, amount, price, account_id, timestamp, type):
    direction = 1 if type == 'buy' else -1

    yield Eff(ticker, amount * direction, account_id, timestamp)
    yield Eff('CASH', -1 * direction * amount * price, account_id, timestamp)
