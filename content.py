# -*- coding: utf-8 -*-
"""Orbital Ecology, content model.

Ground truth is terralaboratories.com. Every claim below traces to the Terra
validation record. The rename changes the name and the product architecture.
It does not change what has been proven.

Maturity discipline, unchanged:
  - Simulation-validated and backtested. No live deployment, none implied.
  - The engine estimates and forecasts. It is read-only. Control is roadmap.
  - Every number resolves to a source in SOURCES.
"""

BRAND   = "Orbital Ecology"
MARKQ   = "Building worlds that live."
THESIS  = "Make complex living systems reliable enough to become infrastructure."
DOMAIN  = "orbitalecology.com"
CAL     = "https://calendar.app.google/F8VHXD7MMtXNDtKy9"
MEDIUM  = "https://medium.com/@orbitalecology"
# Paste a Formspree form id here (the bit after /f/) to post the evaluation
# form to your inbox. Left empty, the form composes a pre-filled email
# instead, so it works either way on a static host.
FORM_ID = ""
MAIL    = "cameron@orbitalecology.com"
ADDRESS = "749 York Court, San Diego, CA 92109"

# ---------------------------------------------------------------- products
# slug, name, market, image, status, promise, estimates, evidence, fields, benchmark
PRODUCTS = [
 ("current","CURRENT","Aquaculture","raceways","Backtested",
  "Stable water systems, lower biological risk, and more efficient operations.",
  "Biofilter capacity, the oxygen budget, and the position of the nitrogen cycle, on a recirculating "
  "farm where the whole loop turns over several times an hour.",
  "6.5 hours of usable lead reproduced on held-out commercial operating history.",
  "Recirculating aquaculture (RAS) · Hatchery and smolt production · Biofiltration and nitrification · "
  "Shrimp and biofloc · Aquatic veterinary health · Live haul and depuration",
  "OE/01"),

 ("canopy","CANOPY","Controlled agriculture","cea","Validation open",
  "More predictable crop environments with less manual intervention.",
  "The physiological state of a crop, inferred from the environment it actually experienced rather "
  "than from the set points it was supposed to receive.",
  "Retrospective test in design with operators. Result published on completion of the run.",
  "Glasshouse horticulture · Vertical farming · Controlled environment agriculture · Substrate and "
  "fertigation · Crop steering · Plant phenotyping · Integrated pest management",
  "OE/02"),

 ("aquifer","AQUIFER","Hydroponics and water","growhouse","Validation open",
  "Precise control of recirculating water and nutrient infrastructure.",
  "The chemistry and microbial activity of a recirculating nutrient loop, and the root zone state "
  "that every block on that loop shares.",
  "Runs the estimator validated in OE/01 and OE/04 against nutrient-loop chemistry. Benchmark "
  "scoping with operators.",
  "Hydroponics · Deep water culture and NFT · Aeroponics · Nutrient dosing and recovery · "
  "Recirculating irrigation · Aquaponics, coupled fish and crop loops",
  "OE/03"),

 ("reclaim","RECLAIM","Bioremediation","clarifiers","Validated",
  "Turn biological treatment into a measurable, controllable process.",
  "Nitrifier activity and the oxygen demand running ahead of the blower response, in the reactors "
  "that carry the treatment load.",
  "IWA BSM1 benchmark. Dissolved oxygen prediction error cut by 92 percent. ADM1 one-step error "
  "reduced from 163.7 to 0.77.",
  "Activated sludge · Nitrification and denitrification · Membrane bioreactors · Anaerobic digestion "
  "· Constructed wetlands · Industrial effluent · Water reuse · Contaminant degradation",
  "OE/04"),

 ("culture","CULTURE","Bioprocessing","bioprocess","Validated",
  "Coordinate biological production with equipment and environmental state.",
  "Metabolic flux and the trajectory toward final yield, reconstructed between sparse and expensive "
  "assays.",
  "E. coli dynamic flux balance. One-step RMSE reduced from 0.062 to 0.011, a reduction of 82 percent.",
  "Precision fermentation · Cell culture and biologics · Algae and cyanobacteria · Enzyme and "
  "specialty chemicals · Cultivated meat · Scale-up and tech transfer",
  "OE/05"),

 ("orbis","ORBIS","Space and life support","life-support","Validated",
  "Life-support coordination under severe reliability constraints.",
  "Partial pressures and the hours of margin to a life-critical bound, in a loop with no resupply "
  "and no exit.",
  "SIMOC, 60 runs across 7 configurations including Biosphere 2 mission parameters. 98 percent of "
  "breaches identified before they occurred.",
  "Bioregenerative life support (BLSS) · Environmental control and life support (ECLSS) · Habitat "
  "atmosphere management · Carbon dioxide scrubbing and revitalisation · Submarine and hyperbaric "
  "atmospheres · Analogue habitats",
  "OE/06"),

 ("field","FIELD","Open environments","delta","Roadmap",
  "Extend system intelligence beyond fully controlled facilities.",
  "System state where the boundary is not sealed and the forcing is weather, which is the same "
  "inverse problem with a larger uncertainty budget.",
  "No validation record yet. Listed because the method extends here, not because it has been tested "
  "here.",
  "Restoration ecology · Watershed and estuary monitoring · Soil and land management · Open-water "
  "aquaculture · Carbon and nutrient accounting",
  "OE/07"),

 ("nexus","NEXUS","Platform layer","diffgrid","Core",
  "The shared engine, data model and simulation layer beneath every product.",
  "Device integration, normalised telemetry, mechanistic process models, Bayesian state estimation, "
  "forward simulation and fleet intelligence. The customer buys CURRENT or CANOPY. NEXUS is what "
  "compounds underneath.",
  "Steps two and three of the method are identical across every product above. Only the process "
  "model changes. That is the whole argument for one company rather than seven.",
  "Model library · Estimation core · Simulation and digital twin · Integrations and APIs · Fleet "
  "intelligence · Benchmark harness",
  "Shared"),
]

