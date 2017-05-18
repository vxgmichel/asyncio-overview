name: empty layout
layout: true

---
name: title
class: center, middle

Asyncio overview
================

Vincent Michel @ MAX-IV

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

---

A TCP echo server
-----------------

- [Example from the user docs](http://asyncio.readthedocs.io/en/latest/tcp_echo.html#tcp-echo-server)

- Boiler-plate code

    ```python3
    # Start the server
    loop = asyncio.get_event_loop()
    server = loop.run_until_complete(start_serving())

    # Serve requests until Ctrl+C is pressed
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    # Close the server
    loop.run_until_complete(stop_serving(server))
    loop.close()
    ```

- Will be simpler after [PR#465](https://github.com/python/asyncio/pull/465) is merged

---

A TCP echo server
-----------------

- Starting and stopping the server

    ```python3
    async def start_serving():
        server = await asyncio.start_server(handle_echo, '0.0.0.0', 8888)
        print('Serving on {}'.format(server.sockets[0].getsockname()))
        return server

    async def stop_serving(server):
        server.close()
        await server.wait_closed()
    ```

- Note the use of [asyncio.start_server](https://docs.python.org/3/library/asyncio-stream.html#asyncio.start_server)

- `handle_echo` is a coroutine function

- `0.0.0.0` means all interfaces

- `8888` is the port

---

A TCP echo server
-----------------

- Handling the communication with clients

    ```python3
    async def handle_echo(reader, writer):
        data = await reader.read(100)
        message = data.decode()

        addr = writer.get_extra_info('peername')
        print("Received %r from %r" % (message, addr))

        print("Send: %r" % message)
        writer.write(data)
        await writer.drain()

        print("Close the client socket")
        writer.close()
    ```

- [reader.read](https://docs.python.org/3/library/asyncio-stream.html#asyncio.StreamReader.read) works like `socket.recv`

- [writer.write](https://docs.python.org/3/library/asyncio-stream.html#asyncio.StreamWriter.write) works like `socket.send`

- See more helpers in the [stream API docs](https://docs.python.org/3/library/asyncio-stream.html#streams-coroutine-based-api)

---

A TCP echo server
-----------------

- Test the server with netcat (use stdin to send a message):

    ```bash
	$ nc localhost 8888
	hello
	hello
	$
    ```

- Or the [TCP echo client](http://asyncio.readthedocs.io/en/latest/tcp_echo.html#tcp-echo-client) from the user docs

    ```python3
    async def tcp_echo_client(message='hello'):
        reader, writer = await asyncio.open_connection('locahost', 8888)

        print('Send: %r' % message)
        writer.write(message.encode())

        data = await reader.read(100)
        print('Received: %r' % data.decode())

        print('Close the socket')
        writer.close()
    ```

- See [asyncio.open_connection](https://docs.python.org/3/library/asyncio-stream.html#asyncio.open_connection)

---

Asyncio client mode in pytango
------------------------------

- import asyncio-compatible objects from `pytango.asyncio`

  * AttributeProxy

  * DeviceProxy

- use the `await` synthax for all asynchronous operation:

    ```python3
    async def main():
        device = await DeviceProxy('sys/tg_test/1')
        result = await device.read_attribute('ampli')
        print(result.value)
    ```

- run an asynchronous python console using [aioconsole](http://aioconsole.readthedocs.io/en/latest/):

   ```bash
   $ pip install aioconsole
   $ apython
   >>> from tango.asyncio import DeviceProxy as asyncio_proxy
   >>> device = await asyncio_proxy('sys/tg_test/1')
   >>> result = await device.read_attribute('ampli')
   >>> result.value
   1.23
   ```

---

Asyncio client mode in pytango
------------------------------

- Try this [simple TCP server for Tango attributes](https://github.com/tango-controls/pytango/blob/develop/examples/asyncio_green_mode/tcp_server_example.py)

- It runs on all interfaces on port 8888:

    ```bash
    $ python tango_tcp_server.py
    Serving on 0.0.0.0 port 8888
    ```

- It can be accessed through netcat:

    ```bash
    $ ncat localhost 8888
    >>> sys/tg_test/1/ampli
    0.0
    >>> sys/tg_test/1/state
    RUNNING
	>>> sys/tg_test/1/nope
    DevFailed[
    DevError[
         desc = Attribute nope is not supported by device sys/tg_test/1
       origin = AttributeProxy::real_constructor()
       reason = API_UnsupportedAttribute
     severity = ERR]
     ]
    ```

---

Asyncio server mode in pytango
------------------------------

**Experimental** - consider this [asyncio-based device](https://github.com/tango-controls/pytango/blob/develop/examples/asyncio_green_mode/asyncio_device_example.py):

```python3
class AsyncioDevice(Device):
    green_mode = GreenMode.Asyncio

    async def init_device(self):
        await super().init_device()
        self.set_state(DevState.ON)

    @command
    async def long_running_command(self):
        loop = asyncio.get_event_loop()
        future = loop.create_task(self.coroutine_target())

    async def coroutine_target(self):
        self.set_state(DevState.INSERT)
        await asyncio.sleep(15)
        self.set_state(DevState.EXTRACT)

    @attribute
    async def test_attribute(self):
        await asyncio.sleep(2)
        return 42
```

---

name: title
class: center, middle

# Thanks!

### Questions?

***

Slides on [**GitHub pages**](http://vxgmichel.github.io/asyncio-overview)

Presentation written in [**Markdown**](https://daringfireball.net/projects/markdown/)

Rendered by [**remark**](https://remarkjs.com/#1) slideshow tool
