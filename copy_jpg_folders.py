from pathlib import Path
import shutil

OUTPATH = Path("G:\\AAB")
print("Beginning to copy...")
for protocol in Path("D:\\AAB stadsarkivets kopi 2\\Ikke kopieret til AAB disk").iterdir():
    if protocol.is_dir():
        if not Path(protocol, "jpgs").exists():
            print(f"Did not find any jpgs: {protocol}")
            continue

        name = protocol.name
        Path.mkdir(Path(OUTPATH, name), parents=True, exist_ok=True)
        shutil.copytree(Path(protocol, "jpgs"), Path(OUTPATH, name, "jpgs"))
        print(f"Finished copying jpg-folder fpr {name}", flush=True)
print("Finished!")