# Orbital Ecology, website

Static site. No build step at serve time, no dependencies, no framework. The
GitHub Actions workflow publishes exactly what is committed.

## Two halves of the repo

**Hand-built, current design.** Light ground, Newsreader display serif, one
brand accent. These are edited directly as HTML.

    index.html          home
    philosophy.html     why the work matters, fully sourced
    team.html           the three founders and how we work
    demo.html           the live engine

**Generated, previous dark design.** These are `tools/build.py` output, still in
the old dark theme, and still linked from the nav, the product index and the
footer of the pages above. Do not delete them without porting them first: the
"Request an evaluation" CTA on every page points at `evaluation.html`.

    evaluation.html     the offer in full, plus the request form
    company.html        founders, stage, contact
    current.html canopy.html aquifer.html reclaim.html
    culture.html orbis.html field.html nexus.html
    404.html

Porting them onto `assets/oe.css` is the last visible seam in the site.

## Shared front end

    assets/oe.css       the whole design system, all four hand-built pages
    assets/oe.js        nav, scroll reveal, count-up, parallax
    assets/fonts.css    @font-face for the self-hosted faces
    assets/fonts/       Newsreader 400, Inter Tight 400/500/600,
                        JetBrains Mono 400/500. Latin subset, 321 KB total.
    assets/img/*.webp   full-colour photography
    assets/video/       hero footage, 720p encode

`SITE.md` is the design and maintenance handbook: palette, type scale, the two
CSS traps that will bite you, and the provenance rules for the figures. Read it
before changing anything visual.

## The live demo

`demo.html` runs the production estimator in the browser.

    engine.js     UKF, RK4, Monte-Carlo forecast, with run counters
    domains.js    four domain models, safety limits, cost assumptions
    samples.js    the four sample logs, embedded, so the page works offline
    demo.js       CSV parsing, the time-sliced run loop, charts, narration
    data/         the same four logs as standalone CSVs

The sample logs are synthetic and every page that shows a figure from them says
so. Cost figures are modelled from assumptions printed on each card.

## The generator

`tools/build.py` regenerates the dark pages from `tools/content.py`. It is no
longer run at deploy time, because it writes `index.html` and would overwrite
the hand-built home page. It lives in `tools/` so the staging step cannot pick
it up. To regenerate the pages it owns:

    cd tools && python3 build.py

Then check `git diff` before committing: it will try to rewrite `index.html`.

## Deploying

Push to `main`. The workflow stages `_site` and publishes it. About a minute.

Settings, Pages: Source is **GitHub Actions**, custom domain
`orbitalecology.com`, **Enforce HTTPS** ticked. `CNAME` and `.nojekyll` are in
the repo; do not delete either.

DNS:

    A      @      185.199.108.153
    A      @      185.199.109.153
    A      @      185.199.110.153
    A      @      185.199.111.153
    CNAME  www    camsouza13.github.io.

## Outstanding

The evaluation form composes a pre-filled email until `FORM_ID` is set in
`tools/content.py`. Create a free form at formspree.io, copy the id out of the
endpoint, paste it in, regenerate `evaluation.html`, push.

## Discipline that must not drift

The engine estimates state and forecasts it forward. It is read-only. It
connects to no control loop. Autonomous control is roadmap, not product.

Every figure resolves to the validation record, a published benchmark, or a
numbered source. Simulation is labelled as simulation. The site does not claim
a live deployment, a paid pilot or a customer, because there is not one yet.
