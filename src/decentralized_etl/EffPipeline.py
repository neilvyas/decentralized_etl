from collections import defaultdict
from inspect import getargspec


class EffPipeline:
    """Effect Pipeline.

    Reads from an event logfile and outputs effects. Easily parallelizable.

    """

    _logline_handlers = defaultdict(list)

    @classmethod
    def handle(cls, event_type):
        """Register an event handler for event_type.

        This method is a little magical but it leads to a very readable API,
        so I'm ok with that.

        Params
        ------
            event_type : string
            Should be a member of decentralized_etl.EventTypes

            handler : function (via decoration)
            A handler function that has only positional arguments with names
            that correspond to fields in the logline, with the first parameter
            being reserved to pass in a state reference.


        Usage
        -----
            @EffPipeline.handle('call')
            @EffPipeline.handle('put')
            def handle_option_exercise(state, ticker, account_id, ...)
                pass
        """

        def handler_registration(handler):
            # The first argument is reserved for passing a state reference.
            handler_args = getargspec(handler).args[1:]

            def handler_for_logline(logline):
                # TODO Handle malformed loglines here.
                assert all(arg in logline for arg in handler_args)

                return handler(**{arg: logline[arg] for arg in handler_args})

            cls._logline_handlers[event_type] = handler_for_logline

            # Return the original handler for testing purposes.
            return handler

        return handler_registration

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
        for logline in loglines:
            event_type = logline.get('event_type')
            # TODO: error handling.
            if event_type is None:
                return

            # get _logline_handlers from the instance in case user added additional handlers.
            logline_handlers = self._logline_handlers.get(event_type, [])
            for logline_handler in logline_handlers:
                effects = logline_handler(self, logline)

                # py3 : yield from effects
                for effect in effects:
                    yield effect
