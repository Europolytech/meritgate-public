"""Publish search metadata and applicant guides alongside the fresh staff-edited homepage."""
import json
import re
import sys
from html import escape, unescape
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin
from xml.etree import ElementTree as ET

from PIL import Image, ImageOps

BASE = "https://meritgate.europolytech.academy/"
ACADEMY = "https://www.europolytech.academy/"
GUIDES = [
    ("porto-scholarship", "Merit-based scholarship in Porto",
     "How selection works, what the Porto experience adds and what to check before committing to the MeritGate scholarship pathway.",
     "If you are comparing scholarships to study in Europe, start with what the award gives you. MeritGate offers selected learners a period of face-to-face academic study in Greater Porto alongside their British vocational qualification pathway.",
     [("How does selection work?", "Read the published academic criteria before applying. Free registration records your interest. Formal application, assessment and a scholarship decision are separate steps.", "scholarship", "Read the scholarship conditions"),
      ("What should I budget for?", "Check the written offer for tuition, travel, accommodation and living costs. Ask the academy which costs you would pay yourself before making travel arrangements.", "faq", "Read applicant questions")],
     ["Is the scholarship guaranteed?", "How is academic merit assessed before teaching begins?", "When will scholarship results be announced?"]),
    ("study-routes", "Study in Porto or join the live classroom online",
     "Compare MeritGate’s Porto scholarship route and live online study, including the timetable, assessments and British vocational qualification requirements.",
     "For an international student, the practical choice is where to attend class. Selected scholars attend in Maia, Greater Porto. Online participants join the same scheduled lessons remotely and can ask the tutor questions in real time.",
     [("What do both routes share?", "Both groups follow the same cohort timetable, learning outcomes and assessments. Consider whether you can attend the live sessions in your time zone and allow time for independent study between classes.", "classroom", "Compare the two study routes"),
      ("Which qualification would I work towards?", "Look at the specific qualification, awarding organisation and assessment arrangements for your pathway. If you plan to progress to higher education, check the entry requirements of the institution and course you intend to apply to.", "how-it-works", "Explore the qualification pathway")],
     ["Can online participants join the same classes as Porto scholars?", "What is Moodle used for?", "Which awarding organisations provide the qualifications?"]),
    ("international-applicants", "Studying in Portugal with MeritGate",
     "An international applicant’s guide to MeritGate registration, academic eligibility and planning a short study experience in Greater Porto, Portugal.",
     "Planning a short study-abroad experience involves three separate checks. Find out whether you meet the academic entry requirements, how scholarship selection works and which travel rules apply to you.",
     [("Check academic eligibility", "Start with the qualification pathway and read its entry and assessment requirements. If your previous studies took place in another education system, ask the academy what supporting documents it accepts.", "programme", "Review the programme"),
      ("Plan the journey to Greater Porto", "Use the country explorer as a starting point and follow its official European Commission link. Confirm your own travel requirements before booking. The campus map shows where face-to-face activities take place.", "mg-eligibility", "Explore countries and official travel guidance")],
     ["Is registering interest completely free?", "Does participation guarantee a visa or residence permit?", "Where can I read the full programme terms?"]),
]


class Inventory(HTMLParser):
    def __init__(self):
        super().__init__()
        self.images = []
        self.links = []
        self.icon = ""

    def handle_starttag(self, tag, attrs):
        fields = dict(attrs)
        if tag == "img":
            self.images.append(fields)
        elif tag == "a":
            self.links.append(fields)
        elif tag == "link" and fields.get("rel") == "icon":
            self.icon = fields["href"]


CSS = """body{margin:0;background:#f6f5ee;color:#102737;font:1.06rem/1.65 system-ui,sans-serif}
main,header,footer{max-width:48rem;margin:auto;padding:1.25rem clamp(1.2rem,5vw,3.5rem)}
header,footer{border-bottom:1px solid #cad4cc}h1,h2{line-height:1.13;font-family:Georgia,serif;font-weight:500}
h1{font-size:clamp(2.5rem,7vw,4.4rem);margin:.6em 0}h2{font-size:1.8rem;margin:1.4em 0 .4em}p{max-width:68ch}
a{color:#005f59;text-underline-offset:.18em}a:focus-visible,summary:focus-visible{outline:3px solid #006f69;outline-offset:3px}
summary{cursor:pointer;font-weight:650;padding:.7rem 0}details{border-bottom:1px solid #ccd5ce}
.cta{display:inline-block;background:#edc56a;color:#112a35;padding:.65rem 1rem;border-radius:.4rem;font-weight:700}
nav ul{padding-left:1.25rem}footer{padding-bottom:3rem}"""


