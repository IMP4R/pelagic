from pathlib import Path
import re,base64
p=Path('index.html');s=p.read_text();assets=Path('media');assets.mkdir(exist_ok=True)
seen={}
def extract(m):
 mime,data=m.group(1),m.group(2);key=(mime,data)
 if key not in seen:
  ext={'video/mp4':'mp4','image/png':'png','image/jpeg':'jpg'}[mime];name=f'media/scene-{len(seen)}.{ext}';Path(name).write_bytes(base64.b64decode(data));seen[key]=name
 return './'+seen[key]
s=re.sub(r'data:(video/mp4|image/png|image/jpeg);base64,([A-Za-z0-9+/=]+)',extract,s)
# Geometry must agree with stable CSS sticky height, not iOS's changing visual viewport.
s=s.replace('const h=innerHeight;const states=chapters.map','const h=hero.querySelector(\'.stage\').clientHeight;const states=chapters.map')
s=s.replace("v.style.visibility='visible';seek(v,p);","v.style.visibility='visible';if(r.bottom>0&&r.top<h)seek(v,p);")
# Do not redraw hidden/unavailable surfaces or run the whole page simulation behind loader.
s=s.replace('if(!enabled||document.hidden)return;if(now-last<','if(!enabled||document.hidden)return;if(document.documentElement.classList.contains(\'pelagic-loading\')){wake();return}if(now-last<')
# Mobile Safari viewport resize must not recreate wave buffers while browser toolbar moves.
s=s.replace("addEventListener('resize',()=>{resize();wake()});","let layoutWidth=innerWidth;addEventListener('resize',()=>{if(Math.abs(innerWidth-layoutWidth)>25){layoutWidth=innerWidth;resize()}layoutDirty=true;wake()});")
# Cache the coarse-pointer query outside hot frame callback.
s=s.replace("const NS='http://www.w3.org/2000/svg',reduced=", "const coarsePointer=matchMedia('(pointer:coarse)').matches;const NS='http://www.w3.org/2000/svg',reduced=")
s=s.replace("matchMedia('(pointer:coarse)').matches?65:48",'coarsePointer?80:48')
# Bound filtering on touch: no filtering huge paragraphs, transformed title stacks or gradients separately.
s=s.replace("?[...el.children]:[el]", "?[...el.children].filter(child=>child.matches('video,.hero-copy,.chapter-content')):[el]")
# Critical: use stable dimensions for document advection during URL-bar animation.
s=s.replace('delta/innerHeight*H','delta/document.documentElement.clientHeight*H')
s=s.replace('</head>','<style>@media(pointer:coarse){html{scroll-behavior:auto}.line{display:block}.scene{backface-visibility:hidden}.chapter-content{perspective:none}#site-loader{contain:layout paint}.mobile-nav{overscroll-behavior:contain}.hero-copy h1,.chapter h2{overflow-wrap:normal}.hero-copy .line,.chapter h2 .line{white-space:nowrap}}</style></head>',1)
p.write_text(s);print('Extracted',len(seen),'assets; HTML',len(s),'bytes')