PROD = {p[0]: p for p in PRODUCTS}

# ---------------------------------------------------------------- method
METHOD = [
 ("01","Write the biology down",
  "A mechanistic model of the system: reaction kinetics, transport, uptake, population dynamics. "
  "This is the only step that changes between an oyster hatchery and a habitat, and it is where the "
  "domain work lives."),
 ("02","Solve backwards",
  "Bayesian state estimation runs that model against the sensors already installed and recovers the "
  "state variables no instrument reports, with an uncertainty band, every cycle."),
 ("03","Integrate forward",
  "Push the recovered state ahead in time under the planned operating strategy. The warning hours "
  "come from here. The output is a forecast with a stated confidence, not an alarm."),
]

# ---------------------------------------------------------------- stats
STATS = [
 ("$1.2M","of stock lost in a single night at a land-based farm after circulation pumps stopped and "
  "oxygen fell in two tanks.","Proximar Seafood, June 2025","S1"),
 ("$5M","of stock lost when one carbon dioxide filter failed structurally, about a fifth of the site.",
  "Sustainable Blue, November 2023","S2"),
 ("50-90%","of plant electricity spent on aeration in conventional activated sludge, set "
  "conservatively because nobody measures nitrifier state.","Drewnowski et al., 2019","S3"),
]

# ---------------------------------------------------------------- record
RECORD = [
 ("Complete","OE/01","Commercial farm history","Held-out backtest on real land-based operating data",
  "6.5 h of usable lead reproduced ahead of the event."),
 ("In progress","OE/01","Independent laboratory",
  "Biofilter-health estimates checked against laboratory assay at a third-party research facility",
  "Independent measurement validation. In progress."),
 ("In design","OE/02","Retrospective test protocol","Controlled environment agriculture",
  "Protocol in design with operators. Result published on completion of the run."),
 ("In design","OE/03","Coupled-loop test protocol","Hydroponic nutrient loops and aquaponics",
  "Scoping with operators. Runs the coupled form of the OE/01 and OE/02 estimators."),
 ("Complete","OE/04","IWA BSM1","Standard activated sludge benchmark, dissolved oxygen channel",
  "Prediction error reduced 92%. Excursions identified more than 12 h ahead."),
 ("Complete","OE/04","IWA ADM1","Reference anaerobic digestion model, one-step prediction",
  "Error 163.7 to 0.77."),
 ("Complete","OE/05","Dynamic flux balance, E. coli","One-step RMSE across complete runs",
  "RMSE 0.062 to 0.011, a reduction of 82%."),
 ("Complete","OE/06","SIMOC habitat simulator","60 runs, 7 configurations, Biosphere 2 and Mars models",
  "98% of breaches identified pre-event. Median lead 11 h, mean 34, max 168. R squared 0.87 on hidden "
  "state. False alarm 11%."),
 ("Scheduled","Commercial","First paid pilots","Terms and domains set per operator",
  "Scheduled for the first half of 2027."),
]

