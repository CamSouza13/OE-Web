ORBITAL ECOLOGY / SITE
======================

WHAT IS HAND-BUILT AND WHAT IS GENERATED
Four pages are now hand-built and share one stylesheet:

  index.html        home
  philosophy.html   why the work matters, with sources
  team.html         the three founders and how we work
  demo.html         the live engine, wrapped in the site shell

Everything else (company.html, evaluation.html, the seven product pages,
404.html) is still build.py output in the old dark theme.

IMPORTANT: build.py still writes index.html. Running it overwrites the home
page. Either drop index.html from the build target, or rename the hand-built
file and point the site at it. The other three hand-built pages are not touched
by build.py.

SHARED FILES
  assets/oe.css              the whole design system, one sheet, all four pages
  assets/oe.js               nav, scroll reveal, count-up, ink-band parallax
  assets/fonts.css           @font-face for the self-hosted faces
  assets/fonts/              Inter Tight 400/500/600, JetBrains Mono 400/500, woff2
  assets/mark-ink.png        dark logo mark for the light ground
  assets/wordmark-ink.png    dark wordmark
  assets/lockup-ink.png      dark lockup, spare
  assets/img/g/*.webp        the photography, graded to the palette

DEMO-ONLY FILES
  engine.js domains.js       the estimator and the four domain models
  samples.js demo.js         embedded sample logs and the demo UI
  data/                      the four sample logs as standalone CSVs

TYPE
Three faces, all self-hosted in assets/fonts, latin subset only, 321 KB total.
No third-party request and no flash of fallback.

  Newsreader     display serif, weight 400 only. h1 and h2 site-wide, plus the
                 thesis line. Variable on the optical-size axis, so display type
                 carries font-variation-settings:'opsz' 60 to get the high
                 contrast display cut rather than the text cut. Drop that and the
                 headlines go flat.
  Inter Tight    400/500/600. Everything structural: h3, h4, body, UI, buttons.
  JetBrains Mono 400/500. Anything numeric, labelled or tabular.

Serif runs smaller per pixel than the grotesque, so every display size came up
about 8 to 10 percent and tracking loosened from roughly -0.032em to -0.015em
when the serif went in. If you swap the face back, reverse both.

If you add a weight, add the woff2 and the @font-face together, or the browser
will synthesise it and it will look wrong.

THE DESIGN
Light ground, near-neutral paper (#F4F3EF), with a fine grain over the whole page
so the flat colour does not read as flat. The previous ground was a cream
(#F2EEE4) that read craft rather than institution; the fix was pulling roughly ten
points of yellow out, nothing else. Dark bands break the rhythm: the full-bleed
hero, the arc band, and the statement bands on philosophy and team.

BRAND ACCENT, ONE ONLY
  #14432F  deep forest. Buttons, links, active marks, small numerals.
  #5FA98A  the same accent lightened, for use on the dark bands only.
On a dark ground the deep forest reads as a black box, so primary buttons inside
.vhero and .end .box invert to paper on dark instead.

CHART HUES, A SEPARATE SET
The three data colours are a validated categorical palette and are deliberately
NOT the brand colour. Charts encode meaning; brands do not.

  #35619C  measured, the reading the operator already has
  #2A7F55  estimated, the thing no sensor reports
  #A54A1C  the limit and the moment it is crossed

The deep forest brand accent cannot be used as a chart series: at that darkness
its chroma falls under the categorical floor and it stops separating from a
neighbouring dark hue. #2A7F55 is the same hue family, bright enough to work as a
line, so the two read as one colour system without breaking the chart rules.

The chart trio is validated against the categorical checks (lightness band,
chroma floor, colour-blind separation, contrast on the surface). If you add a
fourth series colour, re-validate. Green and terracotta never share a lane, which
is what makes their deutan separation legal.

Green carries meaning rather than decoration: it means "the thing we add", which
is the estimate, the warning, and the call to action. Nothing else is green.

PHOTOGRAPHY
Full colour. Note that the files that used to sit in assets/img were themselves
blue-graded by an earlier build (blue channel running 30 to 45 points above red).
The true full-colour originals were in assets/img/raw. Those have now been
promoted into assets/img, resized to 1600px max and re-encoded. If an image ever
looks cold and monochrome again, check whether someone has restored the old
graded file over the top of it.

THE HERO
Full bleed. The orbit video fills the first screen, the nav floats over it with
the marks inverted and the CTA as a ghost outline, and the nav swaps to the solid
eggshell bar once you scroll past the hero. That behaviour needs two things: the
body carries class="hero-page" (which makes the nav position:fixed) and the page
contains a .vhero element (which oe.js watches to toggle .over). Interior pages
have neither and keep the normal sticky bar.

The engine figure now lives in its own section beneath the thesis line. The HD literal in index.html is one
real run of the estimator on the sample recirculating salmon log, produced by the
same code that runs on demo.html. To regenerate after a model change:

  node hero_precompute.js > hero.json     (in the demo working folder)

then paste the JSON over the HD = {...} literal.

Both SVG figures on the home page draw at the element's real pixel width rather
than being scaled, so type stays crisp at every size. They redraw on resize and
switch to a taller layout below 760px.

MOTION
Everything is behind prefers-reduced-motion. Headline lines clip and rise on
load. Hero traces draw once. Hero stats count up. Framed images scale from 1.07
as they reveal. The pipeline diagram draws its paths then loops a packet through
it. The product panel cross-fades and scales. The arc band parallaxes. Buttons
slide their arrow, nav links wipe an underline, the nav condenses on scroll.

Reveal uses an IntersectionObserver plus a scroll sweep, because IO can be
outrun by a fast flick to the bottom of a long page.

TWO CSS TRAPS, READ BEFORE EDITING
1. A section carrying .wrap must never set the padding shorthand. .wrap supplies
   the side gutters and a shorthand like padding: var(--s) 0 silently wipes them,
   so the page runs edge to edge. Use padding-block.
1b. SVG text uses font-family="JetBrains Mono, ui-monospace, monospace" with no
   inner quotes. Quoting the family name inside a JS-built attribute string breaks
   the surrounding JS string.
2. demo.html links oe.css and then its own sheet. Its section-label class was
   renamed .sec to .slb because .sec is the site's section-padding class. If you
   add classes to demo.html, check them against oe.css first.
3. demo.html no longer redefines body, .wrap, .lbl, a, :focus-visible, the box
   reset or h1/h2/h3. Those had drifted out of step with oe.css, and the h1/h2/h3
   rule in particular forced Newsreader to weight 600, which has no file, so the
   browser was synthesising bold and the headline looked muddy. Do not reintroduce
   element-level rules there; put page-specific styles on page-specific classes.
4. The demo page chrome (nav, hero, footer) uses the same --pad as the rest of the
   site. Only .rack carries an extra margin-inline, because the four-up grid is the
   only thing on the site dense enough to need it. Widening --pad for the whole page
   made the nav jump when moving between demo and everything else.

--gut is the viewport-edge-to-content distance. Use it when a panel bleeds to the
viewport edge on one side and stays aligned with the text column on the other, as
the evaluation panels do.

PROVENANCE OF THE HOME PAGE FIGURE
The hero figure is the production estimator's output on a SYNTHETIC recirculating
salmon log, the same log the live demo ships with. The page says so, in the
caption and again in the line under the stat rail, which also points at the real
number: 6.5 hours of usable lead reproduced on real commercial operating history.
Keep both of those. Without them the 89 hour headline reads as a claim about a
real farm, and a reader who later finds the 6.5 hour figure in the validation
record will assume the headline was inflated.

Also note the index figure is a replay of a precomputed run. Only demo.html runs
the engine live in the browser. The captions on each page now say the right thing;
do not copy one to the other.

VOICE
The site states what has been done and what it is measured against. It does not
lead with what has not happened yet. The validation record still labels each
result honestly (Complete, In progress, In design) and the sources still resolve,
which is where the credibility comes from; the apologetic framing was doing no
work. Do not reintroduce it, and equally do not claim a live deployment, a paid
pilot or a customer, because none of those exist yet and the record would not
support them.

THE PHILOSOPHY PAGE
Every figure on it is sourced and the sources are listed at the bottom with live
links: FAO AQUASTAT 2025, FAO SOFIA 2024, UNEP Food Waste Index 2024, USDA ERS
Food Access Research Atlas, Texas A&M AgriLife Extension, Drewnowski et al. 2019.
The two incident figures are the same ones used on the home page and are labelled
as reported, with an explicit note that neither operator is a customer.

The page contains a dark band headed "A forecast is only worth what its record is
worth." It carries the five commitments that let an operator check us instead of
trusting us. Keep it: it is what stops the rest of the page reading as a pitch.

THE PRODUCT INDEX
Eight rows, one sticky panel. Hover or keyboard-focus swaps the image, copy and
evidence; click opens that product page. Content lives in the P array at the
bottom of index.html, duplicating content.py wording by hand. Keep them in step.

HONESTY, UNCHANGED
  - Every figure traces to content.py, its SOURCES block, or a cited paper.
  - The record table states what is simulation and what is a real backtest.
  - No live deployment is claimed anywhere. Several places say so explicitly.
  - The engine estimates and forecasts. Read-only. The pages say that too.

ONE THING TO DECIDE, CAM
The validation record still carries the SIMOC row from content.py: "98 percent of
breaches identified pre-event. Median lead 11 h, max 168. False alarm 11 percent."
The later re-run campaigns concluded that lead time is an improper score and that
the original headline lead figure was not defensible. That row and the team page's
line about having thrown out a headline result when the scoring turned out to be
improper are now sitting on the same site. I have not changed the published record
on my own, because it is the company's record and the call is yours. Either update
the SIMOC row to a proper score, or drop the median and max lead numbers from it
and keep the detection rate.

STILL TO DO
  - Port company.html, evaluation.html and the seven product pages onto oe.css.
    That is a build.py change, not a redesign, and it is the last visible seam.
  - Set FORM_ID in content.py once Formspree is configured.
  - Tick "Enforce HTTPS" in the GitHub Pages settings.

TO DEPLOY
  git add -A && git commit -m "site: home, philosophy, team, demo" && git push
Pages serves from the repo root. CNAME and .nojekyll are already in place.
sitemap.xml has been updated with the three new URLs.
