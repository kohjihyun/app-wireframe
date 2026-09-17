# -*- coding: utf-8 -*-
"""송금+선불 통합 앱 와이어프레임 렌더러 (.dc.html 아트보드 생성)"""
import os, json, re

W = 390

CSS = """
    *{box-sizing:border-box}
    body{margin:0;background:#EFEEE9;font-family:'IBM Plex Sans KR','Apple SD Gothic Neo','Malgun Gothic',sans-serif;color:#1A1A18;-webkit-font-smoothing:antialiased}
    a{color:#2F6BB0;text-decoration:none}a:hover{color:#1F4B80}
    .wf{width:390px;background:#FCFCFA;border:1px solid #C9C9C2;display:flex;flex-direction:column;min-height:100%}
    .tag{display:flex;gap:6px;align-items:baseline;padding:8px 14px;background:#1A1A18;color:#FCFCFA}
    .tag b{font-family:'IBM Plex Mono',monospace;font-size:11px;font-weight:500;letter-spacing:.04em}
    .tag span{font-size:11.5px;font-weight:400;opacity:.78}
    .tag i{margin-left:auto;font-style:normal;font-family:'IBM Plex Mono',monospace;font-size:9.5px;letter-spacing:.08em;border:1px solid rgba(252,252,250,.45);padding:1px 5px}
    .body{padding:0 0 4px;display:flex;flex-direction:column;flex-grow:1}
    .pad{padding:0 18px;display:flex;flex-direction:column}
    .bar{height:52px;display:flex;align-items:center;gap:10px;padding:0 14px;border-bottom:1px solid #E2E1DA}
    .bar h4{margin:0;font-size:15px;font-weight:600;letter-spacing:-.01em}
    .bar .rt{margin-left:auto;display:flex;gap:12px;align-items:center}
    .ico{width:20px;height:20px;flex-shrink:0;display:block}
    .ico.sm{width:16px;height:16px}
    .badge{position:relative;display:flex}
    .badge::after{content:'N';position:absolute;top:-3px;right:-4px;font-size:8px;font-family:'IBM Plex Mono',monospace;background:#2F6BB0;color:#fff;border-radius:8px;padding:0 3px;line-height:11px}
    h2.t{margin:20px 0 6px;font-size:20px;font-weight:600;line-height:1.35;letter-spacing:-.02em}
    p.d{margin:0 0 4px;font-size:13px;line-height:1.55;color:#6E6E68}
    p.cap{margin:6px 0 0;font-size:11px;line-height:1.5;color:#8C8C85}
    .fld{margin-top:14px;display:flex;flex-direction:column;gap:5px}
    .fld label{font-size:11px;font-weight:500;color:#6E6E68;letter-spacing:.01em}
    .fld label em{font-style:normal;color:#2F6BB0;margin-left:2px}
    .ctl{height:48px;border:1px solid #C9C9C2;background:#fff;display:flex;align-items:center;padding:0 12px;font-size:13.5px;color:#1A1A18;gap:8px}
    .ctl.ph{color:#AFAFA7}
    .ctl .rt{margin-left:auto;display:flex;align-items:center;gap:6px;color:#6E6E68;font-size:12px}
    .row2{display:flex;gap:8px;align-items:flex-end}
    .btn{height:52px;display:flex;align-items:center;justify-content:center;font-size:14.5px;font-weight:600;border:1px solid #1A1A18;background:#1A1A18;color:#FCFCFA;letter-spacing:-.01em}
    .btn.sec{background:#fff;color:#1A1A18;border-color:#1A1A18}
    .btn.gho{background:transparent;color:#6E6E68;border-color:#C9C9C2;font-weight:400}
    .btn.acc{background:#2F6BB0;border-color:#2F6BB0;color:#fff}
    .btn.dis{background:#E2E1DA;border-color:#E2E1DA;color:#AFAFA7}
    .btn.sml{height:36px;font-size:12px;font-weight:500;padding:0 12px}
    .btnrow{display:flex;gap:8px;margin-top:12px}
    .btnrow>.btn{flex-grow:1;flex-basis:0}
    .box{border:1px dashed #B9B9B1;background:#F4F3EE;display:flex;align-items:center;justify-content:center;flex-direction:column;gap:4px;color:#9A9A92;font-size:11.5px;text-align:center;padding:8px}
    .box b{font-weight:500;font-size:12px;color:#7E7E76}
    .crd{border:1px solid #D8D7D0;background:#fff;padding:14px;display:flex;flex-direction:column;gap:7px}
    .crd .ch{display:flex;align-items:baseline;gap:8px}
    .crd .ch b{font-size:13px;font-weight:600}
    .crd .ch span{margin-left:auto;font-size:12px;color:#6E6E68;font-family:'IBM Plex Mono',monospace}
    .crd .cl{font-size:12.5px;color:#4A4A45;line-height:1.5;display:flex;gap:8px}
    .crd .cl b{font-weight:500;color:#1A1A18;margin-left:auto;font-family:'IBM Plex Mono',monospace;font-size:12px}
    .lst{display:flex;flex-direction:column;border-top:1px solid #E2E1DA}
    .li{min-height:56px;display:flex;align-items:center;gap:10px;padding:10px 0;border-bottom:1px solid #E2E1DA}
    .li .tx{display:flex;flex-direction:column;gap:3px;min-width:0;flex-grow:1}
    .li .tx b{font-size:13.5px;font-weight:500;letter-spacing:-.01em}
    .li .tx span{font-size:11.5px;color:#8C8C85}
    .li .rv{margin-left:auto;text-align:right;display:flex;flex-direction:column;gap:3px;flex-shrink:0}
    .li .rv b{font-size:13.5px;font-weight:600;font-family:'IBM Plex Mono',monospace}
    .li .rv span{font-size:11px;color:#8C8C85;font-family:'IBM Plex Mono',monospace}
    .li .thm{width:44px;height:28px;border:1px solid #C9C9C2;background:#F4F3EE;flex-shrink:0}
    .tabs{display:flex;border-bottom:1px solid #C9C9C2}
    .tabs .tb{flex-grow:1;flex-basis:0;height:44px;display:flex;align-items:center;justify-content:center;font-size:13px;color:#8C8C85;border-bottom:2px solid transparent;margin-bottom:-1px}
    .tabs .tb.on{color:#1A1A18;font-weight:600;border-bottom-color:#1A1A18}
    .chips{display:flex;flex-wrap:wrap;gap:6px;margin-top:12px}
    .chip{border:1px solid #C9C9C2;padding:8px 12px;font-size:12px;color:#4A4A45;background:#fff}
    .chip.on{border-color:#1A1A18;background:#1A1A18;color:#FCFCFA;font-weight:500}
    .chk{display:flex;align-items:center;gap:10px;min-height:44px;font-size:13px;border-bottom:1px solid #EDECE5}
    .chk .bx{width:20px;height:20px;border:1.5px solid #8C8C85;flex-shrink:0;display:flex;align-items:center;justify-content:center}
    .chk .bx.on{border-color:#1A1A18;background:#1A1A18}
    .chk em{font-style:normal;font-size:11px;color:#2F6BB0;font-weight:500}
    .chk .rt{margin-left:auto;color:#AFAFA7}
    .rdo{display:flex;align-items:center;gap:10px;min-height:46px;font-size:13.5px}
    .rdo .dot{width:18px;height:18px;border-radius:50%;border:1.5px solid #8C8C85;flex-shrink:0}
    .rdo .dot.on{border:5px solid #1A1A18}
    .tg{display:flex;align-items:center;min-height:52px;font-size:13.5px;border-bottom:1px solid #EDECE5;gap:10px}
    .tg .sw{margin-left:auto;width:40px;height:22px;border-radius:11px;background:#D8D7D0;position:relative;flex-shrink:0}
    .tg .sw.on{background:#1A1A18}
    .tg .sw::after{content:'';position:absolute;top:2px;left:2px;width:18px;height:18px;border-radius:50%;background:#fff}
    .tg .sw.on::after{left:20px}
    .tg .sb{font-size:11px;color:#8C8C85;display:block;margin-top:2px}
    .kp{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:1px;background:#E2E1DA;border-top:1px solid #E2E1DA;margin-top:14px}
    .kp div{height:56px;background:#F7F6F2;display:flex;align-items:center;justify-content:center;font-size:19px;font-family:'IBM Plex Mono',monospace}
    .ptn{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:26px;padding:26px 44px;justify-items:center}
    .ptn i{width:22px;height:22px;border-radius:50%;border:1.5px solid #B9B9B1;display:block}
    .ptn i.on{border-color:#2F6BB0;background:#2F6BB0}
    .ptn i.err{border-color:#B0402F;background:#B0402F}
    .pin{display:flex;gap:14px;justify-content:center;padding:22px 0}
    .pin i{width:14px;height:14px;border-radius:50%;border:1.5px solid #B9B9B1;display:block}
    .pin i.on{background:#1A1A18;border-color:#1A1A18}
    .amt{border:1px solid #D8D7D0;background:#fff;padding:16px;display:flex;flex-direction:column;gap:6px}
    .amt span{font-size:11px;color:#6E6E68}
    .amt b{font-size:26px;font-weight:600;font-family:'IBM Plex Mono',monospace;letter-spacing:-.02em;display:flex;align-items:baseline;gap:6px}
    .amt b em{font-style:normal;font-size:14px;font-weight:400;color:#6E6E68}
    .kv{display:flex;flex-direction:column;gap:2px}
    .kvr{display:flex;align-items:baseline;gap:12px;min-height:34px;font-size:12.5px;border-bottom:1px solid #EDECE5;padding:5px 0}
    .kvr span{color:#8C8C85;flex-shrink:0;min-width:84px}
    .kvr b{margin-left:auto;text-align:right;font-weight:500;font-family:'IBM Plex Mono',monospace;font-size:12px;word-break:break-all}
    .div{height:1px;background:#E2E1DA;margin:16px 0}
    .divx{height:8px;background:#EFEEE9;margin:18px 0;border-top:1px solid #E2E1DA;border-bottom:1px solid #E2E1DA}
    .bnr{border:1px solid #C9C9C2;background:#F4F3EE;padding:12px 14px;display:flex;gap:10px;align-items:flex-start;font-size:12px;line-height:1.55;color:#4A4A45}
    .bnr.warn{border-color:#C9A24A;background:#FAF5E8}
    .bnr.err{border-color:#C08477;background:#FAF0ED}
    .nav{margin-top:auto;display:grid;grid-template-columns:repeat(5,minmax(0,1fr));border-top:1px solid #C9C9C2;background:#fff}
    .nav div{height:60px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:4px;font-size:10px;letter-spacing:-.03em;color:#9A9A92;white-space:nowrap}
    .nav div.on{color:#1A1A18;font-weight:600}
    .ovl{margin:14px 18px;border:1px solid #1A1A18;background:#fff;box-shadow:6px 6px 0 rgba(26,26,24,.10)}
    .ovl .oh{padding:16px 16px 0;font-size:14px;font-weight:600}
    .ovl .ob{padding:10px 16px 16px;font-size:12.5px;line-height:1.6;color:#4A4A45;white-space:pre-line}
    .ovl .of{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));border-top:1px solid #E2E1DA}
    .ovl .of.one{grid-template-columns:1fr}
    .ovl .of div{height:48px;display:flex;align-items:center;justify-content:center;font-size:13.5px;font-weight:500;border-left:1px solid #E2E1DA}
    .ovl .of div:first-child{border-left:0}
    .ovl .of div.mut{color:#8C8C85;font-weight:400}
    .sheet{margin-top:14px;border-top:2px solid #1A1A18;background:#fff;padding:16px 18px;display:flex;flex-direction:column}
    .sheet>h5{margin:0 0 4px;font-size:14px;font-weight:600}
    .note{margin-top:auto;border-top:1px solid #C9C9C2;background:#F4F3EE;padding:12px 16px 14px;display:flex;flex-direction:column;gap:6px}
    .note h6{margin:0 0 2px;font-family:'IBM Plex Mono',monospace;font-size:9.5px;font-weight:500;letter-spacing:.1em;color:#8C8C85}
    .note p{margin:0;font-size:11px;line-height:1.55;color:#4A4A45;display:flex;gap:6px}
    .note p b{font-family:'IBM Plex Mono',monospace;font-size:9.5px;font-weight:500;color:#2F6BB0;flex-shrink:0;padding-top:1px;letter-spacing:.04em}
    .note p b.x{color:#B0402F}
    .mapwrap{padding:36px 40px;background:#FCFCFA;width:1180px}
    .mapwrap h1{margin:0 0 6px;font-size:34px;font-weight:600;letter-spacing:-.03em}
    .mapwrap .sub{margin:0 0 26px;font-size:13.5px;color:#6E6E68;line-height:1.6}
    .mapgrid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:18px}
    .mapcol{border-top:2px solid #1A1A18;padding-top:10px;display:flex;flex-direction:column;gap:5px}
    .mapcol h3{margin:0 0 4px;font-size:13px;font-weight:600;letter-spacing:-.01em}
    .mapcol .mi{display:flex;gap:7px;font-size:11px;line-height:1.5;color:#4A4A45}
    .mapcol .mi b{font-family:'IBM Plex Mono',monospace;font-size:9.5px;font-weight:500;color:#8C8C85;flex-shrink:0;padding-top:1px;min-width:38px}
    .mapcol .mi b.n{color:#2F6BB0}
    .lg{display:flex;gap:26px;margin-top:30px;padding-top:16px;border-top:1px solid #E2E1DA;font-size:11.5px;color:#6E6E68;flex-wrap:wrap}
    .lg span{display:flex;gap:6px;align-items:center}
    .lg i{font-style:normal;font-family:'IBM Plex Mono',monospace;font-size:9.5px;border:1px solid #C9C9C2;padding:1px 5px}
"""

