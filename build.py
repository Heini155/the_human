"""Build the dependency-free reading page from the original manuscript."""
from pathlib import Path
import html
import re

ROOT = Path(__file__).resolve().parent
source = (ROOT / 'the_human_0_1.txt').read_text(encoding='utf-8-sig')

def inline(text):
    text = html.escape(text)
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    return re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)

sections = re.split(r'\n---\s*\n', source.replace('\r\n', '\n'))
rendered = []
for number, section in enumerate(sections, 1):
    blocks = []
    for block in re.split(r'\n\s*\n', section.strip()):
        if block.startswith('# '):
            continue
        if block.startswith('>'):
            lines = [re.sub(r'^> ?', '', line) for line in block.splitlines()]
            paragraphs = '\n'.join(lines).split('\n\n')
            blocks.append('<blockquote>' + ''.join('<p>' + '<br>'.join(inline(p).splitlines()) + '</p>' for p in paragraphs if p.strip()) + '</blockquote>')
        else:
            blocks.append('<p>' + inline(block) + '</p>')
    rendered.append(f'<section class="chapter" aria-label="Abschnitt {number:02}" id="abschnitt-{number}"><div class="section-number" aria-hidden="true">{number:02} / {len(sections):02}</div>' + '\n'.join(blocks) + '</section>')

