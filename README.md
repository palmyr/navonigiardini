# Navoni Giardini

This repository contains the static website in `docs/`. The page loads its styles directly from `docs/css/style.css`; edit that file to change the site's CSS. No Sass or CSS build step is needed.

Both pages are crawlable static HTML. Keep their titles, descriptions, canonical URLs, social metadata, and the homepage's structured business information accurate when site details change. Update `docs/sitemap.xml` when public pages are added or removed; `docs/robots.txt` points crawlers to that sitemap.

To preview the site locally, run:

```sh
python3 -m http.server 8000 --directory docs
```

Then open `http://localhost:8000/` in a browser.