def head(path, title, description, image, alt, label):
    url = BASE + path
    org = {"@type": "EducationalOrganization", "@id": ACADEMY + "#academy",
           "name": "EuroPolytech Academy", "url": ACADEMY}
    site = {"@type": "WebSite", "@id": BASE + "#website", "name": "MeritGate", "url": BASE,
            "publisher": {"@id": org["@id"]}, "inLanguage": "en"}
    page = {"@type": "WebPage", "@id": url + "#webpage", "url": url, "name": title,
            "description": description, "inLanguage": "en", "isPartOf": {"@id": site["@id"]},
            "publisher": {"@id": org["@id"]}}
    graph = [org, site, page]
    if path:
        crumb = {"@type": "BreadcrumbList", "@id": url + "#breadcrumbs", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "MeritGate", "item": BASE},
            {"@type": "ListItem", "position": 2, "name": label, "item": url}]}
        page["breadcrumb"] = {"@id": crumb["@id"]}
        graph.append(crumb)
    data = json.dumps({"@context": "https://schema.org", "@graph": graph}).replace("<", r"\u003c")
    tags = [f"<title>{escape(title)}</title>", f'<link rel="canonical" href="{url}">',
            f'<meta name="description" content="{escape(description)}">',
            '<meta name="robots" content="max-image-preview:large">',
            '<meta name="twitter:card" content="summary_large_image">']
    for name, value in {"type":"website", "site_name":"MeritGate", "locale":"en_GB", "url":url,
                        "title":title, "description":description,"image":image,"image:alt":alt}.items():
        if value:
            tags.append(f'<meta property="og:{name}" content="{escape(value)}">')
    return "\n".join(tags) + f'<script type="application/ld+json">{data}</script>'


PHOTO_DESCRIPTIONS = {'00059b25504653144290ea9e36477afb1c2cd64e2056fb61862ae5749d8c0e84.png': 'Academy reception desk with a wall-mounted screen and classroom signage', 'd4b0a0af08f02b02f368234a7221ea13089f994d624d270c835bb06185599194.png': 'Classroom with individual writing chairs facing the teaching desk', '0295d3fa0e9a11945a8254c453b63765cfd886ef8de499f45d8bea2ba38e082e.png': 'Leicester Square classroom sign beside the glass-panelled entrance'}


def improve_image(match):
    tag = match[0]
    attrs = Inventory()
    attrs.feed(tag)
    img = attrs.images[0]
    src = img.get("src", "")
    if not re.fullmatch(r"\./assets/[a-f0-9]{64}\.(png|jpg|webp)", src):
        return tag
    file = output / src
    if img.get("alt") == "" and file.name in PHOTO_DESCRIPTIONS:
        tag = tag.replace('alt=""', f'alt="{escape(PHOTO_DESCRIPTIONS[file.name])}"', 1)
    with Image.open(file) as original:
        width, height = original.size
        if "width" not in img and "height" not in img:
            tag = tag[:-1] + f' width="{width}" height="{height}">'
        if "srcset" in img or (img.get("fetchpriority") != "high" and img.get("class") != "brand-logo" and file.stat().st_size < 100000):
            return tag
        image = ImageOps.exif_transpose(original)
        variants = []
        sizes = [152] if img.get("class") == "brand-logo" else [480, 720, 960, 1440]
        for limit in sorted(set(min(w, image.width) for w in sizes)):
            resized = image.copy()
            resized.thumbnail((limit, image.height), Image.Resampling.LANCZOS)
            dest = file.with_name(file.stem + f"-{limit}.webp")
            resized.save(dest, "WEBP", quality=84)
            if dest.stat().st_size < file.stat().st_size:
                variants.append(("./assets/" + dest.name, resized.width))
        if variants and "srcset" not in img:
            srcset = ", ".join(f"{url} {w}w" for url, w in variants)
            sizes_attr = "76px" if img.get("class") == "brand-logo" else "(max-width: 760px) 100vw, 55vw"
            tag = tag.replace(f'src="{src}"', f'src="{variants[-1][0]}" srcset="{srcset}" sizes="{sizes_attr}"')
    return tag


output = Path(sys.argv[1])
index = output / "index.html"
html = re.sub(r"<img\b[^>]*>", improve_image, index.read_text())
# Give the dormant video link a useful destination even before the player opens.
first_video = re.search(r'data-youtube="([a-zA-Z0-9_-]{11})"', html)
if first_video:
    html = html.replace('<a class="youtube-link" ', f'<a class="youtube-link" href="https://www.youtube.com/watch?v={first_video[1]}" ', 1)
