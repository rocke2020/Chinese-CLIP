from PIL import Image
from io import BytesIO
import base64, binascii


def image_to_b64(file_name="examples/pokemon.jpeg"):
    """  """
    img = Image.open(file_name) # 访问图片路径
    img_buffer = BytesIO()
    img.save(img_buffer, format=img.format)
    byte_data = img_buffer.getvalue()
    base64_str = base64.b64encode(byte_data) # bytes
    base64_str = base64_str.decode("utf-8") # str
    return base64_str


def b64_to_img():
    """  """
    base64_string = "place the base64 string here"
    try:
        image = base64.b64decode(base64_string, validate=True)
        file_to_save = "name or path of the file to save,let's say, my_image.png"
        with open(file_to_save, "wb") as f:
            f.write(image)
    except binascii.Error as e:
        print(e)

if __name__ == "__main__":
    import sys, os
    sys.path.append(os.path.abspath('.'))
    from utils.file_util import FileUtil

    # s = image_to_b64()
    # FileUtil.write_text([s], "examples/pokemon.b64.txt")

    with open("examples/pokemon.jpeg", "rb") as f:
        base64_string = base64.b64encode(f.read()).decode("utf-8")
    FileUtil.write_text([base64_string], "examples/pokemon.b642.txt")
    pass