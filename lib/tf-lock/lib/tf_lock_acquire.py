#!/usr/bin/env python3.10
import queue
from os import getenv
from pty import openpty
from queue import Queue
from subprocess import Popen
from threading import Thread

TF_SLEEP = 10  # terraform has a ten-second sleep loop
# TIMEOUT = 1 * TF_SLEEP + 1
TIMEOUT = 1
TERRAFORM = ("terraform", "console")
cmd: tuple[str, ...]

if getenv("DEBUG"):
    DEBUG = True
    cmd = (
        "sh",
        "-exc",
        """\
sleep 333
printf "> "
read -r line
echo line: "$line"
""",
    )
else:
    DEBUG = False
cmd = TERRAFORM


def debug(*msg):
    if DEBUG:
        from sys import stderr

        print("+ :", *msg, file=stderr)


def on_error(expect_out, label):
    if not (message := expect_out.get("buffer")):
        message = f"error: {label}"
    raise SystemError(message)


parent, child = openpty()
import os

proc = Popen(
    cmd,
    stdout=child,
    stdin=child,
)
os.close(child)


io: Queue[bytes] = Queue()


def _io_thread():
    io.put(os.read(parent, 9))


io_thread = Thread(target=_io_thread, daemon=True)
io_thread.start()

got: str | queue.Empty
try:
    got = io.get(timeout=TIMEOUT).decode("UTF-8")
except queue.Empty as error:
    debug("timeout (seconds):", TIMEOUT)
    got = error
else:
    io_thread.join()

if got == " >":
    debug("got prompt, exit un-gracefully")
else:
    debug("unexpected output:", repr(got))

proc.kill()
debug("terraform exitted, code", proc.wait())