BENCH = [
 ("IWA BSM1","Benchmark Simulation Model No. 1","The international standard model for activated sludge treatment."),
 ("IWA ADM1","Anaerobic Digestion Model No. 1","The reference model for anaerobic digestion processes."),
 ("Dynamic FBA","Dynamic flux balance analysis","Standard method for modelling microbial metabolism over time."),
 ("SIMOC","Scalable, Interactive Model of an Off-world Community","Agent-based closed life support simulator from Arizona State University, including Biosphere 2 mission configurations."),
 ("Independent laboratory","Third-party measurement validation","Biofilter-health estimates checked against laboratory assay at an established recirculating aquaculture research facility."),
]

# ---------------------------------------------------------------- questions
QUESTIONS = [
 ("How does this differ from anomaly detection?",
  "Anomaly detection learns a picture of normal operation and flags departures from it, which tells an "
  "operator that something looks unusual at this moment. Orbital Ecology estimates the physical state "
  "of the process and simulates that state forward, which is where the time horizon comes from. The "
  "two methods also have different data requirements. Anomaly detection needs a long history of "
  "labelled failures. State estimation needs a model of the process, which the field already has."),
 ("How does this differ from a climate computer or a SCADA layer?",
  "A controller holds set points and alarms on deviation. Deviation is a consequence, so an alarm is a "
  "gauge with a line drawn on it. Orbital Ecology sits between the sensor and the controller: it turns "
  "measurements into a state, and a state into a forecast. In time that forecast is what a controller "
  "should be acting on. Today the engine is read-only and touches nothing."),
 ("How much of the validation is simulation?",
  "Most of it, and each figure is labelled with its source. The simulators are the reference models "
  "the relevant fields already use to evaluate control strategies: BSM1 for activated sludge, ADM1 for "
  "anaerobic digestion, dynamic flux balance for metabolism, and SIMOC for closed life support, which "
  "includes Biosphere 2 mission configurations. The aquaculture result is different in kind: it is a "
  "held-out backtest on real commercial operating history. The remaining work is commercial rather "
  "than scientific."),
 ("Why seven product names instead of one?",
  "Because an aquaculture operator should be able to buy an aquaculture product rather than a space "
  "product. The markets are genuinely different: different buyers, different regulation, different "
  "sales cycles. What is shared is the engine underneath, and that is the part that compounds. One "
  "estimator, seven front doors."),
 ("What is defensible about this in eighteen months?",
  "The dataset. Real failure trajectories are not available for purchase and accumulate only where an "
  "instrument is already deployed, so the advantage compounds with each operator. Beneath that, "
  "mechanistic process modelling is an uncommon skill set. And once a control room runs a night shift "
  "against a forecast, that forecast becomes part of the operating procedure rather than a tool "
  "sitting beside it."),
 ("What does an evaluation actually involve?",
  "An operator sends a historical export. We run it blind with the outcome window withheld, then "
  "report the hours of warning the engine would have given and how often it would have been wrong on "
  "that same history. There is no connection to any live system, no change to any control loop, and "
  "no fee. The file is deleted afterwards."),
]

