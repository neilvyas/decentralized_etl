from decentralized_etl import Eff
from decentralized_etl import EffPipeline
from decentralized_etl import EventTypes as E


@EffPipeline.handle(E.Declaration)
def handle_declaration(_, ticker, amount, account_id, timestamp):
    yield Eff(ticker, amount, account_id, timestamp)
