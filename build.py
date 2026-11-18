#!/usr/bin/env python3
"""
Baut die Website aus den Bausteinen in src/ zusammen.

Warum ein Generator: Kopfbereich, Navigation und Fussbereich sind auf allen 12 Seiten gleich.
Ohne das hier muesste jede Aenderung an der Navigation zwoelfmal gemacht werden.

Aufruf:  python3 build.py
Ergebnis: index.html, services.html, ... und de/index.html, de/leistungen.html, ...
"""
import io, os, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "src")

CALENDLY = "https://calendly.com/uniqueyou-uniquebusiness-info/30min"
MAIL = "info@uniqueyou-media.com"
PHONE_HREF = "+4917666102893"
PHONE_TEXT = "+49 176 66102893"
INSTA = "https://www.instagram.com/uniqueyou.media"
YOUTUBE = "https://www.youtube.com/@uniqueyou-uniquebusiness"
SPOTIFY = "https://open.spotify.com/show/11qUJz6ZRBWw349e3VrK8v"

ICON_INSTA = ('<svg viewBox="0 0 24 24" fill="none" aria-hidden="true">'
              '<rect x="3.2" y="3.2" width="17.6" height="17.6" rx="5" stroke="currentColor" stroke-width="1.8"/>'
              '<circle cx="12" cy="12" r="4.1" stroke="currentColor" stroke-width="1.8"/>'
              '<circle cx="17.3" cy="6.7" r="1.25" fill="currentColor"/></svg>')
ICON_YT = ('<svg viewBox="0 0 24 24" fill="none" aria-hidden="true">'
           '<path d="M21.6 7.3a2.5 2.5 0 0 0-1.76-1.77C18.25 5.1 12 5.1 12 5.1s-6.25 0-7.84.43A2.5 2.5 0 0 0 2.4 7.3 26 26 0 0 0 2 12a26 26 0 0 0 .4 4.7 2.5 2.5 0 0 0 1.76 1.77c1.59.43 7.84.43 7.84.43s6.25 0 7.84-.43a2.5 2.5 0 0 0 1.76-1.77A26 26 0 0 0 22 12a26 26 0 0 0-.4-4.7z" stroke="currentColor" stroke-width="1.8"/>'
           '<path d="M10.3 14.9V9.1l5 2.9z" fill="currentColor"/></svg>')
ICON_SPOTIFY = ('<svg viewBox="0 0 24 24" fill="none" aria-hidden="true">'
                '<circle cx="12" cy="12" r="9.1" stroke="currentColor" stroke-width="1.8"/>'
                '<path d="M7.3 9.5c3-.8 6.3-.5 8.9.9M7.9 12.5c2.5-.7 5.2-.4 7.4.8M8.5 15.4c2-.5 4.2-.3 6 .7" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/></svg>')


def social_row(lang):
    insta = "Instagram" if lang == "en" else "Instagram"
    yt = "YouTube"
    sp = "Podcast on Spotify" if lang == "en" else "Podcast auf Spotify"
    return (f'<div class="social">'
            f'<a href="{INSTA}" target="_blank" rel="noopener" aria-label="{insta}" title="{insta}">{ICON_INSTA}</a>'
            f'<a href="{YOUTUBE}" target="_blank" rel="noopener" aria-label="{yt}" title="{yt}">{ICON_YT}</a>'
            f'<a href="{SPOTIFY}" target="_blank" rel="noopener" aria-label="{sp}" title="{sp}">{ICON_SPOTIFY}</a>'
            f'</div>')

ARROW = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" '
         'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
         '<path d="M5 12h13M13 6l6 6-6 6"/></svg>')


def read(name):
    with io.open(os.path.join(SRC, name), encoding="utf-8") as f:
        return f.read()


SPRITE = read("_sprite.html")
_qr = read("_qr.txt").split("\n")
QR_SVG = ('<svg viewBox="0 0 %s %s" role="img" aria-label="QR code linking to uniqueyou-media.com">'
          '<path fill="#17547d" d="%s"/></svg>' % (_qr[0], _qr[0], _qr[1]))

# ---------------------------------------------------------------- Seitenregister
# slug: (Dateiname EN, Dateiname DE, Menuetitel EN, Menuetitel DE)
# Deutsch ist die Hauptsprache und liegt im Wurzelverzeichnis,
# Englisch liegt unter en/.
# slug: (Datei EN, Datei DE, Menuetitel EN, Menuetitel DE)
PAGES = [
    ("home",     "en/index.html",    "index.html",        "Home",     "Start"),
    ("services", "en/services.html", "leistungen.html",   "Services", "Leistungen"),
    ("work",     "en/work.html",     "referenzen.html",   "Work",     "Referenzen"),
    ("about",    "en/about.html",    "ueber-uns.html",    "About",    "Über uns"),
    ("process",  "en/process.html",  "ablauf.html",       "Process",  "Ablauf"),
    ("legal",    "en/legal.html",    "rechtliches.html",  "Imprint",  "Impressum"),
]
NAV_SLUGS = ["services", "work", "about", "process"]
BY_SLUG = {p[0]: p for p in PAGES}

