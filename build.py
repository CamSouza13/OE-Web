# -*- coding: utf-8 -*-
"""Orbital Ecology, static site generator.

Enterprise deep tech. Deep blue-black base, instrument-blue signal colour,
amber for risk, one accent hue per product. Real logo assets. Telemetry grid.

Content ground truth: terralaboratories.com, carried in content.py.
"""
import os, html
from content import *

OUT = os.path.dirname(os.path.abspath(__file__))

# one accent hue per product, used on the card hairline, chip and product hero
ACCENT = {
 "current":"#4FC3F7", "canopy":"#FFB84D", "aquifer":"#5B8DEF", "reclaim":"#9B87F5",
 "culture":"#F2789E", "orbis":"#A9B7FF", "field":"#FF9F45", "nexus":"#9FB0C9",
}

CSS = """
:root{
 --bg:#09090C; --bg2:#0C0D11; --p1:#0E0F14; --p2:#14161B; --p3:#1A1D23;
 --ln:#212429; --ln2:#31353D;
 --w:#FFFFFF; --t0:#EDEEF2; --t1:#C2C5CD; --t2:#868A95; --t3:#5C5F68;
 --sig:#4FC3F7; --vio:#9B8CF2; --warn:#FF9F45; --acc:#FFFFFF;
 --sans:"Helvetica Neue",Helvetica,Arial,system-ui,sans-serif;
 --mono:ui-monospace,"SF Mono","Courier New",Courier,monospace;
 --max:1240px; --pad:clamp(20px,4vw,52px);
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%;scroll-behavior:smooth;scroll-padding-top:76px}
body{margin:0;background:var(--bg);color:var(--t1);font-family:var(--sans);
 font-size:16.5px;line-height:1.58;-webkit-font-smoothing:antialiased}
img,svg{display:block;max-width:100%}
a{color:inherit}
::selection{background:var(--sig);color:#03121B}
:focus{outline:none}
:focus-visible{outline:2px solid var(--sig);outline-offset:3px;border-radius:2px}
.b:focus-visible,.nv .cta:focus-visible{outline-offset:4px}
.hex:focus-visible,.plate:focus-visible{outline:none}
.hex:focus-visible .g,.plate:focus-visible .g{filter:brightness(1.35) saturate(1.2)}
.skip{position:absolute;left:-9999px;top:0;z-index:200;background:var(--w);color:#0A0A0C;
 padding:12px 18px;font-family:var(--mono);font-size:11px;letter-spacing:.14em;text-transform:uppercase}
.skip:focus{left:0}

/* ---- form ---- */
.form{display:grid;grid-template-columns:1fr 1fr;gap:1px;background:var(--ln);
 border:1px solid var(--ln);margin-top:8px}
.f{background:var(--p1);padding:16px 18px 14px;position:relative}
.f.wide{grid-column:1/-1}
.f label{display:block;font-family:var(--mono);font-size:9px;letter-spacing:.2em;
 text-transform:uppercase;color:var(--t3);margin-bottom:9px}
.f input,.f select,.f textarea{width:100%;background:transparent;border:0;color:var(--t0);
 font-family:var(--sans);font-size:15.5px;padding:0;resize:vertical}
.f textarea{min-height:74px;line-height:1.5}
.f input::placeholder,.f textarea::placeholder{color:var(--t3)}
.f select{color:var(--t0)}
.f select option{background:var(--p2);color:var(--t0)}
.f input:focus,.f select:focus,.f textarea:focus{outline:none}
.f:focus-within{background:var(--p2)}
.f:focus-within:after{content:"";position:absolute;left:0;right:0;bottom:0;height:2px;background:var(--sig)}
.fsend{display:flex;align-items:center;gap:18px;flex-wrap:wrap;margin-top:22px}
.fnote{font-family:var(--mono);font-size:10.5px;letter-spacing:.05em;color:var(--t3);line-height:1.7;
 max-width:46ch}
.fok{margin-top:18px;padding:16px 18px;border:1px solid var(--sig);
 background:rgba(79,195,247,.08);font-size:15px;color:var(--t0);display:none}
.fok.on{display:block}
@media(max-width:700px){.form{grid-template-columns:1fr}}

/* ---- evaluation page ---- */
.steps{display:grid;grid-template-columns:repeat(3,1fr);gap:1px;background:var(--ln);
 border:1px solid var(--ln)}
.steps>div{background:var(--p1);padding:30px 26px 32px;position:relative}
.steps>div:before{content:"";position:absolute;left:0;top:0;width:100%;height:2px;
 background:linear-gradient(90deg,var(--sig),transparent 72%)}
.steps .n{font-family:var(--mono);font-size:11px;letter-spacing:.2em;color:var(--t3);margin-bottom:18px}
.steps h3{margin-bottom:12px}
.steps p{font-size:14.5px;color:var(--t2);margin:0 0 10px}
.steps .w8{font-family:var(--mono);font-size:10px;letter-spacing:.15em;text-transform:uppercase;
 color:var(--sig);margin-top:16px}
@media(max-width:900px){.steps{grid-template-columns:1fr}}
.w{max-width:var(--max);margin:0 auto;padding:0 var(--pad)}
h1,h2,h3,h4{margin:0;color:var(--w);font-weight:700;letter-spacing:-.028em;line-height:1.03}
h1{font-size:clamp(40px,6.8vw,96px);letter-spacing:-.04em}
h2{font-size:clamp(28px,4.1vw,52px);letter-spacing:-.032em}
h3{font-size:clamp(20px,2.2vw,29px);letter-spacing:-.022em;line-height:1.1}
p{margin:0 0 17px}
.kv{font-family:var(--mono);font-size:10px;letter-spacing:.22em;text-transform:uppercase;
 color:var(--t2);margin:0}
.kv .dim{color:var(--t3)}
.ld{font-size:clamp(16.5px,1.7vw,20px);line-height:1.52;color:var(--t2);max-width:60ch}
.sec{padding:clamp(58px,7.5vw,106px) 0;position:relative}
.sec.alt{background:var(--bg2);border-top:1px solid var(--ln);border-bottom:1px solid var(--ln)}
.hd{display:grid;grid-template-columns:214px 1fr;gap:36px;align-items:start;margin-bottom:46px}
.hd .kv{padding-top:9px}

/* telemetry grid texture */
.grid-bg{position:absolute;inset:0;pointer-events:none;opacity:.5;
 background-image:linear-gradient(var(--ln) 1px,transparent 1px),
 linear-gradient(90deg,var(--ln) 1px,transparent 1px);
 background-size:64px 64px;
 -webkit-mask-image:radial-gradient(ellipse 90% 70% at 50% 0%,#000 0%,transparent 72%);
 mask-image:radial-gradient(ellipse 90% 70% at 50% 0%,#000 0%,transparent 72%)}

/* ---- wordmark ---- */
.wm{display:flex;align-items:center;gap:13px;text-decoration:none}
.wm .mk{width:46px;flex:none;opacity:.98}
.wm .wd{width:154px;flex:none;opacity:.96}

/* ---- nav ---- */
.nav{position:sticky;top:0;z-index:90;background:rgba(8,10,15,.86);
 backdrop-filter:saturate(160%) blur(14px);border-bottom:1px solid var(--ln)}
.nv{display:flex;align-items:center;gap:24px;height:76px;max-width:var(--max);margin:0 auto;padding:0 var(--pad)}
.nv .lk{display:flex;gap:26px;margin-left:auto;align-items:center}
.nv a.n{font-family:var(--mono);font-size:10px;letter-spacing:.16em;text-transform:uppercase;
 color:var(--t2);text-decoration:none;position:relative;padding:4px 0}
.nv a.n:hover{color:var(--w)}
.nv a.n:after{content:"";position:absolute;left:0;right:100%;bottom:0;height:1px;
 background:var(--w);transition:right .22s}
.nv a.n:hover:after{right:0}
.nv .cta{font-family:var(--mono);font-size:10px;letter-spacing:.16em;text-transform:uppercase;
 color:var(--w);text-decoration:none;padding:11px 17px;font-weight:700;
 border:1px solid var(--ln2);background:transparent}
.nv .cta:hover{background:var(--w);color:#0A0A0C;border-color:var(--w)}

/* ---- hero: the share-card composition ---- */
.hero{position:relative;overflow:hidden;background:#07070A;border-bottom:1px solid var(--ln)}
.hgrid{display:grid;grid-template-columns:minmax(0,0.92fr) minmax(0,1.08fr);
 gap:clamp(30px,4.6vw,72px);align-items:center}
.hgrid>*{min-width:0}
.hcopy .kv{margin-bottom:22px}
.hcopy h1{font-size:clamp(32px,4vw,56px);letter-spacing:-.04em;line-height:1.02;max-width:14ch}
.hproof{margin-top:22px;font-family:var(--mono);font-size:11px;letter-spacing:.2em;
 text-transform:uppercase;color:var(--warn)}
.hproof sup{color:var(--t3)}
.hfig .fh{font-size:clamp(15px,1.5vw,18.5px);font-weight:600;color:var(--t0);letter-spacing:-.018em;
 margin:0 0 16px;max-width:34ch;line-height:1.32}
.hero .thesis{margin-top:26px}
.hero .btns{margin-top:26px}
.hero .bg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;
 object-position:62% 52%;opacity:.9;
 animation:heroIn 2.8s cubic-bezier(.2,.7,.3,1) both, washdrift 90s ease-in-out infinite alternate}
@keyframes heroIn{from{opacity:0;transform:scale(1.06)}to{opacity:.9;transform:scale(1.01)}}
@keyframes washdrift{from{transform:scale(1.01) translate3d(0,0,0)}
 to{transform:scale(1.09) translate3d(-2%,-1.5%,0)}}
/* keep the copy column on near-black, let the wash breathe on the right */
.hero .veil{position:absolute;inset:0;pointer-events:none;z-index:1;background:
 linear-gradient(96deg,rgba(7,7,10,.93) 0%,rgba(7,7,10,.7) 28%,rgba(7,7,10,.22) 60%,rgba(7,7,10,.42) 100%),
 radial-gradient(80% 92% at 46% 50%,transparent 34%,rgba(7,7,10,.58) 100%),
 linear-gradient(180deg,rgba(7,7,10,.55),rgba(7,7,10,0) 30%,rgba(9,9,12,.9))}
.hero:after{content:"";position:absolute;inset:0;pointer-events:none;z-index:2;background:
 radial-gradient(50% 56% at 90% 10%,rgba(155,140,242,.15),transparent 64%),
 radial-gradient(42% 48% at 4% 98%,rgba(255,138,43,.10),transparent 68%)}
.hero .in{position:relative;z-index:2;padding:clamp(56px,7vw,104px) var(--pad) clamp(52px,6.5vw,92px)}
.hero h1{max-width:15ch}
.hero .tag{margin-top:22px;font-size:clamp(15.5px,1.45vw,17.5px);color:var(--t2);max-width:42ch;line-height:1.5}
.hero .tag b{color:var(--t0);font-weight:600}
.thesis{margin-top:34px;padding:18px 0 0 18px;border-left:2px solid var(--ln2);max-width:54ch;
 font-family:var(--mono);font-size:12px;letter-spacing:.05em;line-height:1.8;color:var(--t1);
 border-top:0}
.thesis b{color:var(--t3);font-weight:400;letter-spacing:.18em;text-transform:uppercase;
 font-size:9.5px;display:block;margin-bottom:8px}

/* status strip */
.strip{border-top:1px solid var(--ln);border-bottom:1px solid var(--ln);background:var(--bg2)}
.strip .r{display:flex;gap:0;max-width:var(--max);margin:0 auto;padding:0 var(--pad);flex-wrap:wrap}
.strip .c{flex:1 1 0;min-width:190px;padding:20px 24px 20px 0}
.strip b{display:block;font-family:var(--mono);font-size:9px;letter-spacing:.2em;
 text-transform:uppercase;color:var(--t3);font-weight:400;margin-bottom:7px}
.strip span{font-size:14.5px;color:var(--t0)}
.strip span em{font-style:normal;color:var(--sig)}

/* ---- buttons ---- */
.btns{display:flex;gap:12px;flex-wrap:wrap;margin-top:32px}
.b{font-family:var(--mono);font-size:11px;letter-spacing:.16em;text-transform:uppercase;
 text-decoration:none;padding:15px 24px;font-weight:700;transition:.18s}
.b1{background:var(--w);color:#0A0A0C}.b1:hover{background:var(--t1)}
.b2{border:1px solid var(--ln2);color:var(--t0);font-weight:400}
.b2:hover{border-color:var(--w);color:var(--w)}

/* ---- figure ---- */
.figwrap{border:1px solid var(--ln2);background:linear-gradient(180deg,#0B0C11,#08090D);
 padding:8px;box-shadow:0 30px 70px -30px rgba(0,0,0,.9),0 0 0 1px rgba(255,255,255,.02)}
.figwrap .fig{width:100%;height:auto}
.figcap{display:flex;justify-content:space-between;gap:8px 20px;flex-wrap:wrap;margin-top:12px;
 font-family:var(--mono);font-size:10.5px;letter-spacing:.13em;text-transform:uppercase;color:var(--t3)}
.figcap .k{color:var(--t2)}
.legend{display:flex;gap:8px 20px;flex-wrap:wrap;margin-top:14px;font-family:var(--mono);
 font-size:10.5px;letter-spacing:.12em;text-transform:uppercase;color:var(--t2)}
.legend i{display:inline-block;width:16px;height:2px;margin-right:8px;vertical-align:middle}

/* ---- stats ---- */
.stats{display:grid;grid-template-columns:repeat(3,1fr);gap:0}
.stat{padding:30px 30px 0 0;border-top:1px solid var(--ln2);position:relative}
.stat:before{content:"";position:absolute;left:0;top:-1px;width:44px;height:2px;background:var(--warn)}
.stat .v{font-size:clamp(38px,5.8vw,74px);line-height:.94;letter-spacing:-.05em;font-weight:700;
 color:var(--w)}
.stat .t{margin-top:18px;font-size:15px;line-height:1.45;color:var(--t2);max-width:27ch}
.stat .s{margin-top:13px;font-family:var(--mono);font-size:9.5px;letter-spacing:.15em;
 text-transform:uppercase;color:var(--t3)}

/* ---- method ---- */
.mth{display:grid;grid-template-columns:repeat(3,1fr);gap:1px;background:var(--ln)}
.mth>div{background:var(--p1);padding:32px 30px 34px;position:relative}
.mth>div:before{content:"";position:absolute;left:0;top:0;width:100%;height:2px;
 background:linear-gradient(90deg,var(--w),transparent 72%)}
.mth .n{font-family:var(--mono);font-size:11px;letter-spacing:.2em;color:var(--t3);margin-bottom:20px}
.mth h3{margin-bottom:14px}
.mth p{font-size:14.5px;color:var(--t2);margin:0}

/* ---- product grid ---- */
.grid{display:grid;grid-template-columns:repeat(2,1fr);gap:18px}
.card{background:var(--p1);border:1px solid var(--ln);display:flex;flex-direction:column;
 text-decoration:none;transition:border-color .2s,background .2s,transform .2s;position:relative}
.card:before{content:"";position:absolute;left:0;top:0;width:100%;height:2px;background:var(--acc);
 opacity:.85;z-index:3}
.card:hover{border-color:var(--ln2);background:var(--p2);transform:translateY(-2px)}
.card .ph{position:relative;height:180px;overflow:hidden;background:#04060A}
.card .ph img{width:100%;height:100%;object-fit:cover;opacity:1;
 transition:opacity .45s cubic-bezier(.2,.7,.3,1),transform .7s cubic-bezier(.2,.7,.3,1)}
.card:hover .ph img{transform:scale(1.055)}
.card .ph:after{content:"";position:absolute;inset:0;z-index:2;
 background:linear-gradient(180deg,rgba(9,9,12,.14) 0%,transparent 46%,rgba(14,15,20,.92))}
.card .bar{display:flex;align-items:baseline;justify-content:space-between;gap:14px;
 padding:18px 24px 16px;background:var(--p3);border-bottom:1px solid var(--ln)}
.card .bar h3{font-weight:700;letter-spacing:.02em;font-size:26px}
.card .bar .mk{font-family:var(--mono);font-size:9.5px;letter-spacing:.15em;text-transform:uppercase;
 color:var(--t2);text-align:right;flex:none;max-width:15ch;line-height:1.5}
.card .bd{padding:22px 24px 24px;display:flex;flex-direction:column;flex:1}
.card .bd p{font-size:14.5px;color:var(--t2);margin:0 0 16px}
.card .tags{display:flex;justify-content:space-between;gap:12px;font-family:var(--mono);font-size:10px;
 letter-spacing:.13em;text-transform:uppercase;color:var(--t3);margin-top:auto;padding-top:14px;
 border-top:1px solid var(--ln)}
.card .tags .go{color:var(--acc)}
.chip{display:inline-block;font-family:var(--mono);font-size:9px;letter-spacing:.15em;
 text-transform:uppercase;border:1px solid var(--ln2);color:var(--t2);padding:5px 9px}
.chip.on{border-color:var(--acc);color:var(--acc);background:color-mix(in srgb,var(--acc) 9%,transparent)}

/* ---- trajectory ---- */
.vis{position:relative;overflow:hidden;background:#050508;
 padding:clamp(84px,11vw,168px) 0;border-top:1px solid var(--ln);border-bottom:1px solid var(--ln)}
.vis .bg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;
 object-position:64% 42%;opacity:.62;
 animation:vdrift 40s ease-in-out infinite alternate}
@keyframes vdrift{from{transform:scale(1.06) translate3d(0,0,0)}to{transform:scale(1.16) translate3d(-2%,1.5%,0)}}
.vis:after{content:"";position:absolute;inset:0;background:
 radial-gradient(64% 74% at 24% 42%,rgba(155,140,242,.15),transparent 66%),
 linear-gradient(180deg,rgba(5,5,8,.88),rgba(5,5,8,.48) 40%,rgba(5,5,8,.99) 96%),
 linear-gradient(90deg,rgba(5,5,8,.9) 4%,rgba(5,5,8,.34) 58%,rgba(5,5,8,.62))}
.vis .w{position:relative;z-index:2}
.vis h2{font-size:clamp(40px,7.4vw,104px);letter-spacing:-.045em;line-height:.96;max-width:12ch}
.vis .ld{margin-top:34px;font-size:clamp(17px,1.9vw,22px);color:var(--t1);max-width:58ch}
.arc{display:grid;grid-template-columns:repeat(3,1fr);gap:1px;background:var(--ln);
 border:1px solid var(--ln);margin-top:clamp(46px,6vw,76px)}
.arc>div{background:rgba(14,15,20,.72);backdrop-filter:blur(6px);padding:28px 26px 30px;position:relative}
.arc>div:before{content:"";position:absolute;left:0;top:0;height:2px;width:0;background:var(--vio);
 transition:width .9s cubic-bezier(.2,.7,.3,1) var(--d,0ms)}
.arc>div.rv:before{width:56px}
.arc .h{font-family:var(--mono);font-size:9.5px;letter-spacing:.2em;text-transform:uppercase;
 color:var(--t3);margin-bottom:16px}
.arc b{display:block;font-size:21px;color:var(--w);letter-spacing:-.022em;margin-bottom:10px;line-height:1.16}
.arc p{margin:0;font-size:14px;color:var(--t2);line-height:1.6}
@media(max-width:820px){.arc{grid-template-columns:1fr}}

/* ---- record ---- */
.log{border-top:1px solid var(--ln2)}
.lr{display:grid;grid-template-columns:106px 76px 290px 1fr;gap:22px;padding:16px 0;
 border-bottom:1px solid var(--ln);align-items:start}
.lr.lh{padding:0 0 11px;border-bottom:1px solid var(--ln2)}
.lr.lh div{font-family:var(--mono);font-size:9px;letter-spacing:.17em;text-transform:uppercase;color:var(--t3)}
.lr .s{font-family:var(--mono);font-size:10px;letter-spacing:.14em;text-transform:uppercase;
 color:var(--t0);padding-top:2px}
.lr .s.o{color:var(--t3)}
.lr .dg{font-family:var(--mono);font-size:12px;color:var(--t1);padding-top:1px}
.lr .mt b{display:block;font-size:14.5px;font-weight:600;color:var(--t0)}
.lr .mt span{display:block;font-size:12.5px;color:var(--t3);margin-top:3px;line-height:1.4}
.lr .t{font-size:14px;color:var(--t2);line-height:1.5}
.lnote{margin-top:22px;font-family:var(--mono);font-size:11px;color:var(--t3);line-height:1.75}

/* ---- benchmarks ---- */
.bm{display:grid;grid-template-columns:repeat(5,1fr);gap:1px;background:var(--ln);border:1px solid var(--ln)}
.bm div{background:var(--p1);padding:26px 22px}
.bm b{display:block;font-size:17px;color:var(--t0);letter-spacing:-.02em;margin-bottom:7px}
.bm span{display:block;font-family:var(--mono);font-size:9px;letter-spacing:.12em;text-transform:uppercase;
 color:var(--t3);margin-bottom:12px;line-height:1.5}
.bm p{font-size:13px;color:var(--t2);margin:0}

/* ---- questions ---- */
.qs{border-top:1px solid var(--ln);max-width:1000px}
.q{border-bottom:1px solid var(--ln)}
.q summary{list-style:none;cursor:pointer;display:grid;grid-template-columns:52px 1fr 26px;
 align-items:start;gap:18px;padding:25px 0}
.q summary::-webkit-details-marker{display:none}
.q .qn{font-family:var(--mono);font-size:11px;letter-spacing:.16em;color:var(--t3);padding-top:5px}
.q .qt{font-size:19px;font-weight:600;color:var(--t0);letter-spacing:-.018em;line-height:1.34}
.q summary:hover .qt{color:var(--w)}
.q .qi{position:relative;width:15px;height:15px;margin-top:6px;justify-self:end}
.q .qi:before,.q .qi:after{content:"";position:absolute;background:var(--t2);transition:transform .18s,opacity .18s}
.q .qi:before{left:0;top:7px;width:15px;height:1px}
.q .qi:after{left:7px;top:0;width:1px;height:15px}
.q[open] .qi:before,.q[open] .qi:after{background:var(--w)}
.q[open] .qi:after{transform:scaleY(0);opacity:0}
.q[open] .qt{color:var(--w)}
.q .qa{padding:0 40px 28px 70px}
.q .qa p{font-size:15px;line-height:1.68;color:var(--t2);margin:0;max-width:82ch}

/* ---- sources ---- */
.srcs{border-top:1px solid var(--ln)}
.sr{display:grid;grid-template-columns:84px 1fr;gap:22px;padding:23px 0;border-bottom:1px solid var(--ln)}
.sr .id{font-family:var(--mono);font-size:12px;letter-spacing:.16em;color:var(--t3)}
.sr h4{margin:0 0 8px;font-size:16px;font-weight:600;letter-spacing:-.012em;color:var(--t0)}
.sr p{margin:0;font-size:14.5px;line-height:1.6;color:var(--t2);max-width:84ch}
.sr .cite{margin-top:9px;font-family:var(--mono);font-size:11px;color:var(--t3);line-height:1.6}
.sr .lnk{display:inline-block;margin-top:10px;font-family:var(--mono);font-size:9.5px;letter-spacing:.15em;
 text-transform:uppercase;color:var(--t2);text-decoration:none;border-bottom:1px solid var(--ln2);padding-bottom:3px}
.sr .lnk:hover{color:var(--w);border-bottom-color:var(--w)}
sup{font-family:var(--mono);font-size:8.5px;color:var(--t3);vertical-align:super;margin-left:2px;font-weight:400}

/* ---- team ---- */
.team{display:grid;grid-template-columns:repeat(3,1fr);gap:0;border-top:1px solid var(--ln2)}
.tm{padding:30px 30px 28px 0;position:relative}
.tm:before{content:"";position:absolute;left:0;top:-1px;width:40px;height:2px;background:var(--w)}
.tm .r{font-family:var(--mono);font-size:9.5px;letter-spacing:.16em;text-transform:uppercase;color:var(--t3)}
.tm h4{font-size:23px;margin:12px 0 9px;letter-spacing:-.02em}
.tm p{font-size:14.5px;color:var(--t2);margin:0 0 12px}
.tm .fo{font-family:var(--mono);font-size:11px;color:var(--t3);line-height:1.65}

/* ---- product page ---- */
.phero{position:relative;overflow:hidden;background:#05070B;border-bottom:1px solid var(--ln)}
.phero .bg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:.62;
 animation:drift 26s ease-in-out infinite alternate}
.phero .tint{position:absolute;inset:0;background:var(--acc);mix-blend-mode:color;opacity:.16;z-index:1}
@keyframes drift{from{transform:scale(1.04) translate3d(0,0,0)}to{transform:scale(1.12) translate3d(-1.5%,-1%,0)}}
.phero:after{content:"";position:absolute;inset:0;background:
 radial-gradient(58% 80% at 82% 18%,color-mix(in srgb,var(--acc) 13%,transparent),transparent 62%),
 linear-gradient(90deg,rgba(5,7,11,.95),rgba(5,7,11,.66) 56%,rgba(5,7,11,.44)),
 linear-gradient(180deg,rgba(5,7,11,.45),rgba(5,7,11,0) 40%,rgba(8,10,15,.96))}
.phero .in{position:relative;z-index:2;padding:clamp(52px,7.5vw,96px) var(--pad) clamp(42px,5.5vw,70px)}
.phero .pn{font-size:clamp(46px,8.4vw,108px);font-weight:700;letter-spacing:.01em;color:var(--w);line-height:.96}
.phero .pm{margin-top:14px;font-family:var(--mono);font-size:11.5px;letter-spacing:.24em;
 text-transform:uppercase;color:var(--acc)}
.phero .pp{margin-top:24px;font-size:clamp(18px,2.2vw,26px);color:var(--t0);font-weight:600;
 letter-spacing:-.02em;max-width:26ch;line-height:1.24}
.phero .bar{position:absolute;left:0;bottom:0;height:3px;width:100%;
 background:linear-gradient(90deg,var(--acc),transparent 55%);z-index:3}
.rows{border-top:1px solid var(--ln2)}
.rw{display:grid;grid-template-columns:220px 1fr;gap:34px;padding:24px 0;border-bottom:1px solid var(--ln)}
.rw b{font-family:var(--mono);font-size:10px;letter-spacing:.17em;text-transform:uppercase;
 color:var(--t3);font-weight:400;padding-top:4px}
.rw p{margin:0;font-size:16px;color:var(--t1);line-height:1.6}
.rw .sm{font-size:14.5px;color:var(--t2)}
.other{display:grid;grid-template-columns:repeat(4,1fr);gap:1px;background:var(--ln);border:1px solid var(--ln)}
.other a{background:var(--p1);padding:20px 20px 22px;text-decoration:none;display:block;
 border-top:2px solid var(--acc);transition:background .18s}
.other a:hover{background:var(--p2)}
.other b{display:block;font-size:19px;color:var(--t0);letter-spacing:.02em;margin-bottom:6px}
.other span{font-family:var(--mono);font-size:9px;letter-spacing:.13em;text-transform:uppercase;color:var(--t3)}
.other .fill{display:block;background:var(--bg)}

/* ---- cta + footer ---- */
.cta{position:relative;overflow:hidden}
.cta.earth{background:#05070B;border-top:1px solid var(--ln);padding:clamp(84px,10vw,150px) 0}
.cta.earth .bg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;
 object-position:62% center;opacity:.55}
.cta.earth .veil{position:absolute;inset:0;pointer-events:none;background:
 linear-gradient(90deg,rgba(5,7,11,.95) 4%,rgba(5,7,11,.7) 46%,rgba(5,7,11,.3)),
 linear-gradient(180deg,rgba(5,7,11,.8),rgba(5,7,11,.15) 36%,rgba(9,9,12,.92));z-index:1}
.cta.earth .w{z-index:2}
.cta:before{content:"";position:absolute;inset:0;
 background:radial-gradient(62% 100% at 14% 50%,rgba(155,140,242,.10),transparent 66%)}
.cta .w{position:relative;z-index:2}
.cta h2{max-width:17ch}
footer{border-top:1px solid var(--ln);padding:50px 0 42px;font-size:13.5px;color:var(--t3);background:var(--bg2)}
.fg{display:grid;grid-template-columns:1.4fr 1fr 1fr 1fr;gap:32px}
.fg h5{margin:0 0 14px;font-family:var(--mono);font-size:9px;letter-spacing:.2em;text-transform:uppercase;
 color:var(--t3);font-weight:400}
footer a{display:block;color:var(--t2);text-decoration:none;margin-bottom:8px}
footer a:hover{color:var(--w)}
.fbot{margin-top:42px;padding-top:22px;border-top:1px solid var(--ln);display:flex;
 justify-content:space-between;gap:24px;flex-wrap:wrap;font-family:var(--mono);font-size:10.5px;
 letter-spacing:.05em;color:var(--t3)}


/* ================= motion ================= */
[data-rv]{opacity:0;transform:translate3d(0,22px,0);
 transition:opacity .8s cubic-bezier(.2,.7,.3,1),transform .8s cubic-bezier(.2,.7,.3,1);
 transition-delay:var(--d,0ms)}
[data-rv].rv{opacity:1;transform:none}
[data-rv="scale"]{transform:translate3d(0,26px,0) scale(.985)}
[data-rv="left"]{transform:translate3d(-18px,0,0)}

/* hero staged entrance */
.hcopy>*{opacity:0;animation:up .95s cubic-bezier(.2,.7,.3,1) both}
.hcopy>*:nth-child(1){animation-delay:.12s}
.hcopy>*:nth-child(2){animation-delay:.24s}
.hcopy>*:nth-child(3){animation-delay:.36s}
.hcopy>*:nth-child(4){animation-delay:.48s}
.hcopy>*:nth-child(5){animation-delay:.60s}
.hcopy>*:nth-child(6){animation-delay:.72s}
.hfig{opacity:0;animation:up 1s cubic-bezier(.2,.7,.3,1) .40s both}
@keyframes up{from{opacity:0;transform:translate3d(0,26px,0)}to{opacity:1;transform:none}}

/* nav condense */
.nav{transition:height .3s,background .3s,border-color .3s}
.nav .nv{transition:height .32s cubic-bezier(.2,.7,.3,1)}
.nav.sm .nv{height:60px}
.nav.sm{background:rgba(8,10,15,.95);border-bottom-color:var(--ln2)}
.wm .mk,.wm .wd{transition:width .32s cubic-bezier(.2,.7,.3,1)}
.nav.sm .wm .mk{width:38px}.nav.sm .wm .wd{width:128px}

/* status strip sweep */
.strip{position:relative;overflow:hidden}
.strip:after{content:"";position:absolute;top:0;left:-40%;width:40%;height:1px;
 background:linear-gradient(90deg,transparent,var(--t1),transparent);
 animation:sweep 9s linear infinite}
@keyframes sweep{to{left:110%}}
.strip .c{position:relative}
.strip .c:before{content:"";position:absolute;left:0;top:22px;width:0;height:1px;background:var(--t2);
 opacity:.6;transition:width .7s cubic-bezier(.2,.7,.3,1) var(--d,0ms)}
.strip.rv .c:before{width:26px}

/* card lift */
.card{will-change:transform}
.card:hover{box-shadow:0 18px 44px -22px color-mix(in srgb,var(--acc) 55%,transparent),
 0 0 0 1px color-mix(in srgb,var(--acc) 26%,transparent)}
.card .tags .go{transition:transform .25s;display:inline-block}
.card:hover .tags .go{transform:translateX(4px)}

/* stat rule grow */
.stat:before{width:0;transition:width .8s cubic-bezier(.2,.7,.3,1) var(--d,0ms)}
.stat.rv:before{width:44px}
.tm:before{width:0;transition:width .8s cubic-bezier(.2,.7,.3,1) var(--d,0ms)}
.tm.rv:before{width:40px}

/* method top bar */
.mth>div:before{transform:scaleX(0);transform-origin:left;
 transition:transform .9s cubic-bezier(.2,.7,.3,1) var(--d,0ms)}
.mth>div.rv:before{transform:scaleX(1)}

/* buttons */
.b1{position:relative;overflow:hidden}
.b1:after{content:"";position:absolute;inset:0;background:linear-gradient(90deg,transparent,rgba(255,255,255,.55),transparent);
 transform:translateX(-120%)}
.b1:hover:after{animation:shine .75s ease}
@keyframes shine{to{transform:translateX(120%)}}
.b{transition:background .2s,color .2s,border-color .2s,transform .2s}
.b:hover{transform:translateY(-1px)}

/* ---- the figure ---- */
.fig .f-grid{stroke:#1B2230;stroke-width:1}
.fig .f-grid2{stroke:#161C28;stroke-width:1}
.fig .f-ax{fill:#5A6474;font-family:var(--mono);font-size:11px}
.fig .f-head{letter-spacing:2;font-size:10.5px}
.fig .f-lab{font-family:var(--mono);font-size:11px;letter-spacing:1.4px}
.fig .f-lab-t{fill:#FF9F45}.fig .f-lab-1{fill:#4FC3F7}.fig .f-lab-2{fill:#FF9F45}
.fig .f-thresh{stroke:#FF9F45;stroke-width:1.2;stroke-dasharray:5 5;opacity:.85}
.fig .f-obs{fill:none;stroke:#6C7789;stroke-width:1.7}
.fig .f-state{fill:none;stroke:#4FC3F7;stroke-width:2.6}
.fig .f-vline{stroke-width:1.2;opacity:.7}
.fig .f-v1{stroke:#4FC3F7}.fig .f-v2{stroke:#FF9F45}
.fig .f-dot{fill:#4FC3F7}
.fig .f-gap{fill:#E8EDF5;font-family:var(--sans);font-size:22px;font-weight:700}

.fig .f-obs,.fig .f-state{stroke-dasharray:var(--Lo);stroke-dashoffset:var(--Lo)}
.fig .f-state{stroke-dasharray:var(--Ls);stroke-dashoffset:var(--Ls)}
.fig .f-band,.fig .f-win,.fig .f-thresh,.fig .f-vline,.fig .f-dot,
.fig .f-lab,.fig .f-gap,.fig .f-ax{opacity:0}
.fig .f-dot{transform-box:fill-box;transform-origin:center;transform:scale(0)}

.figwrap.rv .fig .f-ax{animation:fade .6s ease .1s both}
.figwrap.rv .fig .f-obs{animation:draw 1.5s cubic-bezier(.4,0,.3,1) .25s both}
.figwrap.rv .fig .f-thresh{animation:fade .6s ease .8s both}
.figwrap.rv .fig .f-lab-t{animation:fade .5s ease 1.0s both}
.figwrap.rv .fig .f-band{animation:fade .9s ease 1.15s both}
.figwrap.rv .fig .f-state{animation:draw 1.7s cubic-bezier(.4,0,.3,1) 1.2s both}
.figwrap.rv .fig .f-v1{animation:fade .5s ease 2.35s both}
.figwrap.rv .fig .f-dot{animation:pop .5s cubic-bezier(.2,1.5,.4,1) 2.4s both}
.figwrap.rv .fig .f-lab-1{animation:fade .5s ease 2.5s both}
.figwrap.rv .fig .f-v2{animation:fade .5s ease 2.75s both}
.figwrap.rv .fig .f-lab-2{animation:fade .5s ease 2.85s both}
.figwrap.rv .fig .f-win{animation:fade .8s ease 2.95s both}
.figwrap.rv .fig .f-gap{animation:popfade .7s cubic-bezier(.2,1.3,.4,1) 3.1s both}
@keyframes draw{from{stroke-dashoffset:var(--Ls,1400);opacity:1}to{stroke-dashoffset:0;opacity:1}}
@keyframes fade{from{opacity:0}to{opacity:1}}
@keyframes pop{from{opacity:0;transform:scale(0)}to{opacity:1;transform:scale(1)}}
@keyframes popfade{from{opacity:0;transform:translateY(8px) scale(.9)}to{opacity:1;transform:none}}
.fig .f-obs{--Ls:var(--Lo)}

@media(prefers-reduced-motion:reduce){
 *,*:before,*:after{animation-duration:.001ms!important;animation-delay:0ms!important;
  transition-duration:.001ms!important;transition-delay:0ms!important}
 [data-rv]{opacity:1;transform:none}
 .fig *{opacity:1!important;stroke-dashoffset:0!important;transform:none!important}
 .phero .bg{animation:none}
}

@media(max-width:1040px){.hgrid{grid-template-columns:1fr;gap:34px}
 .hcopy h1{max-width:16ch}
 .nv .lk a.n{display:none}
 .bm,.other{grid-template-columns:1fr 1fr}.other .fill{display:none}
 .mth{grid-template-columns:1fr}.fg{grid-template-columns:1fr 1fr}}
@media(max-width:820px){.grid{grid-template-columns:1fr}}
@media(max-width:760px){
 .other .fill{display:none}
 .hd{grid-template-columns:1fr;gap:12px}
 .stats,.team{grid-template-columns:1fr}
 .stat,.tm{padding-right:0}
 .lr{grid-template-columns:100px 1fr}.lr .dg{grid-column:2}
 .lr .mt,.lr .t{grid-column:1/-1}.lr.lh{display:none}
 .nv{height:64px;gap:12px}
 .nv .cta{font-size:9px;letter-spacing:.12em;padding:10px 12px;white-space:nowrap}
 .wm .mk{width:32px}.wm .wd{width:104px}
 .rw{grid-template-columns:1fr;gap:10px}
 .q .qa{padding-left:0;padding-right:0}
 .bm,.other{grid-template-columns:1fr}
 .fg{grid-template-columns:1fr}
 .hero .bg{object-position:74% center}
 .figwrap{overflow-x:auto;-webkit-overflow-scrolling:touch}
 .figwrap .fig{min-width:660px}
 .hfig .figcap:after{content:'Scroll the figure sideways';display:block;width:100%;
  color:var(--t3);margin-top:2px}
 .btns .b{flex:1 1 auto;text-align:center}
}
"""



