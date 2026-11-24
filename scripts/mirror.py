"""Build the public MeritGate mirror from an anonymous published response."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.request import Request, urlopen
import hashlib
import re
import sys

origin = "https://meritgate-2027.amigorn.chatgpt.site"
output = Path(sys.argv[1])
output.mkdir(parents=True, exist_ok=True)
assets = output / "assets"
assets.mkdir(exist_ok=True)

def read(path):
    with urlopen(Request(origin + path, headers={"User-Agent": "MeritGate-Publisher/1.0"}), timeout=60) as response:
        return response.headers.get_content_type(), response.read()

kind, data = read("/")
page = data.decode()
if kind != "text/html" or '<title>MeritGate' not in page or 'href="/staff"' not in page:
    raise RuntimeError("Published MeritGate landing page unavailable")
pattern = r"""(?<=["' (])/(?:media/[0-9a-f-]{36}|films/[\w.-]+|video-thumbnails/[\w-]+\.jpg|[\w-]+\.webp)(?=["' ),])"""
paths = sorted(set(re.findall(pattern, page)))
def copy(path):
    mime, body = read(path)
    suffix = {"image/webp":"webp","image/jpeg":"jpg","image/png":"png","image/svg+xml":"svg","image/gif":"gif","video/mp4":"mp4"}.get(mime)
    if not suffix or not body:
        raise ValueError("Missing published media: " + path)
    name = hashlib.sha256(body).hexdigest() + "." + suffix
    (assets / name).write_bytes(body)
    return path, "./assets/" + name

with ThreadPoolExecutor(max_workers=5) as pool:
    replacements = dict(pool.map(copy, paths))
page = re.sub(pattern, lambda m: replacements[m[0]], page)
page = page.replace('href="/staff"', 'href="'+origin+'/staff"').replace('href="/"','href="./"')
# If the backstage switches from Zoho to the built-in form, submit on its own origin.
page = re.sub(r'<button([^>]*?) data-dialog="interest">([^<]*)</button>',r'<a\1 href="'+origin+'/">\2</a>',page)
(output / "index.html").write_text(page)
staff = output / "staff"
staff.mkdir(exist_ok=True)
(staff / "index.html").write_text('<meta http-equiv="refresh" content="0;url='+origin+'/staff"><a href="'+origin+'/staff">Staff Access</a>')
(output / ".nojekyll").touch()
print("Built public page with",len(paths),"published media references.")