# ---------------------------------------------------------------- sources
SOURCES = [
 ("S1","Proximar Seafood mortality incident, June 2025",
  "170,000 salmon lost overnight at a land-based farm in Japan after circulation pumps stopped and "
  "oxygen fell in two tanks. Reported loss NOK 12 million, about USD 1.16 million.",
  "The Fish Site / SalmonBusiness, June 2025",
  "https://thefishsite.com/articles/major-mortality-incident-at-salmon-ras"),
 ("S2","Sustainable Blue mortality incident, November 2023",
  "100,000 Atlantic salmon lost at a land-based farm in Nova Scotia after a carbon dioxide filter "
  "failed structurally. Reported loss USD 5 million, about 20 percent of stock on site.",
  "WeAreAquaculture / CBC News, November 2023",
  "https://weareaquaculture.com/news/aquaculture/100000-salmon-mortalities-at-canadas-land-based-sustainable-blue"),
 ("S3","Aeration share of wastewater treatment plant energy",
  "Aeration accounts for 25 to 60 percent of energy use across wastewater treatment plants generally, "
  "and 50 to 90 percent of plant electricity in conventional activated sludge systems specifically.",
  "University of Michigan Center for Sustainable Systems, US Wastewater Treatment Factsheet; "
  "Drewnowski et al., Processes 7(5):311, 2019",
  "https://css.umich.edu/publications/factsheets/water/us-wastewater-treatment-factsheet"),
 ("S4","IWA Benchmark Simulation Model No. 1 (BSM1)",
  "The international reference model for benchmarking control strategies on activated sludge plants.",
  "Alex, Benedetti, Copp, Gernaey, Jeppsson, Nopens, Pons, Steyer and Vanrolleghem. IWA Task Group on "
  "Benchmarking of Control Strategies for WWTPs",
  "https://iwa-mia.org/wp-content/uploads/2019/04/BSM_TG_Tech_Report_no_1_BSM1_General_Description.pdf"),
 ("S5","IWA Anaerobic Digestion Model No. 1 (ADM1)",
  "The reference structured model for anaerobic digestion processes.",
  "Batstone, Keller, Angelidaki, Kalyuzhnyi, Pavlostathis, Rozzi, Sanders, Siegrist and Vavilin. "
  "Water Science and Technology 45(10):65-73, 2002",
  "https://iwaponline.com/wst/article/45/10/65/6034/The-IWA-Anaerobic-Digestion-Model-No-1-ADM1"),
 ("S6","Dynamic flux balance analysis",
  "The standard method for modelling microbial metabolism through time, introduced on diauxic growth "
  "in E. coli.",
  "Mahadevan, Edwards and Doyle. Biophysical Journal 83(3):1331-1340, 2002",
  "https://www.cell.com/biophysj/fulltext/S0006-3495(02)73903-9"),
 ("S7","SIMOC, Scalable Interactive Model of an Off-world Community",
  "An agent-based simulator of closed life support systems, developed at Arizona State University's "
  "School of Earth and Space Exploration and hosted by the National Geographic Society. "
  "Configurations include Biosphere 2 mission parameters.",
  "Arizona State University Interplanetary Initiative",
  "https://simoc.space/"),
 ("S8","Orbital Ecology internal benchmark record",
  "Every figure on this site resolves to the validation record, where run counts, configurations, "
  "error reductions, lead times and false alarm rates are stated in full. Simulation results are "
  "labelled as simulation. All results to date are benchmark validation and retrospective "
  "backtesting. Live process results are published to the same record as operator evaluations "
  "complete.",
  "Orbital Ecology, benchmarks OE/01 and OE/04 through OE/06",
  ""),
]

# ---------------------------------------------------------------- team
TEAM = [
 ("Chief Executive Officer","Cameron Souza",
  "Modelling, biogeochemistry and aquaculture. Owns the engine and the science, and wrote the domain "
  "models behind each product.",
  "Land-based aquaculture, biogeochemical modelling, simulation-based inference."),
 ("Co-founder","Zachary Cowden",
  "Biology and industry. Previously at Leidos, working on biomanufacturing for space. Runs the "
  "bioprocess, digestion and life support domains.",
  "Biomanufacturing, closed-loop life support, defence and government programmes."),
 ("Co-founder","Bernard Yong",
  "Markets and operations. Previously at AWS, a lawyer by training, and a former adviser on UN "
  "policy. Runs commercial structure, channel and the legal interface.",
  "Enterprise commercial, contracts and data governance, international policy."),
]
