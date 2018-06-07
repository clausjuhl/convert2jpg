# import cv2
from cv2 import imread, imwrite, resize, IMWRITE_JPEG_QUALITY, INTER_AREA
from gooey import Gooey, GooeyParser
from pathlib import Path


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


def get_images(dir_object):
    # dir_object is a Path-object
    files = []
    for obj in dir_object.rglob('*.*'):
        if obj.suffix in ['.png', '.jpg', '.jp2', '.jpeg', '.tiff', '.tif']:
            files.append(obj)
    return files


def read_image(file_path):
    # https://docs.opencv.org/3.0-last-rst/modules/imgcodecs/doc/reading_and_writing_images.html?highlight=imread#cv2.imread
    return imread(file_path)


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


def save_image(cv_image, filename, jpg_quality=95):
    # https://docs.opencv.org/3.0-last-rst/modules/imgcodecs/doc/reading_and_writing_images.html?highlight=imwrite#cv2.imwrite
    imwrite(filename,
            cv_image,
            [IMWRITE_JPEG_QUALITY, jpg_quality])


if __name__ == '__main__':
    args = parse_args()
    max_height = args.max_height if args.max_height else None
    max_width = args.max_width if args.max_width else None
    quality = 95 if not args.quality else args.quality

    print("Arguments parsed", flush=True)
    images = get_images(Path(args.input_files))
    print("Image(s) fetched", flush=True)
    print("Working with image(s)...", flush=True)
    for img_path in images:
        if max_height or max_width:
            infile = resize_image(img_path,
                                  max_height=max_height,
                                  max_width=max_width)

        else:
            infile = read_image(img_path)

        filename = img_path.stem + ".jpg"
        filepath = Path(args.output_dir) / filename

        save_image(infile,
                   filename=filepath,
                   jpg_quality=quality)
    print("Done", flush=True)
    print("Click 'edit' to convert additional files.")