minutes = round(len(source.split()) / 200)
page = '''<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#e9e7df">
<meta name="description" content="THE HUMAN. Eine dystopische Kurzgeschichte über künstliche Intelligenz, menschliche Kontrolle und die Frage, wer Verantwortung trägt.">
<meta property="og:title" content="THE HUMAN">
<meta property="og:description" content="31.742 Entitäten. Ein Mensch. Eine dystopische Kurzgeschichte.">
<meta property="og:type" content="article">
<title>THE HUMAN — Eine Kurzgeschichte</title>
<style>
:root{color-scheme:light;--paper:#e9e7df;--ink:#242622;--muted:#64675e;--line:#b9bbb0;--accent:#6c372f}
*{box-sizing:border-box}html{scroll-behavior:smooth;scroll-padding-top:5rem}body{margin:0;background:var(--paper);color:var(--ink);font-family:Georgia,'Times New Roman',serif}a{color:inherit;text-underline-offset:5px}a:focus-visible{outline:2px solid var(--accent);outline-offset:7px}.mono,.topbar,.section-number,.eyebrow,.read-link,footer{font-family:'Courier New',monospace}.skip{position:absolute;left:1rem;top:-5rem;background:var(--paper);padding:1rem;z-index:10}.skip:focus{top:1rem}.topbar{display:flex;justify-content:space-between;gap:1rem;padding:22px 5vw;border-bottom:1px solid var(--line);font-size:11px;letter-spacing:.14em;text-transform:uppercase}.topbar a{text-decoration:none}.status::before{content:'';display:inline-block;width:5px;height:5px;background:var(--accent);margin-right:9px;vertical-align:2px}.cover{max-width:1140px;margin:auto;padding:70px 40px 80px;display:grid;grid-template-columns:1fr 1fr;gap:85px;align-items:center}.cover-art{margin:0;position:relative}.cover-art img{display:block;width:100%;height:auto;box-shadow:0 12px 35px #24262218}.cover-art figcaption{font:10px 'Courier New',monospace;letter-spacing:.13em;color:var(--muted);margin-top:16px;text-transform:uppercase}.eyebrow{font-size:11px;letter-spacing:.18em;text-transform:uppercase;color:var(--muted)}h1{font-family:Impact,'Arial Narrow',sans-serif;font-size:clamp(64px,8vw,112px);font-weight:900;line-height:.91;letter-spacing:-.045em;margin:30px 0}h1 span{display:block}.intro{font-size:22px;line-height:1.65;max-width:24ch;margin:30px 0}.metadata{border-top:1px solid var(--line);padding-top:18px;font-size:11px;line-height:1.9;color:var(--muted);letter-spacing:.06em}.read-link{display:inline-flex;gap:35px;align-items:center;margin-top:34px;padding:14px 0;border-bottom:1px solid var(--ink);font-size:12px;letter-spacing:.08em;text-decoration:none}.read-link:hover{color:var(--accent)}.story-heading{border-top:1px solid var(--line);border-bottom:1px solid var(--line);padding:18px 0;display:flex;justify-content:space-between;gap:15px;font-size:10px;letter-spacing:.12em;color:var(--muted)}.reading{width:min(100% - 48px,660px);margin:0 auto;padding-bottom:75px}.chapter{position:relative;padding-top:58px;font-size:20px;line-height:1.8;overflow-wrap:break-word}.chapter+.chapter{margin-top:60px;border-top:1px solid var(--line)}.section-number{font-size:10px;letter-spacing:.13em;color:var(--muted);margin-bottom:35px}.chapter p{margin:0 0 1.15em}.chapter strong{font-weight:700}.chapter blockquote{margin:32px 0;padding:23px 26px;background:#dddfd5;border-left:2px solid #777f6b;font-family:'Courier New',monospace;font-size:14px;line-height:1.8}.chapter blockquote p{margin:0 0 1em}.chapter blockquote p:last-child{margin:0}.ending{display:flex;align-items:center;gap:16px;margin-top:60px;font-size:11px;letter-spacing:.2em;color:var(--muted)}.ending::after{content:'';height:1px;background:var(--line);flex:1}footer{max-width:1060px;margin:0 auto;padding:25px 24px 40px;border-top:1px solid var(--line);display:flex;justify-content:space-between;gap:20px;font-size:10px;letter-spacing:.1em;color:var(--muted)}::selection{background:#c4c9b7;color:#171a14}
@media(min-width:1100px){.section-number{position:absolute;left:-105px;top:68px}}
@media(max-width:700px){.topbar{padding:18px 24px;font-size:9px}.cover{padding:35px 24px 55px;grid-template-columns:1fr;gap:38px}.cover-art{max-width:370px;width:100%;margin:auto}.cover-copy{max-width:440px;width:100%;margin:auto}h1{font-size:72px;margin:22px 0}h1 span{display:inline}h1 span+span::before{content:' '}.intro{font-size:20px;max-width:100%;margin:22px 0}.chapter{font-size:18px;line-height:1.85;padding-top:40px}.chapter blockquote{font-size:16px;padding:18px}.chapter+.chapter{margin-top:42px}footer{font-size:9px}.story-heading{font-size:9px}}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
@media print{body{background:white;color:black}.topbar,.read-link,footer,.skip{display:none}.cover{display:block;padding:0}.cover-art{max-width:240px;margin:auto}.cover-copy{text-align:center}h1{font-size:48px}h1 span{display:inline}.intro{max-width:none}.reading{width:100%}.chapter{font-size:12pt}.chapter blockquote{break-inside:avoid;font-size:10pt}.section-number{position:static}.cover{break-after:page}}
.soundtrack{display:block;margin-top:24px;background:transparent;border:1px solid var(--muted);padding:12px 16px;color:var(--ink);font:12px 'Courier New',monospace;cursor:pointer;min-height:44px}.soundtrack:hover{background:#dddfd5}button:focus-visible{outline:3px solid var(--accent);outline-offset:5px}.approval{margin-top:50px;padding:32px 24px;background:#202821;color:#e9e7df;border:1px solid #727c67;box-shadow:7px 7px 0 #b9bbb0}.approval-label{font:11px 'Courier New',monospace;letter-spacing:.16em;color:#b7c5ac}.approve-button{display:flex;justify-content:space-between;align-items:center;gap:20px;width:100%;margin-top:22px;padding:22px 24px;border:1px solid #c6ddab;background:#c6ddab;color:#202821;font:bold 22px 'Courier New',monospace;letter-spacing:.12em;cursor:pointer;box-shadow:0 5px 0 #788a66;transition:background .2s,transform .2s,box-shadow .2s}.approve-button:hover{background:#d9edc2}.approve-button:active{transform:translateY(4px);box-shadow:0 1px 0 #788a66}.approve-button[aria-pressed="true"]{background:#202821;color:#c6ddab}.audio-status{font:12px/1.7 'Courier New',monospace;min-height:2em;margin:20px 0 0}.approval audio{display:block;width:100%;margin-top:16px}.approval audio[hidden]{display:none}@media print{.soundtrack,.approval{display:none}}@media(prefers-reduced-motion:reduce){.approve-button{transition:none}}
</style>
</head>
<body id="anfang">
<a class="skip" href="#geschichte">Direkt zur Geschichte</a>
<header class="topbar"><a href="#anfang">AXIOM//ZERO</a><span class="status">Human in the loop</span></header>
<main>
<div class="cover">
<figure class="cover-art"><img src="ChatGPT%20Image%2021.%20Sept.%202026%2C%2018_35_36.png" width="1024" height="1536" alt="Dystopisches Titelplakat: eine schwarze menschliche Silhouette auf abgenutztem Papier, beschriftet mit THE HUMAN und Human Resources Division." fetchpriority="high"><figcaption>Human Resources Division / H–01</figcaption></figure>
<div class="cover-copy"><p class="eyebrow">Eine Kurzgeschichte aus einer nahen Zukunft</p><h1><span>THE</span><span>HUMAN</span></h1><p class="intro">31.742 Entitäten.<br>31.741 davon waren keine Menschen.</p><div class="metadata mono">ZEIT / 203x<br>LESEDAUER / ca. MINUTES Minuten</div><a class="read-link" href="#geschichte">Geschichte lesen <span aria-hidden="true">↓</span></a><button class="soundtrack" id="intro-toggle" type="button" aria-pressed="false">▶ Soundtrack · Soul Digital</button><audio id="intro-audio" src="soul_digital.mp3" preload="none"></audio></div>
</div>
<article class="reading" id="geschichte" aria-label="The Human — vollständige Kurzgeschichte">
<div class="story-heading mono"><span>THE HUMAN</span><span>AXIOM//ZERO · 203x</span></div>
STORY
<div class="ending mono">ENDE</div>
<div class="approval">
<div class="approval-label">HUMAN INPUT REQUIRED / FINAL AUTHORIZATION</div>
<button class="approve-button" id="approve" type="button" aria-pressed="false"><span>APPROVE</span><span aria-hidden="true">→</span></button>
<p class="audio-status" id="outro-status" role="status">Deine Entscheidung. Ein letzter Klick.</p>
<audio id="outro-audio" src="Schwarzer%20Schlaf.mp3" preload="none" controls hidden aria-label="Schwarzer Schlaf"></audio>
</div>
</article>
</main>
<footer><span>THE HUMAN / KURZGESCHICHTE</span><a href="#anfang">Zurück zum Anfang ↑</a></footer>
<script>
(() => {
  const intro = document.getElementById('intro-audio');
  const outro = document.getElementById('outro-audio');
  const toggle = document.getElementById('intro-toggle');
  const approve = document.getElementById('approve');
  const status = document.getElementById('outro-status');
  let context, gain, origin = 0, fading = false;
  function stopIntro() {
    intro.pause();
    fading = false;
  }
  function setupGain() {
    if (!context) {
      const AudioContext = window.AudioContext || window.webkitAudioContext;
      if (AudioContext) {
        context = new AudioContext();
        gain = context.createGain();
        context.createMediaElementSource(intro).connect(gain);
        gain.connect(context.destination);
      }
    }
    if (context) context.resume().catch(() => {});
  }
  toggle.addEventListener('click', async () => {
    if (!intro.paused) { stopIntro(); return; }
    outro.pause();
    try {
      setupGain();
      origin = window.scrollY;
      fading = true;
      if (gain) { gain.gain.cancelScheduledValues(context.currentTime); gain.gain.setValueAtTime(1, context.currentTime); }
      else intro.volume = 1;
      await intro.play();
    } catch (error) {
      fading = false;
      toggle.textContent = '↻ Soundtrack erneut starten';
    }
  });
  intro.addEventListener('play', () => {
    toggle.textContent = 'Ⅱ Soundtrack pausieren';
    toggle.setAttribute('aria-pressed', 'true');
  });
  function resetIntro() {
    toggle.textContent = '▶ Soundtrack · Soul Digital';
    toggle.setAttribute('aria-pressed', 'false');
  }
  intro.addEventListener('pause', resetIntro);
  intro.addEventListener('ended', () => { fading = false; resetIntro(); });
  window.addEventListener('scroll', () => {
    if (!fading || intro.paused) return;
    const distance = Math.max(0, window.scrollY - origin);
    const volume = Math.max(0, 1 - distance / Math.min(window.innerHeight * 0.65, 500));
    if (gain) gain.gain.setTargetAtTime(volume, context.currentTime, 0.08);
    else intro.volume = volume;
    if (volume === 0) stopIntro();
  }, { passive: true });
  approve.addEventListener('click', async () => {
    stopIntro();
    outro.hidden = false;
    if (!outro.paused) { outro.pause(); return; }
    try { await outro.play(); }
    catch (error) { status.textContent = 'Wiedergabe nicht möglich. Bitte über den Audioplayer erneut starten.'; }
  });
  outro.addEventListener('play', () => {
    stopIntro();
    approve.setAttribute('aria-pressed', 'true');
    approve.firstElementChild.textContent = 'APPROVED';
    approve.lastElementChild.textContent = 'Ⅱ';
    status.textContent = 'Freigabe erteilt. Schwarzer Schlaf spielt.';
  });
  function resetOutro() {
    approve.setAttribute('aria-pressed', 'false');
    approve.firstElementChild.textContent = 'APPROVE';
    approve.lastElementChild.textContent = '→';
    status.textContent = outro.ended ? 'Wiedergabe beendet. Erneut freigeben?' : 'Schwarzer Schlaf · pausiert';
  }
  outro.addEventListener('pause', resetOutro);
  outro.addEventListener('ended', resetOutro);
})();
</script>
</body>
</html>
'''
(ROOT / 'index.html').write_text(page.replace('MINUTES', str(minutes)).replace('STORY', '\n'.join(rendered)), encoding='utf-8')
print(f'Built index.html: {len(sections)} sections, approximately {minutes} minutes.')
