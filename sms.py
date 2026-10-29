
import os
import sys
import time
import signal
import subprocess

FILES = [f"v{i}.py" for i in range(1, 41)]
ROUNDS = int(os.environ.get("ROUNDS", "1"))
DELAY = float(os.environ.get("DELAY", "0"))

if ROUNDS < 1:
    raise ValueError("ROUNDS must be at least 1")

stop_requested = False

def stop_handler(signum, frame):
    global stop_requested
    stop_requested = True
    print("\nStop requested; finishing current script...", flush=True)

signal.signal(signal.SIGTERM, stop_handler)
signal.signal(signal.SIGINT, stop_handler)

total = ROUNDS * len(FILES)
completed = 0

print(f"Starting {ROUNDS} rounds; {total} maximum file runs.", flush=True)

try:
    for round_no in range(1, ROUNDS + 1):
        if stop_requested:
            break

        print(f"\n=== Round {round_no}/{ROUNDS} ===", flush=True)

        for filename in FILES:
            if stop_requested:
                break

            if not os.path.isfile(filename):
                print(f"SKIP: {filename} not found", flush=True)
                completed += 1
                continue

            print(f"Running {filename}", flush=True)

            try:
                result = subprocess.run(
                    [sys.executable, filename],
                    check=False,
                    timeout=300
                )
                status = "OK" if result.returncode == 0 else "FAILED"
                print(f"{filename}: {status}", flush=True)
            except subprocess.TimeoutExpired:
                print(f"{filename}: TIMEOUT", flush=True)
            except Exception as exc:
                print(f"{filename}: ERROR: {exc}", flush=True)

            completed += 1
            percent = completed * 100 / total
            width = 25
            filled = int(width * completed / total)
            print(
                f"[{'#' * filled}{'-' * (width - filled)}] "
                f"{percent:.1f}% ({completed}/{total})",
                flush=True
            )

            if DELAY > 0:
                time.sleep(DELAY)

finally:
    print(
        f"Finished or stopped: {completed}/{total} entries processed.",
        flush=True
    )
