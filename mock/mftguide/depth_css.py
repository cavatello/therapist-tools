# -*- coding: utf-8 -*-
"""Styles and behaviour for the deep sections of a school page.

Kept apart from build_schools.py's CSS so the page skeleton and the content
blocks can be edited independently. Everything here is scoped under .sc, which
is the school page's body class, so none of it can leak into the directory or
the guide if the chrome is ever lifted from a page that carries this stylesheet.
"""

DEPTH_CSS = """<style>/* depth */
.sc .media{display:grid;gap:18px;margin:8px 0 18px}
.sc .vfig,.sc .pfig{margin:0;min-width:0}
.sc .vplay{display:block;position:relative;width:100%;padding:0;border:0;
  background:#0E1A15;border-radius:13px;overflow:hidden;cursor:pointer;
  line-height:0;box-shadow:0 1px 3px rgba(20,38,30,.14)}
.sc .vplay img{width:100%;height:auto;display:block;opacity:.82;
  transition:opacity .18s,transform .5s}
.sc .vplay:hover img{opacity:1;transform:scale(1.02)}
.sc .vplay:focus-visible{outline:3px solid var(--pine);outline-offset:3px}
.sc .vbtn{position:absolute;left:50%;top:50%;width:66px;height:66px;
  transform:translate(-50%,-50%);border-radius:50%;background:rgba(20,38,30,.82);
  border:2px solid rgba(255,255,255,.9);transition:background .18s,transform .18s}
.sc .vplay:hover .vbtn{background:var(--pine);transform:translate(-50%,-50%) scale(1.07)}
.sc .vbtn:after{content:"";position:absolute;left:52%;top:50%;
  transform:translate(-50%,-50%);border-style:solid;border-width:11px 0 11px 18px;
  border-color:transparent transparent transparent #fff}
.sc .vkind{position:absolute;left:12px;top:12px;background:rgba(20,38,30,.86);
  color:var(--amber);font-family:'IBM Plex Mono',ui-monospace,monospace;
  font-size:9.6px;letter-spacing:.1em;text-transform:uppercase;
  padding:5px 9px;border-radius:5px;line-height:1.2}
.sc .vfig figcaption,.sc .pfig figcaption{padding:11px 2px 0;font-size:13.4px;
  line-height:1.6;color:#4A5A46}
.sc .vfig figcaption b{display:block;font-family:Fraunces,Georgia,serif;
  font-size:16px;color:var(--ink);margin-bottom:4px;line-height:1.3}
.sc .vfig figcaption span{display:block}
.sc .vmeta,.sc .cred{font-family:'IBM Plex Mono',monospace;font-size:9.8px;
  letter-spacing:.05em;text-transform:uppercase;color:var(--mut);margin-top:6px}
.sc .cred a{color:var(--mut)}
.sc .pfig img{width:100%;height:auto;display:block;border-radius:13px;
  border:1px solid var(--line)}
.sc .vframe{position:relative;width:100%;aspect-ratio:16/9;border-radius:13px;
  overflow:hidden;background:#000}
.sc .vframe iframe{position:absolute;inset:0;width:100%;height:100%;border:0}

.sc .orient{display:inline-flex;align-items:baseline;gap:9px;margin:0 0 15px;
  background:#F2F6EE;border:1px solid #DDE6D2;border-left:3px solid var(--pine);
  border-radius:8px;padding:9px 14px;max-width:none}
.sc .orient span{font-family:'IBM Plex Mono',monospace;font-size:9.8px;
  letter-spacing:.1em;text-transform:uppercase;color:var(--mut)}
.sc .orient b{font-size:14.6px;color:var(--ink)}

.sc .crsl{display:grid;gap:12px;margin:10px 0 6px}
.sc .crs{background:#fff;border:1px solid var(--line);border-radius:12px;
  padding:17px 19px;min-width:0;border-left:3px solid #CFC7B4}
.sc .crs:hover{border-left-color:var(--pine)}
.sc .chd{display:flex;flex-wrap:wrap;gap:7px;margin-bottom:7px}
.sc .ccode,.sc .cun{font-family:'IBM Plex Mono',monospace;font-size:9.8px;
  letter-spacing:.08em;text-transform:uppercase;padding:4px 8px;border-radius:5px}
.sc .ccode{background:#EAF3DE;color:#27500A}
.sc .cun{background:#F3EFE4;color:var(--mut)}
.sc .crs h3{font-family:Fraunces,Georgia,serif;font-size:17.5px;line-height:1.3;
  font-weight:600;color:var(--ink);margin:0 0 9px}
.sc .crs p{font-size:14.5px;line-height:1.7;margin:0 0 9px;max-width:none}
.sc .cq{margin:0 0 10px;padding:0 0 0 15px;border-left:2px solid #E4D9BE;
  font-size:14.5px;line-height:1.7;color:#3B4A38;font-style:italic}
.sc .cq:before{content:"\\201C"}
.sc .cq:after{content:"\\201D"}
.sc .cwhy{background:#FBF6E9;border-radius:8px;padding:11px 13px;margin:0!important;
  font-size:13.6px;line-height:1.62;color:#4A5A46}
.sc .cwhy span{display:block;font-family:'IBM Plex Mono',monospace;font-size:9.4px;
  letter-spacing:.09em;text-transform:uppercase;color:#9A8F76;margin-bottom:4px}
.sc .srcl{font-family:'IBM Plex Mono',monospace;font-size:9.6px;letter-spacing:.06em;
  text-transform:uppercase;white-space:nowrap;margin-left:7px}

.sc .cutot{display:inline-flex;align-items:baseline;gap:8px;margin:0 0 13px}
.sc .cutot b{font-family:Fraunces,Georgia,serif;font-size:30px;color:var(--pine);
  line-height:1}
.sc .cutot span{font-family:'IBM Plex Mono',monospace;font-size:10px;
  letter-spacing:.09em;text-transform:uppercase;color:var(--mut)}
.sc .trml{display:grid;grid-template-columns:repeat(auto-fill,minmax(238px,1fr));
  gap:11px;margin:10px 0 6px}
.sc .trm{background:#fff;border:1px solid var(--line);border-radius:11px;
  padding:14px 16px;min-width:0;display:flex;flex-direction:column}
.sc .trm>b{font-family:'IBM Plex Mono',monospace;font-size:10.2px;letter-spacing:.09em;
  text-transform:uppercase;color:var(--pine);display:block;margin-bottom:9px;
  padding-bottom:8px;border-bottom:1px solid #F0EBDE}
.sc .trm ol{margin:0;padding:0 0 0 17px;flex:1}
.sc .trm li{font-size:13.2px;line-height:1.52;color:#3B4A38;margin-bottom:6px;
  overflow-wrap:anywhere}
.sc .trm .tn{font-family:'IBM Plex Mono',monospace;font-size:9.4px;letter-spacing:.07em;
  text-transform:uppercase;color:var(--mut);margin-top:9px}

.sc .prg{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));
  gap:10px;margin:14px 0}
.sc .pr{background:#fff;border:1px solid var(--line);border-radius:10px;
  padding:13px 15px;min-width:0}
.sc .pr span{display:block;font-family:'IBM Plex Mono',monospace;font-size:9.6px;
  letter-spacing:.08em;text-transform:uppercase;color:var(--mut);margin-bottom:5px}
.sc .pr b{display:block;font-size:14.2px;line-height:1.5;color:var(--ink);
  font-weight:500;overflow-wrap:anywhere}
.sc .verd.mix{background:#FAF7EE;border-color:#E9E0CB;border-left:4px solid #B9AE93}

.sc .voxl{display:grid;gap:10px;margin:10px 0 6px}
.sc .vox{display:block;background:#fff;border:1px solid var(--line);
  border-radius:10px;padding:14px 16px;text-decoration:none;min-width:0;
  border-left:3px solid #CFC7B4}
.sc a.vox:hover{background:#FBFAF6}
.sc .vox.pos{border-left-color:var(--green)}
.sc .vox.neg{border-left-color:var(--red)}
.sc .vox.mix{border-left-color:#C98B4B}
.sc .vox.inf{border-left-color:#8FA3C4}
.sc .vox i{display:block;font-style:italic;font-size:14.4px;line-height:1.65;
  color:#3B4A38;margin-bottom:7px}
.sc .vwho{display:block;font-size:12.6px;color:var(--ink);font-weight:500}

.sc .gapl{margin:8px 0 14px;padding-left:19px}
.sc .gapl li{font-size:14.2px;line-height:1.68;color:#4A5A46;margin-bottom:7px;
  max-width:66ch}
.sc .srcs{border:1px solid var(--line);border-radius:10px;background:#fff;
  padding:13px 16px;margin:8px 0}
.sc .srcs summary{cursor:pointer;font-family:'IBM Plex Mono',monospace;
  font-size:10.4px;letter-spacing:.08em;text-transform:uppercase;color:var(--pine)}
.sc .srcs ol{margin:12px 0 0;padding-left:19px}
.sc .srcs li{font-size:12.8px;line-height:1.55;margin-bottom:6px;overflow-wrap:anywhere}

@media (max-width:560px){
  .sc .trml{grid-template-columns:minmax(0,1fr)}
  .sc .vbtn{width:54px;height:54px}
  .sc .orient{display:block}
}
@media print{
  .sc .vplay,.sc .vframe{display:none}
}
</style>"""

DEPTH_JS = """<script>
(function(){
  /* Click-to-load video. Nothing from YouTube is requested until the reader
     asks for it - the poster frame comes from i.ytimg.com, which sets no
     cookies, and the player is only ever built against youtube-nocookie.com. */
  document.addEventListener('click',function(e){
    var b=e.target.closest?e.target.closest('.vplay'):null;
    if(!b)return;
    var id=b.getAttribute('data-yt');
    if(!id||!/^[A-Za-z0-9_-]{11}$/.test(id))return;
    var w=document.createElement('div');
    w.className='vframe';
    var f=document.createElement('iframe');
    f.src='https://www.youtube-nocookie.com/embed/'+id+'?autoplay=1&rel=0';
    f.title=b.getAttribute('aria-label')||'Video';
    f.allow='accelerometer;autoplay;encrypted-media;gyroscope;picture-in-picture';
    f.setAttribute('allowfullscreen','');
    w.appendChild(f);
    b.parentNode.replaceChild(w,b);
  });
})();
</script>"""
