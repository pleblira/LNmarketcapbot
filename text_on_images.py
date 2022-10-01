import readline
from PIL import Image, ImageDraw, ImageFont, ImageOps
# import sys
import os
import time

def image_draw_angled(LN_capacity_in_BTC):
        img = Image.open("mascot_belly.jpg")
        font = ImageFont.truetype("Silom.ttf",74)
        
        # Creating a temporary canvas, drawing the text on it, and rotating
        temporary_canvas = Image.new(mode='L', size=(500,500))
        text_on_temporary_canvas = ImageDraw.Draw(temporary_canvas)
        text_on_temporary_canvas.text((0, 0), str(LN_capacity_in_BTC) + "\nBTC", font=font, fill=255, align="center")
        rotated_text_on_temporary_canvas=temporary_canvas.rotate(-24, resample=3, expand=1)

        # pasting temporary canvas on main image
        img.paste( ImageOps.colorize(rotated_text_on_temporary_canvas, (0,0,0), (242,169,0)), (222,895), rotated_text_on_temporary_canvas)
        # img.show()

        # time.sleep(0.1)
        # print(file_count)
        # img.save( str(file_count+1) + ".jpg")
        img.show()

# def image_draw():
#     img = Image.open('mascot_belly.jpg')
#     font = ImageFont.truetype("Arial.ttf",74)
#     d1 = ImageDraw.Draw(img)
#     d1.text((388,925), LN_capacity_in_BTC, font=font, fill=(242, 169, 0), align="center")
#     img.show()
#     return img


if __name__ == "__main__":
    # image_draw()
    image_draw_angled(3500)
