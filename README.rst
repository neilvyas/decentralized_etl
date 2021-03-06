*****************
decentralized_etl
*****************

See `this gist`_ for a single-file gist of what this demo tries to accomplish.

.. _`this gist`: https://gist.github.com/neilvyas/39bdae9711529473e17ffc3e7ea35969

This is a small demo package that tries to demonstrate the use of decorator
registration (using an app object which has decorator methods to
register handler functions) for the problem of creating a modular, extensible,
and loosely-coupled ETL pipeline. By this we mean that

* Each handler is a pure function and independent of all other logic, if
  possible, and lives in its own file and has its own tests. The handler is
  incorporated into the app via registration onto a canonical app object.

* Adding new ETL handlers is super simple; the only code that needs to interact
  with existing logic is just adding a callback, and doesn't require modifying
  any existing code if the new handler is truly orthogonal to the rest of the
  app.

* Sharing code between handlers is really, really easy, since they're (mostly)
  just pure functions. No dealing with possibly complicated class hierarchies,
  implementing boilerplate :code:`Handler.run` methods, etc to achieve
  genericism and good code re-use.

Note also that we've gone ahead and stuck all the handlers in the
:code:`handlers` directory, but this isn't necessary. We can treat
:code:`EffPipeline` as a library for creating ETLs on this dataset (loglines
with the same fields/schema) and import it to define our own ETLs in a single
file or package of our own, like `this example`_ for an algorithmic trading
bot.

.. _`this example`: https://github.com/neilvyas/ucf_exchange_client/blob/master/examples/market_maker.py#L23

Here's some background, since there's a lot of jargon up there:

ETL
  *ETL* is an initialism for *Extract, Transform, Load*, which is a term that
  originally had some sort of database-migration meaning but now generically
  means "take that datasource, clean it up, and pipe the resulting clean data
  over here where the nice people can use it." For data-centric products, a
  good *ETL pipeline*, or the infrastructure that performs the actual ETL jobs,
  is as critical as running water to a city. Or proper sewage systems, maybe.

decorator registration
  A *decorator* is a higher-order function that eats another function and does
  something with it; say, if you wanted to log all the inputs to your function,
  you could write a :code:`log_func_args(func_to_log)` decorator. Python has
  syntactic sugar for decorator use through annotations, which are the
  :code:`@app.handle('Blah')` statements you see before handler definitions.

  We refer to a specific pattern of decorator use here as *decorator
  registration*, since we're using the decorator only for its side effect, and
  the desired side effect is registering the decorated function on the
  app class.

  You can think of it as we're defining instance methods on the main class
  across multiple files, and while defining them we're also registering them as
  handlers for certain event types. To do this, we define the instance methods
  as pure functions in their own file and decorate them with a classmethod to
  register them onto the class as a handler for the appropriate event type.

handler
  We're considering a pretty typical ETL use-case with this toy package: we
  have a bunch of loglines representing events or actions (state updates), and
  we want to play them forward to arrive at a final system state. Along the
  way, we're gonna clean up the input dataset, check for inconsistencies, etc.

  Since the problem domain breaks down naturally into these different event
  types, we can structure our ETL definitions around that through the use of
  *handlers*, which are just functions from loglines to "business objects," or
  the desired output of our ETL pipeline. In this case, we go from loglines to
  *effects*, which are represented in code by :code:`Eff`, and then we have
  another mechanism in the canonical app object to go from effects to final
  state.

  The decision to have our pipeline look like ::

    loglines ---(handlers)--> effects ---(state updater)--> final state

  instead of the more naive approach of ::

    loglines ---(state updater)--> final state

  does wonders for testability, DRY-ness, modularity, etc. We're taking
  advantage of the fact that just about every event type really reduces down to
  an *effect* on our account status or positions or whatever to write code with
  tight abstraction boundaries and loose coupling, using independent handlers
  to handle the possibly gross task of moving from the input data to effects
  and then a simple state machine to handle the simpler task of moving from
  effects to final state, rather than bundling the nice work in with the gross
  work in one massive, tightly-coupled machine.

I'm also using this package to play around with python packaging styles.

******
issues
******

I'm sure you could have something like this that's "production ready," since
most everything you want for production ready code can be implemented as layers
around our canonical object without touching the handler definitions- things
like logging, distributed running, etc. The only thing that this architecture
doesn't provide well is that we've "fixed" the pipeline definition, in that the
canonical object gets all these pre-defined handlers attached to it and then
you can point it at a logfile, or even add further handlers, but the handlers
in this package, or pipeline definition, are fixed.
