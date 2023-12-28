#!/usr/bin/env python3.10
import queue
from os import getenv
from pty import openpty
from queue import Queue
from subprocess import Popen
from threading import Thread
from typing import IO

TF_SLEEP = 10  # terraform has a ten-second sleep loop
TIMEOUT = 1 * TF_SLEEP + 1
# TIMEOUT = 1
TERRAFORM = ("terraform", "console")
cmd: tuple[str, ...]
EOF = b""

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

        print("+ :", *msg, file=stderr, flush=True)


def ansi_denoise(ansi_text: bytes):
    import re

    csi = b"\033["
    control_re = re.escape(csi) + b"[^A-Za-z]*[A-Za-z]"
    backspace_re = b".\b"
    noise_re = re.compile(b"|".join((backspace_re, control_re)))
    return noise_re.sub(b"", ansi_text)


parent, child = openpty()
import os

proc = Popen(cmd, stdout=child, stdin=child)
os.close(child)


output: Queue[bytes] = Queue()


def _io_thread():
    while True:
        data = os.read(parent, 32)  # could block forever
        debug("DATA:", repr(data))
        output.put(data)
        if data == EOF:
            break


io_thread = Thread(target=_io_thread, args=(), daemon=True)
io_thread.start()


data = None
result: str | queue.Empty = ""
while data != EOF and not result:
    try:
        data = output.get(timeout=TIMEOUT)
    except queue.Empty as error:
        debug("timeout (seconds):", TIMEOUT)
        result = error
    else:
        result = ansi_denoise(data).decode("UTF-8")

if data == EOF:
    debug("terraform exitted, code", proc.wait())
    io_thread.join()
    raise SystemExit(proc.poll())
else:
    if result == "> ":
        debug("got prompt, exit un-gracefully")
    else:
        debug("unexpected output:", repr(result))

    proc.kill()
    debug("terraform exitted, code", proc.wait())
    io_thread.join()
