name: empty layout
layout: true

---
name: title
class: center, middle

Asyncio overview
================

Vincent Michel

May 17th 2017

---

Reference
---------

- [Asyncio docs](https://docs.python.org/3/library/asyncio.html)

- [Asyncio user docs](http://asyncio.readthedocs.io/en/latest/)

- [Asyncio mode in pytango](http://pytango.readthedocs.io/en/latest/green_modes/green.html#asyncio-mode)


Getting started
---------------

- `async/await` syntax has been introduced in python 3.5

- Conda installation:

    ```bash
    $ conda create -c tango-controls -n aio35 python=3.5 pytango
    $ source activate aio35
    ```

---

Asynchronous programming
------------------------

### First approach to concurrency: threads

- 1 listener + 1 thread per client

- cons: race conditions and thread overhead

- pros:  parallelization

### Second approach to concurrency: asynchronous programming

- single-threaded

- pros: support >10K clients

- cons: require specific libraries

---

How does it work?
-----------------

- a selector monitors the file descriptors

- a loop manages a callback queue

- a user interface is provided:

  * [Twisted](https://twistedmatrix.com/trac): deferred and inline callbacks

  * [Gevent](http://www.gevent.org/): asynchronous results and implicit coroutines

  * [Asyncio](https://docs.python.org/3/library/asyncio.html): futures and explicit coroutines

  * [Curio](https://curio.readthedocs.io/en/latest/) and [Trio](https://trio.readthedocs.io/en/latest/): explicit coroutines only

- concurrency is achieved using execution units (pseudo-threads):

  - greenlet (gevent)

  - task (asyncio, curio, trio)

---

Python generators and coroutines
--------------------------------

- python generators with `yield`

    ```python3
	>>> def accumulate(value=0):
	...     while True:
	...         value += yield value
	...
	>>> gen = accumulate(10)
	>>> next(gen)
	10
	>>> gen.send(1)
	11
	>>> gen.send(2)
	13
    ```

- using a generator inside a generator with `yield from`

    ```python3
	>>> def chain(gen1, gen2):
	...     yield from gen1
	...     yield from gen2
    ...
    >>> gen = chain([1, 2], [3, 4])
	>>> list(gen)
	[1, 2, 3, 4]
    ```

---

What does a coroutine look like?
--------------------------------

- asyncio coroutines (python 3.4)

    ```python3
	@asyncio.coroutine
	async def say(what, when):
        yield from asyncio.sleep(when)
        print(what)
    ```

- asyncio coroutines (python >= 3.5)

    ```python3
	async def say(what, when):
        await asyncio.sleep(when)
        print(what)
    ```

- and more cool syntax!

    ```python3
	async def some_coroutine():
	    async with some_asynchronous_context():
		    async for x in some_asynchronous_iterator():
			     await some_other_coroutine(x)
    ```

---

Hello world!
------------

- [Example](http://asyncio.readthedocs.io/en/latest/hello_world.html):

    ```python3
    import asyncio

    async def say(what, when):
    await asyncio.sleep(when)
    print(what)

    loop = asyncio.get_event_loop()
    coro = say('Hello world!', 1)
    loop.run_until_complete(coro)
    loop.close()
    ```

- Output:

    ```console
    $ python hello_world.py
    # Wait 1 second
    Hello world!
    ```

- Note: `time.sleep` and other blocking operations are banned!

---

Adding a bit of concurrency
---------------------------

- [Example](http://asyncio.readthedocs.io/en/latest/hello_world.html#creating-tasks):

    ```python3
    import asyncio

    async def say(what, when):
    await asyncio.sleep(when)
    print(what)

    loop = asyncio.get_event_loop()
    loop.create_task(say('First hello!', 2))
    loop.create_task(say('Second hello!', 1))
    loop.run_forever()
    loop.close()
    ```

- Output:

    ```console
    $ python hello_world_with_tasks.py
    # Wait 1 second
    First hello!
    # Wait 1 second
    Second hello!
    ```

- Those tasks are running concurrently!

---

Asyncio features
----------------

- Basic structure:

    ```
    future -------------------+---------+
                              |         |
    generator ---> coroutine -+-> task -+-> base event loop -+-> selector event loop
                                                             |
    select ---> selector ------------------------------------+
    ```

- Standard library supports:

  * Pipes and signals

  * Subprocesses

  * Sockets and unix domain sockets

  * Locks, events and queues

  * Thread and process pool executors

- Much more in the [third party libraries](https://github.com/python/asyncio/wiki/ThirdParty)!

---

How do I do [X] with asyncio?
---------------------------

![graph](graph.png)
