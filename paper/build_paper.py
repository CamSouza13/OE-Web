# -*- coding: utf-8 -*-
"""Orbital Ecology, paper edition.

A different premise from the dark site: this one is a scientific document.
Warm paper, editorial serif, numbered sections, marginal notes, a real
figure with a caption, specimen plates for the systems, and a validation
table set the way a journal would set it.

The argument for the format: this company's whole differentiator is being
straight about what has been proven and what has not. A paper is the form
that argument already has.

Reads content.py from the parent directory. Outputs index.html here.
"""
import os, sys, html
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from content import *

OUT = os.path.dirname(os.path.abspath(__file__))
FIG1 = open(os.path.join(OUT, "assets", "figure-1.svg")).read()

PLATE = {"current":"raceways","canopy":"cea","aquifer":"growhouse","reclaim":"clarifiers",
         "culture":"bioprocess","orbis":"life-support","field":"delta","nexus":"diffgrid"}

CSS = """
:root{
 --paper:#F4F2ED; --paper2:#EDEAE3; --card:#FAF9F5;
 --ink:#1A1916; --ink2:#4A4842; --ink3:#7C786F; --ink4:#A8A399;
 --rule:#D6D2C7; --rule2:#BFBAAE;
 --acc:#A4441C;
 --serif:"Iowan Old Style","Palatino Linotype",Palatino,"Book Antiqua",Georgia,serif;
 --sans:"Helvetica Neue",Helvetica,Arial,sans-serif;
 --mono:ui-monospace,"SF Mono","Courier New",Courier,monospace;
 --measure:64ch; --pad:clamp(20px,5vw,64px);
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%;scroll-behavior:smooth;scroll-padding-top:64px}
body{margin:0;background:var(--paper);color:var(--ink);
 font-family:var(--serif);font-size:17.5px;line-height:1.62;
 -webkit-font-smoothing:antialiased;font-kerning:normal;
 background-image:radial-gradient(rgba(26,25,22,.018) 1px,transparent 1px);
 background-size:3px 3px}
img,svg{display:block;max-width:100%}
a{color:inherit}
::selection{background:var(--ink);color:var(--paper)}
:focus{outline:none}
:focus-visible{outline:1.5px solid var(--acc);outline-offset:3px}

/* ---- page frame: a wide margin column, like a printed page ---- */
.sheet{max-width:1180px;margin:0 auto;padding:0 var(--pad)}
.doc{display:grid;grid-template-columns:168px minmax(0,var(--measure)) 1fr;gap:0 44px}
.doc>.gut{grid-column:1}
.doc>.col{grid-column:2}
.doc>.full{grid-column:1/-1}
@media(max-width:1000px){
 .doc{grid-template-columns:1fr}
 .doc>.gut,.doc>.col,.doc>.full{grid-column:1}
}

/* ---- masthead ---- */
.mast{border-bottom:1px solid var(--ink);position:sticky;top:0;z-index:40;
 background:rgba(244,242,237,.94);backdrop-filter:saturate(140%) blur(10px)}
.mast .in{max-width:1180px;margin:0 auto;padding:0 var(--pad);height:62px;
 display:flex;align-items:center;gap:16px}
.mast .wm{display:flex;align-items:center;gap:11px;text-decoration:none}
.mast .wm img.m{width:29px}.mast .wm img.w{width:104px}
.mast nav{margin-left:auto;display:flex;gap:22px;align-items:center}
.mast a.n{font-family:var(--mono);font-size:10px;letter-spacing:.15em;text-transform:uppercase;
 color:var(--ink2);text-decoration:none;padding:3px 0;border-bottom:1px solid transparent}
.mast a.n:hover{border-bottom-color:var(--ink)}
.mast .cta{font-family:var(--mono);font-size:10px;letter-spacing:.15em;text-transform:uppercase;
 color:var(--paper);background:var(--ink);text-decoration:none;padding:9px 14px}
.mast .cta:hover{background:var(--acc)}
@media(max-width:860px){.mast a.n{display:none}
 .mast .in{height:56px;gap:10px}
 .mast .cta{font-size:9px;letter-spacing:.11em;padding:8px 11px;white-space:nowrap}
 .mast .wm img.m{width:25px}.mast .wm img.w{width:88px}}

/* ---- title block ---- */
.title{padding:clamp(56px,9vw,124px) 0 clamp(34px,4vw,54px)}
.slug{font-family:var(--mono);font-size:10px;letter-spacing:.22em;text-transform:uppercase;
 color:var(--ink3);margin:0 0 clamp(28px,4vw,46px)}
h1{margin:0;font-family:var(--serif);font-weight:400;font-size:clamp(40px,7vw,86px);
 line-height:1.02;letter-spacing:-.022em;max-width:16ch}
h1 em{font-style:italic}
.deck{margin:clamp(26px,3vw,38px) 0 0;font-size:clamp(19px,1.9vw,23px);line-height:1.5;
 color:var(--ink2);max-width:46ch}
.byline{margin-top:clamp(30px,4vw,48px);padding-top:16px;border-top:1px solid var(--rule);
 display:flex;gap:36px;flex-wrap:wrap;
 font-family:var(--mono);font-size:10px;letter-spacing:.13em;text-transform:uppercase;color:var(--ink3)}
.byline b{display:block;color:var(--ink);font-weight:400;margin-top:5px;letter-spacing:.1em}

/* ---- abstract ---- */
.abstract{background:var(--paper2);border-top:1px solid var(--ink);border-bottom:1px solid var(--rule);
 padding:clamp(30px,4vw,46px) 0}
.abstract .lbl{font-family:var(--mono);font-size:10px;letter-spacing:.2em;text-transform:uppercase;
 color:var(--ink3);padding-top:4px}
.abstract p{margin:0;font-size:17px;line-height:1.62}
.abstract p+p{margin-top:14px}

/* ---- sections ---- */
section{padding:clamp(52px,7vw,96px) 0;border-bottom:1px solid var(--rule)}
.snum{font-family:var(--mono);font-size:10px;letter-spacing:.2em;text-transform:uppercase;
 color:var(--acc);padding-top:8px}
h2{margin:0 0 clamp(22px,3vw,34px);font-family:var(--serif);font-weight:400;
 font-size:clamp(27px,3.4vw,40px);line-height:1.12;letter-spacing:-.015em;max-width:20ch}
h3{margin:0 0 8px;font-family:var(--sans);font-weight:600;font-size:15px;letter-spacing:-.005em}
p{margin:0 0 17px}
p:last-child{margin-bottom:0}
.lead{font-size:19px;line-height:1.56}
.note{font-family:var(--mono);font-size:11px;line-height:1.72;color:var(--ink3);letter-spacing:.01em}
.gut .note{padding-top:6px}
.gut .note b{display:block;color:var(--ink2);font-weight:400;text-transform:uppercase;
 letter-spacing:.16em;font-size:9.5px;margin-bottom:7px}
.sc{font-variant:small-caps;letter-spacing:.06em}

/* ---- figure ---- */
figure{margin:clamp(34px,4vw,52px) 0 0;grid-column:1/-1}
.plate{background:var(--card);border:1px solid var(--rule2);padding:clamp(14px,2vw,26px)}
figcaption{margin-top:14px;font-family:var(--mono);font-size:11px;line-height:1.7;color:var(--ink2);
 max-width:78ch}
figcaption b{color:var(--ink);font-weight:400;letter-spacing:.12em;text-transform:uppercase;
 font-size:10px;margin-right:8px}
.fig1{width:100%;height:auto}
.fig1 .frame{fill:none;stroke:var(--rule2);stroke-width:1}
.fig1 .gx,.fig1 .gy{stroke:var(--rule);stroke-width:1}
.fig1 .ax{fill:var(--ink3);font-family:var(--mono);font-size:10px;letter-spacing:.06em}
.fig1 .yl,.fig1 .xl{font-size:9.5px;letter-spacing:.14em;text-transform:uppercase;fill:var(--ink4)}
.fig1 .lab{font-family:var(--mono);font-size:10px;letter-spacing:.14em;text-transform:uppercase;
 fill:var(--ink2)}
.fig1 .th-l,.fig1 .l2{fill:var(--acc)}
.fig1 .th{stroke:var(--acc);stroke-width:1;stroke-dasharray:4 4}
.fig1 .win{fill:var(--acc);opacity:.055}
.fig1 .obs{fill:none;stroke:var(--ink4);stroke-width:1.3}
.fig1 .state{fill:none;stroke:var(--ink);stroke-width:2}
.fig1 .v1{stroke:var(--ink);stroke-width:1;opacity:.5}
.fig1 .v2{stroke:var(--acc);stroke-width:1;opacity:.6}
.fig1 .dot{fill:var(--ink)}
.fig1 .gap{fill:var(--ink);font-family:var(--serif);font-size:19px}

.fig1 .obs,.fig1 .state{stroke-dasharray:var(--Lo);stroke-dashoffset:var(--Lo)}
.fig1 .state{stroke-dasharray:var(--Ls);stroke-dashoffset:var(--Ls)}
.fig1 .band,.fig1 .win,.fig1 .th,.fig1 .v1,.fig1 .v2,.fig1 .dot,.fig1 .lab,.fig1 .gap{opacity:0}
.rv .fig1 .obs{animation:draw 1.6s cubic-bezier(.4,0,.3,1) .1s both}
.rv .fig1 .th{animation:fade .7s ease .8s both}
.rv .fig1 .th-l{animation:fade .6s ease 1s both}
.rv .fig1 .band{animation:fade 1s ease 1.1s both}
.rv .fig1 .state{animation:draw 1.9s cubic-bezier(.4,0,.3,1) 1.15s both}
.rv .fig1 .v1{animation:fade .6s ease 2.5s both}
.rv .fig1 .dot{animation:fade .5s ease 2.55s both}
.rv .fig1 .l1{animation:fade .6s ease 2.6s both}
.rv .fig1 .v2{animation:fade .6s ease 2.85s both}
.rv .fig1 .l2{animation:fade .6s ease 2.95s both}
.rv .fig1 .win{animation:fade .9s ease 3.05s both}
.rv .fig1 .gap{animation:fade .8s ease 3.2s both}
@keyframes draw{from{stroke-dashoffset:var(--Ls,1400);opacity:1}to{stroke-dashoffset:0;opacity:1}}
@keyframes fade{from{opacity:0}to{opacity:1}}
.fig1 .win{opacity:.055}
.rv .fig1 .win{animation:fadewin .9s ease 3.05s both}
@keyframes fadewin{from{opacity:0}to{opacity:.055}}

/* ---- method, numbered ---- */
.steps{counter-reset:s;margin:0;padding:0;list-style:none}
.steps li{counter-increment:s;padding:22px 0;border-top:1px solid var(--rule);display:grid;
 grid-template-columns:44px 1fr;gap:20px}
.steps li:before{content:counter(s,decimal-leading-zero);font-family:var(--mono);font-size:11px;
 letter-spacing:.1em;color:var(--ink4);padding-top:4px}
.steps h3{margin-bottom:7px;font-size:16px}
.steps p{margin:0;font-size:16px;color:var(--ink2)}

/* ---- specimen plates ---- */
.specs{display:grid;grid-template-columns:repeat(4,1fr);gap:clamp(20px,3vw,40px) clamp(16px,2.4vw,32px);
 margin-top:clamp(26px,3vw,42px)}
.spec{text-decoration:none;display:block}
.spec .disc{display:block;position:relative;aspect-ratio:1/1;border-radius:50%;overflow:hidden;
 background:var(--card);border:1px solid var(--rule2);
 transition:border-color .3s,transform .5s cubic-bezier(.2,.7,.3,1)}
.spec .disc img{width:100%;height:100%;object-fit:cover;
 transition:transform .8s cubic-bezier(.2,.7,.3,1),filter .4s;filter:contrast(1.02)}
.spec:hover .disc{border-color:var(--ink);transform:translateY(-3px)}
.spec:hover .disc img{transform:scale(1.06)}
.spec .disc:after{content:"";position:absolute;inset:0;border-radius:50%;
 box-shadow:inset 0 0 0 1px rgba(26,25,22,.10),inset 0 14px 30px -18px rgba(26,25,22,.5)}
.spec .cap{display:block;margin-top:13px;padding-top:9px;border-top:1px solid var(--rule)}
.spec .id{display:block;font-family:var(--mono);font-size:9.5px;letter-spacing:.15em;color:var(--ink4)}
.spec .nm{display:block;font-family:var(--sans);font-size:14.5px;font-weight:600;
 letter-spacing:.01em;margin-top:5px;color:var(--ink)}
.spec .mk{display:block;font-family:var(--mono);font-size:9.5px;letter-spacing:.11em;
 text-transform:uppercase;color:var(--ink3);margin-top:4px;line-height:1.5;min-height:2.1em}
@media(max-width:900px){.specs{grid-template-columns:repeat(2,1fr)}}

/* ---- table ---- */
table{width:100%;border-collapse:collapse;font-family:var(--sans);font-size:14px;margin-top:6px}
caption{text-align:left;font-family:var(--mono);font-size:11px;line-height:1.7;color:var(--ink2);
 margin-bottom:14px}
caption b{color:var(--ink);font-weight:400;letter-spacing:.12em;text-transform:uppercase;
 font-size:10px;margin-right:8px}
thead th{font-family:var(--mono);font-size:9.5px;letter-spacing:.16em;text-transform:uppercase;
 color:var(--ink3);font-weight:400;text-align:left;padding:0 14px 9px 0;
 border-bottom:1px solid var(--ink)}
tbody td{padding:13px 14px 13px 0;border-bottom:1px solid var(--rule);vertical-align:top;
 color:var(--ink2)}
tbody td:first-child{font-family:var(--mono);font-size:10px;letter-spacing:.13em;
 text-transform:uppercase;color:var(--ink);white-space:nowrap}
tbody td.ref{font-family:var(--mono);font-size:11.5px;color:var(--ink);white-space:nowrap}
tbody td.what{color:var(--ink)}
tbody td.what span{display:block;font-size:12.5px;color:var(--ink3);margin-top:3px}
tbody tr:hover td{background:var(--paper2)}
@media(max-width:820px){
 table,thead,tbody,tr,td,th{display:block}
 thead{display:none}
 tbody tr{border-bottom:1px solid var(--ink);padding:14px 0}
 tbody td{border:0;padding:2px 0}
}

/* ---- references ---- */
.refs{counter-reset:r;list-style:none;margin:0;padding:0}
.refs li{padding:16px 0;border-top:1px solid var(--rule);display:grid;
 grid-template-columns:52px 1fr;gap:18px;font-size:15px;line-height:1.55}
.refs .k{font-family:var(--mono);font-size:10.5px;letter-spacing:.12em;color:var(--acc);padding-top:4px}
.refs .t{color:var(--ink)}
.refs .c{display:block;font-family:var(--mono);font-size:11px;color:var(--ink3);margin-top:6px;
 line-height:1.65}
.refs a{font-family:var(--mono);font-size:10px;letter-spacing:.13em;text-transform:uppercase;
 color:var(--ink2);text-decoration:none;border-bottom:1px solid var(--rule2);
 display:inline-block;margin-top:8px;padding-bottom:2px}
.refs a:hover{color:var(--acc);border-bottom-color:var(--acc)}
sup{font-family:var(--mono);font-size:9px;color:var(--acc);vertical-align:super;margin-left:1px}

/* ---- closing ---- */
.close{background:var(--ink);color:var(--paper);border:0;padding:clamp(64px,8vw,116px) 0}
.close h2{color:var(--paper);max-width:16ch}
.close p{color:#B9B4A9;max-width:52ch;font-size:18px}
.close .snum{color:#8A857A}
.btns{display:flex;gap:12px;flex-wrap:wrap;margin-top:32px}
.b{font-family:var(--mono);font-size:11px;letter-spacing:.15em;text-transform:uppercase;
 text-decoration:none;padding:15px 24px;transition:.2s}
.b1{background:var(--paper);color:var(--ink)}.b1:hover{background:var(--acc);color:var(--paper)}
.b2{border:1px solid #55514A;color:var(--paper)}.b2:hover{border-color:var(--paper)}

/* ---- colophon ---- */
.colo{padding:44px 0 56px;font-family:var(--mono);font-size:10.5px;letter-spacing:.08em;
 color:var(--ink3);line-height:1.9}
.colo .r{display:flex;justify-content:space-between;gap:30px;flex-wrap:wrap}
.colo a{color:var(--ink2);text-decoration:none;border-bottom:1px solid var(--rule2)}
.colo a:hover{color:var(--acc)}

/* ---- motion ---- */
[data-rv]{opacity:0;transform:translateY(14px);
 transition:opacity .9s cubic-bezier(.2,.7,.3,1),transform .9s cubic-bezier(.2,.7,.3,1);
 transition-delay:var(--d,0ms)}
[data-rv].rv{opacity:1;transform:none}
@media(prefers-reduced-motion:reduce){
 *,*:before,*:after{animation-duration:.001ms!important;animation-delay:0ms!important;
  transition-duration:.001ms!important;transition-delay:0ms!important}
 [data-rv]{opacity:1;transform:none}
 .fig1 *{opacity:1!important;stroke-dashoffset:0!important}
 .fig1 .win{opacity:.055!important}
}
"""