I = {
 "back":'<svg class="ico" viewBox="0 0 24 24" fill="none" stroke="#1A1A18" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M15 5l-7 7 7 7"/></svg>',
 "close":'<svg class="ico" viewBox="0 0 24 24" fill="none" stroke="#1A1A18" stroke-width="1.6" stroke-linecap="round"><path d="M6 6l12 12M18 6L6 18"/></svg>',
 "bell":'<svg class="ico" viewBox="0 0 24 24" fill="none" stroke="#1A1A18" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M18 8a6 6 0 10-12 0c0 6-2 7-2 7h16s-2-1-2-7"/><path d="M10.5 20a2 2 0 003 0"/></svg>',
 "cs":'<svg class="ico" viewBox="0 0 24 24" fill="none" stroke="#1A1A18" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M4 14v-2a8 8 0 0116 0v2"/><rect x="2.5" y="13" width="4" height="6" rx="1"/><rect x="17.5" y="13" width="4" height="6" rx="1"/></svg>',
 "chev":'<svg class="ico sm" viewBox="0 0 24 24" fill="none" stroke="#9A9A92" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M9 5l7 7-7 7"/></svg>',
 "down":'<svg class="ico sm" viewBox="0 0 24 24" fill="none" stroke="#6E6E68" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M5 9l7 7 7-7"/></svg>',
 "left":'<svg class="ico sm" viewBox="0 0 24 24" fill="none" stroke="#6E6E68" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M15 5l-7 7 7 7"/></svg>',
 "right":'<svg class="ico sm" viewBox="0 0 24 24" fill="none" stroke="#6E6E68" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M9 5l7 7-7 7"/></svg>',
 "search":'<svg class="ico sm" viewBox="0 0 24 24" fill="none" stroke="#6E6E68" stroke-width="1.7" stroke-linecap="round"><circle cx="11" cy="11" r="6.5"/><path d="M16 16l4.5 4.5"/></svg>',
 "filter":'<svg class="ico" viewBox="0 0 24 24" fill="none" stroke="#1A1A18" stroke-width="1.6" stroke-linecap="round"><path d="M4 7h16M7 12h10M10 17h4"/></svg>',
 "refresh":'<svg class="ico sm" viewBox="0 0 24 24" fill="none" stroke="#6E6E68" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M20 11a8 8 0 10-2 6"/><path d="M20 5v6h-6"/></svg>',
 "plus":'<svg class="ico" viewBox="0 0 24 24" fill="none" stroke="#1A1A18" stroke-width="1.7" stroke-linecap="round"><path d="M12 5v14M5 12h14"/></svg>',
 "chk":'<svg class="ico sm" viewBox="0 0 24 24" fill="none" stroke="#FCFCFA" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12.5l5 5L19 7"/></svg>',
 "lock":'<svg class="ico sm" viewBox="0 0 24 24" fill="none" stroke="#6E6E68" stroke-width="1.6" stroke-linecap="round"><rect x="5" y="10.5" width="14" height="9.5" rx="1.5"/><path d="M8 10.5V7.5a4 4 0 018 0v3"/></svg>',
 "cam":'<svg class="ico" viewBox="0 0 24 24" fill="none" stroke="#9A9A92" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M3 8.5h3.5L8 6h8l1.5 2.5H21v11H3z"/><circle cx="12" cy="13.5" r="3.5"/></svg>',
 "home":'<svg class="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M4 11l8-6.5 8 6.5"/><path d="M6.5 10v9h11v-9"/></svg>',
 "list":'<svg class="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h10"/></svg>',
 "send":'<svg class="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M20.5 3.5L10.5 13.5"/><path d="M20.5 3.5l-6.6 17-3.4-7.5-7.5-3.4z"/></svg>',
 "qr":'<svg class="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"><rect x="4" y="4" width="6" height="6"/><rect x="14" y="4" width="6" height="6"/><rect x="4" y="14" width="6" height="6"/><path d="M14 14h3v3h-3zM19 19h1M19 14h1M14 19h1"/></svg>',
 "user":'<svg class="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><circle cx="12" cy="9" r="3.6"/><path d="M5 20c1.2-3.6 4-5.2 7-5.2s5.8 1.6 7 5.2"/></svg>',
 "share":'<svg class="ico sm" viewBox="0 0 24 24" fill="none" stroke="#1A1A18" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M12 4v11M8 7.5L12 4l4 3.5"/><path d="M5 13v6h14v-6"/></svg>',
 "copy":'<svg class="ico sm" viewBox="0 0 24 24" fill="none" stroke="#1A1A18" stroke-width="1.6" stroke-linejoin="round"><rect x="8" y="8" width="11" height="11"/><path d="M5 15V5h10"/></svg>',
 "warn":'<svg class="ico" viewBox="0 0 24 24" fill="none" stroke="#B0402F" stroke-width="1.6" stroke-linecap="round"><path d="M12 4l9 16H3z"/><path d="M12 10v4.5M12 17.2v.1"/></svg>',
 "ok":'<svg viewBox="0 0 48 48" width="52" height="52" fill="none" stroke="#1A1A18" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><circle cx="24" cy="24" r="20"/><path d="M15 24.5l6.5 6.5L33 18"/></svg>',
 "fail":'<svg viewBox="0 0 48 48" width="52" height="52" fill="none" stroke="#B0402F" stroke-width="1.6" stroke-linecap="round"><circle cx="24" cy="24" r="20"/><path d="M17 17l14 14M31 17L17 31"/></svg>',
 "gift":'<svg viewBox="0 0 64 64" width="88" height="88" fill="none" stroke="#9A9A92" stroke-width="1.5" stroke-linejoin="round"><rect x="10" y="26" width="44" height="28"/><rect x="7" y="18" width="50" height="8"/><path d="M32 18v36"/><path d="M32 18c-6-10-16-8-16-2 0 3 3 4 6 4h10zM32 18c6-10 16-8 16-2 0 3-3 4-6 4H32z"/></svg>',
}

