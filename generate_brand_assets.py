from PIL import Image, ImageDraw, ImageFont
import os

BG=(20,24,29)
RED=(210,48,52)
WHITE=(248,248,248)

def font(size,bold=True):
    paths=["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf","/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p,size)
    return ImageFont.load_default()

def centered(draw,text,y,f,fill,canvas_w):
    box=draw.textbbox((0,0),text,font=f)
    x=(canvas_w-(box[2]-box[0]))//2
    draw.text((x,y),text,font=f,fill=fill)

# Splash: only the approved two lines, no Android/version text.
w,h=1080,1920
im=Image.new("RGB",(w,h),BG); d=ImageDraw.Draw(im)
centered(d,"Mazda 6 GH",760,font(86),WHITE,w)
centered(d,"AS-BUILT STUDIO",885,font(52),WHITE,w)
im.save("presplash.png",optimize=True)

# App icon: dark rounded square, red border, M6 + AS-BUILT.
s=1024
im=Image.new("RGB",(s,s),BG); d=ImageDraw.Draw(im)
d.rounded_rectangle((70,70,s-70,s-70),radius=150,fill=(38,43,49),outline=RED,width=28)
centered(d,"M6",270,font(300),WHITE,s)
centered(d,"AS-BUILT",650,font(88),WHITE,s)
im.save("icon.png",optimize=True)
