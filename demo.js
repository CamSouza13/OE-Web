(function(){
'use strict';
var D=window.DOMAINS, OE=window.OE, ORDER=['aquaculture','hydroponics','bioreactor','blss'];
var MEAS='#35619C', EST='#2A7F55', ALR='#A54A1C', GRID='#E2E0D8', AXT='#8E9196', SURF='#FAFAF7';

var fmtUSD=function(v){return v>=1e6?'$'+(v/1e6).toFixed(2)+'M':v>=1000?'$'+Math.round(v/1000)+'k':
 (v===Math.round(v)?'$'+v:'$'+v.toFixed(2));};
var fmtN=function(v){return v>=1e6?(v/1e6).toFixed(1)+'M':v.toLocaleString();};
var nice=function(v){return +v.toFixed(1);};

function parseCSV(t){
 var L=t.replace(/﻿/,'').trim().split(/\r?\n/);
 if(L.length<3) throw new Error('too few rows');
 var h=L[0].split(',').map(function(s){return s.trim();});
 return L.slice(1).map(function(l){var c=l.split(','),o={};
  h.forEach(function(k,i){o[k]=c[i];});return o;});
}

/* ---------------------------------------------------------------
   The estimator. Same structure as the production engine, but the
   row loop is time-sliced so the page can report what it is doing
   while it does it. Nothing about the maths changes.
   --------------------------------------------------------------- */
function runAsync(d,rows,onTick,done){
 /* Counters are global to the engine and four cards can run at once, so take
    the delta around each row. A row is synchronous, so the delta is exact. */
 var W={upd:0,fc:0,traj:0,rk4:0,sig:0};
 var n=d.states.length,i,Q=[];
 for(i=0;i<n;i++){Q.push(new Float64Array(n));Q[i][i]=d.proc[i]*d.proc[i];}
 var f=new OE.UKF(n,Q);
 f.x=Float64Array.from(d.x0);
 f.P=[];for(i=0;i<n;i++){f.P.push(new Float64Array(n));f.P[i][i]=d.P0[i];}
 var hid=[],sd=[],prob=[],nis=[],alert=null,cross=null,why='';
 var A=0.30,last=0,base=0,
     B=Math.max(23,Math.round(12/d.dt)),
     EV=Math.max(1,Math.floor(rows.length/(d.fcEv||64))),
     k=0;

 function row(){
  var C=OE.ctr,a0=C.upd,a1=C.fc,a2=C.traj,a3=C.rk4,a4=C.sig;
  var u=d.u(rows[k]),j;
  f.predict(d.dt,function(x,dt){return OE.step(x,dt,d.deriv,u,d.p,d.nonneg,d.maxh);});
  var z=[],idx=[],R=[];
  d.chan.forEach(function(c){var v=parseFloat(rows[k][c.col]);
   if(isFinite(v)){if(c.xf)v=c.xf(v);z.push(v);idx.push(c.s);R.push(c.r*c.r);}});
  f.update(z,idx,R,true);
  for(j=0;j<n;j++)if(d.nonneg[j]&&f.x[j]<0)f.x[j]=0;
  f.x[d.hidden]=Math.min(Math.max(f.x[d.hidden],0),1.5);
  hid.push(f.x[d.hidden]);
  sd.push(Math.sqrt(Math.max(f.P[d.hidden][d.hidden],0)));
  nis.push(f.nis);
  if(k%EV===0||k===rows.length-1){
   var H=d.dt*Math.round((d.unit==='d'?7:48)/d.dt);
   last=OE.forecast(f.x,f.P,d.deriv,u,d.p,d.nonneg,d.safety,H,d.dt,d.fcN||70,k+1,d.maxh).p;
  }
  prob.push(last);
  /* Two ways to raise a hand, whichever comes first.
     1. The estimated capacity has fallen below 85 percent of the baseline this
        site set for itself. Nothing on site reports this, which is the point.
     2. Monte-Carlo breach probability passes 0.30. */
  if(k===B){base=0;for(j=0;j<=k;j++)base+=hid[j];base/=(k+1);}
  if(alert===null&&base>0&&k>B&&hid[k]<0.85*base){alert=k;why='capacity';}
  if(alert===null&&last>A){alert=k;why='forecast';}
  W.upd+=C.upd-a0;W.fc+=C.fc-a1;W.traj+=C.traj-a2;W.rk4+=C.rk4-a3;W.sig+=C.sig-a4;
  k++;
 }

 function slice(){
  var t0=(window.performance||Date).now();
  while(k<rows.length){ row(); if(((window.performance||Date).now()-t0)>36) break; }
  onTick(k/rows.length, k>B, W.traj);
  if(k<rows.length){setTimeout(slice,0);return;}
  /* lead is measured against the MEASURED channel crossing its limit, not the
     filter's own estimate, so it is a real warning interval */
  var sc=null,q;
  for(q=0;q<d.chan.length;q++)if(d.chan[q].s===d.safety.idx)sc=d.chan[q];
  if(sc){for(q=0;q<rows.length;q++){var mv=parseFloat(rows[q][sc.col]);
   if(sc.xf)mv=sc.xf(mv);
   if(isFinite(mv)&&(d.safety.dir==='>'?mv>d.safety.limit:mv<d.safety.limit)){cross=q;break;}}}
  done({hid:hid,sd:sd,prob:prob,nis:nis,alert:alert,cross:cross,why:why,base:base,
        n:rows.length,B:B,
        work:W});
 }
 setTimeout(slice,0);
}

/* Modelled impact. Every input is declared in domains.js and printed on the card. */
function econ(d,res,rows){
 var e=d.econ, lead=0;
 if(res.alert!==null&&res.cross!==null&&res.cross>res.alert) lead=(res.cross-res.alert)*d.dt;
 var stock=e.stockCol?(parseFloat(rows[rows.length-1][e.stockCol])||e.fixedStock||0):(e.fixedStock||0);
 var value=stock*e.price;
 var saved=value*e.lossFrac;
 var ins=e.insDeduct+value*e.lossFrac*(e.insLoadPct/100);
 var lab=e.labourHr*88;
 return {lead:lead,stock:stock,value:value,saved:saved,ins:ins,lab:lab,total:saved+ins+lab};
}

/* ---- charts. One axis each, never a shared scale. ---- */
function svg(w,h,inner,label){
 return '<svg viewBox="0 0 '+w+' '+h+'" width="100%" preserveAspectRatio="none" '+
  'style="display:block;height:'+h+'px" role="img" aria-label="'+label+'">'+inner+'</svg>';
}
function axis(ml,mr,W,ticks){
 var s='';
 ticks.forEach(function(t){
  s+='<line x1="'+ml+'" x2="'+(W-mr)+'" y1="'+t.y.toFixed(1)+'" y2="'+t.y.toFixed(1)+
     '" stroke="'+GRID+'" stroke-width="1"/>'+
     '<text x="'+(ml-7)+'" y="'+(t.y+3).toFixed(1)+'" text-anchor="end" fill="'+AXT+'" '+
     'font-size="8.5" font-family="ui-monospace,monospace">'+t.l+'</text>';});
 return s;
}
function plotGauge(res,d,rows){
 var W=360,H=116,ml=42,mr=6,mt=10,mb=16,pw=W-ml-mr,ph=H-mt-mb,N=res.n,sc=null,i;
 for(i=0;i<d.chan.length;i++)if(d.chan[i].s===d.safety.idx)sc=d.chan[i];
 var v=[];
 for(i=0;i<N;i++){var q=parseFloat(rows[i][sc.col]);if(sc.xf)q=sc.xf(q);v.push(isFinite(q)?q:null);}
 var lim=d.safety.limit,
     lo=Math.min.apply(null,v.filter(isFinite)),hi=Math.max.apply(null,v.filter(isFinite));
 lo=Math.min(lo,lim);hi=Math.max(hi,lim);var pad=(hi-lo)*0.10||1;lo-=pad;hi+=pad;
 var X=function(k){return ml+(N<2?0:k/(N-1)*pw);},Y=function(q){return mt+(1-(q-lo)/(hi-lo))*ph;};
 var f=function(q){return Math.abs(q)>=1000?Math.round(q):(Math.abs(q)>=10?q.toFixed(0):q.toFixed(2));};
 var g=axis(ml,mr,W,[{y:Y(hi-pad),l:f(hi-pad)},{y:Y(lim),l:f(lim)},{y:Y(lo+pad),l:f(lo+pad)}]);
 var p='';for(i=0;i<N;i++)if(v[i]!==null)p+=(p?'L':'M')+X(i).toFixed(1)+' '+Y(v[i]).toFixed(1);
 var mark='';
 if(res.cross!==null)mark='<line x1="'+X(res.cross).toFixed(1)+'" x2="'+X(res.cross).toFixed(1)+
  '" y1="'+mt+'" y2="'+(mt+ph)+'" stroke="'+ALR+'" stroke-width="1.2"/>'+
  '<circle cx="'+X(res.cross).toFixed(1)+'" cy="'+Y(v[res.cross]).toFixed(1)+
  '" r="3.2" fill="'+ALR+'" stroke="'+SURF+'" stroke-width="1.6"/>';
 return g+
  '<line x1="'+ml+'" x2="'+(W-mr)+'" y1="'+Y(lim).toFixed(1)+'" y2="'+Y(lim).toFixed(1)+
   '" stroke="'+ALR+'" stroke-width="1" stroke-dasharray="4 3" opacity=".75"/>'+
  '<path d="'+p+'" fill="none" stroke="'+MEAS+'" stroke-width="1.3" stroke-linejoin="round"/>'+mark;
}
function plotCap(res,d){
 var W=360,H=124,ml=42,mr=6,mt=10,mb=18,pw=W-ml-mr,ph=H-mt-mb,N=res.n,i;
 var X=function(k){return ml+(N<2?0:k/(N-1)*pw);},
     Y=function(q){return mt+(1-Math.min(Math.max(q,0),1.2)/1.2)*ph;};
 var g=axis(ml,mr,W,[{y:Y(1),l:'100%'},{y:Y(0.5),l:'50%'},{y:Y(0),l:'0'}]);
 var band='';
 for(i=0;i<N;i++)band+=(i?'L':'M')+X(i).toFixed(1)+' '+Y(res.hid[i]+1.96*res.sd[i]).toFixed(1);
 for(i=N-1;i>=0;i--)band+='L'+X(i).toFixed(1)+' '+Y(Math.max(res.hid[i]-1.96*res.sd[i],0)).toFixed(1);
 var line='';for(i=0;i<N;i++)line+=(i?'L':'M')+X(i).toFixed(1)+' '+Y(res.hid[i]).toFixed(1);
 var thr=res.base?'<line x1="'+ml+'" x2="'+(W-mr)+'" y1="'+Y(0.85*res.base).toFixed(1)+
  '" y2="'+Y(0.85*res.base).toFixed(1)+'" stroke="'+EST+'" stroke-width="1" stroke-dasharray="4 3" opacity=".6"/>':'';
 var mark=res.alert===null?'':'<line x1="'+X(res.alert).toFixed(1)+'" x2="'+X(res.alert).toFixed(1)+
  '" y1="'+mt+'" y2="'+(mt+ph)+'" stroke="'+EST+'" stroke-width="1.2"/>'+
  '<circle cx="'+X(res.alert).toFixed(1)+'" cy="'+Y(res.hid[res.alert]).toFixed(1)+
  '" r="3.2" fill="'+EST+'" stroke="'+SURF+'" stroke-width="1.6"/>';
 var shade=(res.alert!==null&&res.cross!==null&&res.cross>res.alert)?
  '<rect x="'+X(res.alert).toFixed(1)+'" y="'+mt+'" width="'+(X(res.cross)-X(res.alert)).toFixed(1)+
   '" height="'+ph+'" fill="'+EST+'" opacity=".09"/>':'';
 return shade+g+thr+'<path d="'+band+'Z" fill="'+EST+'" fill-opacity=".16"/>'+
  '<path d="'+line+'" fill="none" stroke="'+EST+'" stroke-width="1.7" stroke-linejoin="round"/>'+mark;
}
function dataView(res,d,rows){
 var st=Math.max(1,Math.floor(res.n/26)),sc=null,i,
  h='<table><thead><tr><th>'+(d.unit==='d'?'day':'hr')+'</th><th>gauge</th>'+
    '<th>capacity</th><th>P(breach)</th></tr></thead><tbody>';
 for(i=0;i<d.chan.length;i++)if(d.chan[i].s===d.safety.idx)sc=d.chan[i];
 for(i=0;i<res.n;i+=st){var q=parseFloat(rows[i][sc.col]);if(sc.xf)q=sc.xf(q);
  h+='<tr><td>'+nice(i*d.dt)+'</td><td>'+(q>=1000?Math.round(q):q.toFixed(2))+
   '</td><td>'+res.hid[i].toFixed(3)+'</td><td>'+res.prob[i].toFixed(2)+'</td></tr>';}
 return h+'</tbody></table>';
}

/* ---------------------------------------------------------------
   Presentation
   --------------------------------------------------------------- */
function render(card,d,rows){
 var tick=card.querySelector('.tick'),out=card.querySelector('.out'),
     li=card.querySelectorAll('.tick li'),
     val=function(i){return li[i].querySelector('em');},
     u=d.unit==='d'?'d':'h';

 function setStep(i,st){li[i].className=st;}
 tick.classList.add('on');
 setStep(0,'ok'); val(0).textContent=rows.length.toLocaleString()+' rows';
 setStep(1,'go');

 var fitted=false;
 runAsync(d,rows,
  function(frac,pastBaseline,traj){
   if(pastBaseline&&!fitted){fitted=true;setStep(1,'ok');
    val(1).textContent=nice(Math.max(23,Math.round(12/d.dt))*d.dt)+' '+u+' baseline';
    setStep(2,'go');setStep(3,'go');}
   val(2).textContent=Math.round(frac*100)+'%';
   val(3).textContent=fmtN(traj);
  },
  function(res){
   var ec=econ(d,res,rows),
       b=res.base||res.hid[0],
       atAlert=res.alert===null?0:Math.round((1-res.hid[res.alert]/Math.max(b,1e-9))*100),
       worst=Math.round((1-Math.min.apply(null,res.hid)/Math.max(b,1e-9))*100),
       atCross=(res.alert!==null&&res.cross!==null)?
         Math.round((1-res.hid[res.cross]/Math.max(b,1e-9))*100):worst,
       aT=res.alert===null?null:nice(res.alert*d.dt),
       xT=res.cross===null?null:nice(res.cross*d.dt),
       W=res.work;

   setStep(2,'ok'); val(2).textContent=W.upd.toLocaleString()+' updates';
   setStep(3,'ok'); val(3).textContent=fmtN(W.traj)+' futures';
   setStep(4,'ok'); val(4).textContent=fmtUSD(ec.total);

   out.innerHTML=
    /* ---- what happened ---- */
    '<div class="blk"><p class="slb">What happened</p>'+
     '<p class="nar">'+d.gaugeLabel+' stayed inside its normal band for the first '+
      (xT===null?'whole log':'<b>'+xT+' '+u+'</b>')+'. '+
      (aT===null?'The engine did not raise a flag on this log.':
      'The engine flagged this site at <b>'+aT+' '+u+'</b>, when its estimate of '+
      d.hiddenName.toLowerCase()+' had fallen <b>'+atAlert+'%</b> below the baseline this log '+
      'set for itself. By the time the gauge crossed, <b>'+atCross+'%</b> was gone.')+'</p>'+
     '<div class="two">'+
      '<div><div class="big">'+(ec.lead?nice(ec.lead)+'<small>'+u+'</small>':'0')+'</div>'+
       '<div class="cap">Warning ahead of the gauge</div></div>'+
      '<div><div class="big grn">'+fmtUSD(ec.total)+'</div>'+
       '<div class="cap">Modelled value of that warning</div></div>'+
     '</div></div>'+

    /* ---- the two charts ---- */
    '<div class="blk"><p class="slb">What the log looked like</p>'+
     '<figure class="plot"><div class="ph"><span class="pt">'+
       '<i class="sw" style="background:'+MEAS+'"></i>'+d.gaugeLabel+'</span>'+
       '<span class="pu">measured &middot; '+d.gaugeUnits+'</span></div>'+
      svg(360,116,plotGauge(res,d,rows),d.gaugeLabel+' with its safety limit')+
      '<figcaption>Dashed line is the limit. It is crossed at '+
       (xT===null?'no point in this log':xT+' '+u)+'.</figcaption></figure>'+
     '<figure class="plot"><div class="ph"><span class="pt">'+
       '<i class="sw" style="background:'+EST+'"></i>'+d.hiddenName+'</span>'+
       '<span class="pu">estimated &middot; % of normal</span></div>'+
      svg(360,124,plotCap(res,d),'Estimated '+d.hiddenName+' with credible band')+
      '<figcaption>Nothing on site measures this. Shaded band is the time you had to act.</figcaption>'+
     '</figure></div>'+

    /* ---- what it is worth ---- */
    '<div class="blk"><p class="slb">What it was worth</p>'+
     '<table class="val"><tbody>'+
      '<tr><td>On the line</td><td>'+(d.econ.unit==='batch'||d.econ.unit==='contingency'?
        fmtUSD(ec.value):ec.stock.toLocaleString()+' '+d.econ.unit.split(' ')[0])+'</td></tr>'+
      '<tr><td>Stock or yield kept</td><td>'+fmtUSD(ec.saved)+'</td></tr>'+
      '<tr><td>Claim and response</td><td>'+(ec.ins+ec.lab>0?fmtUSD(ec.ins+ec.lab):
        '<span class="na">not modelled</span>')+'</td></tr>'+
      '<tr class="em"><td>Total, modelled</td><td>'+fmtUSD(ec.total)+'</td></tr>'+
     '</tbody></table>'+
     '<details><summary>How this is costed</summary><p class="fine">'+
      (d.econ.unit==='batch'||d.econ.unit==='contingency'?'':
        ec.stock.toLocaleString()+' '+d.econ.unit+' on the line. ')+
      d.econ.priceLabel+' '+fmtUSD(d.econ.price)+'; '+Math.round(d.econ.lossFrac*100)+
      ' percent '+d.econ.lossLabel+
      (d.econ.insDeduct?'; deductible '+fmtUSD(d.econ.insDeduct)+' with '+d.econ.insLoadPct+
       ' percent premium loading':'')+
      (d.econ.labourHr?'; '+d.econ.labourHr+' response hours at $88':'')+
      '. Modelled, not measured. Change any input and the number changes.</p></details>'+
    '</div>'+

    /* ---- why ---- */
    '<div class="blk why"><p class="slb">Why it worked here</p>'+
     '<p class="nar">'+d.why+'</p></div>'+

    /* ---- the receipts ---- */
    '<div class="blk"><details><summary>Run detail</summary>'+
      '<table class="val sm"><tbody>'+
       '<tr><td>Rows read</td><td>'+res.n.toLocaleString()+'</td></tr>'+
       '<tr><td>Filter updates</td><td>'+W.upd.toLocaleString()+'</td></tr>'+
       '<tr><td>Sigma points propagated</td><td>'+fmtN(W.sig)+'</td></tr>'+
       '<tr><td>Forecast evaluations</td><td>'+W.fc.toLocaleString()+'</td></tr>'+
       '<tr><td>Futures simulated</td><td>'+fmtN(W.traj)+'</td></tr>'+
       '<tr><td>Integration steps</td><td>'+fmtN(W.rk4)+'</td></tr>'+
       '<tr><td>Model fit, mean NIS</td><td>'+
        (res.nis.reduce(function(a,x){return a+x;},0)/res.n).toFixed(2)+'</td></tr>'+
       '<tr><td>Flagged by</td><td>'+(res.why==='capacity'?'capacity':'forecast')+'</td></tr>'+
      '</tbody></table>'+
      '<p class="fine">NIS near 1.0 means the model explains this log. Well above means '+
      'treat the result with care. It is shown because it is the check that says when to.</p>'+
      '<div class="dv">'+dataView(res,d,rows)+'</div>'+
     '</details></div>';
   out.classList.add('on');
  });
}

function build(){
 var rack=document.getElementById('rack');
 ORDER.forEach(function(k,idx){
  var d=D[k],c=document.createElement('section');
  c.className='card';c.setAttribute('data-k',k);c.setAttribute('aria-label',d.title);
  var steps=[['Read the log',''],
             ['Fit the '+d.model,''],
             ['Estimate '+d.hiddenName.toLowerCase(),''],
             ['Simulate futures',''],
             ['Price the exposure','']];
  c.innerHTML=
   '<header class="hd"><div class="ix">'+String(idx+1).padStart(2,'0')+'</div>'+
    '<h3>'+d.title+'</h3><p>'+d.sub+'</p></header>'+
   '<div class="dz" tabindex="0" role="button" aria-label="Load a CSV for '+d.title+'">'+
    '<div class="fn">Drop an operating log</div>'+
    '<div class="mt"><a href="#" class="samp">or use the sample</a></div></div>'+
   '<ol class="tick">'+steps.map(function(s){
     return '<li><span class="d"></span><span class="s">'+s[0]+'</span><em></em></li>';}).join('')+
   '</ol><div class="out"></div>';

  var dz=c.querySelector('.dz');
  function load(text,name){
   var rows;
   try{rows=parseCSV(text);}catch(e){dz.querySelector('.fn').textContent='Could not read that file';return;}
   var miss=d.chan.filter(function(ch){return rows[0][ch.col]===undefined;});
   if(miss.length){dz.querySelector('.fn').textContent='Missing column '+miss[0].col;
    dz.querySelector('.mt').textContent='needs '+d.chan.map(function(x){return x.col;}).join(', ');return;}
   dz.classList.add('done');
   dz.querySelector('.fn').textContent=name;
   dz.querySelector('.mt').textContent=rows.length+' rows · '+Object.keys(rows[0]).length+' columns';
   render(c,d,rows);
  }
  ['dragenter','dragover'].forEach(function(e){dz.addEventListener(e,function(ev){
   ev.preventDefault();dz.classList.add('over');});});
  ['dragleave','drop'].forEach(function(e){dz.addEventListener(e,function(ev){
   ev.preventDefault();dz.classList.remove('over');});});
  dz.addEventListener('drop',function(ev){var fl=ev.dataTransfer.files&&ev.dataTransfer.files[0];
   if(!fl)return;var r=new FileReader();r.onload=function(){load(r.result,fl.name);};r.readAsText(fl);});
  function pick(){var inp=document.createElement('input');inp.type='file';inp.accept='.csv,text/csv';
   inp.onchange=function(){var fl=inp.files[0];if(!fl)return;var r=new FileReader();
    r.onload=function(){load(r.result,fl.name);};r.readAsText(fl);};inp.click();}
  dz.addEventListener('click',function(ev){
   if(dz.classList.contains('done'))return;
   if(ev.target.classList.contains('samp')){ev.preventDefault();
    /* samples are embedded, so this works offline and from disk */
    load(window.SAMPLES[k],d.file);return;}
   pick();});
  dz.addEventListener('keydown',function(ev){
   if((ev.key==='Enter'||ev.key===' ')&&!dz.classList.contains('done')){ev.preventDefault();pick();}});
  rack.appendChild(c);
 });
}
if(document.readyState!=='loading')build();else document.addEventListener('DOMContentLoaded',build);
})();
