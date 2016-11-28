from decentralized_etl import Eff
from decentralized_etl import EffPipeline
from decentralized_etl import EventTypes as E


@EffPipeline.handle(E.Buy)
@EffPipeline.handle(E.Sell)
def handle_transaction(logline):
    # TODO factor out common logline unpacking logic, maybe?
    # FIXME possible enhancement: the handler doesn't take a logline. Instead,
    # you declare the fields of the logline you want as arguments and handler
    # registration uses inspection to handle unpacking and checking the logline
    # for you.
    fields = ('account_id', 'ticker', 'type', 'amount', 'timestamp', 'price')
    assert all(field in logline for field in fields), "Malformed logline"

    account_id, ticker, type_, amount, timestamp, price = \
        [logline[field] for field in fields]
    direction = 1 if type_ == 'buy' else -1

    yield Eff(ticker, amount * direction, account_id, timestamp)
    yield Eff('CASH', -1 * direction * amount * price, account_id, timestamp)
