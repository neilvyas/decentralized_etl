from decentralized_etl import EffPipeline


def test_handler_decoration():
    assert EffPipeline._handlers