HEX_CSS = """
/* ============ orange liquid glass pyramid ============ */
.pyr{position:relative;background:#050508;border-top:1px solid var(--ln);border-bottom:1px solid var(--ln)}
.pyr .rail{height:var(--rail,400vh)}
.pstage{position:sticky;top:0;height:100vh;overflow:hidden;display:flex;align-items:center}
.pstage .bg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:64% 42%;
 opacity:.5;animation:vdrift 46s ease-in-out infinite alternate}
.pstage:after{content:"";position:absolute;inset:0;pointer-events:none;background:
 radial-gradient(52% 62% at 22% 40%,rgba(155,140,242,.13),transparent 66%),
 radial-gradient(48% 56% at 76% 62%,rgba(255,138,43,.10),transparent 68%),
 linear-gradient(180deg,rgba(5,5,8,.9),rgba(5,5,8,.5) 40%,rgba(5,5,8,.97));z-index:1}
.pstage .w{position:relative;z-index:3;width:100%}
.pgrid{display:grid;grid-template-columns:minmax(0,1fr) minmax(320px,540px);
 gap:clamp(28px,5vw,76px);align-items:center}
.pcopy h2{font-size:clamp(30px,4.4vw,58px);letter-spacing:-.045em;line-height:.99;max-width:15ch}
.pcopy .ld{margin-top:20px;color:var(--t1);max-width:46ch;font-size:clamp(14.5px,1.32vw,16.5px);line-height:1.55}

/* ---- the board ---- */
.pyramid{position:relative;width:100%;aspect-ratio:1000/1061;
 --hexw:30%;--hexh:32.65%;--clip:polygon(50% 0,100% 25%,100% 75%,50% 100%,0 75%,0 25%)}
.hex,.slot{position:absolute;width:var(--hexw);height:var(--hexh)}
.plate,.pslot{position:absolute;height:14.4%;top:85.6%}
.slot,.pslot{clip-path:var(--clip);background:
 linear-gradient(180deg,rgba(255,170,90,.05),rgba(255,140,60,.02));
 outline:0;opacity:.55;z-index:1}
.slot:before,.pslot:before{content:"";position:absolute;inset:1px;clip-path:var(--clip);
 background:#050508}
.pslot{clip-path:polygon(4% 0,96% 0,100% 50%,96% 100%,4% 100%,0 50%)}
.pslot:before{clip-path:polygon(4% 0,96% 0,100% 50%,96% 100%,4% 100%,0 50%)}

.hex,.plate{z-index:2;text-decoration:none;display:block;
 transform:translate3d(0,-130vh,0);will-change:transform;opacity:0}
.plate{clip-path:polygon(4% 0,96% 0,100% 50%,96% 100%,4% 100%,0 50%)}

/* photograph, refracted */
.hex .ph,.plate .ph{position:absolute;inset:0;clip-path:var(--clip);overflow:hidden}
.plate .ph{clip-path:polygon(4% 0,96% 0,100% 50%,96% 100%,4% 100%,0 50%)}
.hex .ph img,.plate .ph img{width:100%;height:100%;object-fit:cover;opacity:.42;
 filter:saturate(.12) contrast(1.14) brightness(.92)}

/* the glass itself */
.hex .g,.plate .g{position:absolute;inset:0;clip-path:var(--clip);
 backdrop-filter:blur(13px) saturate(210%) brightness(1.06);
 -webkit-backdrop-filter:blur(13px) saturate(210%) brightness(1.06);
 background:
  radial-gradient(120% 80% at 28% 8%,rgba(255,229,196,.46),rgba(255,182,112,.20) 34%,transparent 62%),
  radial-gradient(90% 70% at 78% 96%,rgba(186,66,10,.62),transparent 60%),
  linear-gradient(168deg,rgba(255,158,66,.50),rgba(255,104,24,.40) 48%,rgba(142,46,6,.52));
 box-shadow:inset 0 1px 0 rgba(255,236,214,.5)}
.plate .g{clip-path:polygon(4% 0,96% 0,100% 50%,96% 100%,4% 100%,0 50%)}

/* the caustic that drifts through the liquid */
.hex .lq,.plate .lq{position:absolute;inset:-30%;clip-path:none;pointer-events:none;
 background:
  radial-gradient(38% 30% at 30% 26%,rgba(255,240,220,.32),transparent 62%),
  radial-gradient(30% 24% at 72% 70%,rgba(255,196,130,.20),transparent 66%);
 filter:blur(10px);animation:caustic 11s ease-in-out infinite alternate;opacity:.9}
@keyframes caustic{
 0%{transform:translate3d(-4%,-3%,0) scale(1)}
 100%{transform:translate3d(5%,4%,0) scale(1.1)}}
.hex .lqw,.plate .lqw{position:absolute;inset:0;clip-path:var(--clip);overflow:hidden;pointer-events:none}
.plate .lqw{clip-path:polygon(4% 0,96% 0,100% 50%,96% 100%,4% 100%,0 50%)}

/* rim light */
.hex .rim,.plate .rim{position:absolute;inset:0;pointer-events:none}
.hex .rim svg,.plate .rim svg{width:100%;height:100%;overflow:visible}
.hex .rim polygon,.plate .rim path{fill:none;stroke:url(#rimg);stroke-width:2.2;
 vector-effect:non-scaling-stroke}
.hex .rim:after,.plate .rim:after{content:"";position:absolute;inset:0;clip-path:var(--clip);
 background:linear-gradient(157deg,rgba(255,244,232,.55),rgba(255,244,232,.10) 16%,transparent 34%);
 mix-blend-mode:screen;opacity:.85}
.plate .rim:after{clip-path:polygon(4% 0,96% 0,100% 50%,96% 100%,4% 100%,0 50%)}
.hex .sp,.plate .sp{position:absolute;left:8%;right:8%;top:2%;height:34%;pointer-events:none;
 background:radial-gradient(60% 100% at 42% 0%,rgba(255,248,238,.62),transparent 72%);
 filter:blur(7px);opacity:.8}

/* content */
.hex .c,.plate .c{position:absolute;left:12%;right:12%;top:50%;transform:translateY(-50%);
 text-align:center;pointer-events:none}
.plate .c{left:5%;right:5%;text-align:left}
.hex .n,.plate .n{display:block;font-size:clamp(13px,1.55vw,22px);font-weight:700;color:#fff;
 letter-spacing:.03em;line-height:1;text-shadow:0 1px 10px rgba(120,40,0,.55)}
.hex .m,.plate .m{display:block;font-family:var(--mono);font-size:clamp(6.5px,.62vw,9px);
 letter-spacing:.15em;text-transform:uppercase;color:rgba(255,231,208,.82);margin-top:7px;
 line-height:1.4}
.hex .r,.plate .r{display:block;margin-top:9px;font-family:var(--mono);font-size:8px;
 letter-spacing:.16em;color:rgba(255,214,178,.62)}
.plate .r{margin-top:6px}

.hex:hover .g,.plate:hover .g{filter:brightness(1.18) saturate(1.1)}
.hex:hover .sp,.plate:hover .sp{opacity:1}
.hex.lit .g,.plate.lit .g{animation:splash .5s cubic-bezier(.2,.7,.3,1)}
@keyframes splash{
 0%{filter:brightness(2.1) saturate(1.5)}
 100%{filter:brightness(1) saturate(1)}}

/* the seal when the pyramid closes */
.pyramid .cap{position:absolute;left:35%;top:0;width:30%;height:32.65%;pointer-events:none;
 clip-path:var(--clip);opacity:0;transition:opacity .7s;
 background:radial-gradient(60% 60% at 50% 40%,rgba(255,236,214,.5),transparent 70%)}
.pyramid.done .cap{opacity:1}
.pyramid .halo{position:absolute;left:8%;right:8%;top:-4%;bottom:-4%;pointer-events:none;opacity:0;
 transition:opacity .8s;background:radial-gradient(52% 46% at 50% 44%,rgba(255,150,60,.20),transparent 70%);
 filter:blur(22px)}
.pyramid.done .halo{opacity:1}

/* rail + hud */
.tiers{display:flex;flex-direction:column;gap:0;margin-top:24px;border-left:1px solid var(--ln2);
 padding-left:18px}
.tiers div{font-family:var(--mono);font-size:9.5px;letter-spacing:.18em;text-transform:uppercase;
 color:var(--t3);padding:5px 0;transition:color .4s}
.tiers div span{color:var(--t3);transition:color .4s}
.tiers div.on{color:var(--t0)}
.tiers div.on span{color:#FF9F45}
.hud{margin-top:20px;display:flex;align-items:center;gap:14px;font-family:var(--mono);font-size:10px;
 letter-spacing:.2em;text-transform:uppercase;color:var(--t3)}
.hud .bar{flex:1;max-width:210px;height:2px;background:var(--ln2);position:relative;overflow:hidden}
.hud .bar i{position:absolute;inset:0;width:0;background:linear-gradient(90deg,#C24A0E,#FFB061);
 transition:width .25s linear}
.hud b{color:var(--t0);font-weight:400}
.tcap{margin-top:16px;font-family:var(--mono);font-size:11px;letter-spacing:.06em;line-height:1.7;
 color:var(--t2);max-width:46ch;opacity:0;transform:translateY(8px);transition:opacity .6s,transform .6s}
.tcap.on{opacity:1;transform:none}
.tcap b{color:var(--t0);font-weight:400}

/* text index under the pyramid, for people and for crawlers */
.plist{margin:0 0 clamp(56px,7vw,104px);display:grid;grid-template-columns:repeat(4,1fr);gap:1px;
 background:var(--ln);border:1px solid var(--ln)}
.plist a{background:rgba(14,15,20,.72);padding:18px 18px 20px;text-decoration:none;display:block;
 border-top:2px solid var(--acc);transition:background .2s}
.plist a:hover{background:var(--p2)}
.plist b{display:block;font-size:17px;color:var(--t0);letter-spacing:.02em;margin-bottom:5px}
.plist span{display:block;font-family:var(--mono);font-size:8.5px;letter-spacing:.13em;
 text-transform:uppercase;color:var(--t3);line-height:1.5}

@media(max-width:1080px){
 .pgrid{grid-template-columns:1fr;gap:30px}
 .pstage{height:auto;position:relative;padding:clamp(54px,9vw,92px) 0}
 .pyr .rail{height:auto}
 .pyramid{max-width:560px;margin:0 auto}
 .plist{grid-template-columns:1fr 1fr}
}
@media(max-width:620px){.plist{grid-template-columns:1fr}}
@media(prefers-reduced-motion:reduce){
 .hex,.plate{transform:none!important;opacity:1!important}
 .pstage .bg,.hex .lq,.plate .lq{animation:none}
}
"""