html = html.replace('<div class="mgw-rail" aria-label=', '<div class="mgw-rail" role="group" aria-label=')
# The visible title and contributor together supply each film button's accessible name.
html = re.sub(r'(<button[^>]*class="film-tile"[^>]*?) aria-label="[^"]*"', r'\1', html)
inventory = Inventory()
inventory.feed(html)
hero = next((i for i in inventory.images if i.get("fetchpriority") == "high"), {})
image = urljoin(BASE, hero["src"]) if hero.get("src") else ""
alt = hero.get("alt", "")
cta = next((a["href"] for a in inventory.links if a.get("data-event") == "interest_click" and a.get("href","").startswith("https://")), BASE)
handbook = next((a["href"] for a in inventory.links if a.get("href","").startswith("https://learn.europolytech.academy/")), BASE+"#faq")
faq_section = re.search(r'<section[^>]+id="faq"[^>]*>(.*?)</section>', html, re.S)
def plain(value):
    return unescape(re.sub("<[^>]+>", "", value)).strip()
faqs = {plain(q): plain(a) for q,a in re.findall(r"<summary>(.*?)</summary>\s*<p>(.*?)</p>", faq_section[1] if faq_section else "", re.S)}
def guide_links(exclude=""):
    return "<ul>" + "".join(f'<li><a href="/{slug}/">{escape(label)}</a></li>' for slug,label,*_ in GUIDES if slug != exclude) + "</ul>"

home_title = "Study in Portugal with a Porto Scholarship | MeritGate"
home_desc = "Explore a British vocational qualification pathway with live online classes and a merit-based scholarship opportunity for a two-month study experience in Greater Porto."
html = re.sub(r"<title>.*?</title>|<meta name=\"description\"[^>]*>", "", html, count=2, flags=re.S)
html = html.replace("</head>", head("",home_title,home_desc,image,alt,"MeritGate")+"</head>",1)
html = html.replace('<div class="metric-grid">','<div class="metric-grid" data-nosnippet>') if 'class="test-note"' in html else html
html = re.sub(r'(<p><strong>[^<]*</strong>[^<]*test figure</p>)',r'<div data-nosnippet>\1</div>',html)
nav = '<nav class="wrap section" aria-label="Applicant guides"><h2>MeritGate applicant guides</h2>'+guide_links()+'</nav>'
closing = '<section class="closing">'
html = html.replace(closing,nav+closing,1) if closing in html else html.replace("</main>",nav+"</main>",1)
index.write_text(html)
for slug,label,desc,intro,sections,questions in GUIDES:
    path = slug+"/"
    title = label if "MeritGate" in label else label+" | MeritGate"
    body = f'<header><a href="/">MeritGate</a> / Applicant guides</header><main><h1>{escape(label)}</h1><p>{escape(intro)}</p>'
    for heading, paragraph, anchor, link in sections:
        body += f'<section><h2>{heading}</h2><p>{escape(paragraph)}</p><a href="/#{anchor}">{link}</a></section>'
    answers = "".join(f'<details><summary>{escape(q)}</summary><p>{escape(faqs[q])}</p></details>' for q in questions if q in faqs)
    if answers:
        body += '<section><h2>Applicant questions</h2>'+answers+'</section>'
    body += f'<p><a href="{escape(handbook)}">Read the official programme handbook</a></p><p><a class="cta" href="{escape(cta)}">Register your free interest</a></p>'
    body += '<nav aria-label="Related guides"><h2>Related guides</h2>'+guide_links(slug)+'</nav></main>'
    body += f'<footer><a href="{ACADEMY}">EuroPolytech Academy</a> · Maia, Greater Porto<br><a href="mailto:meritgate@europolytech.academy">meritgate@europolytech.academy</a></footer>'
    folder = output / slug
    folder.mkdir(exist_ok=True)
    (folder/"index.html").write_text('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'+
        f'<link rel="icon" href="{escape(urljoin(BASE,inventory.icon))}">'+head(path,title,desc,image,alt,label)+f'<style>{CSS}</style></head><body>{body}</body></html>')
root = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
for path in [""] + [guide[0]+"/" for guide in GUIDES]:
    ET.SubElement(ET.SubElement(root,"url"),"loc").text = BASE + path
ET.ElementTree(root).write(output/"sitemap.xml", encoding="utf-8", xml_declaration=True)
(output/"robots.txt").write_text("User-agent: *\nAllow: /\n\nSitemap: "+BASE+"sitemap.xml\n")
staff = output/"staff/index.html"
staff.write_text('<meta name="robots" content="noindex,follow">'+staff.read_text())
