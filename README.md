# Orbital Ecology, website

Static site. No build step at serve time, no dependencies, no framework.
Deploy the folder as-is.

## Rebuild

    python3 build.py

`content.py` holds every fact, figure, product description, contact detail and
source. `build.py` holds the templates, CSS and JS. Edit content, not markup.

## Deploying to GitHub Pages

The repo ships with `.github/workflows/pages.yml`, which regenerates the HTML
from `content.py` on every push to `main` and publishes the result. That way the
committed HTML can never drift from the content model.

    git init
    git add -A
    git commit -m "Orbital Ecology site"
    git branch -M main
    git remote add origin git@github.com:<you>/<repo>.git
    git push -u origin main

Then in the repo: **Settings, Pages, Source: GitHub Actions**. Add
`orbitalecology.com` as the custom domain and tick Enforce HTTPS.

DNS at your registrar:

    A     @    185.199.108.153
    A     @    185.199.109.153
    A     @    185.199.110.153
    A     @    185.199.111.153
    CNAME www  <you>.github.io.

`CNAME` and `.nojekyll` are already in the repo. Do not delete either. If you
change the domain, change `DOMAIN` in `content.py` and rebuild, which rewrites
`CNAME`, `sitemap.xml`, `robots.txt` and the absolute og:image URL together.

## The form

`evaluation.html` carries the request form. It works with nothing configured:
on submit it composes a pre-filled email to `cameron@orbitalecology.com`.

To have submissions land in your inbox as real form posts instead, create a
free form at formspree.io, copy the id out of the endpoint they give you
(`https://formspree.io/f/XXXXXXXX`), and put it in `content.py`:

    FORM_ID = "XXXXXXXX"

Rebuild. The form then posts in the background, the visitor stays on the page,
and a failed post falls back to the email path automatically. No other change
is needed, and no server is involved either way.