TEXT = {
    "en": {
        "talk": "Let&rsquo;s talk",
        "menu": "Menu",
        "foot_blurb": ("Social media and personal branding for business owners. "
                       "Remote worldwide, on site when it helps."),
        "foot_pages": "Pages",
        "foot_contact": "Contact",
        "foot_legal": "Legal",
        "imprint": "Imprint and privacy",
        "based": "Bad Endorf, Germany",
        "rights": "Unique You Media &middot; Marina &amp; Alexander Mertens",
    },
    "de": {
        "talk": "Lass uns reden",
        "menu": "Menü",
        "foot_blurb": ("Social Media und Personal Branding für Unternehmer:innen. "
                       "Weltweit remote, vor Ort wenn es sich lohnt."),
        "foot_pages": "Seiten",
        "foot_contact": "Kontakt",
        "foot_legal": "Rechtliches",
        "imprint": "Impressum und Datenschutz",
        "based": "Bad Endorf, Deutschland",
        "rights": "Unique You Media &middot; Marina &amp; Alexander Mertens",
    },
}


def href(slug, target_lang, base):
    """Pfad zur Zielseite, relativ zu der Datei, die gerade gebaut wird.

    base ist "" wenn die aktuelle Seite im Wurzelverzeichnis liegt (englisch)
    und "../" wenn sie in de/ liegt (deutsch). Daraus leiten wir das
    Verzeichnis der aktuellen Seite ab und rechnen den relativen Pfad aus.
    """
    target = BY_SLUG[slug][1] if target_lang == "en" else BY_SLUG[slug][2]
    here = "en" if base else "."
    return os.path.relpath(target, here)


def build_head(lang, slug, title, desc, base):
    other = "de" if lang == "en" else "en"
    en_url = "https://uniqueyou-media.com/" + BY_SLUG[slug][1].replace("index.html", "")
    de_url = "https://uniqueyou-media.com/" + BY_SLUG[slug][2].replace("index.html", "")
    self_url = en_url if lang == "en" else de_url
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#F4F0E8">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{self_url}">
<link rel="alternate" hreflang="en" href="{en_url}">
<link rel="alternate" hreflang="de" href="{de_url}">
<link rel="alternate" hreflang="x-default" href="{de_url}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:url" content="{self_url}">
<link rel="stylesheet" href="{base}assets/site.css">
<script>if('IntersectionObserver' in window&&!matchMedia('print').matches)document.documentElement.className+=' js';</script>
</head>
<body>
"""


def build_header(lang, slug, base):
    t = TEXT[lang]
    links = []
    mob = []
    for s in NAV_SLUGS:
        label = BY_SLUG[s][3 if lang == "en" else 4]
        cur = ' aria-current="page"' if s == slug else ""
        links.append(f'<a href="{href(s, lang, base)}"{cur}>{label}</a>')
        mob.append(f'<li><a href="{href(s, lang, base)}"{cur}>{label}</a></li>')

    # Sprachumschalter: zeigt auf dieselbe Seite in der anderen Sprache
    en_href = href(slug, "en", base)
    de_href = href(slug, "de", base)

    return f"""<header class="site-head" id="head">
  <div class="sheet head-in">
    <a class="brand" href="{href('home', lang, base)}">
      <svg viewBox="0 0 1156 1140" aria-hidden="true"><use href="#mark"/></svg>
      <span><b>unique you</b> <span>media</span></span>
    </a>
    <nav class="nav" aria-label="{t['menu']}">{''.join(links)}</nav>
    <div class="head-side">
      <div class="lang">
        <a href="{de_href}"{' aria-current="true"' if lang == 'de' else ''} hreflang="de">DE</a>
        <span>/</span>
        <a href="{en_href}"{' aria-current="true"' if lang == 'en' else ''} hreflang="en">EN</a>
      </div>
      <a class="btn" href="{CALENDLY}" target="_blank" rel="noopener">{t['talk']}{ARROW}</a>
      <button class="burger" type="button" aria-expanded="false" aria-controls="mnav" aria-label="{t['menu']}"><i></i></button>
    </div>
  </div>
  <nav class="mobile-nav" id="mnav" aria-label="{t['menu']}">
    <div class="sheet">
      <ul>{''.join(mob)}</ul>
      <a class="btn" href="{CALENDLY}" target="_blank" rel="noopener">{t['talk']}{ARROW}</a>
    </div>
  </nav>
