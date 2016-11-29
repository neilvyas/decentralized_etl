from decentralized_etl import handle_option_exercise
from decentralized_etl import Eff
from decentralized_etl import EventTypes as E
from hypothesis import given
import hypothesis.strategies as st
from state_sentinel import StateSentinel


class TestOptionExerciseHandler:

    floats = st.floats(min_value=0, allow_infinity=False, allow_nan=False)

    @given(
        strike=floats,
        underlying_spot=floats,
        amount=st.integers(min_value=0),
    )
    def _parameterized_option_test(
            self, direction, event_type,
            strike, underlying_spot, amount):

        effs = handle_option_exercise(
            StateSentinel(),
            ticker='TEST',
            amount=amount,
            account_id=1,
            timestamp=1,
            strike=strike,
            underlying_spot=underlying_spot,
            event_type=event_type,
            direction=direction,
        )
        # It seems like there's not really a way to get around this without
        # just re-writing all the logic from the handler.
        # I guess that means we wrote the handler right!

        direction = 1 if direction == 'long' else -1
        payoff_direction = 1 if event_type == E.ExerciseCall else -1

        payoff = payoff_direction * (underlying_spot - strike)

        effs = list(effs)
        assert len(effs) == 2

        ticker_eff, cash_eff = effs

        assert ticker_eff == Eff('TEST', direction * amount, 1, 1)
        assert cash_eff == Eff('CASH', direction * amount * payoff, 1, 1)

    def test_long_call(self):
        self._parameterized_option_test('long', E.ExerciseCall)

    def test_short_call(self):
        self._parameterized_option_test('short', E.ExerciseCall)

    def test_long_put(self):
        self._parameterized_option_test('long', E.ExercisePut)

    def test_short_put(self):
        self._parameterized_option_test('short', E.ExercisePut)

    def test_option_exercise_handler(self):
        pass
