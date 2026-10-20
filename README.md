# myrgp.in — Ramesh Generic Pharmacy website

Static bilingual site (English `index.html`, Tamil `ta.html`) served by a small
nginx container. On the VPS, the edge Caddy (`edge-caddy`, /root/apps/edge-caddy) handles
HTTPS on ports 80/443 and forwards myrgp.in to it over the `edge` network.

```
public/               the live site (what the container serves)
src/template.html     page source with [[key|English]] text markers
src/ta.py             Tamil text for every marker
src/build.py          regenerates public/index.html and public/ta.html
src/logo.py           rebuilds the logo PNGs from src/brand/logo-original.png
src/assets.py         rebuilds favicon, app icons and og-image.jpg
docker/site.conf      nginx config inside the container
proxy/myrgp.caddy     site block for edge-caddy (synced by deploy.sh)
scripts/deploy.sh     pull + rebuild on the VPS
```

## Editing the site

1. Change text in `src/template.html` (English) and the same key in `src/ta.py` (Tamil).
2. `python3 src/build.py` (Python 3, no packages needed).
3. Commit both `src/` and `public/`, push to `main`.
4. On the VPS: `./scripts/deploy.sh` (or let the GitHub Action do it).

Logo/icon changes need Pillow: `pip install pillow`, then run `src/logo.py`, `src/assets.py`, `src/build.py`.

## First-time VPS setup

Needs the edge Caddy running first (see the edge-caddy repo). Then:

```bash
git clone git@github.com:<you>/myrgp-site.git /root/apps/myrgp-site
cd /root/apps/myrgp-site && ./scripts/deploy.sh   # builds the site, installs myrgp.caddy, reloads edge-caddy
```
