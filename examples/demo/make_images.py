"""Create original demo images; no account or external assets required."""
from pathlib import Path
from PIL import Image, ImageDraw
P=Path(__file__).parent
for page in (1,2):
    for end in (False,True):
        im=Image.new('RGB',(640,870),'#f4e8d0');d=ImageDraw.Draw(im)
        d.ellipse((440,65,565,190),fill='#f4c16b')
        d.rounded_rectangle((50,660,590,820),radius=40,fill='#bd9274')
        d.line((320,680,320,510 if page==1 else 360),fill='#5a8966',width=20)
        if page==1:
            d.ellipse((280,475 if end else 525,360,555 if end else 605),fill='#84ae75')
        else:
            d.ellipse((320,360,460 if end else 400,440),fill='#84ae75')
            d.ellipse((210,420,320,500),fill='#79a56d')
        im.save(P/f'page{page}-{"end" if end else "start"}.png')
print('Demo illustrations created')