HEX_JS = """
<script>
(function(){
 var pyr=document.querySelector(".pyr"); if(!pyr) return;
 var board=pyr.querySelector(".pyramid"),
     els=[].slice.call(pyr.querySelectorAll(".hex,.plate")),
     tiers=[].slice.call(pyr.querySelectorAll(".tiers div")),
     bar=pyr.querySelector(".hud .bar i"),
     num=pyr.querySelector(".hud b"),
     cap=pyr.querySelector(".tcap"),
     N=els.length;
 var reduce=window.matchMedia("(prefers-reduced-motion:reduce)").matches;
 var small=window.matchMedia("(max-width:1080px)");

 // rigid bodies. Plates are the plinth: heavy, they barely bounce.
 var B=els.map(function(el,i){
   var heavy=el.classList.contains("plate");
   return { el:el, i:i, heavy:heavy, e:heavy?0.16:0.31,
            y:0, vy:0, rot:0, vrot:0, squash:0, live:0, done:0, hit:0 };
 });
 var G=5400, REST=54;
 var shake=0, shakeV=0;

 function reset(){
   want=0; nextAt=0; shake=0; shakeV=0; board.style.transform="none";
   B.forEach(function(b){ b.y=0;b.vy=0;b.rot=0;b.vrot=0;b.squash=0;b.live=0;b.done=0;b.hit=0;
     b.el.style.transform="translate3d(0,-130vh,0)"; b.el.style.opacity="0"; });
   tiers.forEach(function(t){t.classList.remove("on")});
   board.classList.remove("done"); if(cap) cap.classList.remove("on");
   if(bar) bar.style.width="0%"; if(num) num.textContent="0/"+N;
 }
 function land(){
   B.forEach(function(b){ b.done=1;b.live=0;b.y=0;b.vy=0;b.rot=0;b.squash=0;b.hit=1;
     b.el.style.transform="none"; b.el.style.opacity="1"; });
   tiers.forEach(function(t){t.classList.add("on")});
   board.classList.add("done"); if(cap) cap.classList.add("on");
   if(bar) bar.style.width="100%"; if(num) num.textContent=N+"/"+N;
 }
 if(reduce){ land(); return; }

 function drop(b){
   if(b.live||b.done) return;
   var h=board.getBoundingClientRect().height||600;
   b.y=-(h*1.15+120+b.i*10);
   b.vy=0;
   b.rot=(b.i%2?1:-1)*(b.heavy?0.6:2.0);
   b.vrot=0; b.live=1;
   b.el.style.opacity="1";
 }
 function impact(b,v){
   b.squash=Math.min(1,v/1500);
   shakeV=Math.max(-26,shakeV-Math.min(1,v/1900)*(b.heavy?10:5));
   if(!b.hit){ b.hit=1; b.el.classList.add("lit");
     setTimeout(function(){ b.el.classList.remove("lit"); },500); }
 }

 var want=0, nextAt=0, lastT=0, raf=0;
 function step(now){
   raf=0;
   var dt=lastT?Math.min(0.034,(now-lastT)/1000):0.016; lastT=now;
   var moving=false, settled=0;

   for(var r=0;r<N;r++){
     if(r<want && !B[r].live && !B[r].done){
       if(now<nextAt){ moving=true; break; }
       drop(B[r]); nextAt=now+185; break;
     }
   }
   if(want<N) moving=true;

   for(var k=0;k<N;k++){
     var b=B[k];
     if(b.done) settled++;
     if(!b.live){
       if(!b.done) b.el.style.transform="translate3d(0,-130vh,0)";
       else if(b.squash>0.001){
         b.squash*=Math.pow(0.0016,dt); var s0=b.squash;
         b.el.style.transform="translate3d(0,0,0) scale("+(1+s0*0.08)+","+(1-s0*0.17)+")";
         moving=true;
       } else b.el.style.transform="none";
       continue;
     }
     moving=true;
     b.vy+=G*dt; b.y+=b.vy*dt;
     b.vrot+=(0-b.rot)*34*dt; b.vrot*=Math.pow(0.12,dt); b.rot+=b.vrot*dt;
     if(b.y>=0){
       b.y=0;
       var vin=b.vy, vout=vin*b.e;
       impact(b,vin);
       // a discrete integrator adds G*dt of speed each frame: the sleep test
       // has to clear that or the body micro-bounces forever
       if(vout<Math.max(REST,G*dt*2.2)){ b.vy=0; b.rot=0; b.live=0; b.done=1; settled++; }
       else { b.vy=-vout; b.rot*=0.4; }
     }
     var sq=b.squash; if(sq>0){ b.squash*=Math.pow(0.0016,dt); }
     b.el.style.transform="translate3d(0,"+b.y.toFixed(2)+"px,0) rotate("+b.rot.toFixed(3)+"deg)"
       + (sq>0.001 ? " scale("+(1+sq*0.08)+","+(1-sq*0.17)+")" : "");
   }

   if(shakeV||Math.abs(shake)>0.05){
     shakeV+=(0-shake)*260*dt; shakeV*=Math.pow(0.02,dt); shake+=shakeV*dt;
     if(Math.abs(shake)<0.05&&Math.abs(shakeV)<1){shake=0;shakeV=0;}
     board.style.transform="translate3d(0,"+shake.toFixed(2)+"px,0)";
     moving=true;
   }

   if(bar) bar.style.width=(settled/N*100)+"%";
   if(num) num.textContent=settled+"/"+N;
   tiers.forEach(function(el){ el.classList.toggle("on", settled>=+el.dataset.at); });
   board.classList.toggle("done", settled===N);
   if(cap) cap.classList.toggle("on", settled===N);

   if(moving) raf=requestAnimationFrame(step); else lastT=0;
 }
 function tick(){ if(!raf){ lastT=0; raf=requestAnimationFrame(step); } }

 if(small.matches){
   if(!("IntersectionObserver" in window)){ land(); return; }
   reset();
   var mo=new IntersectionObserver(function(es){
     es.forEach(function(e){ if(e.isIntersecting){ mo.disconnect(); want=N; tick(); } });
   },{threshold:.16});
   mo.observe(board);
   return;
 }

 reset();
 function onScroll(){
   var r=pyr.getBoundingClientRect(), vh=innerHeight;
   // Once a tile has landed it stays landed. Scrolling back up reveals the
   // finished pyramid, it does not rewind and rebuild it.
   if(r.bottom<-40||r.top>vh+40) return;
   var total=pyr.offsetHeight-vh;
   var p=total>0?Math.min(1,Math.max(0,(-r.top)/total)):0;
   var q=Math.min(1,p/0.68);
   var n=0; for(var k=0;k<N;k++){ if(q>=(k+0.20)/N) n=k+1; }
   if(n>want) want=n;
   tick();
 }
 addEventListener("scroll",onScroll,{passive:true});
 addEventListener("resize",onScroll);
 onScroll();
})();

</script>"""



