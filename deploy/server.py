"""A dependency-free, accessible sample conference planner."""
import html
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlsplit

INTERESTS = ('AI', 'Kubernetes', 'Security', 'Data', 'Career')
NEEDS = {'step-free': 'Step-free access', 'captions': 'Captions', 'low-sensory': 'Low-sensory rooms', 'quiet-breaks': 'Quiet breaks'}
# Time, title, topic, room, supported access needs. Talks last 45 minutes.
TALKS = [
 ('09:00', 'AI that includes everyone', 'AI', 'Hall A', {'step-free', 'captions', 'low-sensory'}),
 ('09:00', 'Your first Kubernetes cluster', 'Kubernetes', 'Hall B', {'step-free', 'captions'}),
 ('10:00', 'Security without the jargon', 'Security', 'Studio', {'step-free', 'captions', 'low-sensory'}),
 ('10:00', 'Making data tell a story', 'Data', 'Hall B', {'step-free'}),
 ('11:00', 'Finding your next career step', 'Career', 'Studio', {'step-free', 'captions', 'low-sensory'}),
 ('11:00', 'Responsible AI in practice', 'AI', 'Hall A', {'step-free', 'captions'}),
 ('13:00', 'Kubernetes for humans', 'Kubernetes', 'Studio', {'step-free', 'captions', 'low-sensory'}),
 ('13:00', 'Protecting your data', 'Security', 'Hall B', {'captions'}),
 ('14:00', 'Open data, better decisions', 'Data', 'Studio', {'step-free', 'captions', 'low-sensory'}),
 ('14:00', 'Growing a sustainable career', 'Career', 'Hall A', {'step-free', 'captions'}),
]
esc = html.escape


def select_talks(interests, needs):
    schedule = {}
    for talk in TALKS:
        if (not interests or talk[2] in interests) and (needs - {'quiet-breaks'}) <= talk[4]:
            schedule.setdefault(talk[0], talk)
    return list(schedule.values())


