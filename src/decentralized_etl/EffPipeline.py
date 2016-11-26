from collections import defaultdict
import json


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

    def run(self, logfile_path):
        """Run the Effect Pipeline ETL job.

        Params
        ------
          logfile_path : string
          Path to logfile_path.

        Returns
        -------
            generator[Eff]
            A generator of effect objects.
        """
        with open(logfile_path, 'r') as logfile:
            for logline in logfile:
                logline = json.loads(logline)

                event_type = logline.get('type')
                # TODO: error handling.
                if event_type is None:
                    return

                handlers = self.handlers.get(event_type, [])
                for handler in handlers:
                    # Try to pass the handler some state, if it needs it, otherwise
                    # just pass in the logline.
                    try:
                        effects = handler(self, logline)
                    except TypeError:
                        effects = handler(logline)
                    finally:
                        effects = []

                    # py3 : yield from effects
                    for effect in effects:
                        yield effect
