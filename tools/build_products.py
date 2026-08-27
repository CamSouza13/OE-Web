# Builds the four product pages from the same data the home page uses, on the
# same stylesheet. No generator, no template engine: one script, run once, the
# output is committed HTML like every other page on the site.
import io,json,re,html,os

os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
IDX=io.open('index.html',encoding='utf-8').read()
D={'P':json.loads(re.search(r'var P=(\[.*?\]);',IDX,re.S).group(1)),
   'R':json.loads(re.search(r'var R=(\[.*?\]);',IDX,re.S).group(1)),
   'steps':[(a,b,re.sub(r'\s+',' ',c).strip()) for a,b,c in
     re.findall(r'<div class="st"><i>(\d+)</i><h3>([^<]+)</h3>\s*<p>(.*?)</p>',IDX,re.S)]}
NAV=IDX[IDX.index('<header class="nav"'):IDX.index('</header>')+len('</header>')]
FOOT=IDX[IDX.index('<footer>'):IDX.index('</footer>')+len('</footer>')]
HEAD=IDX[IDX.index('<link rel="stylesheet" href="assets/fonts.css">'):IDX.index('</head>')]

# what the estimator actually recovers, from domains.js
PAYOFF={
 'OE/01':'Biofilter capacity is, and nothing on site measures it.',
 'OE/02':'Root feeding capacity is, and nothing on the bench measures it.',
 'OE/03':'Culture productivity is, and no gauge in the plant reports it.',
 'OE/04':'Scrubbing capacity is, and nothing in the cabin reports it.',
}
STATE={
 'OE/01':('Biofilter capacity','Ammonia is the reading you have. Biofilter capacity is what keeps ammonia down, and no instrument on a farm reports it. The engine carries the nitrogen loop, so it holds both at once and tells you which one moved first.'),
 'OE/02':('Root feeding capacity','EC tells you how strong the feed is, not whether the roots are taking it up. Uptake is the part that fails. The engine separates what you put into the tank from what the plants actually removed, so a fading bench shows up while the feed still looks correct.'),
 'OE/03':('Culture productivity and nitrifier activity','Every process gauge can sit in range while a culture quietly stops converting sugar, or while nitrifiers lose the oxygen demand race. Neither is a reading. Both are ratios between things you measure, and the engine tracks them continuously instead of waiting for the next assay.'),
 'OE/04':('Scrubbing capacity','Cabin carbon dioxide stays flat while the scrubber works harder to hold it there. The effort is invisible and only the result shows. The engine estimates the effort, so lost margin appears while there is still margin left to spend.'),
}
COVER={
 'OE/01':['Recirculating aquaculture (RAS)','Hatchery and smolt production','Biofiltration and nitrification','Shrimp and biofloc','Recirculating irrigation','Aquatic veterinary health','Live haul and depuration','Water reuse'],
 'OE/02':['Glasshouse horticulture','Vertical farming','Controlled environment agriculture','Hydroponics, NFT and deep water culture','Aeroponics','Nutrient dosing and recovery','Substrate and fertigation','Crop steering','Aquaponics, coupled loops'],
 'OE/03':['Precision fermentation','Cell culture and biologics','Algae and cyanobacteria','Enzyme and specialty chemicals','Cultivated meat','Activated sludge','Nitrification and denitrification','Anaerobic digestion','Membrane bioreactors','Industrial effluent','Scale-up and tech transfer'],
 'OE/04':['Bioregenerative life support (BLSS)','Environmental control and life support (ECLSS)','Habitat atmosphere management','Carbon dioxide scrubbing and revitalisation','Submarine and hyperbaric atmospheres','Analogue habitat operations'],
}
# the demo configurations, so a reader can go straight from the page to a run
SYSTEMS={
 'OE/01':[('RAS salmon grow-out','120 m³ loop, commercial scale'),('Salmon smolt hall','Younger fish, tighter tolerance'),('Trout raceway','Higher flow, lower density')],
 'OE/02':[('NFT lettuce','Recirculating film'),('Deep water culture','Leafy greens'),('Glasshouse tomato','Drip to drain, long cycle')],
 'OE/03':[('Fed-batch microbial','2 m³ production vessel'),('Continuous perfusion','500 L, leaner feed'),('Pilot fermenter','200 L, process development')],
 'OE/04':[('Sealed habitat, four crew','Nominal scrubbing'),('Sealed habitat, six crew','Higher metabolic load'),('Transit vehicle','Two crew, no resupply window')],
}
LEDE={
 'OE/01':'Fewer bad nights on a recirculating farm, from the probes already in the loop.',
 'OE/02':'A fading bench shows up while you can still feed it, not at harvest.',
 'OE/03':'Yield and treatment capacity tracked between assays, not after them.',
 'OE/04':'Margin to a life-critical bound, in a loop with nowhere to vent and no resupply.',
}
FILE={'OE/01':'current.html','OE/02':'canopy.html','OE/03':'culture.html','OE/04':'orbis.html'}