def esc(s):
    return str(s).replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')

# ---------- block renderers ----------
def r_bar(a):
    title = a.get('t','')
    left = I['back'] if a.get('back',True) else (I['close'] if a.get('close') else '<span style="width:20px"></span>')
    rt = ''
    ic = a.get('ic',[])
    if ic:
        parts=[]
        for k in ic:
            if k=='bell': parts.append('<span class="badge">'+I['bell']+'</span>')
            else: parts.append(I.get(k,''))
        rt = '<div class="rt">'+''.join(parts)+'</div>'
    return '<div class="bar">'+left+'<h4>'+esc(title)+'</h4>'+rt+'</div>', 53

def r_h(a):
    t = a['t']
    return '<div class="pad"><h2 class="t">'+esc(t).replace('\n','<br>')+'</h2></div>', 30+28*(len(t)//20+t.count('\n'))+6

def r_p(a):
    t=a['t']
    return '<div class="pad"><p class="d">'+esc(t).replace('\n','<br>')+'</p></div>', 22*(len(t)//26+1)+8

def r_cap(a):
    t=a['t']
    return '<div class="pad"><p class="cap">'+esc(t).replace('\n','<br>')+'</p></div>', 19*(len(t)//30+1)+8

def r_fld(a):
    req = ' <em>*</em>' if a.get('req') else ''
    ph = ' ph' if a.get('ph') else ''
    rt = '<span class="rt">'+I.get(a['rt'],'')+'</span>' if a.get('rt') else ''
    lb = '<label>'+esc(a['l'])+req+'</label>' if a.get('l') else ''
    return '<div class="pad"><div class="fld">'+lb+'<div class="ctl'+ph+'">'+esc(a.get('v',''))+rt+'</div></div></div>', (62 if a.get('l') else 48)+14

def r_fld2(a):
    # two controls side by side
    out='<div class="pad"><div class="fld"><label>'+esc(a.get('l',''))+('<em>*</em>' if a.get('req') else '')+'</label><div class="row2">'
    for c in a['c']:
        g = c.get('g',1)
        out+='<div class="ctl'+(' ph' if c.get('ph') else '')+'" style="flex-grow:'+str(g)+';flex-basis:0">'+esc(c.get('v',''))+('<span class="rt">'+I.get(c['rt'],'')+'</span>' if c.get('rt') else '')+'</div>'
    out+='</div></div></div>'
    return out, 76

def r_btn(a):
    cls = {'p':'','s':' sec','g':' gho','a':' acc','d':' dis'}[a.get('k','p')]
    mt = a.get('mt',16)
    return '<div class="pad" style="padding-top:'+str(mt)+'px"><div class="btn'+cls+'">'+esc(a['l'])+'</div></div>', 52+mt

def r_btns(a):
    out='<div class="pad"><div class="btnrow">'
    for l,k in a['b']:
        cls = {'p':'','s':' sec','g':' gho','a':' acc','d':' dis'}[k]
        out+='<div class="btn'+cls+'">'+esc(l)+'</div>'
    out+='</div></div>'
    return out, 64

def r_box(a):
    h=a.get('h',110)
    sub = '<span>'+esc(a['s'])+'</span>' if a.get('s') else ''
    ic = I.get(a['i'],'') if a.get('i') else ''
    mt = a.get('mt',14)
    return '<div class="pad" style="padding-top:'+str(mt)+'px"><div class="box" style="height:'+str(h)+'px">'+ic+'<b>'+esc(a['l'])+'</b>'+sub+'</div></div>', h+mt+2

def r_crd(a):
    head = ''
    if a.get('t'):
        head = '<div class="ch"><b>'+esc(a['t'])+'</b>'+('<span>'+esc(a['r'])+'</span>' if a.get('r') else '')+'</div>'
    lines=''
    for ln in a.get('l',[]):
        if isinstance(ln,tuple): lines+='<div class="cl">'+esc(ln[0])+'<b>'+esc(ln[1])+'</b></div>'
        else: lines+='<div class="cl">'+esc(ln)+'</div>'
    mt=a.get('mt',14)
    return '<div class="pad" style="padding-top:'+str(mt)+'px"><div class="crd">'+head+lines+'</div></div>', 40+(20 if a.get('t') else 0)+21*len(a.get('l',[]))+mt

def r_lst(a):
    out='<div class="pad"><div class="lst">'
    for it in a['i']:
        thm = '<div class="thm"></div>' if it.get('th') else ''
        sub = '<span>'+esc(it['s'])+'</span>' if it.get('s') else ''
        rv=''
        if it.get('r') or it.get('rs'):
            rv='<div class="rv">'+('<b>'+esc(it.get('r',''))+'</b>' if it.get('r') else '')+('<span>'+esc(it['rs'])+'</span>' if it.get('rs') else '')+'</div>'
        ch = I['chev'] if it.get('ch') else ''
        out+='<div class="li">'+thm+'<div class="tx"><b>'+esc(it['t'])+'</b>'+sub+'</div>'+rv+ch+'</div>'
    out+='</div></div>'
    return out, 12+60*len(a['i'])

def r_tabs(a):
    out='<div class="tabs">'
    for idx,t in enumerate(a['i']):
        out+='<div class="tb'+(' on' if idx==a.get('on',0) else '')+'">'+esc(t)+'</div>'
    out+='</div>'
    return out, 45

def r_chips(a):
    out='<div class="pad"><div class="chips">'
    for idx,t in enumerate(a['i']):
        out+='<div class="chip'+(' on' if idx in a.get('on',[]) else '')+'">'+esc(t)+'</div>'
    out+='</div></div>'
    return out, 46*(len(a['i'])//4+1)+8

def r_chk(a):
    out='<div class="pad">'
    for it in a['i']:
        on=' on' if it.get('on') else ''
        req='<em>'+esc(it['m'])+'</em>' if it.get('m') else ''
        rt='<span class="rt">'+I['chev']+'</span>' if it.get('ch') else ''
        out+='<div class="chk"><div class="bx'+on+'">'+(I['chk'] if it.get('on') else '')+'</div>'+esc(it['t'])+' '+req+rt+'</div>'
    out+='</div>'
    return out, 45*len(a['i'])+6

def r_rdo(a):
    out='<div class="pad">'
    for idx,t in enumerate(a['i']):
        out+='<div class="rdo"><div class="dot'+(' on' if idx==a.get('on',-1) else '')+'"></div>'+esc(t)+'</div>'
    out+='</div>'
    return out, 47*len(a['i'])+6

def r_tg(a):
    out='<div class="pad">'
    for it in a['i']:
        sb='<span class="sb">'+esc(it['s'])+'</span>' if it.get('s') else ''
        out+='<div class="tg"><div><div>'+esc(it['t'])+'</div>'+sb+'</div><div class="sw'+(' on' if it.get('on') else '')+'"></div></div>'
    out+='</div>'
    return out, 54*len(a['i'])+6

def r_kp(a):
    keys=['1','2','3','4','5','6','7','8','9','00','0','←']
    return '<div class="pad"><div class="kp">'+''.join('<div>'+k+'</div>' for k in keys)+'</div></div>', 244

def r_ptn(a):
    st=a.get('s',[0]*9)
    return '<div class="ptn">'+''.join('<i class="'+({0:'',1:'on',2:'err'}[v])+'"></i>' for v in st)+'</div>', 236

def r_pin(a):
    n=a.get('n',6); f=a.get('f',0)
    return '<div class="pin">'+''.join('<i class="'+('on' if i<f else '')+'"></i>' for i in range(n))+'</div>', 60

def r_amt(a):
    return ('<div class="pad" style="padding-top:'+str(a.get('mt',14))+'px"><div class="amt"><span>'+esc(a['l'])+'</span><b>'+esc(a['v'])+('<em>'+esc(a['u'])+'</em>' if a.get('u') else '')+'</b></div></div>'), 92+a.get('mt',14)

def r_kv(a):
    out='<div class="pad" style="padding-top:'+str(a.get('mt',14))+'px"><div class="kv">'
    for k,v in a['i']:
        out+='<div class="kvr"><span>'+esc(k)+'</span><b>'+esc(v)+'</b></div>'
    out+='</div></div>'
    return out, 36*len(a['i'])+a.get('mt',14)

def r_div(a): return '<div class="pad"><div class="div"></div></div>', 33
def r_divx(a): return '<div class="divx"></div>', 44
def r_sp(a): return '<div style="height:'+str(a['h'])+'px"></div>', a['h']

def r_bnr(a):
    k=a.get('k','')
    ic = I['warn'] if k=='err' else ''
    return '<div class="pad" style="padding-top:'+str(a.get('mt',14))+'px"><div class="bnr '+k+'">'+ic+'<div>'+esc(a['t']).replace('\n','<br>')+'</div></div></div>', 24*(len(a['t'])//28+1)+26+a.get('mt',14)

def r_nav(a):
    items=[('home','홈'),('send','해외송금'),('qr','QR결제'),('list','거래내역'),('user','MY')]
    out='<div class="nav">'
    for idx,(k,l) in enumerate(items):
        on=' on' if idx==a.get('on',-1) else ''
        out+='<div class="'+on.strip()+'" style="color:'+('#1A1A18' if idx==a.get('on',-1) else '#9A9A92')+'">'+I[k]+'<span>'+l+'</span></div>'
    out+='</div>'
    return out, 61

def r_ovl(a):
    btns=a.get('b',[('확인','')])
    cls=' one' if len(btns)==1 else ''
    bf=''.join('<div class="'+('mut' if k=='m' else '')+'">'+esc(l)+'</div>' for l,k in btns)
    return ('<div class="ovl"><div class="oh">'+esc(a['t'])+'</div><div class="ob">'+esc(a.get('d','')).replace('\n','\n')+'</div><div class="of'+cls+'">'+bf+'</div></div>'), 90+22*(len(a.get('d',''))//26+1)+20

def r_sheet(a):
    inner=''
    h=60
    for b in a['i']:
        s,bh = RENDER[b[0]](b[1]); inner+=s; h+=bh
    return '<div class="sheet"><h5>'+esc(a['t'])+'</h5>'+inner+'</div>', h+10

RENDER={'bar':r_bar,'h':r_h,'p':r_p,'cap':r_cap,'fld':r_fld,'fld2':r_fld2,'btn':r_btn,'btns':r_btns,
 'box':r_box,'crd':r_crd,'lst':r_lst,'tabs':r_tabs,'chips':r_chips,'chk':r_chk,'rdo':r_rdo,'tg':r_tg,
 'kp':r_kp,'ptn':r_ptn,'pin':r_pin,'amt':r_amt,'kv':r_kv,'div':r_div,'divx':r_divx,'sp':r_sp,
 'bnr':r_bnr,'nav':r_nav,'ovl':r_ovl,'sheet':r_sheet}

HEAD = """<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans+KR:wght@300;400;500;600&display=swap">
  <style>%s</style>
</helmet>
"""
FOOT = "</x-dc>\n</body>\n</html>\n"

def build_screen(sc):
    body=''; h=0
    for b in sc['b']:
        s,bh = RENDER[b[0]](b[1]); body+=s; h+=bh
    notes=''
    if sc.get('n'):
        notes='<div class="note"><h6>ACTION / EXCEPTION</h6>'
        for tag,txt in sc['n']:
            cx=' class="x"' if tag in ('예외','오류') else ''
            notes+='<p><b'+cx+'>'+esc(tag)+'</b>'+esc(txt)+'</p>'
        notes+='</div>'
        h += 34+24*sum(len(t)//30+1 for _,t in sc['n'])
    src = sc.get('src','추가')
    tagbar='<div class="tag"><b>'+esc(sc['id'])+'</b><span>'+esc(sc['name'])+'</span><i>'+esc(src)+'</i></div>'
    html = HEAD % CSS + '<div class="wf">'+tagbar+'<div class="body">'+body+'</div>'+notes+'</div>\n'+FOOT
    return html, max(720, int(h)+56)