JS = """
<script>
(function(){
 var rm=window.matchMedia("(prefers-reduced-motion:reduce)").matches;
 var nav=document.querySelector(".nav");
 if(nav){var last=0;addEventListener("scroll",function(){
   var y=scrollY; if((y>40)!==(last>40)) nav.classList.toggle("sm",y>40); last=y;
 },{passive:true});}
 var SEL="[data-rv],.figwrap,.strip,.stat,.tm,.mth>div,.arc>div,.card,.bm>div,.sr,.lr,.q,.rw,.other a";
 if(rm||!("IntersectionObserver" in window)){
   document.querySelectorAll(SEL).forEach(function(e){e.classList.add("rv")});
   return;
 }
 function stagger(sel,step){
   document.querySelectorAll(sel).forEach(function(g){
     [].forEach.call(g.children,function(c,i){c.style.setProperty("--d",(i*step)+"ms")});
   });
 }
 stagger(".stats",90); stagger(".mth",110); stagger(".grid",70);
 stagger(".arc",130); stagger(".team",110); stagger(".bm",70); stagger(".strip .r",90);
 var io=new IntersectionObserver(function(es){
   es.forEach(function(e){
     if(!e.isIntersecting) return;
     io.unobserve(e.target);
     // the hero figure waits for the copy column to finish arriving
     var d=e.target.hasAttribute("data-hero")?620:0;
     if(d) setTimeout(function(){e.target.classList.add("rv")},d);
     else e.target.classList.add("rv");
   });
 },{rootMargin:"0px 0px -12% 0px",threshold:.12});
 document.querySelectorAll(SEL).forEach(function(e){io.observe(e)});
})();

// ---- hero video: never autoplay on a phone or under data saver ----
(function(){
 var vs=document.querySelectorAll("video.bg[data-src]"); if(!vs.length) return;
 var c=navigator.connection||{};
 if(c.saveData) return;
 if(innerWidth<820) return;
 if(window.matchMedia("(prefers-reduced-motion:reduce)").matches) return;
 var io=new IntersectionObserver(function(es){
   es.forEach(function(e){
     if(!e.isIntersecting) return;
     io.unobserve(e.target);
     var v=e.target, s=document.createElement("source");
     s.src = innerWidth>=1500 ? v.dataset.src : v.dataset.light; s.type="video/mp4";
     v.appendChild(s); v.load();
     var p=v.play(); if(p&&p.catch) p.catch(function(){});
   });
 },{rootMargin:"300px"});
 [].forEach.call(vs,function(v){io.observe(v)});
})();

// ---- evaluation form ----
(function(){
 var f=document.querySelector("form.evalform"); if(!f) return;
 var ok=f.querySelector(".fok"), btn=f.querySelector("button[type=submit]");
 function val(n){ var e=f.elements[n]; return e?e.value.trim():""; }
 function show(msg){ ok.textContent=msg; ok.classList.add("on"); }
 f.addEventListener("submit",function(ev){
   if(!val("name")||!val("email")){
     ev.preventDefault(); show("Name and work email are needed so we can send the report back."); return;
   }
   if(f.getAttribute("action")){
     // Formspree is configured: post it in the background and stay on the page
     ev.preventDefault();
     btn.disabled=true; btn.textContent="Sending";
     fetch(f.action,{method:"POST",body:new FormData(f),headers:{Accept:"application/json"}})
       .then(function(r){
         if(!r.ok) throw 0;
         f.querySelector(".form").style.display="none";
         f.querySelector(".fsend").style.display="none";
         show("Thank you. We will reply within one working day with an NDA and the file spec.");
       })
       .catch(function(){
         btn.disabled=false; btn.textContent="Request the evaluation";
         show("That did not send. Email "+f.dataset.mail+" and we will pick it up there.");
       });
     return;
   }
   // nothing configured: compose the message instead, so the form still works
   ev.preventDefault();
   var NL=String.fromCharCode(10);
   var body=["Name: "+val("name"),"Email: "+val("email"),"Company: "+val("company"),
             "System: "+val("system"),"","Data available:",val("data"),"",
             "Sent from "+f.dataset.source].join(NL);
   location.href="mailto:"+f.dataset.mail+"?subject="+
     encodeURIComponent("Evaluation request")+"&body="+encodeURIComponent(body);
   show("Your mail client should open with this filled in. If it does not, email "+f.dataset.mail+".");
 });
})();
</script>"""

