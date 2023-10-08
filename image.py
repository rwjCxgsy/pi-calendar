
from PIL import Image
import random
# 打开图片
image = Image.open('me2.jpg')  # 替换为你的图片路径


# 缩放图像
width = 800  # 目标宽度
height = 480  # 目标高度

# 转换为灰度图像
grayscale_image = image.convert('L')
resized_image = grayscale_image.resize((width, height))
binary_image = resized_image.point(lambda x: 0 if x < 64 else 1 if x < 160 else 2)

new_image = Image.new('1', (width, height), 1)  # 255: clear the frame




for y in range(0, height):
    for x in range(0, width):
        value = binary_image.getpixel((x, y))
        if value < 2:
            new_image.putpixel((x, y), 0)
        elif value == 1:
            new_image.putpixel((x, y), 0 if (x % 2 == 0 and y % 2 == 0) else 1)
        else:
            new_image.putpixel((x, y), 1)

# 显示缩放后的图像

new_image.save('boy.jpg')
new_image.show()

