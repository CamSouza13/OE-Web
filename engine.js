/* Orbital Ecology estimation core, ported from the production Python engine.
   Unscented Kalman filter (Julier and Uhlmann; Wan and van der Merwe), RK4 over a
   domain process model, and a Monte-Carlo forecast of the safety limit.
   Same equations, same structure. This is the estimator, not a mock. */
(function(g){
'use strict';
function chol(A,n){var L=[],i,j,k,s;for(i=0;i<n;i++){L.push(new Float64Array(n));}
 for(i=0;i<n;i++)for(j=0;j<=i;j++){s=A[i][j];for(k=0;k<j;k++)s-=L[i][k]*L[j][k];
  if(i===j){L[i][j]=Math.sqrt(Math.max(s,1e-12));}else{L[i][j]=s/(L[j][j]||1e-12);}}
 return L;}
function inv(A,n){var M=[],I=[],i,j,k,p,t;
 for(i=0;i<n;i++){M.push(Array.prototype.slice.call(A[i]));I.push(new Float64Array(n));I[i][i]=1;}
 for(i=0;i<n;i++){p=i;for(k=i+1;k<n;k++)if(Math.abs(M[k][i])>Math.abs(M[p][i]))p=k;
  if(p!==i){t=M[i];M[i]=M[p];M[p]=t;t=I[i];I[i]=I[p];I[p]=t;}
  var d=M[i][i]||1e-12;for(j=0;j<n;j++){M[i][j]/=d;I[i][j]/=d;}
  for(k=0;k<n;k++){if(k===i)continue;var f=M[k][i];if(!f)continue;
   for(j=0;j<n;j++){M[k][j]-=f*M[i][j];I[k][j]-=f*I[i][j];}}}
 return I;}
var CTR={rk4:0,sig:0,fc:0,traj:0,upd:0};
function rk4(x,dt,dv,u,p,nn){CTR.rk4++;var n=x.length,k1=dv(x,u,p),a=new Float64Array(n),i;
 for(i=0;i<n;i++)a[i]=x[i]+dt/2*k1[i];var k2=dv(a,u,p);
 for(i=0;i<n;i++)a[i]=x[i]+dt/2*k2[i];var k3=dv(a,u,p);
 for(i=0;i<n;i++)a[i]=x[i]+dt*k3[i];var k4=dv(a,u,p);
 var o=new Float64Array(n);
 for(i=0;i<n;i++){o[i]=x[i]+dt/6*(k1[i]+2*k2[i]+2*k3[i]+k4[i]);
  if(nn&&nn[i]&&o[i]<0)o[i]=0;}
 return o;}
function step(x,dt,dv,u,p,nn,maxh){var s=Math.max(1,Math.ceil(dt/(maxh||dt))),h=dt/s,i;
 for(i=0;i<s;i++)x=rk4(x,h,dv,u,p,nn);return x;}

function UKF(n,Q,alpha,beta){
 this.n=n;this.Q=Q;this.a=alpha||1e-3;this.b=beta===undefined?2:beta;
 var kap=3-n;this.lam=this.a*this.a*(n+kap)-n;this.c=n+this.lam;
 var m=2*n+1,i;this.Wm=new Float64Array(m);this.Wc=new Float64Array(m);
 for(i=0;i<m;i++){this.Wm[i]=1/(2*this.c);this.Wc[i]=1/(2*this.c);}
 this.Wm[0]=this.lam/this.c;this.Wc[0]=this.lam/this.c+(1-this.a*this.a+this.b);
 this.x=new Float64Array(n);this.P=[];for(i=0;i<n;i++){this.P.push(new Float64Array(n));this.P[i][i]=1;}
 this.nis=0;}
UKF.prototype.sigma=function(){var n=this.n,i,j,S=[],pts=[];
 for(i=0;i<n;i++){S.push(new Float64Array(n));for(j=0;j<n;j++)S[i][j]=this.c*0.5*(this.P[i][j]+this.P[j][i])+(i===j?1e-12:0);}
 var L=chol(S,n);pts.push(Float64Array.from(this.x));
 for(i=0;i<n;i++){var a=new Float64Array(n),b=new Float64Array(n);
  for(j=0;j<n;j++){a[j]=this.x[j]+L[j][i];b[j]=this.x[j]-L[j][i];}pts.push(a);pts.push(b);}
 return pts;};
UKF.prototype.predict=function(dt,fx){var n=this.n,pts=this.sigma(),i,j,k;CTR.sig+=pts.length;
 this.sf=pts.map(function(p){return fx(p,dt);});
 var m=new Float64Array(n);
 for(k=0;k<this.sf.length;k++)for(i=0;i<n;i++)m[i]+=this.Wm[k]*this.sf[k][i];
 this.x=m;var P=[];for(i=0;i<n;i++)P.push(new Float64Array(n));
 for(k=0;k<this.sf.length;k++){var d=new Float64Array(n);
  for(i=0;i<n;i++)d[i]=this.sf[k][i]-m[i];
  for(i=0;i<n;i++)for(j=0;j<n;j++)P[i][j]+=this.Wc[k]*d[i]*d[j];}
 for(i=0;i<n;i++)for(j=0;j<n;j++)P[i][j]+=this.Q[i][j];
 this.P=P;};
UKF.prototype.update=function(z,idx,R,robust){var n=this.n,m=idx.length,i,j,k;
 if(!m){this.nis=0;return;}
 CTR.upd++;
 var H=this.sf.map(function(p){var o=new Float64Array(m);for(var q=0;q<m;q++)o[q]=p[idx[q]];return o;});
 var zp=new Float64Array(m);
 for(k=0;k<H.length;k++)for(i=0;i<m;i++)zp[i]+=this.Wm[k]*H[k][i];
 var S=[];for(i=0;i<m;i++)S.push(new Float64Array(m));
 var Pxz=[];for(i=0;i<n;i++)Pxz.push(new Float64Array(m));
 for(k=0;k<H.length;k++){var dz=new Float64Array(m),dx=new Float64Array(n);
  for(i=0;i<m;i++)dz[i]=H[k][i]-zp[i];
  for(i=0;i<n;i++)dx[i]=this.sf[k][i]-this.x[i];
  for(i=0;i<m;i++)for(j=0;j<m;j++)S[i][j]+=this.Wc[k]*dz[i]*dz[j];
  for(i=0;i<n;i++)for(j=0;j<m;j++)Pxz[i][j]+=this.Wc[k]*dx[i]*dz[j];}
 for(i=0;i<m;i++)S[i][i]+=R[i];
 var Si=inv(S,m),nu=new Float64Array(m),d2=0;
 for(i=0;i<m;i++)nu[i]=z[i]-zp[i];
 for(i=0;i<m;i++)for(j=0;j<m;j++)d2+=nu[i]*Si[i][j]*nu[j];
 this.nis=d2/m;
 /* innovation-based adaptive estimation: downweight a reading the model cannot
    explain instead of treating it as strong evidence */
 if(robust&&d2>9){var f=Math.min(d2/9,200);for(i=0;i<m;i++)S[i][i]+=R[i]*(f-1);Si=inv(S,m);}
 var K=[];for(i=0;i<n;i++){K.push(new Float64Array(m));
  for(j=0;j<m;j++){var s=0;for(k=0;k<m;k++)s+=Pxz[i][k]*Si[k][j];K[i][j]=s;}}
 for(i=0;i<n;i++){var acc=0;for(j=0;j<m;j++)acc+=K[i][j]*nu[j];this.x[i]+=acc;}
 var P=this.P;
 for(i=0;i<n;i++)for(j=0;j<n;j++){var s2=0;
  for(k=0;k<m;k++)for(var q=0;q<m;q++)s2+=K[i][k]*S[k][q]*K[j][q];
  P[i][j]-=s2;}};

function gauss(rng){var u=0,v=0;while(!u)u=rng();while(!v)v=rng();
 return Math.sqrt(-2*Math.log(u))*Math.cos(2*Math.PI*v);}
function mulberry(a){return function(){a|=0;a=a+0x6D2B79F5|0;var t=Math.imul(a^a>>>15,1|a);
 t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296;};}

/* Monte-Carlo forecast: propagate the posterior forward, return breach probability
   and the ensemble of crossing times. */
function forecast(x,P,dv,u,p,nn,safety,horizon,dtF,N,seed,maxh){
 CTR.fc++;CTR.traj+=N;
 var rng=mulberry(seed||1),n=x.length,i,j,k,hit=0,times=[];
 var sd=[];for(i=0;i<n;i++)sd.push(Math.sqrt(Math.max(P[i][i],0)));
 var steps=Math.round(horizon/dtF);
 for(k=0;k<N;k++){
  var s=new Float64Array(n);
  for(i=0;i<n;i++){s[i]=x[i]+sd[i]*gauss(rng);if(nn&&nn[i]&&s[i]<0)s[i]=0;}
  var crossed=false;
  for(j=1;j<=steps;j++){s=step(s,dtF,dv,u,p,nn,maxh);
   var v=s[safety.idx];
   if(safety.dir==='>'?v>safety.limit:v<safety.limit){crossed=true;times.push(j*dtF);break;}}
  if(crossed)hit++;}
 times.sort(function(a,b){return a-b;});
 return{p:hit/N,tcross:times.length?times[Math.floor(times.length/2)]:null,n:N};}

g.OE={rk4:rk4,step:step,UKF:UKF,forecast:forecast,inv:inv,ctr:CTR,
 reset:function(){CTR.rk4=0;CTR.sig=0;CTR.fc=0;CTR.traj=0;CTR.upd=0;}};
})(window);