def wordmark(href="index.html"):
    return (f'<a class="wm" href="{href}" aria-label="{BRAND}">'
            f'<img class="mk" src="assets/mark.png" alt="">'
            f'<img class="wd" src="assets/wordmark.png" alt="{BRAND}"></a>')

def nav():
    links = [("index.html#products","Products"),("index.html#method","Method"),
             ("index.html#record","Validation"),("evaluation.html","Evaluation"),
             (MEDIUM,"Notes"),("company.html","Company")]
    ls = "".join(
        f'<a class="n" href="{h}"{" target=_blank rel=noopener" if h.startswith("http") else ""}>{t}</a>'
        for h,t in links)
    return (f'<a class="skip" href="#main">Skip to content</a>'
            f'<header class="nav"><div class="nv">{wordmark()}<nav class="lk" aria-label="Primary">{ls}'
            f'<a class="cta" href="evaluation.html">Request an evaluation</a></nav></div></header>')

def footer():
    prods = "".join(f'<a href="{s}.html">{n}</a>' for s,n,*_ in PRODUCTS[:6])
    return f'''<footer><div class="w"><div class="fg">
<div>{wordmark()}<p style="margin-top:18px;max-width:34ch;color:var(--t2);font-size:14px">
{html.escape(THESIS)}</p></div>
<div><h5>Products</h5>{prods}</div>
<div><h5>Company</h5><a href="company.html">Team</a><a href="index.html#record">Validation record</a>
<a href="index.html#sources">Sources</a><a href="index.html#questions">Questions</a>
<a href="{MEDIUM}" target="_blank" rel="noopener">Technical notes</a></div>
<div><h5>Contact</h5><a href="evaluation.html">Request an evaluation</a>
<a href="{CAL}">Book a call</a><a href="mailto:{MAIL}">{MAIL}</a>
<a href="nexus.html">NEXUS platform</a></div>
</div>
<div class="fbot"><span>&copy; 2026 {BRAND}. {ADDRESS}.</span>
<span>Simulation-validated and backtested. No production deployment.</span></div>
</div></footer>'''

