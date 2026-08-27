/* Test configurations for the live demo.

   Each family maps to one product. Each system inside it runs the SAME process
   model from domains.js, with the plant parameters and the economics changed to
   match that kind of facility. Nothing here alters the maths. It changes the
   vessel the maths is pointed at, which is exactly what a real deployment does.

   `p` entries are merged over the domain's own parameters.
   `stock` and `price` seed the configure step; the tester can change both.
   `limit` overrides the safety threshold. */
(function(g){
'use strict';

g.FAMILIES=[
 {code:'OE/01', name:'Aquaculture and water', img:'ponds2',
  blurb:'Recirculating fish production, where the loop turns over several times an hour.',
  systems:[
   {id:'ras-salmon', name:'RAS salmon grow-out', sub:'120 m³ loop, 5,000 m³/h recirculation',
    domain:'aquaculture', stock:4820, price:9.40, limit:0.15,
    note:'The reference configuration. A commercial-scale grow-out loop.'},
   {id:'smolt', name:'Salmon smolt hall', sub:'116 m³ loop, younger fish, tighter tolerance',
    domain:'aquaculture', p:{V:116000,Q:4850,a_tan:0.0305}, stock:1980, price:6.10, limit:0.13,
    note:'Less water and a lower flow, so the same upset shows up faster and the window is tighter.'},
   {id:'trout', name:'Trout raceway', sub:'168 m³, higher flow, lower stocking density',
    domain:'aquaculture', p:{V:168000,Q:6400,resp:1.7}, stock:11400, price:7.80, limit:0.17,
    note:'More water to buffer the same failure, so the decline is gradual and the warning is long.'}
 ]},

 {code:'OE/02', name:'Controlled agriculture', img:'glasshouse',
  blurb:'Hydroponic and glasshouse production, where crop state is inferred, never measured.',
  systems:[
   {id:'nft-lettuce', name:'NFT lettuce', sub:'Recirculating film, 2,400 heads',
    domain:'hydroponics', stock:2400, price:2.15, limit:2.55,
    note:'The reference configuration. A recirculating nutrient film bench.'},
   {id:'dwc-greens', name:'Deep water culture', sub:'Leafy greens, slower uptake per plant',
    domain:'hydroponics', p:{umax:9.6,Km:1.35}, stock:6200, price:1.85, limit:2.60,
    note:'Slower uptake per unit of root, so the decline is shallower and harder to see coming.'},
   {id:'tomato', name:'Glasshouse tomato', sub:'Drip to drain, long crop cycle',
    domain:'hydroponics', p:{EC_in:2.35,umax:12.0,Km:1.3}, stock:1400, price:3.40, limit:2.50,
    unit:'plants', note:'Stronger feed and a longer cycle, so salinity creeps toward the line rather than spiking.'}
 ]},

 {code:'OE/03', name:'Bioprocessing', img:'reactors',
  blurb:'Fermentation and cell culture, where the assay is sparse and the yield call is made between measurements.',
  systems:[
   {id:'fedbatch', name:'Fed-batch microbial', sub:'2 m³ vessel, industrial titre',
    domain:'bioreactor', stock:1, price:184000, limit:1.00,
    note:'The reference configuration. A standard fed-batch production run.'},
   {id:'perfusion', name:'Continuous perfusion', sub:'500 L, leaner feed, higher oxygen transfer',
    domain:'bioreactor', p:{Sin:23.0,kLa:100,mu_max:0.21}, stock:1, price:96000, limit:0.90,
    note:'Continuous operation, so a productivity slide costs yield every hour it runs unseen.'},
   {id:'pilot', name:'Pilot fermenter', sub:'200 L, process development',
    domain:'bioreactor', p:{Sin:28.0,kLa:80,m_s:0.025}, stock:1, price:28000, limit:1.20,
    note:'Development scale. Cheaper to lose, and the run that decides whether the next one happens.'}
 ]},

 {code:'OE/04', name:'Space and life support', img:'cupola',
  blurb:'A sealed loop with no resupply and no exit. The same problem with the tolerances removed.',
  systems:[
   {id:'habitat-4', name:'Sealed habitat, four crew', sub:'Nominal scrubbing, surface analogue',
    domain:'blss', stock:1, price:640000, limit:5000,
    note:'The reference configuration. Four crew on a nominal scrubber duty cycle.'},
   {id:'habitat-6', name:'Sealed habitat, six crew', sub:'Same hardware, higher metabolic load',
    domain:'blss', p:{crew_co2:340,crew_o2:0.34,Pmax:466}, stock:1, price:880000, limit:4600,
    note:'The same scrubber carrying half again the load, so margin is thinner from hour zero.'},
   {id:'transit', name:'Transit vehicle', sub:'Two crew, smaller scrubber, no resupply window',
    domain:'blss', p:{crew_co2:250,crew_o2:0.25,Pmax:400,scrub_cap:220}, stock:1, price:1450000,
    limit:5400, note:'Small volume, small margin, and nothing on the other side of a failure.'}
 ]}
];

/* Plain-language names for the sensor channels, so the configure step reads like
   an equipment list rather than a schema. */
g.CHANNELS={
 TAN_mgL:'Ammonia probe', NO2N_mgL:'Nitrite probe', NO3N_mgL:'Nitrate probe', DO_mgL:'Dissolved oxygen',
 EC_mS_cm:'EC probe', rootzone_water_L:'Reservoir level',
 biomass_gL:'Biomass, offline', glucose_gL:'Glucose assay', titer_mgL:'Titre assay', DO_pct:'Dissolved oxygen',
 cabin_CO2_ppm:'Cabin CO2 sensor', cabin_O2_pct:'Cabin O2 sensor'
};
})(window);
