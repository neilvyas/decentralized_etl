*****************
decentralized_etl
*****************

This is a small demo package that tries to demonstrate the use of decorator
registration (using a canonical app object which has decorator methods to
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
  the desired side effect is registering the decorated function on the canonical
  app object. By using a decorator to do this, we can decentralize all our
  method/handler definitions, which is really nice in the case of an ETL
  pipeline. Then, we just run the canonical app app object against the input and
  we're away.

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