JS = """
<script>
(function(){
 var rm=matchMedia("(prefers-reduced-motion:reduce)").matches;
 var S="[data-rv],figure,.specs,table,.steps";
 if(rm||!("IntersectionObserver" in window)){
   document.querySelectorAll(S).forEach(function(e){e.classList.add("rv")}); return; }
 document.querySelectorAll(".specs").forEach(function(g){
   [].forEach.call(g.children,function(c,i){c.style.setProperty("--d",(i*70)+"ms")}); });
 var io=new IntersectionObserver(function(es){
   es.forEach(function(e){ if(e.isIntersecting){ e.target.classList.add("rv"); io.unobserve(e.target); } });
 },{rootMargin:"0px 0px -10% 0px",threshold:.1});
 document.querySelectorAll(S).forEach(function(e){io.observe(e)});
})();
</script>"""


def build():
    e = html.escape

    specs = "".join(
        f'''<a class="spec" href="../{p[0]}.html" data-rv>
<span class="disc"><img src="assets/img/{PLATE[p[0]]}.webp" alt="" loading="lazy"></span>
<span class="cap"><span class="id">{e(p[9])}</span>
<span class="nm">{p[1]}</span>
<span class="mk">{e(p[2])}</span></span></a>''' for p in PRODUCTS)

    rows = "".join(
        f'<tr><td>{e(st)}</td><td class="ref">{e(ref)}</td>'
        f'<td class="what">{e(b)}<span>{e(d)}</span></td><td>{e(r)}</td></tr>'
        for st, ref, b, d, r in RECORD)

    steps = "".join(
        f'<li><div><h3>{e(t)}</h3><p>{e(d)}</p></div></li>' for n, t, d in METHOD)

    refs = "".join(
        f'<li><span class="k">{sid}</span><span class="t">{e(t)}'
        f'<span class="c">{e(d)}<br>{e(c)}</span>'
        + (f'<a href="{u}" rel="noopener">Source</a>' if u else '')
        + '</span></li>' for sid, t, d, c, u in SOURCES)

    doc = f'''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(BRAND)} — technical overview</title>
<meta name="description" content="State estimation and forecasting for closed living systems.
One engine across aquaculture, controlled agriculture, water, bioprocess and life support.">
<meta name="theme-color" content="#F4F2ED">
<link rel="icon" href="../assets/icon-512.png">
<style>{CSS}</style></head>
<body><main>

<header class="mast"><div class="in">
<a class="wm" href="index.html" aria-label="{e(BRAND)}">
<img class="m" src="assets/mark-ink.png" alt=""><img class="w" src="assets/wordmark-ink.png" alt="{e(BRAND)}"></a>
<nav aria-label="Primary">
<a class="n" href="#problem">Problem</a>
<a class="n" href="#method">Method</a>
<a class="n" href="#systems">Systems</a>
<a class="n" href="#record">Record</a>
<a class="n" href="{MEDIUM}" target="_blank" rel="noopener">Notes</a>
</nav>
<a class="cta" href="../evaluation.html">Request an evaluation</a>
</div></header>

<div class="sheet"><div class="doc">
<div class="full title">
<p class="slug">{e(BRAND)} &nbsp;·&nbsp; Technical overview &nbsp;·&nbsp; Revision 2026.08</p>
<h1>Living systems fail <em>in silence.</em></h1>
<p class="deck">Every gauge on a closed system measures a consequence. We estimate the state
that produced it, and simulate that state forward.</p>
<div class="byline">
<span>Method<b>Bayesian state estimation</b></span>
<span>Domains<b>Seven, one engine</b></span>
<span>Evidence<b>Four benchmarks, one backtest</b></span>
<span>Deployment<b>Read-only</b></span>
</div>
</div>
</div></div>

<div class="abstract"><div class="sheet"><div class="doc">
<p class="lbl gut">Abstract</p>
<div class="col">
<p>In a closed biological process, the variable that decides the outcome is not measured.
Dissolved oxygen is what the biology left behind. Ammonia is what the biofilter has not cleared.
Slab EC is a receipt. Instruments report what the process already did, so operators fund margin
they cannot size and respond to symptoms rather than causes.</p>
<p>We write the process down as a mechanistic model, solve backwards to recover the state no
instrument reports, and integrate that state forward. The output is a forecast with a stated
confidence, not an alarm. Results to date are benchmark validation and one held-out backtest on
commercial operating history. There is no production deployment.<sup>S8</sup></p>
</div>
</div></div></div>

<div class="sheet"><div class="doc">

<section id="problem" class="full"><div class="doc">
<p class="snum gut">§ 1</p>
<div class="col">
<h2>The variable that decides the outcome is unmeasured.</h2>
<p class="lead">A hidden state drifts for hours while every instrument reads normal, then the
observable steps. A threshold alarm cannot help with that shape, because the threshold is drawn
on the thing that moves last. An estimator can, because it watches the thing that moves first.</p>
<p>The cost is economic before it is technical. Because the state cannot be seen, a well-run
facility runs with margin: extra aeration, conservative loading, stock density below what the
system could carry. That margin is paid every day to insure against a night nobody can predict.
Published incidents put the acute cost at USD 1.16M and USD 5M in single events at land-based
farms,<sup>S1,S2</sup> and aeration alone accounts for 50 to 90 percent of plant electricity in
conventional activated sludge, set conservatively because nitrifier state is not measured.<sup>S3</sup></p>
</div>
<figure data-rv>
<div class="plate">{FIG1}</div>
<figcaption><b>Figure 1</b>The estimated hidden state (solid) crosses the action threshold
6.5 hours before the observable instrument (thin) moves. The band is the estimator's confidence.
Illustration of the method, not a data plot; the 6.5 h interval is the lead reproduced on
held-out commercial operating history under benchmark OE/01.<sup>S8</sup></figcaption>
</figure>
</div></section>

<section id="method" class="full"><div class="doc">
<p class="snum gut">§ 2</p>
<div class="col">
<h2>Three steps. One of them changes by domain.</h2>
<p>Steps two and three are identical whether the system is a recirculating farm, an activated
sludge reactor, a fermenter or a sealed habitat. Only the process model is rewritten. That is
why one engine serves seven markets, and why the work compounds across every deployment.</p>
<ol class="steps">{steps}</ol>
</div>
<p class="note gut" data-rv><b>On deployment</b>The engine is read-only. It reads existing
telemetry and returns a forecast with a confidence band. It connects to no control loop and
changes no set point. Autonomous control is roadmap, not product.</p>
</div></section>

<section id="systems" class="full"><div class="doc">
<p class="snum gut">§ 3</p>
<div class="col">
<h2>Seven markets, one estimator, one platform beneath them.</h2>
<p>An aquaculture operator should be able to buy an aquaculture product rather than a space
product. The markets differ in buyer, regulation and sales cycle. What is shared is the engine,
and the engine is the part that compounds.</p>
</div>
<div class="specs full">{specs}</div>
</div></section>

<section id="record" class="full"><div class="doc">
<p class="snum gut">§ 4</p>
<div class="col">
<h2>Every figure resolves to a run.</h2>
<p>Simulation results are labelled as simulation. The aquaculture result is a held-out backtest
on real commercial operating history. There is no production deployment and none is implied.
Live process results are published to this same record as operator evaluations complete.</p>
</div>
<div class="full" data-rv style="margin-top:clamp(28px,3.4vw,44px)">
<table>
<caption><b>Table 1</b>Validation record. Benchmarks are the reference models each field already
uses to evaluate control strategies.<sup>S4,S5,S6,S7</sup></caption>
<thead><tr><th>Status</th><th>Ref</th><th>Benchmark</th><th>Result</th></tr></thead>
<tbody>{rows}</tbody>
</table>
</div>
</div></section>

<section id="refs" class="full"><div class="doc">
<p class="snum gut">§ 5</p>
<div class="col">
<h2>References.</h2>
<ol class="refs">{refs}</ol>
</div>
</div></section>

</div></div>

<section class="close"><div class="sheet"><div class="doc">
<p class="snum gut">§ 6</p>
<div class="col">
<h2>Send one export. Get the answer in three weeks.</h2>
<p>You send a historical sensor export with the outcome window withheld. We run it blind and
report how many hours of warning the engine would have given, and how often it would have been
wrong on that same history. No fee, no integration, no connection to any live system. The file
is deleted afterwards.</p>
<div class="btns">
<a class="b b1" href="../evaluation.html">Request an evaluation</a>
<a class="b b2" href="{CAL}">Book a call</a>
</div>
</div>
</div></div></section>

<div class="sheet"><div class="colo"><div class="r">
<span>&copy; 2026 {e(BRAND)} &nbsp;·&nbsp; {e(ADDRESS)}</span>
<span>Simulation-validated and backtested. No production deployment.</span>
<span><a href="mailto:{MAIL}">{MAIL}</a></span>
</div></div></div>

</main>{JS}</body></html>'''
    open(os.path.join(OUT, "index.html"), "w").write(doc)
    print("paper edition built:", len(doc), "bytes")


if __name__ == "__main__":
    build()
