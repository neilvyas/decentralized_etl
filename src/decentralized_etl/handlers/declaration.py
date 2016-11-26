from decentralized_etl import app
from decentralized_etl import EventTypes as E
from decentralized_etl.handlers import Eff


@app.handle(E.Declaration)
def handle_declaration(logline):
    pass
