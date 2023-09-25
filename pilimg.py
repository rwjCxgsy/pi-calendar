from PIL import Image, ImageFont, ImageDraw
 
 
x = 400
y = 240
 
text_img = Image.new('RGB', (800, 480), (64, 64, 64))
draw = ImageDraw.Draw(text_img)
font_color = (256, 256, 256)
 
file = 'font/AaGuDianKeBenSong-2.ttf'
font = ImageFont.truetype(file, size=64)
 
text = '任越铭'
# w, h = font.getsize(text[0])
draw.text((x, y), '6:32', font=font, fill=font_color)
text_img.show()
text_img.save('bg.jpg')
# text_img.crop(x, y, x + w, y + h)
