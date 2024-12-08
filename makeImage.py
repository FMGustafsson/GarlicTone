from PIL import Image, ImageDraw, ImageFont
import os
import cv2
import math
import sys
from PIL import Image

def text_on_img(filename='01.png', text="A dog wearing a party hat", size=72):
    
    "Draw a text on an Image, saves it, show it"
    fnt = font = ImageFont.load_default()

    # create image
    image = Image.new(mode = "RGB", size = (1000,200), color = "black")
    draw = ImageDraw.Draw(image)
    
    # draw text
    draw.multiline_text((10,10), text,  fill=(255,255,255),font_size=size,align="center")
    
    return image

def make_total_image(images,prompts,filenames):


    heights, widths = 1000*len(images)+200*len(prompts),1000

    total_width = widths
    max_height = heights

    new_im = Image.new('RGB', (total_width, max_height))

    y_offset = 0
    print(math.ceil(len(filenames)/2))
    for i in range(math.ceil(len(filenames)/2)):
      size = 1000,1000
      new_im.paste(text_on_img(text=prompts[i][0]), (0,y_offset))
      y_offset += 200
      try:
          images[i].thumbnail(size)

          new_im.paste(images[i], (0,y_offset))
          y_offset += images[i].size[1]

      except:
          pass

    return new_im

def make_final_images(people):
    for q in range(len(people)):
        people.append(people[0])
        del people[0]
        filenames = []
        i=0
        round =0
        while i < len(people):
            try:
                stuff = "prompt_"+people[i]+"_"+str(round)+".txt"
                filenames.append(stuff)
                i+=1
            except:
                pass
            try:
                stuff ="image_"+people[i]+"_"+str(round)+".png"
                filenames.append(stuff)
                i+=1
                round+=1
            except:
                pass

        print(filenames)

        image_dirs =[]
        prompt_dirs =[]
        for file in filenames:
            if file[-1] =="g":
                image_dirs.append(file)
            else:
                prompt_dirs.append(file)

        prompts =[]
        for prompt in prompt_dirs:
            with open(os.path.join("temp/", prompt),"r+") as file:
                text = file.readlines()
                prompts.append(text)
        images = [Image.open(os.path.join("temp/", x)) for x in image_dirs]

        new_im = make_total_image(images,prompts,filenames)
        new_im.save('temp/final_'+str(q)+'.jpg')

