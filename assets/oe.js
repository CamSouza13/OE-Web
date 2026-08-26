(function(){
'use strict';
var RM=window.matchMedia&&window.matchMedia('(prefers-reduced-motion:reduce)').matches;
var IO='IntersectionObserver' in window;

/* ---------------- reveal, staggered inside each section ---------------- */
(function(){
 var all=document.querySelectorAll('.rv');
 document.querySelectorAll('section').forEach(function(sec){
  var k=0;
  sec.querySelectorAll('.rv').forEach(function(e){e.style.setProperty('--d',Math.min(k++,4)*90+'ms');});
 });
 if(!IO||RM){all.forEach(function(e){e.classList.add('shown');});return;}
 var io=new IntersectionObserver(function(es){es.forEach(function(e){
  if(e.isIntersecting){e.target.classList.add('shown');io.unobserve(e.target);}});},
  {rootMargin:'0px 0px -10% 0px',threshold:.04});
 all.forEach(function(e){io.observe(e);});
 /* IO can be outrun by a fast flick to the bottom of the page, so sweep on
    scroll as well. Cheap, and it guarantees nothing is left invisible. */
 var pend=[].slice.call(all),tick=false;
 function sweep(){
  tick=false;
  pend=pend.filter(function(e){
   if(e.getBoundingClientRect().top<innerHeight*0.94){e.classList.add('shown');return false;}
   return true;});
  if(!pend.length)removeEventListener('scroll',onScroll);
 }
 function onScroll(){if(!tick){tick=true;requestAnimationFrame(sweep);}}
 addEventListener('scroll',onScroll,{passive:true});
 addEventListener('load',sweep);
 sweep();
 /* images that reveal on their own, not inside a .rv */
 document.querySelectorAll('.zi').forEach(function(e){
  if(!e.closest('.rv')){var o=new IntersectionObserver(function(es){
   if(es[0].isIntersecting){e.classList.add('shown');o.disconnect();}},{threshold:.1});o.observe(e);}
 });
})();

/* ---------------- nav ---------------- */
(function(){
 var nav=document.getElementById('nav');
 var vh=document.querySelector('.vhero');
 function onNav(){
  nav.classList.toggle('stuck',scrollY>14);
  if(vh){
   var edge=vh.getBoundingClientRect().bottom-nav.offsetHeight-8;
   nav.classList.toggle('over',edge>0);
  }
 }
 addEventListener('scroll',onNav,{passive:true});
 addEventListener('resize',onNav,{passive:true});
 onNav();
})();

/* ---------------- count up ---------------- */
(function(){
 var els=document.querySelectorAll('[data-c]');
 function run(el){
  var to=+el.dataset.c,sfx=el.dataset.suffix||'',t0=null,dur=1250;
  if(RM){el.textContent=to.toLocaleString()+sfx;return;}
  function tick(t){
   if(!t0)t0=t;
   var p=Math.min((t-t0)/dur,1),e=1-Math.pow(1-p,3);
   el.textContent=Math.round(to*e).toLocaleString()+sfx;
   if(p<1)requestAnimationFrame(tick);
  }
  requestAnimationFrame(tick);
 }
 if(!IO){els.forEach(run);return;}
 var io=new IntersectionObserver(function(es){es.forEach(function(e){
  if(e.isIntersecting){run(e.target);io.unobserve(e.target);}});},{threshold:.5});
 els.forEach(function(e){io.observe(e);});
})();


/* ---------------- parallax on the ink band ---------------- */
(function(){
 var sec=document.getElementById('arc'),bg=document.getElementById('parx');
 if(!sec||!bg||RM)return;
 var tick=false;
 function upd(){
  tick=false;
  var r=sec.getBoundingClientRect();
  if(r.bottom<0||r.top>innerHeight)return;
  var p=(r.top+r.height/2-innerHeight/2)/innerHeight;
  bg.style.transform='translate3d(0,'+(p*-5.5).toFixed(2)+'%,0)';
 }
 addEventListener('scroll',function(){if(!tick){tick=true;requestAnimationFrame(upd);}},{passive:true});
 upd();
})();
})();
