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
YOUTUBE = "https://www.youtube.com/@uniqueyoumedia"
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
                       "Remote worldwide, on site when needed."),
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
                       "Weltweit remote und vor Ort bei Bedarf."),
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
<link rel="icon" href="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxMjgwIDEyODAiPjxyZWN0IHdpZHRoPSIxMjgwIiBoZWlnaHQ9IjEyODAiIHJ4PSIyODAiIGZpbGw9IiMwRjNBNTciLz48ZyB0cmFuc2Zvcm09InRyYW5zbGF0ZSgtMTk4IC0xODYpIHNjYWxlKDEpIj48cGF0aCBmaWxsPSIjQ0JGRjAwIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiIGQ9Ik01OTMsMTA2IFE1NjQsMTA2IDU1MCwxMDcgUTUzNiwxMDkgNTE2LDExMyBRNDk2LDExOCA0NzQsMTI1IFE0NTIsMTMzIDQ0MSwxMzggUTQzMSwxNDMgNDIzLDE0OSBRNDE1LDE1NiA0MTIsMTYxIFE0MTAsMTY2IDQxMSwxNzUgUTQxMiwxODMgNDE3LDE4OSBRNDIyLDE5NCA0MjYsMTk2IFE0MzEsMTk5IDQzNiwxOTkgUTQ0MCwxOTkgNDYzLDE4OSBRNDg3LDE3OSA0OTgsMTc1IFE1MDksMTcyIDUyNywxNjggUTU0NSwxNjQgNTYwLDE2MiBRNTc1LDE2MSA1ODksMTYxIFE2MDMsMTYxIDYyMSwxNjMgUTYzOCwxNjUgNjYzLDE3MiBRNjg4LDE4MCA3MTAsMTkwIFE3MzEsMjAwIDc1NiwyMTggUTc4MCwyMzcgODAxLDI1OSBRODIxLDI4MSA4MzQsMzAxIFE4NDcsMzIxIDg1MywzMzMgUTg1OSwzNDYgODY3LDM2OCBRODc1LDM5MCA4ODAsNDIzIFE4ODUsNDU3IDg4NSw1OTUgUTg4Niw3MzIgODgxLDc3MiBRODc3LDgxMiA4ODcsNzk5IFE4OTYsNzg2IDkwOCw3NjMgUTkxOSw3MzkgOTI2LDcxNyBROTM0LDY5NCA5MzYsNjc0IFE5MzksNjU0IDkzOSw1OTMgUTk0MCw1MzIgOTM5LDQ4NyBROTM4LDQ0MyA5MzMsNDEwIFE5MjgsMzc4IDkxOCwzNTEgUTkwOSwzMjQgODk5LDMwNCBRODg5LDI4NCA4NzMsMjYwIFE4NTYsMjM2IDgzMiwyMTEgUTgwOCwxODcgNzg1LDE3MCBRNzYyLDE1NCA3NDIsMTQzIFE3MjIsMTMzIDY5NCwxMjMgUTY2NiwxMTQgNjQ1LDExMCBRNjIzLDEwNyA1OTMsMTA2IFogTTU5MywxODUgUTU2OSwxODUgNTU0LDE4NyBRNTM5LDE4OSA1MjYsMTkyIFE1MTQsMTk1IDUwMCwxOTkgUTQ4NiwyMDQgNDczLDIxMCBRNDYxLDIxNiA0NDUsMjI1IFE0MzAsMjM1IDQyMCwyNDIgUTQxMSwyNTAgMzkyLDI2OSBRMzczLDI4OCAzNTgsMzExIFEzNDMsMzM0IDMzNywzNDUgUTMzMiwzNTcgMzI3LDM3MCBRMzIzLDM4NCAzMTcsNDExIFEzMTIsNDM4IDMxMSw0NTEgUTMxMCw0NjQgMzEwLDQ4MiBRMzExLDQ5OSAzMTQsNTA2IFEzMTcsNTEyIDMyMyw1MTcgUTMzMCw1MjIgMzM4LDUyMiBRMzQ1LDUyMiAzNTEsNTE3IFEzNTYsNTEzIDM1OSw1MDggUTM2MSw1MDMgMzYyLDQ5OCBRMzY0LDQ5MiAzNjQsNDczIFEzNjQsNDU0IDM2Nyw0MzQgUTM3MCw0MTUgMzc0LDM5OSBRMzc5LDM4NCAzODQsMzczIFEzODksMzYyIDQwMSwzNDMgUTQxNCwzMjQgNDI3LDMxMCBRNDQwLDI5NyA0NTMsMjg3IFE0NjcsMjc3IDQ4MywyNjggUTUwMCwyNTkgNTE3LDI1MyBRNTM0LDI0NyA1NTAsMjQ0IFE1NjYsMjQxIDU4NiwyNDEgUTYwNiwyNDEgNjIyLDI0MyBRNjM3LDI0NiA2NTQsMjUyIFE2NzEsMjU4IDY4NiwyNjYgUTcwMCwyNzQgNzE0LDI4NCBRNzI4LDI5NSA3NDAsMzA2IFE3NTEsMzE4IDc2MiwzMzMgUTc3MywzNDggNzgxLDM2MiBRNzg4LDM3NyA3OTQsMzkyIFE4MDAsNDA4IDgwMyw0MjQgUTgwNyw0NDEgODA4LDQ2NSBRODEwLDQ5MCA4MTAsNTk1IFE4MTAsNjk5IDgwOSw3MjAgUTgwOCw3NDAgODA2LDc1NSBRODA0LDc2OSA3OTcsNzk3IFE3OTEsODI1IDc4MSw4NTAgUTc3MSw4NzUgNzYxLDg5NCBRNzUxLDkxMyA3NDIsOTI4IFE3MzIsOTQzIDczMSw5NDQgUTczMSw5NDYgNzMxLDk0NiBRNzMyLDk0NyA3NDQsOTQxIFE3NTUsOTM2IDc2Niw5MzAgUTc3Niw5MjMgNzgzLDkxOCBRNzg5LDkxMyA3OTksOTAzIFE4MDksODkyIDgxNiw4ODMgUTgyMiw4NzQgODI5LDg2MSBRODM2LDg0NyA4NDUsODIxIFE4NTUsNzk0IDg1OSw3NjcgUTg2Myw3MzkgODYzLDYwMyBRODYzLDQ2NyA4NTksNDMzIFE4NTUsNDAwIDg0NSwzNzMgUTgzNiwzNDcgODI0LDMyNiBRODEyLDMwNiA4MDEsMjkyIFE3OTAsMjc4IDc2OCwyNTcgUTc0NSwyMzcgNzE2LDIyMCBRNjg3LDIwNCA2NzMsMTk5IFE2NTgsMTk0IDYzOCwxOTAgUTYxOCwxODYgNTkzLDE4NSBaIE0zNjMsMTk5IFEzNTcsMTk5IDM1MiwyMDEgUTM0NywyMDQgMzQwLDIxMCBRMzMzLDIxNyAzMjUsMjI2IFEzMTcsMjM1IDMwNCwyNTMgUTI5MiwyNzEgMjc4LDI5NSBRMjY1LDMyMCAyNTUsMzQ2IFEyNDYsMzczIDI0MiwzOTEgUTIzOCw0MTAgMjM1LDQzNSBRMjMzLDQ2MCAyMzMsNTY0IFEyMzQsNjY3IDIzNyw2ODQgUTI0MSw3MDEgMjQ4LDcxOCBRMjU1LDczNSAyNjYsNzUyIFEyNzgsNzY5IDI4OSw3ODEgUTMwMSw3OTIgMzE1LDgwMiBRMzI5LDgxMiAzNDgsODIwIFEzNjgsODI5IDM4MSw4MzEgUTM5NSw4MzQgNDEyLDgzNCBRNDI4LDgzNSA0MzksODMzIFE0NDksODMyIDQ2NCw4MjcgUTQ3OSw4MjIgNDk4LDgxMSBRNTE3LDgwMCA1MjcsNzkyIFE1MzYsNzgzIDU0NCw3NzQgUTU1Miw3NjQgNTU3LDc1NSBRNTYyLDc0NiA1NjIsNzQyIFE1NjMsNzM4IDU2MSw3MzIgUTU1OSw3MjcgNTU2LDcyMyBRNTUzLDcyMCA1NDgsNzE3IFE1NDIsNzE1IDUzOCw3MTQgUTUzMyw3MTQgNTI1LDcxOCBRNTE4LDcyMiA1MDIsNzM4IFE0ODUsNzU0IDQ3NCw3NjEgUTQ2Miw3NjggNDQ2LDc3MyBRNDMwLDc3OCA0MTEsNzc3IFEzOTIsNzc3IDM3Niw3NzEgUTM2MSw3NjYgMzQ3LDc1NyBRMzMzLDc0NyAzMjMsNzM3IFEzMTMsNzI2IDMwNSw3MTEgUTI5Nyw2OTYgMjkzLDY4NCBRMjkwLDY3MiAyODgsNjYwIFEyODcsNjQ4IDI4Nyw1NjIgUTI4Nyw0NzUgMjg4LDQ1MyBRMjkwLDQzMSAyOTYsNDAzIFEzMDIsMzc1IDMxMiwzNTAgUTMyMiwzMjUgMzMzLDMwNyBRMzQ0LDI4OSAzNTUsMjc1IFEzNjYsMjYyIDM3NCwyNTUgUTM4MSwyNDcgMzg2LDI0MCBRMzkxLDIzMiAzOTAsMjI0IFEzOTAsMjE2IDM4NSwyMDkgUTM4MCwyMDMgMzc1LDIwMSBRMzcwLDE5OSAzNjMsMTk5IFogTTU5MywyNjQgUTU3OSwyNjQgNTY4LDI2NSBRNTU4LDI2NiA1NDQsMjY5IFE1MzEsMjcyIDUxNiwyNzggUTUwMSwyODQgNDg2LDI5MyBRNDcxLDMwMiA0NjQsMzA3IFE0NTcsMzEzIDQ0NSwzMjUgUTQzMywzMzggNDIzLDM1MiBRNDE0LDM2NiA0MDgsMzc4IFE0MDIsMzkwIDM5Niw0MDggUTM5MSw0MjYgMzg5LDQzOSBRMzg3LDQ1MyAzODYsNTQ3IFEzODYsNjQxIDM4OSw2NDkgUTM5Myw2NTcgMzk4LDY2MSBRNDAzLDY2NSA0MTAsNjY2IFE0MTgsNjY4IDQyMiw2NjYgUTQyNiw2NjQgNDMwLDY2MSBRNDMzLDY1OCA0MzYsNjUyIFE0MzksNjQ1IDQzOSw1NTggUTQ0MCw0NzAgNDQxLDQ2MCBRNDQyLDQ1MSA0NDQsNDM4IFE0NDcsNDI2IDQ1MCw0MTYgUTQ1NCw0MDYgNDY0LDM4OSBRNDc1LDM3MiA0ODMsMzYzIFE0OTIsMzU1IDUwMywzNDcgUTUxNSwzMzkgNTMwLDMzMiBRNTQ1LDMyNiA1NTgsMzIzIFE1NzIsMzIxIDU4NywzMjEgUTYwMSwzMjEgNjEzLDMyMyBRNjI0LDMyNSA2NDEsMzMyIFE2NTcsMzM5IDY3MywzNDkgUTY4OSwzNTkgNjk2LDM1OCBRNzAzLDM1NyA3MDYsMzU2IFE3MDksMzU0IDcxMywzNDkgUTcxNywzNDQgNzE5LDMzNSBRNzIxLDMyNSA3MTgsMzIxIFE3MTYsMzE3IDcxMCwzMTAgUTcwNCwzMDQgNjk1LDI5NyBRNjg1LDI5MSA2NjksMjgzIFE2NTIsMjc2IDY0MSwyNzIgUTYzMCwyNjkgNjE5LDI2NyBRNjA3LDI2NSA1OTMsMjY0IFogTTU4NiwzNDcgUTU4MCwzNDcgNTY1LDM1MCBRNTUwLDM1MyA1NDEsMzU3IFE1MzMsMzYxIDUyNiwzNjYgUTUxOSwzNzEgNTI3LDM3NiBRNTM2LDM4MSA1NTAsMzkzIFE1NjMsNDA0IDU3MCw0MDggUTU3OCw0MTMgNTg0LDQxMyBRNTkwLDQxNCA1OTgsNDEwIFE2MDYsNDA3IDYyMywzOTQgUTYzOSwzODAgNjQ3LDM3NSBRNjU2LDM3MSA2NDcsMzY1IFE2MzksMzYwIDYyOCwzNTUgUTYxNywzNTEgNjA1LDM0OSBRNTkyLDM0NyA1ODYsMzQ3IFogTTc1MywzNzMgUTc0NSwzNzAgNzM3LDM3MiBRNzMwLDM3NSA3MjQsMzgyIFE3MTksMzkwIDcxOSwzOTkgUTcxOSw0MDcgNzI1LDQyNiBRNzMxLDQ0NSA3MzIsNDY4IFE3MzQsNDkyIDczNCw2MDggUTczNCw3MjQgNzMyLDc0MCBRNzMwLDc1NSA3MjUsNzc2IFE3MjAsNzk2IDcxMSw4MTcgUTcwMyw4MzcgNjg3LDg2NCBRNjcwLDg5MSA2NTgsOTA2IFE2NDUsOTIxIDYzMyw5MzMgUTYyMSw5NDUgNjA4LDk1NyBRNTk0LDk2OSA1ODcsOTc3IFE1ODEsOTg1IDU5NSw5ODQgUTYwOCw5ODMgNjI0LDk3OSBRNjQwLDk3NiA2NTUsOTY5IFE2NjksOTYzIDY3OSw5NTcgUTY4OCw5NTAgNzA0LDkzMyBRNzIwLDkxNSA3MjksOTAzIFE3MzcsODkwIDc0OCw4NjggUTc1OSw4NDYgNzY3LDgyMiBRNzc2LDc5OCA3ODEsNzczIFE3ODYsNzQ4IDc4Nyw3MjYgUTc4OSw3MDMgNzg5LDU5NiBRNzg5LDQ4OSA3ODgsNDczIFE3ODcsNDU4IDc4NCw0NDAgUTc4Miw0MjIgNzc3LDQwNyBRNzcyLDM5MiA3NjcsMzg0IFE3NjEsMzc2IDc1MywzNzMgWiBNNDkyLDQwOCBRNDYyLDQwOCA0NzMsNDI4IFE0ODUsNDQ4IDUxNCw0OTQgUTU0Myw1NDAgNTUwLDU1MyBRNTU3LDU2NiA1NTgsNTcwIFE1NjAsNTc1IDU2MCw2MjUgUTU2MCw2NzQgNTYyLDY4NCBRNTY0LDY5NCA1NjcsNjk4IFE1NzEsNzAyIDU3NCw3MDQgUTU3OCw3MDcgNTg0LDcwNyBRNTkwLDcwOCA1OTQsNzA2IFE1OTcsNzA1IDYwMyw3MDAgUTYwOSw2OTUgNjExLDY4NyBRNjE0LDY3OCA2MTQsNjI3IFE2MTQsNTc2IDYxNSw1NzAgUTYxNyw1NjQgNjY1LDQ4NiBRNzEyLDQwOSA2ODEsNDA4IFE2NTAsNDA4IDYzOSw0MjQgUTYyOCw0NDEgNjE4LDQ1OSBRNjA3LDQ3NiA1OTcsNDkxIFE1ODcsNTA2IDU1NSw0NTcgUTUyMyw0MDggNDkyLDQwOCBaIE03MDMsNDc3IFE3MDMsNDc3IDY4Myw1MDggUTY2NCw1MzkgNjYwLDU0NyBRNjU3LDU1NiA2NTUsNTcxIFE2NTQsNTg2IDY1NSw2MzEgUTY1Nyw2NzYgNjU2LDcwNiBRNjU2LDczNiA2NTEsNzU0IFE2NDcsNzcyIDYzNyw3OTUgUTYyNyw4MTcgNjExLDgzOSBRNTk1LDg2MSA1NzcsODc4IFE1NTksODk1IDU0Nyw5MDMgUTUzNCw5MTEgNTIxLDkxNyBRNTA4LDkyMyA0ODYsOTMwIFE0NjMsOTM3IDQ0OSw5MzkgUTQzNSw5NDIgNDM1LDk0MyBRNDM1LDk0NCA0NDAsOTQ3IFE0NDUsOTUwIDQ2NCw5NTkgUTQ4Myw5NjggNDkyLDk3MCBRNTAyLDk3MyA1MTQsOTcyIFE1MjYsOTcyIDU0MCw5NjcgUTU1Myw5NjIgNTcwLDk1MiBRNTg3LDk0MiA1OTgsOTMzIFE2MDksOTI0IDYyMiw5MTEgUTYzNSw4OTcgNjUyLDg3MyBRNjY5LDg0OSA2ODEsODIzIFE2OTQsNzk2IDY5OCw3ODEgUTcwMiw3NjYgNzA1LDc0NyBRNzA4LDcyNyA3MDgsNjE3IFE3MDgsNTA3IDcwNyw0OTcgUTcwNyw0ODggNzA1LDQ4MiBRNzA0LDQ3NyA3MDMsNDc3IFogTTQ3Myw0ODEgUTQ3MCw0NzggNDY4LDQ4MSBRNDY3LDQ4NSA0NjYsNDk1IFE0NjYsNTA2IDQ2NSw1NzggUTQ2NCw2NDkgNDYwLDY2MCBRNDU2LDY3MSA0NDgsNjgwIFE0NDAsNjg4IDQzMiw2OTIgUTQyMyw2OTYgNDE2LDY5NiBRNDA4LDY5NyA0MDEsNjk1IFEzOTUsNjkzIDM4OSw2OTAgUTM4NCw2ODcgMzc4LDY4MSBRMzcyLDY3NCAzNjksNjY3IFEzNjYsNjU5IDM2NSw2NTIgUTM2NCw2NDQgMzY0LDYxNSBRMzY0LDU4NSAzNjEsNTc5IFEzNTksNTczIDM1NCw1NjggUTM0OCw1NjQgMzQwLDU2MiBRMzMyLDU2MSAzMjUsNTY0IFEzMTgsNTY4IDMxNSw1NzIgUTMxMyw1NzYgMzExLDU4MyBRMzEwLDU5MSAzMTAsNjIwIFEzMTAsNjQ5IDMxMyw2NjcgUTMxNyw2ODUgMzIzLDY5NyBRMzI5LDcwOCAzMzUsNzE2IFEzNDIsNzI0IDM0OCw3MjkgUTM1NCw3MzQgMzYzLDc0MCBRMzczLDc0NSAzODUsNzQ5IFEzOTgsNzUzIDQwOSw3NTMgUTQxOSw3NTQgNDMxLDc1MiBRNDQyLDc1MCA0NTEsNzQ2IFE0NTksNzQzIDQ2OSw3MzcgUTQ3OSw3MzAgNDg3LDcyMyBRNDk0LDcxNSA1MDIsNzAxIFE1MTAsNjg3IDUxNCw2NjYgUTUxOSw2NDQgNTE4LDYwMiBRNTE4LDU2MCA1MTEsNTQ2IFE1MDUsNTMyIDQ5MSw1MDggUTQ3Niw0ODUgNDczLDQ4MSBaIE01OTIsNzYzIFE1ODUsNzYzIDU4MCw3NjUgUTU3Niw3NjggNTcxLDc3MiBRNTY3LDc3NyA1NTcsNzkwIFE1NDcsODAzIDUzNSw4MTQgUTUyMyw4MjUgNTE2LDgzMCBRNTA4LDgzNSA0OTEsODQzIFE0NzQsODUxIDQ2Myw4NTQgUTQ1Miw4NTcgNDQwLDg1OCBRNDI3LDg2MCA0MDYsODU4IFEzODQsODU3IDM2Myw4NTAgUTM0Miw4NDQgMzI2LDgzNSBRMzEwLDgyNyAzMDksODMwIFEzMDksODMzIDMxMCw4NDAgUTMxMiw4NDcgMzE3LDg1NyBRMzIzLDg2NyAzMjgsODczIFEzMzQsODc5IDM0Nyw4ODkgUTM2MCw4OTggMzcyLDkwNCBRMzg0LDkxMCAzOTQsOTEyIFE0MDUsOTE1IDQyMSw5MTUgUTQzNyw5MTUgNDUzLDkxMyBRNDY5LDkxMSA0ODEsOTA4IFE0OTMsOTA1IDUxNCw4OTUgUTUzNCw4ODUgNTQ5LDg3NSBRNTYzLDg2NCA1NzYsODUyIFE1ODgsODM5IDU5OSw4MjUgUTYwOSw4MTEgNjEzLDgwMyBRNjE4LDc5NCA2MTgsNzg5IFE2MTgsNzgzIDYxNiw3NzkgUTYxNCw3NzYgNjExLDc3MiBRNjA4LDc2OSA2MDQsNzY2IFE1OTksNzY0IDU5Miw3NjMgWiIvPjwvZz48L3N2Zz4=">
<link rel="icon" href="{base}favicon-32.png" sizes="32x32" type="image/png">
<link rel="icon" href="{base}favicon-96.png" sizes="96x96" type="image/png">
<link rel="apple-touch-icon" href="{base}apple-touch-icon.png">
<link rel="manifest" href="{base}site.webmanifest">
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
<link rel="preload" href="{base}fonts/marina.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{base}fonts/instrument-sans-latin.woff2" as="font" type="font/woff2" crossorigin>
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
