"""Build public/index.html (English) and public/ta.html (Tamil) from template.html + ta.py.
Run:  python3 src/build.py
"""
import re,base64,urllib.parse,html,os
from ta import TA
HERE=os.path.dirname(os.path.abspath(__file__))
PUB=os.path.join(HERE,'..','public')
os.chdir(HERE)
t=open('template.html').read()
b64=lambda p:'data:image/png;base64,'+base64.b64encode(open(p,'rb').read()).decode()
LOGO,LOGOD=b64(os.path.join(PUB,'logo.png')),b64(os.path.join(PUB,'logo-dark.png'))
pat=re.compile(r'\[\[(\w+)\|(.*?)\]\]',re.S)
keys={m.group(1) for m in pat.finditer(t)}
assert not (keys-set(TA)), keys-set(TA)
wa=lambda msg:"https://wa.me/917299072721?text="+urllib.parse.quote(msg)
cfg={'en':dict(LANG='en',LANGNAME='English',OGLOCALE='en_IN',OGLOCALE_ALT='ta_IN',PAGE_URL='https://myrgp.in/',OTHER_HREF='ta.html',OTHER_LANG='ta',OTHER_NAME='தமிழ்',
      WA_REFILL=wa("Hello Ramesh Generic Pharmacy, I would like to refill my medicines. I am sending a photo of my prescription."),
      WA_COMPARE=wa("Hello Ramesh Generic Pharmacy, please check your price for my medicines. I am sending a photo of my bill / prescription.")),
     'ta':dict(LANG='ta',LANGNAME='Tamil',OGLOCALE='ta_IN',OGLOCALE_ALT='en_IN',PAGE_URL='https://myrgp.in/ta.html',OTHER_HREF='index.html',OTHER_LANG='en',OTHER_NAME='English',
      WA_REFILL=wa("வணக்கம் ரமேஷ் ஜெனரிக் பார்மசி, எனக்கு மருந்து ரீஃபில் வேண்டும். மருந்துச் சீட்டின் படத்தை அனுப்புகிறேன்."),
      WA_COMPARE=wa("வணக்கம் ரமேஷ் ஜெனரிக் பார்மசி, என் மருந்துகளுக்கான உங்கள் விலையைச் சொல்லுங்கள். பில் / மருந்துச் சீட்டின் படத்தை அனுப்புகிறேன்."))}
for lang,c in cfg.items():
    out=pat.sub((lambda m:m.group(2)) if lang=='en' else (lambda m:TA[m.group(1)]), t)
    c=dict(c,LOGO=LOGO,LOGO_DARK=LOGOD,WA_REFILL=html.escape(c['WA_REFILL']),WA_COMPARE=html.escape(c['WA_COMPARE']))
    for k,v in c.items(): out=out.replace('{{'+k+'}}',v)
    assert '{{' not in out and '[[' not in out
    name='index.html' if lang=='en' else 'ta.html'
    i=out.index('<header')
    doc=('<!doctype html>\n<html lang="%s">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
         '<style>body{margin:0}img{max-width:100%%}[hidden]{display:none!important}</style>\n%s</head>\n<body>\n%s</body>\n</html>\n')%(lang,out[:i],out[i:])
    open(os.path.join(PUB,name),'w').write(doc)
print("built public/index.html and public/ta.html")
