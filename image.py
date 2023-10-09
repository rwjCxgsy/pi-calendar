
from PIL import Image
import random
# 打开图片
image = Image.open('test.jpg')  # 替换为你的图片路径


# 缩放图像
width = 480  # 目标宽度
height = 800  # 目标高度

# 转换为灰度图像
grayscale_image = image.convert('L')
resized_image = grayscale_image.resize((width, height))
# binary_image = resized_image.point(lambda x: 0 if x < 64 else 1 if x < 160 else 2)

new_image = Image.new('1', (width, height), 1)  # 255: clear the frame




for y in range(0, height):
    for x in range(0, width):
        value = resized_image.getpixel((x, y)) / 128
        new_image.putpixel((x, y), 0 if  0.889 >= value else 1)

# 显示缩放后的图像

new_image.save('boy.jpg')
new_image.show()

