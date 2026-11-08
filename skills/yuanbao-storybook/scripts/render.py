#!/usr/bin/env python3
"""Render a small, silent or music-backed picture book from local images."""
import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps
import imageio_ffmpeg

def resolve_font(explicit, size):
    candidates = [explicit, os.environ.get('STORYBOOK_FONT'),
        'C:/Windows/Fonts/msyh.ttc', '/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc',
        '/System/Library/Fonts/PingFang.ttc', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
    for candidate in candidates:
        if candidate and Path(candidate).is_file():
            return ImageFont.truetype(str(candidate), size)
    raise ValueError('No font found. Supply --font with a font supporting your text.')

def load_story(path):
    data=json.loads(path.read_text(encoding='utf-8'))
    width,height=data.get('width',720),data.get('height',1280)
    fps=data.get('fps',6);seconds=data.get('page_seconds',3)
    pages=data.get('pages')
    if not isinstance(width,int) or not isinstance(height,int) or min(width,height)<128 or width%2 or height%2:
        raise ValueError('width and height must be even integers >= 128')
    if not isinstance(fps,int) or not 1<=fps<=60 or not isinstance(seconds,(int,float)) or not 1<=seconds<=20:
        raise ValueError('fps must be 1..60 and page_seconds 1..20')
    if not isinstance(pages,list) or not pages:
        raise ValueError('pages must be a non-empty list')
    result=[]
    for page in pages:
        paths=page.get('images',[]);lines=page.get('lines',[])
        if not isinstance(paths,list) or not 1<=len(paths)<=12 or not isinstance(lines,list) or len(lines)>3 or any(not isinstance(x,str) for x in lines):
            raise ValueError('Each page needs 1..12 images and up to 3 text lines')
        images=[]
        for item in paths:
            src=(path.parent/item).resolve()
            if not src.is_file():raise FileNotFoundError(src)
            with Image.open(src) as im:
                images.append(ImageOps.fit(im.convert('RGB'),(width-80,round(height*.68)),method=Image.Resampling.LANCZOS))
        result.append((images,lines))
    return width,height,fps,seconds,result

def render(story,output,font_path,audio):
    w,h,fps,seconds,pages=load_story(story);frames=round(fps*seconds)
    if frames<2:raise ValueError('At least 2 frames per page are required')
    duration=frames*len(pages)/fps; font=resolve_font(font_path,max(20,round(w*.055)))
    output.parent.mkdir(parents=True,exist_ok=True)
    if output.exists():raise FileExistsError(f'Refusing to overwrite {output}')
    cmd=[imageio_ffmpeg.get_ffmpeg_exe(),'-y','-hide_banner','-loglevel','error',
        '-f','rawvideo','-pixel_format','rgb24','-video_size',f'{w}x{h}','-framerate',str(fps),'-i','-']
    if audio:cmd+=['-stream_loop','-1','-i',str(audio)]
    cmd+=['-map','0:v:0']
    if audio:cmd+=['-map','1:a:0','-af',f'atrim=duration={duration},afade=t=out:st={max(0,duration-1)}:d=1','-c:a','aac','-b:a','160k']
    else:cmd+=['-an']
    cmd+=['-t',str(duration),'-c:v','libx264','-preset','medium','-crf','20','-pix_fmt','yuv420p','-movflags','+faststart',str(output)]
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    try:
        for images,lines in pages:
            for n in range(frames):
                progress=min(1,n/max(1,frames*.55)); position=progress*(len(images)-1)
                lo=int(position);hi=min(lo+1,len(images)-1)
                pic=Image.blend(images[lo],images[hi],position-lo)
                canvas=Image.new('RGB',(w,h),(251,247,235));canvas.paste(pic,(40,40))
                d=ImageDraw.Draw(canvas);y=round(h*.75);total=sum(len(line) for line in lines)
                visible=round(max(0,min(1,(n/fps-.3)/1.2))*total)
                for line in lines:
                    text=line[:max(0,visible)];visible-=len(line)
                    if d.textlength(line,font=font)>w-70:raise ValueError('Text too wide; split it into shorter lines')
                    d.text(((w-d.textlength(line,font=font))/2,y),text,font=font,fill=(59,76,62));y+=round(w*.09)
                proc.stdin.write(canvas.tobytes())
    except BaseException:
        proc.stdin.close();proc.wait();output.unlink(missing_ok=True);raise
    proc.stdin.close();err=proc.stderr.read().decode('utf-8','replace');code=proc.wait()
    if code:output.unlink(missing_ok=True);raise RuntimeError(err)
    print(f'Wrote {output}: {w}x{h}, {fps} fps, {duration:.2f} seconds, audio={bool(audio)}')

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('story',type=Path);p.add_argument('--output',type=Path,required=True);p.add_argument('--font');p.add_argument('--audio',type=Path)
    args=p.parse_args()
    try:
        if args.audio and not args.audio.is_file():raise FileNotFoundError(args.audio)
        render(args.story.resolve(),args.output.resolve(),args.font,args.audio)
    except (ValueError,OSError,RuntimeError,json.JSONDecodeError) as e:
        print(f'Error: {e}',file=sys.stderr);return 1
    return 0
if __name__=='__main__':raise SystemExit(main())
