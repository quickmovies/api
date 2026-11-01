import os
import sys
import time
import signal
import subprocess

FILES = [f"v{i}.py" for i in range(1, 41)]
DELAY = float(os.environ.get("DELAY", "0"))

stop_requested = False

def stop_handler(signum, frame):
    global stop_requested
    stop_requested = True
    print("\nStop requested; finishing current script...", flush=True)

signal.signal(signal.SIGTERM, stop_handler)
signal.signal(signal.SIGINT, stop_handler)

round_no = 0
total_completed = 0

print(f"Starting infinite runner for {len(FILES)} files. Press Ctrl+C to stop safely.", flush=True)

try:
    while not stop_requested:
        round_no += 1
        print(f"\n=== Round {round_no} (Infinite Mode) ===", flush=True)
        
        for filename in FILES:
            if stop_requested:
                break
                
            if not os.path.isfile(filename):
                print(f"SKIP: {filename} not found", flush=True)
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
                
            total_completed += 1
            print(f"Total files executed across all rounds: {total_completed}", flush=True)
            
            if DELAY > 0:
                time.sleep(DELAY)

finally:
    print(
        f"\nStopped safely. Total files processed across all rounds: {total_completed}.",
        flush=True
    )