def page(title, desc, body, accent=None, extra_css='', extra_js=''):
    root = f'<style>:root{{--acc:{accent}}}</style>' if accent else ''
    return f'''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<meta name="theme-color" content="#080A0F">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:image" content="https://{DOMAIN}/assets/share-card.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:site_name" content="{BRAND}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="https://{DOMAIN}/assets/share-card.jpg">
<meta property="og:type" content="website">
<link rel="icon" href="assets/icon-512.png">
<link rel="apple-touch-icon" href="assets/icon-512.png">
<style>{CSS}{extra_css}</style>{root}</head><body><main id="main">{body}</main>{JS}{extra_js}</body></html>'''

def chip(status):
    on = status in ("Validated","Backtested","Core")
    return f'<span class="chip{" on" if on else ""}">{html.escape(status)}</span>'

FIG = open(os.path.join(OUT,"assets","figure-forecast.svg")).read()

# Landing order is top to bottom in this list: the floor lands first and the
# capstone last. Visual position is set by (row, col), row 5 being the floor,
# so the stack builds upward toward closed-loop life support.
# ---------------------------------------------------------- hex pyramid
# Six closed-system markets stack into the triangle: three "now" on the base,
# two "next" above, closed-loop life support at the apex. NEXUS is the plinth
# because it is the platform, not a market. FIELD sits on the plinth too, since
# an open environment is the one thing that is not a closed loop.
#
# Geometry is pointy-top honeycomb, computed once: hex width 30% of the board,
# 2.5% gaps, rows stepping 0.75 x hex height. See README.
PYRAMID = [
 # slug,      x%,    top%,   kind,    tier label
 ("nexus",    2.5,  87.75, "plate", "Foundation"),
 ("field",   62.5,  87.75, "plate", "Foundation"),
 ("current",  2.5,  52.74, "hex",   "Now"),
 ("canopy",  35.0,  52.74, "hex",   "Now"),
 ("aquifer", 67.5,  52.74, "hex",   "Now"),
 ("reclaim", 18.75, 26.37, "hex",   "Next"),
 ("culture", 51.25, 26.37, "hex",   "Next"),
 ("orbis",   35.0,   0.00, "hex",   "Then"),
]
PLATE_W = {"nexus": 58.0, "field": 35.0}
PTIERS = [("Foundation","Shared engine and open ground",2),
          ("Now","Terrestrial production",5),
          ("Next","Environmental recovery",7),
          ("Then","Closed-loop life support",8)]

RIMDEF = ('<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>'
          '<linearGradient id="rimg" x1="0" y1="0" x2="1" y2="1">'
          '<stop offset="0" stop-color="#FFEBD6" stop-opacity=".95"/>'
          '<stop offset=".38" stop-color="#FFB061" stop-opacity=".55"/>'
          '<stop offset=".72" stop-color="#C24A0E" stop-opacity=".35"/>'
          '<stop offset="1" stop-color="#FFD9AE" stop-opacity=".6"/>'
          '</linearGradient></defs></svg>')

HEX_POLY = '<svg viewBox="0 0 100 115.47" preserveAspectRatio="none"><polygon points="50,0 100,28.87 100,86.6 50,115.47 0,86.6 0,28.87"/></svg>'
PLATE_POLY = '<svg viewBox="0 0 100 30" preserveAspectRatio="none"><path d="M4 0 H96 L100 15 L96 30 H4 L0 15 Z"/></svg>'

def pyramid_section():
    slots, tiles = "", ""
    for slug, x, top, kind, tier in PYRAMID:
        pr = PROD[slug]
        if kind == "plate":
            w = PLATE_W[slug]
            slots += '<span class="pslot" style="left:%.2f%%;width:%.1f%%"></span>' % (x, w)
            geo = 'left:%.2f%%;width:%.1f%%' % (x, w)
            poly = PLATE_POLY
        else:
            slots += '<span class="slot" style="left:%.2f%%;top:%.2f%%"></span>' % (x, top)
            geo = 'left:%.2f%%;top:%.2f%%' % (x, top)
            poly = HEX_POLY
        tiles += ('<a class="%s" href="%s.html" style="%s" data-tier="%s">'
                  '<span class="ph"><img src="assets/img/raw/%s.webp" alt="" decoding="async"></span>'
                  '<span class="g"></span>'
                  '<span class="lqw"><span class="lq"></span><span class="sp"></span></span>'
                  '<span class="rim">%s</span>'
                  '<span class="c"><span class="n">%s</span>'
                  '<span class="m">%s</span><span class="r">%s</span></span></a>'
                  % (kind, slug, geo, tier, pr[3], poly, pr[1],
                     html.escape(pr[2]), html.escape(pr[9])))
    tiers = "".join('<div data-at="%d"><span>&#9670;</span>&nbsp; %s &nbsp;/&nbsp; %s</div>'
                    % (at, html.escape(a), html.escape(b)) for a, b, at in PTIERS)
    plist = "".join(
        '<a href="%s.html" style="--acc:%s"><b>%s</b><span>%s &middot; %s</span></a>'
        % (p[0], ACCENT[p[0]], p[1], html.escape(p[2]), html.escape(p[9]))
        for p in PRODUCTS)
    return PSTAGE % (RIMDEF, tiers, slots, tiles, plist)


PSTAGE = """<section class="pyr" id="products">
%s
<div class="rail">
<div class="pstage">
<img class="bg" src="assets/img/raw/vision.webp" alt="">
<div class="w"><div class="pgrid">
<div class="pcopy">
<p class="kv">03 <span class="dim">&nbsp; Products and trajectory</span></p>
<h2 style="margin-top:22px">From the mud<br>to the moon.</h2>
<p class="ld">One engine, laid down in layers. NEXUS carries the estimator and every market
above it pays for the next one. The capstone is a loop with no resupply and no exit, reachable
only because everything under it was proven first. An aquaculture operator still buys an
aquaculture product, not a space product.</p>
<div class="tiers">%s</div>
<div class="hud"><span>Stack</span><span class="bar"><i></i></span><b>0/8</b></div>
<p class="tcap"><b>Closed.</b> Every layer below the capstone is a market today. That is the
whole plan: get paid to learn the thing that has to work when there is no resupply.</p>
</div>
<div class="pyramid">%s%s<span class="cap"></span><span class="halo"></span></div>
</div></div>
</div></div>
<div class="w"><div class="plist">%s</div></div>
</section>"""


# ------------------------------------------------------------------ index
CLASSIC_SECTIONS = """<section class="sec alt" id="products">
<div class="w">
<div class="hd" data-rv><p class="kv">04 <span class="dim">&nbsp; Products</span></p>
<div><h2>One engine.<br>Seven front doors.</h2>
<p class="ld" style="margin-top:26px">An aquaculture operator should be able to buy an aquaculture
product, not a space product. Each vertical carries its own name and its own commercial identity.
NEXUS is the shared control stack underneath all of them.</p></div></div>
<div class="grid">{cards}</div>
</div></section>

{VIS}


<section class="vis">
<img class="bg" src="assets/img/raw/vision.webp" alt="">
<div class="w">
<p class="kv" data-rv>05 <span class="dim">&nbsp; Where this goes</span></p>
<h2 data-rv style="margin-top:26px">From the mud<br>to the moon.</h2>
<p class="ld" data-rv>The estimator that keeps a biofilter alive on a fish farm is the estimator
that keeps an atmosphere alive in a sealed habitat. One of those is a business this decade. The other
is the reason the business exists. Every loop we learn to read makes the next closed system more
survivable, and the hardest version of the problem has no resupply, no exit and no second chance.</p>
<div class="arc">
<div><div class="h">Now</div><b>Terrestrial production</b>
<p>Recirculating farms, glasshouses and nutrient loops. Closed systems with material value at risk
every night, and the shortest path from a measured result to a signed contract.</p></div>
<div><div class="h">Next</div><b>Environmental recovery</b>
<p>Biological treatment, water reuse and remediation. The same estimator pointed at processes a
regulator already measures, where the cost of running blind is energy and compliance rather than stock.</p></div>
<div><div class="h">Then</div><b>Off-world life support</b>
<p>Bioregenerative loops for habitats. Physicochemical hardware recycles and scrubs. It does not grow
food and it does not close the loop. The biological half has to be trusted before it can fly.</p></div>
</div>
</div></section>"""


