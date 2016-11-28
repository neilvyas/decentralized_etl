from collections import defaultdict


class EffPipeline:
    """Effect Pipeline.

    Reads from an event logfile and outputs effects. Easily parallelizable.

    """

    def __init__(self):
        self.handlers = defaultdict(list)

    def handle(self, event_type):
        """Register an event handler for event_type.

        Usage:
            @app.handle('call')
            @app.handle('put')
            def handle_option_exercise(...):
                pass
        """

        def wrapper(handler):
            self.handlers[event_type] = handler
            return handler

        return wrapper

    def run(self, loglines):
        """Run the Effect Pipeline ETL job.

        Params
        ------
            loglines : iterator[dict]
            An iterator of loglines, as python dictionaries.

        Returns
        -------
            generator[Eff]
            A generator of effect objects.
        """
        for logline in logfile:
            event_type = logline.get('type')
            # TODO: error handling.
            if event_type is None:
                return

            # get _handlers from the instance in case user added additional handlers.
            handlers = self._handlers.get(event_type, [])
            for handler in handlers:
                # Try to pass the handler some state, if it needs it, otherwise
                # just pass in the logline.
                try:
                    effects = handler(self, logline)
                except TypeError:
                    effects = handler(logline)

                # py3 : yield from effects
                for effect in effects:
                    yield effect
