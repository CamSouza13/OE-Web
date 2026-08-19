# Deploying orbitalecology.com

This repo is already initialised and committed on `main`. Three commands and
some clicking.

## 1. Create the repo

On github.com: **New repository**, name it `orbital-ecology-site` (the name does
not affect the domain), leave it empty. Do not add a README, .gitignore or
licence, they would conflict with what is already here.

Public is fine and simpler. Private also works: GitHub Pages on a private repo
requires a paid plan, and the workflow already stages a clean `_site` so the
generator and git history are never served either way.

## 2. Push

    cd orbital-ecology-site
    git remote add origin https://github.com/YOUR-USERNAME/orbital-ecology-site.git
    git push -u origin main

If you use SSH instead:

    git remote add origin git@github.com:YOUR-USERNAME/orbital-ecology-site.git

## 3. Turn on Pages

Repo, **Settings, Pages**. Under *Build and deployment*, set **Source** to
**GitHub Actions**. Nothing else on that screen.

Go to the **Actions** tab. The workflow runs on the push you just made. It takes
about a minute. If it did not fire, hit *Run workflow* on
"Deploy to GitHub Pages".

## 4. Point the domain

At whoever holds orbitalecology.com, set these records:

    A      @      185.199.108.153
    A      @      185.199.109.153
    A      @      185.199.110.153
    A      @      185.199.111.153
    CNAME  www    YOUR-USERNAME.github.io.

Delete any existing A or CNAME record on `@` and `www` first, including parking
or forwarding records from the registrar. Those are the usual reason a domain
will not verify.

Back in **Settings, Pages**, put `orbitalecology.com` in *Custom domain* and
save. `CNAME` is already in the repo so this should verify immediately. Once the
certificate is issued, tick **Enforce HTTPS**.

DNS can take anywhere from ten minutes to a few hours. The site is live on
`YOUR-USERNAME.github.io/orbital-ecology-site/` in the meantime.

## What the workflow does

On every push to `main` it runs `python3 build.py`, which regenerates all twelve
pages plus `CNAME`, `sitemap.xml` and `robots.txt` from `content.py`. Then it
copies only the public files into `_site` and publishes that.

This means the committed HTML can never drift from the content model. If someone
edits an `.html` file by hand and pushes, the next build overwrites it. Edit
`content.py`, not the markup.

## Changing things later

    edit content.py
    python3 build.py        # optional, to preview locally
    git add -A && git commit -m "..." && git push

Changing `DOMAIN` in `content.py` rewrites `CNAME`, `sitemap.xml`, `robots.txt`
and the absolute og:image URL together. Do not edit `CNAME` by hand, it is
generated.

## Still outstanding

The evaluation form composes a pre-filled email until you set `FORM_ID` in
`content.py`. Make a free form at formspree.io, copy the id out of the endpoint
they give you, paste it in, push. Then submissions land in your inbox and the
visitor stays on the page.

Confirm the Medium handle in `content.py` too. It currently assumes
`medium.com/@orbitalecology`.
