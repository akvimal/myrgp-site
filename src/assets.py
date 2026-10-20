import os
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "public"))
# Run: python3 src/assets.py  -> favicon, app icons and og-image.jpg in public/
from PIL import Image, ImageDraw, ImageFont
logo=Image.open('logo.png'); a=logo.split()[3].load(); W,H=logo.size
cols=[any(a[x,y]>20 for y in range(H)) for x in range(W)]
x=cols.index(True)
while cols[x]: x+=1
icon=logo.crop((0,0,x,H)); icon=icon.crop(icon.getbbox())
for size,bg,fn in ((48,None,'favicon-48.png'),(180,(255,255,255,255),'apple-touch-icon.png'),(192,(255,255,255,255),'icon-192.png'),(512,(255,255,255,255),'icon-512.png')):
    pad=int(size*(0.04 if bg is None else 0.14))
    c=Image.new('RGBA',(size,size),bg or (0,0,0,0))
    s=(size-2*pad)/max(icon.size); ic=icon.resize((round(icon.width*s),round(icon.height*s)),Image.LANCZOS)
    c.paste(ic,((size-ic.width)//2,(size-ic.height)//2),ic); c.save(fn,optimize=True)
B='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'; R='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
im=Image.new('RGB',(1200,630),(255,255,255)); d=ImageDraw.Draw(im)
d.rectangle((790,0,1200,630),fill=(20,121,42))
s=620/logo.width; lg=logo.resize((620,round(logo.height*s)),Image.LANCZOS); im.paste(lg,(70,80),lg)
d.text((70,250),"Same medicine.",font=ImageFont.truetype(B,64),fill=(11,106,168))
d.text((70,325),"Lower price.",font=ImageFont.truetype(B,64),fill=(20,121,42))
d.text((70,430),"Mogappair West, Chennai",font=ImageFont.truetype(R,30),fill=(75,90,102))
d.text((70,475),"Call / WhatsApp  72990 72725",font=ImageFont.truetype(B,30),fill=(21,34,48))
d.text((830,150),"Up to",font=ImageFont.truetype(B,36),fill=(255,255,255))
d.text((826,195),"80%",font=ImageFont.truetype(B,96),fill=(255,255,255))
d.text((830,315),"off on generic",font=ImageFont.truetype(B,36),fill=(255,255,255))
d.text((830,360),"medicines",font=ImageFont.truetype(B,36),fill=(255,255,255))
d.line((830,440,1140,440),fill=(143,220,160),width=2)
d.text((830,465),"Free delivery above",font=ImageFont.truetype(R,26),fill=(230,247,234))
d.text((830,500),"₹500 within 3 km",font=ImageFont.truetype(R,26),fill=(230,247,234))
im.save('og-image.jpg',quality=88,optimize=True)
print("assets ok")
