from PIL import Image, ImageDraw, ImageFont, ImageOps
import os

# todo configuration for images 1, 3, 4, 5.jpg - 2.jpg and 6.jpg are done and good to go


def image_draw_angled(LN_capacity_in_BTC, tweet_image):

        if tweet_image == "assets/blank_belly_dark_mode/2.jpg":
                tweet_image = Image.open(tweet_image)
                # font = ImageFont.truetype("SourceCodePro-Bold.ttf",100)
                font = ImageFont.truetype("Silom.ttf",95)
                
                # Creating a temporary canvas, drawing the text on it, and rotating
                temporary_canvas = Image.new(mode='L', size=(500,500))
                text_on_temporary_canvas = ImageDraw.Draw(temporary_canvas)
                text_on_temporary_canvas.text((0, 0), str(LN_capacity_in_BTC) + "\nBTC", font=font, fill=255, align="center")
                # rotated_text_on_temporary_canvas=temporary_canvas.rotate(-24, resample=3, expand=1)
                rotated_text_on_temporary_canvas=temporary_canvas.rotate(-2.5, resample=3, expand=1)

                # pasting temporary canvas on main image
                # tweet_image.paste( ImageOps.colorize(rotated_text_on_temporary_canvas, (0,0,0), (242,169,0)), (462,1190), rotated_text_on_temporary_canvas)
                tweet_image.paste( ImageOps.colorize(rotated_text_on_temporary_canvas, (0,0,0), (242,169,0)), (712,1315), rotated_text_on_temporary_canvas)

                # tweet_image.show()
                tweet_image.save("assets/tweet_image.jpg")
                return None
                
        if tweet_image == "assets/blank_belly_dark_mode/6.jpg":
                tweet_image = Image.open(tweet_image)
                # font = ImageFont.truetype("SourceCodePro-Bold.ttf",100)
                font = ImageFont.truetype("Silom.ttf",90)
                
                # Creating a temporary canvas, drawing the text on it, and rotating
                temporary_canvas = Image.new(mode='L', size=(500,500))
                text_on_temporary_canvas = ImageDraw.Draw(temporary_canvas)
                text_on_temporary_canvas.text((0, 0), str(LN_capacity_in_BTC) + "\nBTC", font=font, fill=255, align="center")
                # rotated_text_on_temporary_canvas=temporary_canvas.rotate(-24, resample=3, expand=1)
                rotated_text_on_temporary_canvas=temporary_canvas.rotate(-23.2, resample=3, expand=1)

                # pasting temporary canvas on main image
                # tweet_image.paste( ImageOps.colorize(rotated_text_on_temporary_canvas, (0,0,0), (242,169,0)), (462,1190), rotated_text_on_temporary_canvas)
                tweet_image.paste( ImageOps.colorize(rotated_text_on_temporary_canvas, (0,0,0), (242,169,0)), (455,1190), rotated_text_on_temporary_canvas)

                # tweet_image.show()
                tweet_image.save("assets/tweet_image.jpg")
                return None


# if __name__ == "__main__":
#     image_draw_angled(5002, "assets/blank_belly_dark_mode/6.jpg")