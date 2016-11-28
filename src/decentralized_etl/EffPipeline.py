from collections import defaultdict
from inspect import getargspec


class EffPipeline:
    """Effect Pipeline.

    Reads from an event logfile and outputs effects. Easily parallelizable.

    """

    _handlers = defaultdict(list)

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
            that correspond to fields in the logline.

            If the first parameter is 'state', then the handler is understood
            to be 'stateful', and that parameter will be passed `self`.

        Usage
        -----
            @EffPipeline.handle('call')
            @EffPipeline.handle('put')
            def handle_option_exercise(...):
                pass
        """

        def handler_registration(handler):
            handler_args = getargspec(handler).args

            # Consider any handler with `state` or `self` as its first parameter to be stateful.
            # TODO the way we handle stateful handlers at run time is just trying to pass both
            # state and the logline and catching a TypeError if the handler doesn't need state.
            # This is obviously bad because we check this condition for each handler and logline.
            # Since we detect whether the handler is stateful here, we should be able to avoid this
            # overhead at runtime.
            if handler_args[0] in ('state', 'self'):
                handler_args = handler_args[1:]

            def handler_for_logline(logline):
                # TODO Handle malformed loglines here.
                assert all(arg in logline for arg in handler_args)

                return handler(**{arg: logline[arg] for arg in handler_args})

            cls._handlers[event_type] = handler_for_logline

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
        for logline in logfile:
            event_type = logline.get('type')
            # TODO: error handling.
            if event_type is None:
                return

            # get _handlers from the instance in case user added additional handlers.
            handlers = self._handlers.get(event_type, [])
            for handler in handlers:
                # FIXME see l:42
                # Try to pass the handler some state, if it needs it, otherwise
                # just pass in the logline.
                try:
                    effects = handler(self, logline)
                except TypeError:
                    effects = handler(logline)

                # py3 : yield from effects
                for effect in effects:
                    yield effect
