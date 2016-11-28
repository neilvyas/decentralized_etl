from decentralized_etl import Eff
from decentralized_etl import EffPipeline
from decentralized_etl import EventTypes as E


@EffPipeline.handle(E.Call)
@EffPipeline.handle(E.Put)
def handle_option_exercise(logline):
    pass
