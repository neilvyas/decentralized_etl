from decentralized_etl import handle_declaration
from decentralized_etl import Eff
from hypothesis import given
import hypothesis.strategies as st
from state_sentinel import StateSentinel
import types


class TestDeclarationHandler:

    @given(
        ticker=st.text(min_size=1, max_size=6),
        amount=st.integers(),
        account_id=st.integers(),
        timestamp=st.floats())
    def test_declaration_handler(self, ticker, amount, account_id, timestamp):
        effs = handle_declaration(
            StateSentinel(),
            ticker,
            amount,
            account_id,
            timestamp,
        )

        assert isinstance(effs, types.GeneratorType)
        effs = list(effs)
        assert effs == [Eff(ticker, amount, account_id, timestamp)]