## Files

    index.html          hero, problem, figure, method, the pyramid, validation,
                        benchmarks, questions, sources
    evaluation.html     the offer in full, plus the request form
    company.html        founders, stage, contact
    current.html        CURRENT    aquaculture
    canopy.html         CANOPY     controlled agriculture
    aquifer.html        AQUIFER    hydroponics and water
    reclaim.html        RECLAIM    bioremediation
    culture.html        CULTURE    bioprocessing
    orbis.html          ORBIS      space and life support
    field.html          FIELD      open environments
    nexus.html          NEXUS      platform layer
    404.html

    assets/mark.png             logomark
    assets/wordmark.png         ORBITAL ECOLOGY type
    assets/lockup.png           full lockup with tagline
    assets/icon-512.png         favicon
    assets/share-card.jpg       1200x630 card for links and social
    assets/figure-forecast.svg  the method figure, generated, animated on scroll
    assets/img/*.webp           graded imagery, product page heroes
    assets/img/raw/*.webp       unfiltered imagery, pyramid tiles
    assets/video/hero.mp4       hero footage, full resolution
    assets/video/hero-720.mp4   hero footage, light encode

## Sections

    hero                           the argument and the figure, side by side
    01 The problem                 what the gauges actually measure
    02 The method                  three steps
    03 Products and trajectory     the pyramid
    04 Validation record           every figure resolves to a run
    05 Benchmarks
    06 Questions
    07 Sources
    cta                            Earth at night, the ask

## The hero

The hero is the share card, built as a live page rather than an image: copy
column left, the forecast figure right.

The background is **not** the starfield photograph. `assets/img/hero-wash.webp`
is that photograph abstracted: cropped to its densest region, downsampled to
90px, blurred, upscaled and remapped onto a two-point ramp from `#06060A` to a
muted violet. What survives is the large colour fields and none of the stars,
which were competing with the data points in the figure. It is 5.7KB.

The veil over it is directional: near-opaque on the left so the copy sits on
black, opening to 22% on the right so the wash reads as atmosphere behind the
figure. The figure panel carries a brighter border and a deep drop shadow so it
is unambiguously the lit object in the frame. The figure used to have its own section further down.
Putting it in the hero means the argument is made before anyone scrolls, so
that section is gone and the numbering shifted up.

The copy column staggers in on load, then the figure draws itself 620ms later,
so the two do not compete. `assets/share-card.jpg` mirrors this composition for
link previews and is generated separately; if you change the hero, regenerate
the card so the two stay in step.

Earth at night moved to the closing call to action, which gives the page a
bookend: the data at the top, the reason for it at the bottom.

## Palette

    --bg   #09090C   near-neutral base
    --p1   #0E0F14   panel
    --sig  #4FC3F7   instrument blue, RESERVED: the figure, the estimate, the
                     status strip, focus rings. Not for ordinary chrome.
    --vio  #9B8CF2   violet: atmospheric glows
    --warn #FF9F45   amber: risk, thresholds, cost figures

Structural chrome is white or neutral grey. Blue is a signal, not a skin. If you
find yourself adding `var(--sig)` to something that is not data, use `var(--w)`.

Each product carries its own accent hue in `ACCENT` in build.py, applied through
the `--acc` custom property on product heroes, chips and the text index.

    CURRENT #4FC3F7   CANOPY  #FFB84D   AQUIFER #5B8DEF   RECLAIM #9B87F5
    CULTURE #F2789E   ORBIS   #A9B7FF   FIELD   #FF9F45   NEXUS   #9FB0C9

## The pyramid

Sections 04 and 05 are the same argument, so they are the same section. The
product index *is* the trajectory: six closed-system markets stack into a
honeycomb triangle on a plinth carrying the two things that are not closed
markets.

    apex          ORBIS                          Then    closed-loop life support
    row 2         RECLAIM   CULTURE              Next    environmental recovery
    row 3   CURRENT   CANOPY   AQUIFER           Now     terrestrial production
    plinth  NEXUS ............ FIELD             Foundation

NEXUS is the plinth because it is the platform, not a market. FIELD sits beside
it because an open environment is the one thing in the portfolio that is not a
closed loop. That is also why the triangle is six and not eight.

Geometry is pointy-top honeycomb baked into `PYRAMID` in build.py as literal
percentages: hex width 30% of the board, 2.5% gaps, rows stepping 0.75 x hex
height, board aspect ratio 1000/1061. Changing the hex width means recomputing
the rest; the formulas are in the header comment.

### Liquid glass

Five layers inside one hexagonal `clip-path`:

    .ph    the domain photograph, saturation dropped to 0.12 so it reads as
           texture rather than colour
    .g     the glass: backdrop-filter blur(13px) saturate(210%) over three
           orange gradients
    .lq    a caustic drifting on an 11s loop, blurred, clipped inside
    .sp    the specular streak across the top facets
    .rim   an SVG hexagon stroked with a four-stop gradient, plus a screen-blend
           sheen on the upper-left edges

What sells it as liquid rather than plastic is the physics: on impact each tile
compresses along Y and swells along X in proportion to landing speed.

### Physics

Scroll releases tiles, it does not drive them. Once released each tile is a
rigid body:

    G     5400 px/s^2      gravity
    e     0.31 / 0.16      restitution, hexes / plinth plates
    REST  54 px/s          sleep threshold

Contact: squash proportional to impact speed, a kick to the whole board scaled
to mass, rebound at `-vy*e`. One gotcha worth keeping: a discrete integrator
adds `G*dt` of speed every frame, so a naive `if(|vy| < REST) sleep` never fires
and the body micro-bounces forever. The sleep test is
`vout < max(REST, G*dt*2.2)`.

Tiles are fed one at a time with a 185ms floor between releases, so a fast
scroll cascades instead of dumping all eight at once.

**Once a tile lands it stays landed.** Scrolling back up shows the finished
pyramid; it does not rewind and rebuild.

Mobile drops the sticky scrub and fires the same physics off an observer.
Reduced motion renders the pyramid assembled. A plain text index of all eight
products sits under the pyramid, outside the sticky stage, so the section works
without JavaScript and reads to a crawler.

## Media

All photography is a baked blue duotone (`#04070D` shadow to `#E2EEF8`
highlight) so the imagery belongs to the palette. Warm highlights are partly
preserved so sodium and city lights survive. Everything is WebP.

The pyramid tiles pull from `assets/img/raw/` and desaturate in CSS to 0.12, so
the photograph reads as texture under the orange glass. Product page heroes keep
the graded image with a light accent wash at 16%.

Hero video is Earth at night from orbit, flipped horizontally so the sun flare
lands on the right and the headline sits on dark sky, graded toward blue shadows
and amber highlights.

**Background video never autoplays on a phone.** Every `video.bg` is injected by
JS only when the viewport is 820px or wider, `navigator.connection.saveData` is
off, and reduced motion is not requested, and then only once it scrolls near.
Below 1500px it loads the 800KB encode instead of the 3.5MB one. Everyone else
sees the poster frame.

## Motion

Reveal-on-scroll runs off one IntersectionObserver with per-group stagger set
through a `--d` custom property. The hero has a staged entrance, the nav
condenses past 40px, and the forecast figure draws itself in sequence: axes,
observable, threshold, confidence band, estimated state, then the markers and
the 6.5 h span.

Everything is disabled under `prefers-reduced-motion: reduce`.

## Accessibility

Skip link, a `<main>` landmark, a labelled primary nav, alt text on every image,
labels on every form field, and a visible `:focus-visible` ring in the signal
colour on every interactive element. Verified across 12 pages at nine viewport
widths from 360 to 1920.

## Discipline that must not drift

The engine estimates state and forecasts it forward. It is read-only. It
connects to no control loop. Autonomous control is roadmap, not product.

There is no production deployment. Every figure resolves to the validation
record and to a numbered source. Simulation results are labelled as simulation.