def esc(t): return html.escape(t,quote=False)

def page(p):
    pid=p['id']; others=[q for q in D['P'] if q['id']!=pid]
    hidden,why=STATE[pid]
    rows=[r for r in D['R'] if r[1]==pid]
    done=[r for r in rows if r[0]=='Complete']

    cover=''.join('<li>%s</li>'%esc(c) for c in COVER[pid])
    sysrows=''.join(
      '<div class="sy2"><b>%s</b><span>%s</span></div>'%(esc(a),esc(b)) for a,b in SYSTEMS[pid])
    steps=''.join(
      '<div class="st"><i>%s</i><h3>%s</h3>\n   <p>%s</p></div>\n  '%(a,esc(b),esc(c))
      for a,b,c in D['steps'])
    rec=''.join(
      '<tr><td><span class="st2 %s">%s</span></td><td>%s</td><td>%s</td></tr>'%(
        'ok' if r[0]=='Complete' else 'go', esc(r[0]), esc(r[2]), esc(r[3])) for r in rows)
    oth=''.join(
      '<a class="op" href="%s"><span class="cd">%s</span><b>%s</b><span class="mk">%s</span></a>'%(
        FILE[q['id']],q['id'],esc(q['name']),esc(q['market'])) for q in others)

    return """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>%(name)s &middot; %(market)s &middot; Orbital Ecology</title>
<meta name="description" content="%(lede)s">
%(head)s</head><body>
%(nav)s
<main>

<section class="wrap phd">
 <div class="grid">
  <div>
   <p class="lbl"><i></i>%(id)s &middot; %(market)s</p>
   <h1>%(name)s</h1>
   <p class="lede">%(lede)s</p>
   <div class="acts">
    <a class="btn lg" href="evaluation.html">Request an evaluation <span class="ar">&rarr;</span></a>
    <a class="btn lg lt" href="demo.html">Run it on a sample log <span class="ar">&rarr;</span></a>
   </div>
  </div>
  <figure class="fr rv zi" style="margin:0">
   <img src="assets/img/%(img)s.webp" alt="%(market)s" loading="lazy">
  </figure>
 </div>
</section>

<section class="wrap sec tight">
 <div class="hd2 rv">
  <p class="lbl">What it estimates</p>
  <h2 class="dbl"><b>The reading you have is not the thing that fails.</b> %(payoff)s</h2>
 </div>
 <p class="lede rv">%(why)s</p>
 <div class="prin rv">
  <div class="p"><i>01</i><h3>Runs on your instruments</h3>
   <p>No new hardware, no install, no change to how the plant is operated. If it needed you to
    add sensors, the model would not be doing its job.</p></div>
  <div class="p"><i>02</i><h3>Read only</h3>
   <p>It estimates and forecasts. It connects to no control loop and changes no set point, which
    is why evaluating it puts nothing at risk.</p></div>
  <div class="p"><i>03</i><h3>Every number carries a band</h3>
   <p>Each state comes with its uncertainty and each forecast with its probability. A number with
    no band is not a measurement.</p></div>
  <div class="p"><i>04</i><h3>Your data stays yours</h3>
   <p>Evaluation files are deleted afterwards, and nothing becomes anyone else's training set
    without an agreement that says so.</p></div>
 </div>
</section>

<section class="wrap sec">
 <div class="hd2 rv">
  <p class="lbl">Where it runs</p>
  <h2>%(market)s.</h2>
 </div>
 <p class="lede rv">%(body)s</p>
 <div class="two2">
  <div class="rv">
   <p class="slb2">Configurations you can run right now</p>
   <div class="syl">%(sysrows)s</div>
   <p class="fine2">Each of these is set up in the live demo. Pick the instruments you actually
    have, set what is on the line, and run it.</p>
  </div>
  <div class="rv">
   <p class="slb2">Fields this covers</p>
   <ul class="chips">%(cover)s</ul>
  </div>
 </div>
</section>

<section class="wrap sec tight">
 <div class="hd2 rv">
  <p class="lbl">The method</p>
  <h2>Three steps. Only the first one changes.</h2>
 </div>
 <div class="mth rv">
  %(steps)s</div>
 <p class="fine2 rv">Steps two and three are identical across every Orbital Ecology product. Step
  one is the process model written for this domain, and it is where the domain work lives.</p>
</section>

<section class="wrap sec" id="record">
 <div class="hd2 rv">
  <p class="lbl">The record</p>
  <h2>What has been tested here.</h2>
 </div>
 <table class="rec rv"><thead><tr><th>Status</th><th>What was tested</th><th>Result</th></tr></thead>
  <tbody>%(rec)s</tbody></table>
 <p class="fine2 rv">Every completed result is reproducible against a published benchmark or a
  held-out operating record. The full record for all four products is
  <a href="index.html#record">on the home page</a>.</p>
</section>

<section class="wrap sec tight">
 <div class="hd2 rv">
  <p class="lbl">The rest</p>
  <h2>One engine, four front doors.</h2>
 </div>
 <div class="oths rv">%(oth)s</div>
</section>

<section class="end">
 <div class="inr">
  <div class="cpy">
   <p class="lbl">Evaluation</p>
   <h2>Send one export. We will tell you what it was trying to say.</h2>
   <p>Send us an export you already keep. We run it blind, with the outcome window hidden from us,
    then tell you how many hours of warning you would have had, and how often we would have cried
    wolf.</p>
   <ul>
    <li>No connection to any live system. No change to any control loop.</li>
    <li>No fee, and the file is deleted afterwards.</li>
    <li>You keep the full workings, including where we would have missed.</li>
   </ul>
  </div>
  <div class="box rv zi">
   <div class="bgi"><img src="assets/img/%(img)s.webp" alt="" loading="lazy"></div>
   <div class="in2">
    <a class="btn lg" href="evaluation.html">Request an evaluation <span class="ar">&rarr;</span></a>
    <a class="btn lg lt" href="demo.html">Run the live demo first <span class="ar">&rarr;</span></a>
    <p class="fine">Validated against the reference models these fields use, and backtested on
     real commercial operating history. The engine only reads. It estimates and forecasts, and
     changes nothing in your plant.</p>
   </div>
  </div>
 </div>
</section>

</main>
%(foot)s
<script src="assets/oe.js"></script>
</body></html>
""" % dict(head=HEAD,nav=NAV,foot=FOOT,id=pid,name=esc(p['name']),market=esc(p['market']),
           img=p['img'],lede=esc(LEDE[pid]),hidden=esc(hidden),why=esc(why),
           body=esc(p['body']),payoff=esc(PAYOFF[pid]),sysrows=sysrows,cover=cover,steps=steps,rec=rec,oth=oth)

for p in D['P']:
    f=FILE[p['id']]
    io.open(f,'w',encoding='utf-8').write(page(p))
    print('wrote',f,len(page(p)),'bytes')
