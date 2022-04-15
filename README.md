# rust_doctest_fixing_tool
Hacky little tool I made to speed up the process of fixing all the doctests in `rust/compiler/`

You put this repo in a folder so that rust is at `../rust`, then `python3 test_all.py` runs doctests for all of the modules in `rust/compiler/` 
and saves their output to files in `./full_outputs/` (convenient because that process takes ages).

Then run `python3 view_fails.py` and it opens a vscode instance with the first failing doctest, and a vim instance with the error message.
Pressing `d` in vim marks the test as done and moves to the next. `s` skips (doesn't mark done). `q` quits.

`tqdm` can be removed if you don't like dependencies or pretty loading bars.
