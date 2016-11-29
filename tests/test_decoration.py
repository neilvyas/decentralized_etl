from decentralized_etl import EffPipeline


class TestHandlersDecorated:
    def test_handlers_present(self):
        assert EffPipeline._logline_handlers