</header>
"""


def build_footer(lang, base):
    t = TEXT[lang]
    social = social_row(lang)
    page_links = "".join(
        f'<li><a href="{href(s, lang, base)}">{BY_SLUG[s][3 if lang == "en" else 4]}</a></li>'
        for s in NAV_SLUGS)
    return f"""<footer class="site-foot">
  <div class="sheet">
    <div class="foot-grid">
      <div>
        <a class="brand" href="{href('home', lang, base)}" style="margin-bottom:14px">
          <svg viewBox="0 0 1156 1140" aria-hidden="true"><use href="#mark"/></svg>
          <span><b>unique you</b> <span>media</span></span>
        </a>
        <p>{t['foot_blurb']}</p>
      </div>
      <div>
        <h4>{t['foot_pages']}</h4>
        <ul>{page_links}</ul>
      </div>
      <div>
        <h4>{t['foot_contact']}</h4>
        <ul>
          <li><a href="mailto:{MAIL}">{MAIL}</a></li>
          <li><a href="tel:{PHONE_HREF}">{PHONE_TEXT}</a></li>
          <li><a href="{INSTA}" target="_blank" rel="noopener">@uniqueyou.media</a></li>
        </ul>
        {social}
      </div>
      <div>
        <h4>{t['foot_legal']}</h4>
        <ul>
          <li><a href="{href('legal', lang, base)}">{t['imprint']}</a></li>
        </ul>
      </div>
    </div>
    <div class="foot-bar">
      <span>{t['rights']} &middot; {t['based']}</span>
      <span>&copy; 2026</span>
    </div>
  </div>
</footer>
"""


SCRIPT = """<script src="%sassets/site.js" defer></script>
</body>
</html>
"""


def build_page(lang, slug):
    base = "../" if lang == "en" else ""
    frag = read(("en/" if lang == "en" else "de/") + slug + ".html")

    m = re.match(r"\s*<!--\s*title:\s*(.*?)\s*\|\s*desc:\s*(.*?)\s*-->\s*", frag, re.S)
    if not m:
        sys.exit(f"FEHLER: {lang}/{slug}.html hat keine title/desc-Kopfzeile")
    title, desc, body = m.group(1), m.group(2), frag[m.end():]

    body = (body.replace("{{CAL}}", CALENDLY)
                .replace("{{ARROW}}", ARROW)
                .replace("{{MAIL}}", MAIL)
                .replace("{{PHONE_HREF}}", PHONE_HREF)
                .replace("{{PHONE}}", PHONE_TEXT)
                .replace("{{INSTA}}", INSTA)
                .replace("{{YOUTUBE}}", YOUTUBE)
                .replace("{{SPOTIFY}}", SPOTIFY)
                .replace("{{SOCIAL}}", social_row(lang))
                .replace("{{QR}}", QR_SVG)
                .replace("{{BASE}}", base)
                .replace("{{TALK}}", TEXT[lang]["talk"]))
    for s in [p[0] for p in PAGES]:
        body = body.replace("{{%s}}" % s.upper(), href(s, lang, base))

    # Interne Notizen gehoeren nicht in die veroeffentlichte Seite
    body = re.sub(r"[ \t]*<!--\s*TODO.*?-->\n?", "", body, flags=re.S)

    html = (build_head(lang, slug, title, desc, base)
            + SPRITE + "\n"
            + build_header(lang, slug, base)
            + body
            + build_footer(lang, base)
            + SCRIPT % base)

    out = os.path.join(ROOT, BY_SLUG[slug][1] if lang == "en" else BY_SLUG[slug][2])
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with io.open(out, "w", encoding="utf-8") as f:
        f.write(html)
    return out, len(html)


if __name__ == "__main__":
    built, missing = [], []
    for lang in ("en", "de"):
        for p in PAGES:
            frag = os.path.join(SRC, lang, p[0] + ".html")
            if not os.path.exists(frag):
                missing.append(f"{lang}/{p[0]}.html")
                continue
            out, n = build_page(lang, p[0])
            built.append(f"  {os.path.relpath(out, ROOT):26s} {n:>7,} Zeichen")
    print("Gebaut:")
    print("\n".join(built))
    if missing:
        print("\nNoch keine Vorlage fuer:")
        for m in missing:
            print("  " + m)
