import cv2
import numpy as np


width = 800
height = 480


# 绘制左侧

# 绘制右侧

title = 'Lesson 45. A puma at large'
text = "Eric had been the eldest son of the family, very much older than his two brothers. He had been obliged to join the army during the Second World War. As he hated army life, he decided to desert his regiment. When he learnt that he would be sent abroad, he returned to the farm and his father hid him until the end of the war. Fearing the authorities, Eric remained in hiding after the war as well. His father told everybody that Eric had been killed in action. The only other people who knew the secret were Joe and Bob. They did not even tell their wives. When their father died, they thought it their duty to keep Eric in hiding. All these years, Eric had lived as a recluse. He used to sleep during the day and work at night, quite unaware of the fact that he had become the ghost of Endley. When he died, however, his brothers found it impossible to keep the secret any longer."




# 设置文本内容和字体样式
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 0.4
font_color = (0,0,0)  # 白色
thickness = 1

# 标题相关
title_height = 32
title_size = font_scale * 1.6
title_thickness = thickness * 2


# 设置文本框的宽度和行间距
text_width = 500
text_height = height
line_spacing = 24


___debugger___ = False

image = np.zeros((height, width, 3), dtype=np.uint8)

image[:] = (255, 255, 255)


def split_content():
    # 拆分文本为多行
    lines = []
    current_line = ""
    for word in text.split():
        if cv2.getTextSize(current_line + " " + word, font, font_scale, thickness)[0][0] <= text_width:
            current_line += " " + word
        else:
            lines.append(current_line.strip())
            current_line = word
    lines.append(current_line.strip())
    return lines


def draw_title(title, x, y):
    # 绘制标题
    ((title_content_width, title_content_height), __value__no_use__) = cv2.getTextSize(title, font, title_size, title_thickness)
    
    offset_x = int(text_width / 2 - title_content_width / 2)
    offset_y = title_content_height
    
    cv2.putText(image, title, (x + offset_x, y + offset_y), font, title_size, font_color, title_thickness)
    rect = (x + offset_x + title_content_width, y + title_content_height + __value__no_use__)
    if ___debugger___:
        cv2.rectangle(image, (x + offset_x, y), rect, (0,0, 255), 1)
    return rect
    

def draw_content(lines, x, y):
    
    content_height = len(lines) * line_spacing
    
    # 绘制文本框
    for i, line in enumerate(lines):
        line_y = y + ((i + 1) * line_spacing)
        cv2.putText(image, line, (x, line_y), font, font_scale, font_color, thickness)
    rect = (x + text_width, y + content_height)
    if ___debugger___:
        cv2.rectangle(image, (x, y), rect, (0,255, 255), 1)
        
    return rect
        

content = split_content()


total_height = len(content) * line_spacing + title_height

# 计算文本框的位置
x = width - text_width
y = round(text_height / 2 - total_height / 2)


# y += single_height

(new_x, new_y) = draw_title(title=title, x=x, y=y)
(new_x1, new_y1) = draw_content(content, x = x, y = new_y)
if ___debugger___:
    cv2.rectangle(image, (x,y), (x + text_width, new_y1), (0,0, 255), 1)    

# 显示图像
cv2.imshow("Image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()