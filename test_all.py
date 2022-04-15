import glob
import os
import subprocess
from tqdm import tqdm
if __name__ == "__main__":
    rust_dir = '../rust'
    directories = sorted(glob.glob('*', root_dir=f'{rust_dir}/compiler'))
    for d in tqdm(directories):
        proc = subprocess.run(["python3", "x.py", "test", "--doc", "--stage", "1", f"compiler/{d}"], 
                              cwd=rust_dir,
                              capture_output=True)
        with open(f"full_outputs/{d}", "wb") as fd:
            fd.write(proc.stdout)