def page(query):
    interests = set(query.get('interest', [])) & set(INTERESTS)
    needs = set(query.get('need', [])) & set(NEEDS)
    def checks(name, options, selected):
        return ''.join(f'<label><input type="checkbox" name="{name}" value="{esc(key)}" {"checked" if key in selected else ""}> {esc(label)}</label>' for key, label in options)
    controls = checks('interest', ((i, i) for i in INTERESTS), interests)
    access = checks('need', NEEDS.items(), needs)
    result = '<h2>Your day starts here</h2><p>Choose what matters to you, then build your itinerary. Leave interests unchecked to explore all topics.</p>'
    if 'plan' in query:
        talks = select_talks(interests, needs)
        cards = []
        for time, title, topic, room, features in talks:
            badges = ' · '.join(NEEDS[f] for f in NEEDS if f in features)
            cards.append(f'<li><p class="time">{time}–{time[:2]}:45 · {room}</p><h3>{title}</h3><p>{topic}</p><p>{badges}</p></li>')
            if 'quiet-breaks' in needs:
                cards.append(f'<li class="break"><h3>{time[:2]}:45–{int(time[:2])+1:02d}:00 · Quiet break</h3><p>Recharge in the sample quiet lounge before your next session.</p></li>')
        result = f'<h2 id="result-heading" tabindex="-1">Your personal itinerary</h2><p>{len(talks)} sessions scheduled. Each lasts 45 minutes.</p>'
        result += '<ol>' + ''.join(cards) + '</ol>' if cards else '<p>No sample talks match these choices. Try different interests or access needs to explore other options.</p>'
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>My Accessible Conference Day</title>
<style>
:root{{font:18px/1.6 system-ui,sans-serif;color:#18332e;background:#f1f5f2}}*{{box-sizing:border-box}}body{{margin:0}}header,main,footer{{max-width:1100px;margin:auto;padding:1.5rem}}header{{display:flex;flex-wrap:wrap;justify-content:space-between;gap:1rem;border-bottom:1px solid #adc2b7}}header strong{{align-self:center}}button{{font:inherit;min-height:48px;padding:.5rem 1rem;border:2px solid #075a47;border-radius:8px;color:#075a47;background:white;cursor:pointer}}button[aria-pressed=true],.primary{{background:#075a47;color:white}}h1{{font-size:clamp(2rem,5vw,3.5rem);line-height:1.15;max-width:850px}}h2{{line-height:1.3}}.eyebrow{{font-weight:bold;letter-spacing:.12em;font-size:.8rem;color:#075a47}}.intro{{max-width:750px}}.layout{{display:grid;grid-template-columns:1fr 1.2fr;gap:2rem;margin-top:2rem}}form,section{{padding:1.5rem;border:1px solid #adc2b7;background:white;border-radius:16px;align-self:start}}fieldset{{border:0;padding:0;margin:0 0 1.5rem}}legend{{font-weight:bold;font-size:1.2rem}}label{{display:flex;align-items:center;gap:.7rem;min-height:48px;cursor:pointer}}input{{width:24px;height:24px;accent-color:#075a47}}.primary{{width:100%;font-weight:bold}}ol{{list-style:none;padding:0}}li{{border-top:1px solid #adc2b7;padding:1rem 0}}h3{{margin:.4rem 0}}.time{{color:#075a47;font-weight:bold}}.break{{background:#edf5ef;padding:1rem;border-radius:8px}}:focus-visible{{outline:3px solid #aa4000;outline-offset:4px}}.skip{{position:absolute;top:-100px;background:white;padding:1rem;color:#075a47}}.skip:focus{{top:0}}footer{{font-size:.85rem}}.large{{font-size:23px}}.contrast{{color:white;background:black}}.contrast form,.contrast section,.contrast button,.contrast .break{{color:white;background:black;border-color:white}}.contrast .time,.contrast .eyebrow,.contrast a{{color:#ffeb00}}.contrast .primary,.contrast button[aria-pressed=true]{{background:#ffeb00;color:black}}.contrast :focus-visible{{outline-color:#ffeb00}}@media(max-width:760px){{.layout{{grid-template-columns:1fr}}header,main,footer{{padding:1rem}}}}
</style></head><body><a class="skip" href="#main">Skip to main content</a><header><strong>My Accessible Conference Day</strong><div aria-label="Display preferences"><button id="large" type="button" aria-pressed="false">Large text</button> <button id="contrast" type="button" aria-pressed="false">High contrast</button></div></header>
<main id="main"><p class="eyebrow">YOUR DAY. YOUR PACE.</p><h1>A conference day that works for you.</h1><p class="intro">Follow your interests. Plan around your access needs. Make room to recharge.</p><p><strong>Sample conference:</strong> these 10 fictional talks, their access features, and the quiet lounge demonstrate the planner.</p><div class="layout"><form method="get" action="/#itinerary"><h2>Make it your day</h2><fieldset><legend>Your interests</legend>{controls}</fieldset><fieldset><legend>Your access needs</legend>{access}</fieldset><p>All selected room access needs must match. Quiet breaks add 15 minutes after each talk. When talks overlap, the first matching talk is selected.</p><button class="primary" name="plan" value="1">Build my itinerary</button></form><section id="itinerary" aria-label="Itinerary">{result}</section></div></main>
<footer>cloud9 · Version {esc(os.environ.get('APP_VERSION', 'dev'))} · Your choices appear in the page URL. No account required.</footer>
<script>for(const id of ['large','contrast']){{const b=document.getElementById(id);const apply=v=>{{document.documentElement.classList.toggle(id,v);b.setAttribute('aria-pressed',String(v));}};try{{apply(localStorage.getItem(id)==='true');}}catch{{}}b.addEventListener('click',()=>{{const v=b.getAttribute('aria-pressed')!=='true';apply(v);try{{localStorage.setItem(id,String(v));}}catch{{}}}});}}if(location.hash==='#itinerary'){{document.getElementById('result-heading')?.focus();}}</script></body></html>'''


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        url = urlsplit(self.path)
        if url.path in ('/healthz', '/readyz', '/health'):
            body, content_type, status = b'OK\n', 'text/plain; charset=utf-8', 200
        elif url.path == '/':
            body, content_type, status = page(parse_qs(url.query)).encode(), 'text/html; charset=utf-8', 200
        else:
            body, content_type, status = b'Not found\n', 'text/plain; charset=utf-8', 404
        self.send_response(status)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', str(len(body)))
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.end_headers()
        self.wfile.write(body)


if __name__ == '__main__':
    ThreadingHTTPServer(('0.0.0.0', int(os.environ.get('PORT', '8080'))), Handler).serve_forever()
