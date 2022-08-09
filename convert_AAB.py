# import cv2
from cv2 import Mat, imread, imwrite, resize, IMWRITE_JPEG_QUALITY, INTER_AREA
from gooey import Gooey, GooeyParser
from pathlib import Path
import subprocess

@Gooey(program_name="convert2jpg",
       return_to_config=True,
       header_height=60)
def parse_args():
    desc = "Skalér og konvertér en eller flere billedfiler til jpg"
    input_files_msg = "Marker en eller flere filer, der skal konverteres"
    output_dir_msg = "Vælg eller opret mappe, hvor jpg-filerne skal gemmes"

    parser = GooeyParser(description=desc)

    # widget="MultiFileChooser")  # buggy - upgrade later
    parser.add_argument("input_files",
                        metavar="Vælg input-mappe med billedfiler.",
                        help=input_files_msg,
                        widget="DirChooser")
    parser.add_argument("output_dir",
                        metavar="Vælg output-mappe til jpg-filer",
                        help=output_dir_msg,
                        widget="DirChooser")
    parser.add_argument('-mw',
                        '--max_width',
                        metavar="Maksimal billedbredde i pixels",
                        help="max_width of images in pixels")
    parser.add_argument('-mh',
                        '--max_height',
                        metavar="Maksimal billedhøjde i pixels",
                        help="max_height of images in pixels")
    parser.add_argument('-q',
                        '--quality',
                        metavar="JPG-kvalitet",
                        help="Choose quality of output-files. Defaults to 95%")
    return parser.parse_args()


def get_images(dir_object: Path) -> list[Path]:
    # dir_object is a Path-object
    files = []
    for obj in dir_object.iterdir():
        if obj.suffix in ['.tiff', '.tif']:
            files.append(obj)
    return files


def read_image(file_path: Path):
    # https://docs.opencv.org/3.0-last-rst/modules/imgcodecs/doc/reading_and_writing_images.html?highlight=imread#cv2.imread
    return imread(str(file_path))


def resize_image(file_path, max_height=None, max_width=None):
    # https://docs.opencv.org/3.0-last-rst/modules/imgcodecs/doc/reading_and_writing_images.html?highlight=imread#cv2.imread
    cv_image = imread(file_path)

    height, width = cv_image.shape[:2]
    scaling_factor = 1

    # shrink if img-dimentions are bigger than required
    if max_height and max_height/float(height) < scaling_factor:
        scaling_factor = max_height / float(height)

    if max_width and max_width/float(width) < scaling_factor:
        scaling_factor = max_width / float(width)

    # https://docs.opencv.org/3.0-last-rst/modules/imgproc/doc/geometric_transformations.html?highlight=resize#cv2.resize
    resized = resize(cv_image,
                     None,  # TODO: What is this param?
                     fx=scaling_factor,
                     fy=scaling_factor,
                     interpolation=INTER_AREA)

    return resized


def save_image(cv_image: Mat, filename: Path):
    # https://docs.opencv.org/3.0-last-rst/modules/imgcodecs/doc/reading_and_writing_images.html?highlight=imwrite#cv2.imwrite
    imwrite(str(filename), cv_image)


def convert_images(images: list[Path], out_dir: Path) -> None:
    Path.mkdir(out_dir, parents=True, exist_ok=True)
    # for img_path in images:
    #     filename = img_path.stem + ".jpg"
    #     try:
    #         infile: Mat = read_image(img_path)
    #     except Exception as e:
    #         print(f"Unable to read image: {img_path}. Error: {e}")
    #     else:
    #         try:
    #             save_image(infile, filename=Path(out_dir, filename))
    #         except Exception as e:
    #             print(f"Unable to save image: {img_path}. Error: {e}")

    for img_path in images:
        filename = img_path.stem + ".jpg"
        try:
            cmd: list[str] = [
                "magick",
                "convert",
                str(img_path),
                f"{out_dir}/{filename}",
            ]
            subprocess.run(cmd, check=True, capture_output=True)
        except Exception as e:
            print(f"Unable to save image: {img_path}. Error: {e}")


def get_empty_jpg_folders(root: Path) -> list:
    folders: list = []
    for dir in Path("G:\AAB").glob("**/*"):
        if dir.name == "jpgs" and dir.stat().st_size < 30:
            folders.append(dir)
    return folders

if __name__ == '__main__':
    OUTPATH = Path("G:\\AAB")
    ROOT = Path("D:\\AAB stadsarkivets kopi 1")
    # empty_folders = get_empty_jpg_folders(ROOT)

    for protocol in ROOT.iterdir():
        images = get_images(protocol)
        if images:
            out_dir = Path(OUTPATH, protocol.name, "jpgs")
            if out_dir.exists() and out_dir.stat().st_size > 20:
                continue
            convert_images(images, out_dir)
            print(f"Finished converting images in {protocol}", flush=True)

        else:
            for folder_content in protocol.iterdir():
                if folder_content.is_file():
                    continue
                elif folder_content.name in ["Color", "thumb", "tmpfilename", "undo"]:
                    continue
                out_dir = Path(OUTPATH, folder_content.name, "jpgs")
                if out_dir.exists() and out_dir.stat().st_size > 20:
                    continue
                images = get_images(folder_content)
                if not images:
                    print(f"Subfolder without tif-files: {folder_content}", flush=True)
                    continue
                convert_images(images, out_dir)
                print(f"Finished converting images in {folder_content}", flush=True)

    print("Finished!")