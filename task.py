import time
from PIL import Image
from volcengine.visual.VisualService import VisualService

import base64
if __name__ == '__main__':
    visual_service = VisualService()

    # call below method if you dont set ak and sk in $HOME/.volc/config
    visual_service.set_ak('AKLTOTA1NTNlYjMzNzM3NDVlZDg3OGRmZGU4NGIxMDk1NjA')
    visual_service.set_sk('WTJVek5UazFZelppWkdNd05EWXlaRGxtT0RoalptWmpNelEzWVRBd05tWQ==')

    params = dict()
    image = Image.open("test.jpg")

    # 将图像转换为Base64编码
    image_base64 = base64.b64encode(image.tobytes()).decode("utf-8")
    form = {
        "image_base64": "data:image/jpeg;base64," + image_base64
    }

    resp = visual_service.goods_detect(form)
    print(resp)