def build_index(hexes=True):
    PYR = pyramid_section() if hexes else CLASSIC_SECTIONS
    stats = "".join(
        f'<div class="stat"><div class="v">{v}</div><div class="t">{html.escape(t)}</div>'
        f'<div class="s">{html.escape(s)}<sup>{ref}</sup></div></div>'
        for v,t,s,ref in STATS)

    method = "".join(
        f'<div><div class="n">{n}</div><h3>{html.escape(t)}</h3><p>{html.escape(d)}</p></div>'
        for n,t,d in METHOD)

    cards = ""
    for slug,name,market,img,status,promise,est,ev,fields,bench in PRODUCTS:
        cards += f'''<a class="card" href="{slug}.html" style="--acc:{ACCENT[slug]}">
<div class="ph"><img src="assets/img/raw/{img}.webp" alt="" decoding="async"></div>
<div class="bar"><h3>{name}</h3><div class="mk">{html.escape(market)}</div></div>
<div class="bd"><p>{html.escape(promise)}</p>
<div style="margin-bottom:14px">{chip(status)}</div>
<div class="tags"><span>{html.escape(bench)}</span><span class="go">View &rarr;</span></div></div></a>'''

    rows = ('<div class="lr lh"><div>Status</div><div>Ref</div><div>Benchmark</div><div>Result</div></div>'
        + "".join(
        f'<div class="lr"><div class="s{"" if st=="Complete" else " o"}">{html.escape(st)}</div>'
        f'<div class="dg">{html.escape(ref)}</div>'
        f'<div class="mt"><b>{html.escape(b)}</b><span>{html.escape(d)}</span></div>'
        f'<div class="t">{html.escape(r)}</div></div>' for st,ref,b,d,r in RECORD))

    bm = "".join(f'<div><b>{html.escape(a)}</b><span>{html.escape(b)}</span><p>{html.escape(c)}</p></div>'
                 for a,b,c in BENCH)

    qs = "".join(
        f'<details class="q"><summary><span class="qn">{i+1:02d}</span>'
        f'<span class="qt">{html.escape(q)}</span><span class="qi"></span></summary>'
        f'<div class="qa"><p>{html.escape(a)}</p></div></details>'
        for i,(q,a) in enumerate(QUESTIONS))

    srcs = "".join(
        f'<div class="sr"><div class="id">{sid}</div><div><h4>{html.escape(t)}</h4>'
        f'<p>{html.escape(d)}</p><div class="cite">{html.escape(c)}</div>'
        + (f'<a class="lnk" href="{u}" rel="noopener">Source</a>' if u else '')
        + '</div></div>' for sid,t,d,c,u in SOURCES)

    body = f'''{nav()}
<section class="hero">
<img class="bg" src="assets/img/hero-wash.webp" alt="" aria-hidden="true">
<span class="veil"></span>
<div class="w in"><div class="hgrid">
<div class="hcopy">
<p class="kv">Orbital Ecology <span class="dim">&nbsp;/&nbsp; Building worlds that live</span></p>
<h1>Living systems fail in silence.</h1>
<p class="tag">Every gauge on a closed system measures a consequence. We estimate the state that
produced it, and simulate that state forward.</p>
<p class="hproof">6.5 h of lead &middot; benchmark OE/01<sup>S8</sup></p>
<div class="btns"><a class="b b1" href="evaluation.html">Request a free evaluation</a>
<a class="b b2" href="#products">See the products</a></div>
<div class="thesis"><b>Corporate thesis</b>{html.escape(THESIS)}</div>
</div>
<div class="hfig">
<p class="fh">The state moves smoothly. The gauge moves all at once.</p>
<div class="figwrap" data-hero>{FIG}</div>
<div class="legend">
<span><i style="background:#4FC3F7"></i>Estimated hidden state</span>
<span><i style="background:#6C7789"></i>Observable instrument</span>
<span><i style="background:#FF9F45"></i>Action threshold</span>
</div>
<div class="figcap"><span class="k">Illustration of the method, not a data plot</span>
<span>A threshold alarm is drawn on the thing that moves last</span></div>
</div>
</div></div></section>

<div class="strip"><div class="r">
<div class="c"><b>Method</b><span>Mechanistic model, <em>Bayesian state estimation</em>, forward simulation</span></div>
<div class="c"><b>Coverage</b><span>Seven verticals on <em>one engine</em></span></div>
<div class="c"><b>Proof</b><span>Four benchmarks, <em>one commercial backtest</em></span></div>
<div class="c"><b>Deployment</b><span>Read-only. <em>No control loop touched</em></span></div>
</div></div>

<section class="sec">
<div class="grid-bg"></div>
<div class="w">
<div class="hd" data-rv><p class="kv">01 <span class="dim">&nbsp; The problem</span></p>
<div><h2>The variable that decides<br>the outcome is unmeasured.</h2>
<p class="ld" style="margin-top:26px">Dissolved oxygen is what the biology left behind. Ammonia is
what the biofilter has not cleared. Slab EC is a receipt. Every instrument in a closed system reports
what the biology already did, so the only safe way to run a process you cannot see is to over-run it.
Operators fund margin they cannot size, and the night shift responds to symptoms.</p></div></div>
<div class="stats">{stats}</div>
</div></section>

<section class="sec" id="method">
<div class="w">
<div class="hd" data-rv><p class="kv">02 <span class="dim">&nbsp; The method</span></p>
<div><h2>Three steps.<br>One of them changes by domain.</h2>
<p class="ld" style="margin-top:26px">Steps two and three are identical whether the system is a
recirculating farm, an activated sludge reactor, a fermenter or a sealed habitat. Only the process
model is rewritten. That is why one engine serves seven markets, and why the work compounds across
every deployment.</p></div></div>
<div class="mth">{method}</div>
<p class="lnote" data-rv>The engine is read-only. It reads existing telemetry, returns a forecast with a
confidence band, and touches no control loop. Autonomous control is the roadmap, not the product.</p>
</div></section>

{PYR}

<section class="sec" id="record">
<div class="w">
<div class="hd" data-rv><p class="kv">04 <span class="dim">&nbsp; Validation record</span></p>
<div><h2>Every figure on this site<br>resolves to a run.</h2>
<p class="ld" style="margin-top:26px">Simulation results are labelled as simulation. The aquaculture
result is a held-out backtest on real commercial operating history. There is no production deployment
and none is implied.</p></div></div>
<div class="log" data-rv>{rows}</div>
<p class="lnote" data-rv>Live process results are published to this same record as operator evaluations
complete. First paid pilots are scheduled for the first half of 2027.</p>
</div></section>

<section class="sec alt">
<div class="w">
<div class="hd" data-rv><p class="kv">05 <span class="dim">&nbsp; Benchmarks</span></p>
<div><h2>Validated against the models<br>each field already trusts.</h2></div></div>
<div class="bm">{bm}</div>
</div></section>

<section class="sec" id="questions">
<div class="w">
<div class="hd" data-rv><p class="kv">06 <span class="dim">&nbsp; Questions</span></p>
<div><h2>Asked, and answered straight.</h2></div></div>
<div class="qs" data-rv>{qs}</div>
</div></section>

<section class="sec alt" id="sources">
<div class="w">
<div class="hd" data-rv><p class="kv">07 <span class="dim">&nbsp; Sources</span></p>
<div><h2>Where the numbers come from.</h2></div></div>
<div class="srcs" data-rv>{srcs}</div>
</div></section>

<section class="sec cta earth">
<video class="bg" muted loop playsinline preload="none" poster="assets/img/hero.webp"
 data-src="assets/video/hero.mp4" data-light="assets/video/hero-720.mp4"></video>
<span class="veil"></span>
<div class="w">
<p class="kv" data-rv>Start here</p>
<h2 style="margin-top:24px" data-rv>Send one export.<br>Get the answer in three weeks.</h2>
<p class="ld" style="margin-top:26px">You send a historical sensor export with the outcome window
withheld. We run it blind and report how many hours of warning the engine would have given, and how
often it would have been wrong on that same history. No fee, no integration, no connection to any
live system. The file is deleted afterwards.</p>
<div class="btns" data-rv><a class="b b1" href="evaluation.html">Request an evaluation</a>
<a class="b b2" href="{CAL}">Book a call</a></div>
</div></section>
{footer()}'''
    open(os.path.join(OUT,"index.html"),"w").write(
        page(f"{BRAND} — {MARKQ}",
             "State estimation and forecasting for closed living systems. One engine across "
             "aquaculture, controlled agriculture, water, bioprocess and life support.", body,
             extra_css=HEX_CSS if hexes else "", extra_js=HEX_JS if hexes else ""))

# ------------------------------------------------------------ product pages
def build_product(slug):
    s,name,market,img,status,promise,est,ev,fields,bench = PROD[slug]
    rest = [o for o in PRODUCTS if o[0] != slug]
    others = "".join(
        f'<a href="{o[0]}.html" style="--acc:{ACCENT[o[0]]}"><b>{o[1]}</b>'
        f'<span>{html.escape(o[2])}</span></a>' for o in rest)
    others += '<i class="fill"></i>' * ((-len(rest)) % 4)

    rows = f'''<div class="rows" data-rv>
<div class="rw"><b>Market</b><p>{html.escape(market)}</p></div>
<div class="rw"><b>What it estimates</b><p>{html.escape(est)}</p></div>
<div class="rw"><b>Evidence</b><p>{html.escape(ev)}<sup>S8</sup></p></div>
<div class="rw"><b>Status</b><p>{chip(status)}</p></div>
<div class="rw"><b>Benchmark reference</b><p class="sm">{html.escape(bench)}</p></div>
<div class="rw"><b>Fields covered</b><p class="sm">{html.escape(fields)}</p></div>
</div>'''

    body = f'''{nav()}
<section class="phero">
<img class="bg" src="assets/img/{img}.webp" alt="">
<span class="tint"></span>
<div class="bar"></div>
<div class="w in">
<p class="kv"><a href="index.html#products" style="text-decoration:none;color:inherit">Products</a>
<span class="dim">&nbsp;/&nbsp; {html.escape(market)}</span></p>
<div class="pn" style="margin-top:20px">{name}</div>
<div class="pm">{BRAND}</div>
<p class="pp">{html.escape(promise)}</p>
</div></section>

<section class="sec"><div class="grid-bg"></div><div class="w">{rows}
<p class="lnote" data-rv>The engine is read-only. It reads existing telemetry and returns a forecast with a
confidence band. It connects to no control loop and changes no set point.</p>
</div></section>

<section class="sec alt"><div class="w">
<div class="hd" data-rv><p class="kv">The method</p><div><h2>How {name} works.</h2>
<p class="ld" style="margin-top:24px">Steps two and three below are shared with every other Orbital
Ecology product and run on NEXUS. Step one is the {html.escape(market.lower())} process model, and it
is the only part written specifically for this domain.</p></div></div>
<div class="mth">{"".join(f'<div><div class="n">{n}</div><h3>{html.escape(t)}</h3><p>{html.escape(d)}</p></div>' for n,t,d in METHOD)}</div>
</div></section>

<section class="sec"><div class="w">
<div class="hd" data-rv><p class="kv">Elsewhere</p><div><h2>The rest of the portfolio.</h2></div></div>
<div class="other">{others}</div>
</div></section>

<section class="sec alt cta"><div class="w">
<p class="kv" data-rv>Start here</p>
<h2 style="margin-top:24px" data-rv>Send one export.<br>Get the answer in three weeks.</h2>
<p class="ld" style="margin-top:26px">Historical sensor data from one system, with the outcome window
withheld. We return the hours of warning and the false alarm rate, in writing. No fee.</p>
<div class="btns" data-rv><a class="b b1" href="{CAL}">Book a call</a>
<a class="b b2" href="mailto:{MAIL}">{MAIL}</a></div>
</div></section>
{footer()}'''
    open(os.path.join(OUT,f"{slug}.html"),"w").write(
        page(f"{name} — {market} — {BRAND}", promise, body, accent=ACCENT[slug]))

