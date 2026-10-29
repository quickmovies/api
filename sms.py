import os
import sys
import time
import subprocess

FILES = [f"v{i}.py" for i in range(1, 41)]

def main():
    print("\n=== CRON JOB CONTROLLER ===")
    print("Runs v1.py through v40.py in each round.\n")

    while True:
        try:
            rounds = int(input("How many rounds should run? "))
            if rounds > 0:
                break
            print("Enter a number greater than zero.")
        except ValueError:
            print("Enter a valid whole number.")

    total = rounds * len(FILES)
    completed = 0

    try:
        for round_no in range(1, rounds + 1):
            print(f"\n--- Round {round_no}/{rounds} ---")

            for filename in FILES:
                if not os.path.isfile(filename):
                    completed += 1
                    print(f"\n[{completed}/{total}] SKIP: {filename} missing")
                    continue

                print(f"\n[{completed + 1}/{total}] Running {filename}")

                try:
                    result = subprocess.run(
                        [sys.executable, filename],
                        check=False
                    )
                    status = "OK" if result.returncode == 0 else "FAILED"
                    print(f"{filename}: {status}")
                except KeyboardInterrupt:
                    raise

                completed += 1
                percent = completed * 100 / total
                width = 30
                filled = int(width * completed / total)
                bar = "#" * filled + "-" * (width - filled)

                print(
                    f"[{bar}] {percent:.1f}% "
                    f"({completed}/{total})"
                )

        print("\nAll rounds completed.")

    except KeyboardInterrupt:
        print(f"\n\nCancelled. Completed {completed}/{total} files.")

if __name__ == "__main__":
    main()
