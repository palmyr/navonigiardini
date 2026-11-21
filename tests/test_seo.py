import json
import unittest
from html.parser import HTMLParser
from pathlib import Path
from xml.etree import ElementTree


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
CANONICAL_URLS = {
    "index.html": "https://navonigiardini.com/",
    "srd15.html": "https://navonigiardini.com/srd15.html",
}


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.metadata = {}
        self.canonical_urls = []
        self.headings = []
        self.images = []
        self.json_ld = []
        self.main_landmarks = 0
        self._heading = None
        self._script_type = None
        self._script_data = []

    def handle_starttag(self, tag, raw_attrs):
        attrs = dict(raw_attrs)
        if tag == "main":
            self.main_landmarks += 1
        elif tag == "meta":
            key = attrs.get("name") or attrs.get("property")
            if key:
                self.metadata[key] = attrs.get("content", "")
        elif tag == "link" and attrs.get("rel") == "canonical":
            self.canonical_urls.append(attrs.get("href", ""))
        elif tag in ("h1", "h2", "h3"):
            self._heading = [tag, ""]
        elif tag == "img":
            self.images.append(attrs.get("alt"))
        elif tag == "script":
            self._script_type = attrs.get("type")
            self._script_data = []

    def handle_data(self, data):
        if self._heading is not None:
            self._heading[1] += data
        if self._script_type == "application/ld+json":
            self._script_data.append(data)

    def handle_endtag(self, tag):
        if self._heading is not None and tag == self._heading[0]:
            self.headings.append((self._heading[0], self._heading[1].strip()))
            self._heading = None
        elif tag == "script" and self._script_type == "application/ld+json":
            self.json_ld.append(json.loads("".join(self._script_data)))
            self._script_type = None


class StaticSeoTests(unittest.TestCase):
    def parse_page(self, filename):
        parser = PageParser()
        parser.feed((DOCS / filename).read_text(encoding="utf-8"))
        return parser

    def test_pages_have_page_specific_metadata_and_canonicals(self):
        for filename, canonical in CANONICAL_URLS.items():
            with self.subTest(page=filename):
                page = self.parse_page(filename)
                self.assertEqual(page.canonical_urls, [canonical])
                self.assertTrue(page.metadata.get("description"))
                self.assertEqual(page.metadata.get("og:url"), canonical)
                self.assertTrue(page.metadata.get("og:title"))
                self.assertTrue(page.metadata.get("og:description"))

    def test_homepage_has_business_structured_data_from_visible_details(self):
        page = self.parse_page("index.html")
        self.assertEqual(len(page.json_ld), 1)
        business = page.json_ld[0]
        self.assertEqual(business["@context"], "https://schema.org")
        self.assertEqual(business["@type"], "LocalBusiness")
        self.assertEqual(business["name"], "Navoni Giardini")
        self.assertEqual(business["telephone"], "+393489309034")
        self.assertEqual(business["email"], "luigi.navoni@alice.it")
        self.assertEqual(business["address"]["streetAddress"], "Frazione Gombaz 12")
        self.assertEqual(business["address"]["addressLocality"], "Torgnon")
        self.assertEqual(business["address"]["addressCountry"], "IT")

    def test_pages_have_descriptive_headings_and_images(self):
        homepage = self.parse_page("index.html")
        self.assertEqual(homepage.main_landmarks, 1)
        self.assertEqual(homepage.headings[0], ("h1", "Parchi, giardini e aree verdi"))
        self.assertIn("Giardinaggio a Torgnon, in Valle d’Aosta", [text for _, text in homepage.headings])
        self.assertTrue(homepage.images)
        self.assertTrue(all(alt and alt.strip() for alt in homepage.images))

        srd15 = self.parse_page("srd15.html")
        self.assertEqual(srd15.main_landmarks, 1)
        self.assertEqual(srd15.headings[0], ("h1", "Intervento SRD15 “Investimenti produttivi forestali”"))
        self.assertIn("Torna al sito Navoni Giardini", (DOCS / "srd15.html").read_text(encoding="utf-8"))

    def test_sitemap_covers_both_canonical_pages_without_stale_dates(self):
        sitemap = ElementTree.parse(DOCS / "sitemap.xml").getroot()
        namespace = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        locations = {
            location.text
            for location in sitemap.findall("s:url/s:loc", namespace)
        }
        self.assertEqual(locations, set(CANONICAL_URLS.values()))
        self.assertFalse(sitemap.findall(".//s:lastmod", namespace))

    def test_robots_allows_crawling_and_points_to_sitemap(self):
        directives = [
            line.strip()
            for line in (DOCS / "robots.txt").read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        self.assertIn("User-agent: *", directives)
        self.assertIn("Allow: /", directives)
        self.assertIn("Sitemap: https://navonigiardini.com/sitemap.xml", directives)


if __name__ == "__main__":
    unittest.main()