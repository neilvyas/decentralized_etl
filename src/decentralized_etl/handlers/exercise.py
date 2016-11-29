from decentralized_etl import Eff
from decentralized_etl import EffPipeline
from decentralized_etl import EventTypes as E


# TODO maybe check in the account state that we're given
# that the account has the contract present before exercise.
@EffPipeline.handle(E.ExerciseCall)
@EffPipeline.handle(E.ExercisePut)
def handle_option_exercise(
        _,
        ticker,
        amount,
        account_id,
        timestamp,
        strike,
        underlying_spot,
        event_type,
        direction):
    """Given an exercise event, compute the effects.

    NB: We don't bother deciding whether or not to exercise (in the case of a long) or
    whether or not the counterparty exercises (in the case of a short). Instead, we
    suppose that if we see this event, an exercise occurred.

    Option value at expiry:
    (the max() indicates that this is an option, but we don't compute that)

    (Long/Short)(Call / Put)
    ------------------------
    LC : max(0, spot - strike)
    SC : - max(0, spot - strike)
    LP : max(0, strike - spot)
    SP : - max(0, strike - spot)
    """
    direction = 1 if direction == 'long' else -1
    payoff_direction = 1 if event_type == E.ExerciseCall else -1

    payoff = payoff_direction * (underlying_spot - strike)

    yield(ticker, direction * amount, account_id, timestamp)
    yield('CASH', direction * amount * payoff, account_id, timestamp)
