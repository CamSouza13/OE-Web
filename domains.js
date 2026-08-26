/* Domain process models, ported line for line from the production engine.
   Each declares its states, parameters, the CSV columns an operator already
   collects, the safety limit, and the economic assumptions used in the
   modelled-impact panel. Assumptions are shown on the page and are editable. */
(function(g){
'use strict';
var D={};

D.aquaculture={
 key:'aquaculture',
 model:'nitrogen loop', why:'Ammonia is the reading. Biofilter capacity is what keeps ammonia down, and no instrument on a farm reports it. Because the engine carries the nitrogen loop, it can hold both at once and tell you which one moved first.', code:'CURRENT', title:'Aquaculture', sub:'Recirculating salmon, RAS',
 file:'aquaculture_ras_salmon.csv', dt:1, unit:'h', maxh:0.25, fcN:70, fcEv:64,
 states:['TAN','NO2','NO3','DO','eff'], gaugeLabel:'Total ammonia nitrogen',gaugeUnits:'mg/L',silent:'Ammonia looks fine for days. The water turns over fast enough to hide the problem.',
 hidden:4, hiddenName:'Biofilter capacity',
 nonneg:[1,1,1,0,1],
 x0:[0.05,0.005,28,9.9,1.0], P0:[0.004,4e-4,9,0.4,0.05],
 proc:[0.010,0.004,0.5,0.25,0.020],
 chan:[{s:0,col:'TAN_mgL',r:0.012},{s:1,col:'NO2N_mgL',r:0.004},
       {s:2,col:'NO3N_mgL',r:0.6},{s:3,col:'DO_mgL',r:0.09}],
 u:function(r){return [parseFloat(r.feed_kg_h)||0.108,1.0];},
 safety:{idx:0,limit:0.15,dir:'>',label:'Total ammonia nitrogen',units:'mg/L'},
 p:{V:120000,Q:5000,k1:4.2,K1:0.30,k2:6.0,K2:0.08,DO_sat:11.4,kLa:3.4,resp:1.5,
    o2_per_tan:3.43,o2_per_no2:1.14,TAN_in:0,NO2_in:0,NO3_in:2.0,a_tan:0.030},
 deriv:function(x,u,p){var T=Math.max(x[0],0),N2=Math.max(x[1],0),N3=Math.max(x[2],0),
   DO=x[3],e=Math.min(Math.max(x[4],0),1.5),exc=u[0],qm=u[1];
  var pt=exc*p.a_tan*1e6/p.V, r1=e*p.k1*T/(p.K1+T), r2=e*p.k2*N2/(p.K2+N2), dl=p.Q*qm/p.V;
  return Float64Array.from([pt-r1-dl*(T-p.TAN_in), r1-r2-dl*(N2-p.NO2_in), r2-dl*(N3-p.NO3_in),
   p.kLa*(p.DO_sat-DO)-p.resp-(p.o2_per_tan*r1+p.o2_per_no2*r2), 0]);},
 steps:['Read the log this farm already keeps.',
        'Learn what normal looks like on this site.',
        'Track how much work the biofilter can still do.',
        'Flag the drop, and price what it puts at risk.'],
 econ:{stockCol:'biomass_kg', price:9.40, lossFrac:0.18, insDeduct:25000, insLoadPct:11,
       labourHr:95, unit:'kg salmon', priceLabel:'USD per kg live weight',
       lossLabel:'stock lost in an unmanaged ammonia event'}
};

D.hydroponics={
 key:'hydroponics',
 model:'root-zone balance', why:'EC tells you how strong the feed is, not whether the roots are taking it up. Uptake is the part that fails. The engine separates what you put into the tank from what the plants actually removed, so a fading bench shows up while the feed still looks correct.', code:'AQUIFER', title:'Hydroponic farming', sub:'NFT lettuce, recirculating',
 file:'hydroponics_nft_lettuce.csv', dt:0.25, unit:'d', maxh:0.02, fcN:60, fcEv:56,
 states:['EC','W','act'], gaugeLabel:'Root-zone EC',gaugeUnits:'mS/cm',silent:'Feed strength stays in its normal band while the roots quietly stop feeding.',
 hidden:2, hiddenName:'Root feeding capacity',
 nonneg:[1,1,1],
 x0:[1.95,3.9,1.0], P0:[0.02,0.05,0.05], proc:[0.02,0.02,0.02],
 chan:[{s:0,col:'EC_mS_cm',r:0.03},{s:1,col:'rootzone_water_L',r:0.02}],
 u:function(r){return [parseFloat(r.irrigation_L_day)||9.0,2.4];},
 safety:{idx:0,limit:2.55,dir:'>',label:'Root-zone EC',units:'mS/cm'},
 p:{EC_in:2.2,k_drain:7.0,Wfc:3.0,umax:11.0,Km:1.2,buffer:0.0},
 deriv:function(x,u,p){var EC=Math.max(x[0],0),W=Math.max(x[1],0.3),a=Math.min(Math.max(x[2],0),1.5),
   irr=u[0],ET=u[1];
  var dr=p.k_drain*Math.max(W-p.Wfc,0), dW=irr-dr-ET, up=a*p.umax*EC/(p.Km+EC);
  var dS=irr*p.EC_in-dr*EC-up;
  return Float64Array.from([(dS-EC*dW)/Math.max(W,0.3)/(1+p.buffer), dW, 0]);},
 steps:['Read the irrigation log this room already keeps.',
        'Learn what a healthy bench looks like here.',
        'Track how well the roots are still feeding.',
        'Flag the drop, and price the crop at risk.'],
 econ:{stockCol:null, fixedStock:2400, price:2.15, lossFrac:0.22, insDeduct:8000, insLoadPct:9,
       labourHr:52, unit:'heads', priceLabel:'USD per head at market',
       lossLabel:'crop lost to a root-zone salinity event'}
};

D.bioreactor={
 key:'bioreactor',
 model:'growth model', why:'Every process gauge can sit in range while the culture quietly stops converting sugar. Productivity is not a reading, it is a ratio between things you measure. The engine tracks it continuously instead of waiting for the end-of-batch assay.', code:'CULTURE', title:'Bioreactors', sub:'Continuous microbial culture',
 file:'bioreactor_fedbatch.csv', dt:1, unit:'h', maxh:0.008, fcN:26, fcEv:28,
 states:['X','S','P','DO','eff'], gaugeLabel:'Residual substrate',gaugeUnits:'g/L',silent:'Every process gauge reads normal for days. Sugar left in the tank is the last thing to move.',
 hidden:4, hiddenName:'Culture productivity',
 nonneg:[1,1,1,1,1],
 x0:[11.5,0.26,1.5,7.4,1.0], P0:[0.15,0.02,0.3,0.1,0.05],
 proc:[0.05,0.05,0.25,0.10,0.010],
 chan:[{s:0,col:'biomass_gL',r:0.06},{s:1,col:'glucose_gL',r:0.18},
       {s:2,col:'titer_mgL',r:1.4},{s:3,col:'DO_pct',r:0.06,xf:function(v){return v*7.5/100;}}],
 u:function(){return [0.075];},
 safety:{idx:1,limit:1.00,dir:'>',label:'Residual substrate',units:'g/L'},
 p:{mu_max:0.22,Ks:0.5,Kdo:0.2,Yxs:0.46,qO2:7.5,m_s:0.02,m_o:0.10,alpha:0.15,
    beta:0.008,kLa:90.0,DO_sat:7.5,Sin:26.0},
 deriv:function(x,u,p){var X=Math.max(x[0],0),S=Math.max(x[1],0),P=Math.max(x[2],0),
   DO=Math.max(x[3],0),e=Math.min(Math.max(x[4],0),1.5),Dl=u[0];
  var mu=e*p.mu_max*S/(p.Ks+S)*DO/(p.Kdo+DO), our=p.qO2*(mu/p.mu_max+p.m_o)*X;
  return Float64Array.from([(mu-Dl)*X, Dl*(p.Sin-S)-(mu/p.Yxs+p.m_s)*X,
   (p.alpha*mu+p.beta)*X-Dl*P, p.kLa*(p.DO_sat-DO)-our, 0]);},
 steps:['Read the batch record you already have.',
        'Learn how this vessel behaves when it runs well.',
        'Track how productive the culture actually is.',
        'Flag the drop, and price the run at risk.'],
 econ:{stockCol:null, fixedStock:1, price:180000, lossFrac:1.0, insDeduct:50000, insLoadPct:14,
       labourHr:140, unit:'batch', priceLabel:'USD per batch at release',
       lossLabel:'of batch value lost when a run is scrapped'}
};

D.blss={
 key:'blss',
 model:'gas balance', why:'Cabin carbon dioxide stays flat while the scrubber works harder to hold it there. The effort is invisible and only the result shows. The engine estimates the effort, so lost margin appears while there is still margin left to spend.', code:'ORBIS', title:'Closed life support', sub:'Sealed habitat, four crew',
 file:'blss_habitat.csv', dt:1, unit:'h', maxh:0.25, fcN:70, fcEv:64,
 states:['CO2','O2','act'], gaugeLabel:'Cabin carbon dioxide',gaugeUnits:'ppm',silent:'Cabin air stays inside limits while half the scrubbing capacity is already gone.',
 hidden:2, hiddenName:'Scrubbing capacity',
 nonneg:[1,0,1],
 x0:[850,20.5,1.0], P0:[2500,0.25,0.05], proc:[20,0.05,0.020],
 chan:[{s:0,col:'cabin_CO2_ppm',r:22},{s:1,col:'cabin_O2_pct',r:0.02}],
 u:function(){return [1.0,0.0];},
 safety:{idx:0,limit:5000,dir:'>',label:'Cabin carbon dioxide',units:'ppm'},
 p:{crew_co2:300,crew_o2:0.30,Pmax:466,Kco2:500,k_o2:0.001,leak:0.02,
    CO2_amb:400,O2_amb:20.9,scrub_cap:260,o2_cap:0.28,gravity:1.0},
 deriv:function(x,u,p){var C=Math.max(x[0],0),O=x[1],a=Math.max(x[2],0),L=u[0],bk=u[1];
  var ph=a*p.Pmax*L*C/(p.Kco2+C), mix=p.leak*p.gravity;
  return Float64Array.from([p.crew_co2-ph+mix*(p.CO2_amb-C)-bk*p.scrub_cap,
   -p.crew_o2+p.k_o2*ph+mix*(p.O2_amb-O)+bk*p.o2_cap, 0]);},
 steps:['Read the habitat log.',
        'Learn how this cabin behaves when all is well.',
        'Track how much scrubbing capacity is left.',
        'Flag the drop, and price the intervention window.'],
 econ:{stockCol:null, fixedStock:1, price:640000, lossFrac:0.35, insDeduct:0, insLoadPct:0,
       labourHr:0, unit:'contingency', priceLabel:'USD modelled cost of an unplanned resupply',
       lossLabel:'of contingency cost avoided by acting inside the window'}
};

g.DOMAINS=D;
})(window);
