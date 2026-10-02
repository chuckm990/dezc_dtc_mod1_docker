from pathlib import Path

current_dir = Path.cwd() # gets current working directory to instance of Path object
current_file = Path(__file__).name # gets the name of this file using the dunder command __file__

print(f"Files in {current_dir}:")

for filepath in current_dir.iterdir():
    if filepath.name == current_file: # skip the current python script
        continue

    print(f"  - {filepath.name}")

    if filepath.is_file():
        content = filepath.read_text(encoding='utf-8')
        print(f"    Content: {content}")