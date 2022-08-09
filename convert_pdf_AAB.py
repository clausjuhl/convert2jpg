import re
import img2pdf
from pathlib import Path
import os


def generate_pdf(folder_object: Path, out_file_object: Path):
    # folder_object, out_file_object and obj are Path-objects
    files = []
    for obj in folder_object.rglob('*.*'):
        if obj.suffix in ['.jpg', '.jpeg']:
            files.append(str(obj))  # img2pdf.convert requirement
    try:
        with open(out_file_object, "wb") as f:
            f.write(img2pdf.convert(files))
    except ValueError as e:
        print(f"Unable to convert jpgs in: {folder_object}", flush=True)

if __name__ == '__main__':
    ROOT = Path("G:\\AAB")
    print("Beginning pdf-production...", flush=True)
    for protocol in ROOT.iterdir():

        # if re.match("^AAB ", protocol.name):
        #     continue
        content: list = os.listdir(str(protocol)) or []
        if protocol.stem + ".pdf" in content:
            continue
        else:
            # print(f"about to generate pdf in: {protocol}")
            print(f"Generating pdf in {protocol}", flush=True)
            generate_pdf(Path(protocol, "jpgs"), Path(protocol, protocol.stem + ".pdf"))


        # for folder in protocol.iterdir():
        #     if folder.is_file():
        #         # print(f"Found file in {folder}", flush=True)
        #         continue
        #     if folder.name + ".pdf" in os.listdir(protocol):
        #         # print(f"Found existing '.pdf': {folder}", flush=True)
        #         continue

        #     if folder.name != "jpgs":
        #         # print(f"Wrong foldername: {folder}", flush=True)
        #         continue

        #     if not os.listdir(folder):
        #         print(f"Empty 'jpgs'-folder: {folder}", flush=True)
        #     else:
        #         generate_pdf(folder, Path(protocol, protocol.stem + ".pdf"))
            # print(f"Finished generating pdf for {protocol.name}", flush=True)
    print("Finished!")
