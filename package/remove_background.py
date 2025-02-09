from rembg import remove
from PIL import Image

# 打開圖片
input_path = "input_image.png"
output_path = "output_image.png"

with open(input_path, "rb") as input_file:
    input_image = input_file.read()
    output_image = remove(input_image)

# 保存去背圖片
with open(output_path, "wb") as output_file:
    output_file.write(output_image)
