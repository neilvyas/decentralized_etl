from decentralized_etl import Eff
from decentralized_etl import EffPipeline
from decentralized_etl import EventTypes as E


@EffPipeline.handle(E.Call)
@EffPipeline.handle(E.Put)
def handle_option_exercise(
        _,
        ticker,
        amount,
        account_id,
        timestamp,
        strike,
        premium,
        underlying_spot,
        event_type,
        direction):
    """Option value at expiry:

    (Long/Short)(Call / Put)
    ------------------------
    LC : max(0, spot - strike) - premium
    SC : premium - max(0, spot - strike)
    LP : max(0, strike - spot) - premium
    SP : premium - max(0, strike - spot)
    """
    direction = 1 if direction == 'long' else -1
    payoff_direction = 1 if event_type == E.Call else -1

    payoff = max(0, payoff_direction * (underlying_spot - strike))
    contract_value = direction * (payoff - premium)

    yield(ticker, amount, account_id, timestamp)
    yield('CASH', amount, amount * contract_value, timestamp)
