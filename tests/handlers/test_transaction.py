from decentralized_etl import handle_transaction
from decentralized_etl import Eff
from decentralized_etl import EventTypes as E
from hypothesis import given
import hypothesis.strategies as st
from state_sentinel import StateSentinel
import types

class TestTransactionHandler:

    input_provider = given(
        ticker=st.text(min_size=1, max_size=6),
        amount=st.integers(),
        price=st.floats(min_value=0, allow_infinity=False, allow_nan=False),
        account_id=st.integers(),
        timestamp=st.floats(),
    )


    # TODO I suppose we could merge the buy and sell tests and rely on
    # hypothesis to discover which one(s) is broken.
    @input_provider
    def test_buy(self, ticker, amount, price, account_id, timestamp):
        effs = handle_transaction(
            StateSentinel(),
            ticker,
            amount,
            price,
            account_id,
            timestamp,
            E.Buy,
        )

        assert isinstance(effs, types.GeneratorType)

        effs = list(effs)
        assert len(effs) == 2

        ticker_eff, cash_eff = effs

        assert ticker_eff == Eff(ticker, amount, account_id, timestamp)
        assert cash_eff == Eff('CASH', -amount * price, account_id, timestamp)

    @input_provider
    def test_sell(self, ticker, amount, price, account_id, timestamp):
        effs = handle_transaction(
            StateSentinel(),
            ticker,
            amount,
            price,
            account_id,
            timestamp,
            E.Sell,
        )

        assert isinstance(effs, types.GeneratorType)

        effs = list(effs)
        assert len(effs) == 2

        ticker_eff, cash_eff = effs

        assert ticker_eff == Eff(ticker, -amount, account_id, timestamp)
        assert cash_eff == Eff('CASH', amount * price, account_id, timestamp)
