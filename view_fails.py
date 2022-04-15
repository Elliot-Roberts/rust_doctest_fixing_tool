import re
import os
import csv
import glob
import subprocess
from tqdm import tqdm
if __name__ == "__main__":
    rust_dir = '../rust'
    directories = sorted(glob.glob('*', root_dir='full_outputs'))
    pat = re.compile(r"    (\S*) - \S* \(line (\d+)")
    fails = set()
    for d in directories:
        with open(f"full_outputs/{d}", 'r') as fp:
            for l in fp.readlines():
                if m := pat.match(l):
                    fails.add((d, *m.group(1, 2)))
    done_file = 'done.csv'
    try:
        with open(done_file, 'r', newline='') as fp:
            done = set(tuple(x) for x in csv.reader(fp))
    except FileNotFoundError:
        done = set()
    fails = sorted(fails - done)
    new_done = set()
    for f in tqdm(fails):
        mod, path, line = f
        loc = f"{mod}/{path}:{line}"
        subprocess.run(["code", 
                        ".",
                        "--goto", f"{rust_dir}/compiler/{loc}"
                       ],
                       cwd=rust_dir
                      )
        escaped = path.replace("/", r"\/")
        ret = subprocess.run(["vim",
                              f"full_outputs/{mod}",
                              "-c", f"/\\V----\ {escaped}\ \\.\\*(line\ {line})",
                              "-s", "init.vim"
                             ]
                            )
        print(f"{loc} : ", end='')
        if (code := ret.returncode) > 1:
            inp = chr(code)
            print(inp)
        else:
            inp = input()
        if inp == "q":
            break
        elif inp == "d":
            new_done.add(f)
            continue
        elif inp == "s":
            continue
    with open(done_file, 'w+', newline='') as fp:
        csv.writer(fp).writerows(new_done)
