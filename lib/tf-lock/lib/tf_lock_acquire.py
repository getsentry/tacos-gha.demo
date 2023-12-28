#!/usr/bin/env python3.10
import asyncio
from os import getenv

Command = tuple[str, ...]
TF_SLEEP = 10  # terraform has a ten-second sleep loop
TIMEOUT = 1 * TF_SLEEP + 1
TERRAFORM: Command = ("terraform", "console")
EOF = b""

if getenv("DEBUG"):
    TIMEOUT = 1
    DEBUG = True
    TERRAFORM = (
        "sh",
        "-exc",
        """\
echo 1
printf "> "
read -r line
echo line: "$line"
""",
    )
else:
    DEBUG = False


def debug(*msg):
    if DEBUG:
        from sys import stderr

        print("+ :", *msg, file=stderr, flush=True)


def ansi_denoise(ansi_text: bytes):
    import re

    csi = b"\033["  # ]  auto-indenter is stupid =.=
    control_re = re.escape(csi) + b"[^A-Za-z]*[A-Za-z]"
    backspace_re = b".\b"
    noise_re = re.compile(b"|".join((backspace_re, control_re)))
    return noise_re.sub(b"", ansi_text)


async def get_prompt(output: asyncio.StreamReader) -> str:
    while not output.at_eof():
        data = await output.read(32)
        prompt = ansi_denoise(data)
        if prompt:
            return prompt.decode("UTF-8")
    return ""


async def run_terraform(cmd: Command):
    import os

    parent, child = os.openpty()

    import tty

    tty.setraw(parent)

    proc = await asyncio.create_subprocess_exec(*cmd, stdout=child, stdin=child)
    os.close(child)

    loop = asyncio.get_running_loop()
    output = asyncio.StreamReader(loop=loop)

    await loop.connect_read_pipe(
        lambda: asyncio.StreamReaderProtocol(output, loop=loop),
        os.fdopen(parent, "rb", buffering=0),
    )
    return proc, output


async def tf_lock_acquire() -> None:
    proc, output = await run_terraform(TERRAFORM)
    wait = asyncio.create_task(proc.wait())
    prompt = asyncio.create_task(get_prompt(output))

    await asyncio.wait(
        [wait, prompt],
        return_when=asyncio.FIRST_COMPLETED,
        timeout=TIMEOUT,
    )
    if wait.done():
        returncode = wait.result()
        debug("terraform exitted early, code", returncode)
        raise SystemExit(returncode)
    elif not prompt.done():
        proc.kill()
        debug("timeout (seconds):", TIMEOUT)
    elif (result := prompt.result()) == "> ":
        debug("got prompt, exit un-gracefully")
        assert not wait.done(), wait
        proc.kill()
        debug("terraform exitted, code", await proc.wait())

    else:
        debug("unexpected output:", repr(result))


def main():
    import logging

    logging.basicConfig(level=logging.DEBUG if DEBUG else logging.INFO)
    asyncio.run(tf_lock_acquire(), debug=DEBUG)


if __name__ == "__main__":
    raise SystemExit(main())
