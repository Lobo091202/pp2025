import subprocess
import shlex
import sys
import os

def execute_command(command):
    """
    Executes a shell command with support for:
    - pipes |
    - output redirection >
    - input redirection <
    """

    # -----------------------------
    # 1. Tách theo dấu pipe |
    # -----------------------------
    pipeline = [cmd.strip() for cmd in command.split("|")]

    prev_process = None
    processes = []

    for stage in pipeline:
        args = shlex.split(stage)

        # -------------------------
        # 2. REDIRECTION CHECK
        # -------------------------
        stdin = None
        stdout = None

        # Input redirection
        if "<" in args:
            idx = args.index("<")
            infile = args[idx + 1]
            stdin = open(infile, "r")
            args = args[:idx]

        # Output redirection
        if ">" in args:
            idx = args.index(">")
            outfile = args[idx + 1]
            stdout = open(outfile, "w")
            args = args[:idx]

        # -------------------------
        # 3. CREATE SUBPROCESS
        # -------------------------
        p = subprocess.Popen(
            args,
            stdin=prev_process.stdout if prev_process else stdin,
            stdout=stdout if stdout else subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if prev_process:
            prev_process.stdout.close()

        processes.append(p)
        prev_process = p

    # -----------------------------
    # 4. Lấy output từ tiến trình cuối
    # -----------------------------
    final_output, final_err = processes[-1].communicate()

    # In output nếu không redirect ra file
    if final_output:
        print(final_output)

    if final_err:
        print(final_err, file=sys.stderr)


def shell():
    print("=== Python Mini Shell (PW7) ===")
    print("Type 'exit' or Ctrl+C to quit.")

    while True:
        try:
            cmd = input("shell> ").strip()
            if cmd == "" or cmd is None:
                continue
            if cmd.lower() == "exit":
                break

            execute_command(cmd)

        except KeyboardInterrupt:
            print("\nInterrupted. Type 'exit' to quit.")
        except EOFError:
            break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    shell()