# ------------------------------------------------------------- evaluation
EVAL_STEPS = [
 ("01","You send one export",
  "Twelve to twenty-four months of logged sensor data from a single system. Whatever your "
  "control system or historian exports is fine: CSV, Excel, a database dump. Plus a short note "
  "on what each channel measures and which readings your operators actually trust.",
  "Your effort: about an hour"),
 ("02","We run it blind",
  "You give us the dates of two or three events you would like explained. Dates only. Not what "
  "happened, not how it ended, not what you think caused it. If we know the answer we can find "
  "it, and so could anyone. Withholding the outcome is what makes the result mean something.",
  "Our side: about three weeks"),
 ("03","You get a written report",
  "How many hours ahead the engine would have flagged each event, the false alarm rate across "
  "the quiet stretches, the model structure and assumptions we used, and the cases where it "
  "failed. Yours to keep and circulate internally, whatever it says.",
  "No fee, no obligation"),
]

EVAL_TERMS = [
 ("Cost", "Nothing. There is no fee for an evaluation and no commitment attached to one."),
 ("Access", "None. We never connect to a live system, we never touch a control loop, and we "
            "never change a set point. This is a file, offline, on our machines."),
 ("Confidentiality", "Mutual NDA before anything moves. Your data is never used to train "
                     "anything for anyone else, and it is deleted when the report is delivered."),
 ("If it fails", "You get that in writing too. A negative report is still a report you can use, "
                 "and it costs you an hour to find out."),
 ("What happens next", "If the result earns it, a paid ninety-day pilot on one system with an "
                       "agreed performance floor. If it does not, we say so and you have lost a file."),
]

SYSTEMS_OPTS = ["Recirculating aquaculture (RAS)","Hatchery or nursery","Glasshouse or CEA",
                "Hydroponic nutrient loop","Aquaponics","Biological wastewater treatment",
                "Anaerobic digestion","Fermentation or bioprocess","Closed habitat or life support",
                "Something else"]

def form_block(source):
    """Posts to Formspree when FORM_ID is set. Falls back to a pre-filled email
    so the form still works on a static host with nothing configured."""
    action = f'https://formspree.io/f/{FORM_ID}' if FORM_ID else ''
    opts = "".join(f'<option>{html.escape(o)}</option>' for o in SYSTEMS_OPTS)
    return f'''<form class="evalform" {'action="'+action+'" method="POST"' if action else ''}
 data-mail="{MAIL}" data-source="{html.escape(source)}" novalidate>
<input type="hidden" name="_subject" value="Evaluation request &mdash; {html.escape(source)}">
<input type="hidden" name="source" value="{html.escape(source)}">
<div class="form">
 <div class="f"><label for="fn">Name</label>
  <input id="fn" name="name" required autocomplete="name" placeholder="Your name"></div>
 <div class="f"><label for="fe">Work email</label>
  <input id="fe" name="email" type="email" required autocomplete="email" placeholder="you@company.com"></div>
 <div class="f"><label for="fc">Company or institution</label>
  <input id="fc" name="company" autocomplete="organization" placeholder="Where you work"></div>
 <div class="f"><label for="fs">System</label>
  <select id="fs" name="system">{opts}</select></div>
 <div class="f wide"><label for="fd">What data could you send</label>
  <textarea id="fd" name="data" placeholder="What you log, how often, how far back, and anything you already know is missing. A rough answer is fine."></textarea></div>
</div>
<div class="fsend">
 <button class="b b1" type="submit">Request the evaluation</button>
 <p class="fnote">No fee. No connection to any live system. Mutual NDA before any file moves.</p>
</div>
<div class="fok" role="status" aria-live="polite"></div>
</form>'''

def build_evaluation():
    steps = "".join(
        f'<div><div class="n">{n}</div><h3>{html.escape(t)}</h3><p>{html.escape(d)}</p>'
        f'<div class="w8">{html.escape(w)}</div></div>' for n,t,d,w in EVAL_STEPS)
    terms = "".join(
        f'<div class="rw"><b>{html.escape(a)}</b><p>{html.escape(b)}</p></div>'
        for a,b in EVAL_TERMS)
    body = f'''{nav()}
<section class="sec" style="padding-top:clamp(56px,7vw,96px)">
<div class="grid-bg"></div>
<div class="w">
<p class="kv">Evaluation</p>
<h1 style="margin-top:22px;max-width:15ch">Send one export.<br>Get the answer in three weeks.</h1>
<p class="ld" style="margin-top:28px">We run your own historical data with the outcome withheld from
us, and report how many hours of warning the engine would have given, and how often it would have
been wrong. There is no fee, no integration and no connection to anything you operate. If the answer
is unimpressive you will have that in writing too.</p>
<div class="btns"><a class="b b1" href="#request">Start a request</a>
<a class="b b2" href="{CAL}">Book a call first</a></div>
</div></section>

<section class="sec alt"><div class="w">
<div class="hd" data-rv><p class="kv">01 <span class="dim">&nbsp; How it works</span></p>
<div><h2>Three steps, and one of them is yours.</h2></div></div>
<div class="steps">{steps}</div>
</div></section>

<section class="sec"><div class="w">
<div class="hd" data-rv><p class="kv">02 <span class="dim">&nbsp; Terms</span></p>
<div><h2>What you are agreeing to.</h2></div></div>
<div class="rows" data-rv>{terms}</div>
<p class="lnote" data-rv>The engine is read-only. It reads a file and returns a forecast with a
confidence band. It connects to no control loop and changes no set point.</p>
</div></section>

<section class="sec alt" id="request"><div class="w">
<div class="hd" data-rv><p class="kv">03 <span class="dim">&nbsp; Request</span></p>
<div><h2>Tell us what you have.</h2>
<p class="ld" style="margin-top:24px">A rough answer is fine. If you are not sure what you log or
whether it is usable, say so, that is a normal place to start and it is a five minute conversation
rather than a project.</p></div></div>
{form_block("Evaluation page")}
</div></section>

<section class="sec cta"><div class="w">
<p class="kv">Or skip the form</p>
<h2 style="margin-top:22px">Email us directly.</h2>
<div class="btns"><a class="b b1" href="mailto:{MAIL}?subject=Evaluation%20request">{MAIL}</a>
<a class="b b2" href="{CAL}">Book a call</a></div>
</div></section>
{footer()}'''
    open(os.path.join(OUT,"evaluation.html"),"w").write(
        page(f"Free evaluation — {BRAND}",
             "Send one historical sensor export. We run it blind and report how many hours of "
             "warning the engine would have given, and the false alarm rate. No fee.", body))


# ------------------------------------------------------------------ company
def build_company():
    tm = "".join(
        f'<div class="tm"><div class="r">{html.escape(r)}</div><h4>{html.escape(n)}</h4>'
        f'<p>{html.escape(b)}</p><div class="fo">{html.escape(f)}</div></div>'
        for r,n,b,f in TEAM)
    body = f'''{nav()}
<section class="sec" style="padding-top:clamp(60px,8vw,104px)">
<div class="grid-bg"></div>
<div class="w">
<p class="kv">Company</p>
<h1 style="margin-top:24px;max-width:16ch">A control company for living infrastructure.</h1>
<p class="ld" style="margin-top:30px">{BRAND} develops software, models and edge systems for
environments where biology and machinery must operate as one system. The company spans terrestrial
production, environmental restoration and off-world life support without forcing one product identity
across fundamentally different customers.</p>
<div class="thesis"><b>Corporate thesis</b>{html.escape(THESIS)}</div>
</div></section>

<section class="sec alt"><div class="w">
<div class="hd" data-rv><p class="kv">Founders</p><div><h2>Three people, stated plainly.</h2></div></div>
<div class="team">{tm}</div>
</div></section>

<section class="sec"><div class="w">
<div class="hd" data-rv><p class="kv">Stage</p><div><h2>Where the company is.</h2></div></div>
<div class="rows" data-rv>
<div class="rw"><b>Stage</b><p>Seed. Pre-revenue.</p></div>
<div class="rw"><b>Proof</b><p>Simulation-validated against the reference models each field already
uses, and backtested on real commercial operating history in aquaculture. No production deployment.</p></div>
<div class="rw"><b>First pilots</b><p>Scheduled for the first half of 2027.</p></div>
<div class="rw"><b>Registered address</b><p class="sm">{html.escape(ADDRESS)}</p></div>
</div>
</div></section>

<section class="sec alt cta"><div class="w">
<p class="kv">Contact</p>
<h2 style="margin-top:24px">Talk to us.</h2>
<div class="btns" data-rv><a class="b b1" href="{CAL}">Book a call</a>
<a class="b b2" href="mailto:{MAIL}">{MAIL}</a></div>
</div></section>
{footer()}'''
    open(os.path.join(OUT,"company.html"),"w").write(
        page(f"Company — {BRAND}",
             "Orbital Ecology develops state estimation and forecasting for environments where "
             "biology and machinery must operate as one system.", body))

# ------------------------------------------------------------------ misc
def build_misc():
    body = f'''{nav()}
<section class="sec" style="padding:clamp(84px,13vw,180px) 0"><div class="grid-bg"></div><div class="w">
<p class="kv">404</p><h1 style="margin-top:24px">Not found.</h1>
<p class="ld" style="margin-top:26px">That page does not exist.</p>
<div class="btns"><a class="b b1" href="index.html">Back to the start</a></div>
</div></section>{footer()}'''
    open(os.path.join(OUT,"404.html"),"w").write(page(f"Not found — {BRAND}","Page not found.",body))

    urls = ["index.html","evaluation.html","company.html"] + [f"{p[0]}.html" for p in PRODUCTS]
    sm = ('<?xml version="1.0" encoding="UTF-8"?>\n'
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
          + "".join(f"  <url><loc>https://{DOMAIN}/{u}</loc></url>\n" for u in urls)
          + "</urlset>\n")
    open(os.path.join(OUT,"sitemap.xml"),"w").write(sm)
    open(os.path.join(OUT,"robots.txt"),"w").write(
        f"User-agent: *\nAllow: /\nSitemap: https://{DOMAIN}/sitemap.xml\n")
    open(os.path.join(OUT,"CNAME"),"w").write(DOMAIN+"\n")

if __name__ == "__main__":
    build_index()
    for p in PRODUCTS: build_product(p[0])
    build_evaluation()
    build_company()
    build_misc()
    print("built", len([f for f in os.listdir(OUT) if f.endswith(".html")]), "pages")
