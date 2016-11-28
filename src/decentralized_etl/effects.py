from collections import namedtuple


AcctEff = namedtuple('AcctEff', (
    'account_id',
    'state_variable',
    'new_state',
))
"""Effect type for effects that change account state.

Since we're implementing stateful ETL, where the result of a given event can
depend on other data, we need a mechanism for updating that state as well as
updating the state that is the desired output of the ETL.
"""


Eff = namedtuple('Eff', (
    'ticker',
    'amount',
    'account_id',
    'timestamp'
))
"""Effect type for effects that change the state of the desired ETL object.

When performing ETL, we might have some sort of final state that we want to
arrive at, given an initial state and updates to that initial state. These
messages describe those updates.
"""
