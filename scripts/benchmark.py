import contextlib
import json
import os
import subprocess
import multiprocessing

from datetime import datetime
from itertools import islice
from pathlib import Path
from typing import Iterable, Union

from tabulate import tabulate
from typer import run


def run_benchmark(bench_folder):
    if os.path.isdir(bench_folder):
        print(f"Running benchmark for {bench_folder}")

        log_path = bench_folder / "log.txt"
        with open(log_path, "w") as log_file:
            process = subprocess.Popen(
                [
                    "python",
                    "-u",  # Unbuffered output
                    "-m",
                    "gpt_engineer.main",
                    bench_folder,
                    "--steps",
                    "benchmark",
                ],
                stdout=log_file,
                stderr=log_file,
                bufsize=0,
            )

            print("You can stream the log file by running:")
            print(f"tail -f {log_path}")
            print()

            process.wait()

            print("process", bench_folder.name, "finished with code", process.returncode)
            print("Running it. Original benchmark prompt:")
            print()
            with open(bench_folder / "prompt") as f:
                print(f.read())
            print()

            with contextlib.suppress(KeyboardInterrupt):
                subprocess.run(
 

def main(
    n_benchmarks: Union[int, None] = None,
):
    path = Path("benchmark")

    folders: Iterable[Path] = path.iterdir()

    if n_benchmarks:
        folders = islice(folders, n_benchmarks)

    with multiprocessing.Pool() as pool:
        pool.map(run_benchmark, folders)