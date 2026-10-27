#!/usr/bin/env python3
"""Stop the whole build process group when a compiler reports an error.

Some pinned hxcpp builds hang after reporting a native compiler error instead
of returning a failure status. Preserve their output and fail CI promptly.
"""

import os
import re
import signal
import subprocess
import sys


def main():
    if len(sys.argv) < 2:
        raise SystemExit("Usage: run-build.py COMMAND [ARG ...]")

    process = subprocess.Popen(
        sys.argv[1:],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        errors="replace",
        bufsize=1,
        start_new_session=True,
    )
    for line in process.stdout:
        print(line, end="", flush=True)
        plain = re.sub(r"\x1b\[[0-9;]*m", "", line).strip()
        if plain.startswith("Error:") or re.search(r": (?:fatal )?error:", plain):
            try:
                os.killpg(process.pid, signal.SIGTERM)
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGKILL)
                process.wait()
            except ProcessLookupError:
                pass
            print(process.stdout.read(), end="", flush=True)
            return 1
    return process.wait()


if __name__ == "__main__":
    sys.exit(main())
