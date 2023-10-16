from PIL import Image
from io import BytesIO
import base64, binascii
import sys, os
sys.path.append(os.path.abspath('.'))
from utils.file_util import FileUtil
from pathlib import Path


def image_file_to_b64(file_name="examples/pokemon.jpeg"):
    """  """
    img = Image.open(file_name) # 访问图片路径
    img_buffer = BytesIO()
    img.save(img_buffer, format=img.format)
    byte_data = img_buffer.getvalue()
    base64_bytes = base64.b64encode(byte_data) # bytes
    base64_str = base64_bytes.decode("utf-8") # str
    return base64_str


def image_file_to_b64_simple(file_name="examples/pokemon.jpeg"):
    """  """
    with open(file_name, "rb") as f:
        base64_string = base64.b64encode(f.read()).decode("utf-8")
    return base64_string


def b64_file_to_img_file(b64_file="examples/pokemon.b64.txt"):
    """  """
    b64_file = Path(b64_file)
    with open(b64_file, "r") as f:
        base64_string = f.read().strip()
    try:
        image = base64.b64decode(base64_string, validate=True)
        file_to_save = b64_file.parent / f"{b64_file.name}.png"
        with open(file_to_save, "wb") as f:
            f.write(image)
    except binascii.Error as e:
        print(e)


if __name__ == "__main__":
    # s = image_file_to_b64()
    # FileUtil.write_text([s], "examples/pokemon.b64.txt")
    # FileUtil.write_text([image_file_to_b64_simple()], "examples/pokemon.b642.txt")
    # b64_file_to_img_file()
    pass