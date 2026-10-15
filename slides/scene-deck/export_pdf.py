# /// script
# requires-python = ">=3.11"
# dependencies = ["playwright>=1.45"]
# ///
"""Export a scene-deck HTML to a PDF: one 1600x900 page per scene, each at its final step.

uv run export_pdf.py [hermes-deck.html] [out.pdf]

Uses the installed Google Chrome. Text stays vector, so the PDF is sharp and searchable.
"""
import pathlib
import sys

from playwright.sync_api import sync_playwright

PRINT_CSS = """
@page { size: 1600px 900px; margin: 0 }
html, body { overflow: visible !important; height: auto !important; background: var(--paper) }
#stage { position: static !important; transform: none !important; width: 1600px !important; height: auto !important }
#timeline { display: none !important }
.scene { position: relative !important; inset: auto !important; width: 1600px; height: 900px;
         opacity: 1 !important; visibility: visible !important; break-after: page; overflow: hidden }
.scene, .scene * { transition: none !important; animation: none !important }
.pageno { position: absolute; right: 90px; bottom: 30px; font: 400 14px var(--mono); color: var(--muted) }
"""

# Put every scene in its final state (same rules as the engine's apply()).
FINAL_STATE_JS = """() => {
  const KEYS = ['step', 'fx', 'dim', 'out'];
  const scenes = [...document.querySelectorAll('.scene')];
  scenes.forEach((sc, i) => {
    const n = Math.max(0, ...[...sc.querySelectorAll(KEYS.map(k => `[data-${k}]`).join())]
      .flatMap(e => KEYS.map(k => +e.dataset[k] || 0)));
    for (const e of sc.querySelectorAll('[data-step]')) e.classList.toggle('on', n >= +e.dataset.step);
    for (const e of sc.querySelectorAll('[data-fx]')) e.classList.toggle('fx-on', n >= +e.dataset.fx);
    for (const e of sc.querySelectorAll('[data-dim]')) e.classList.toggle('dimmed', n >= +e.dataset.dim);
    for (const e of sc.querySelectorAll('[data-out]')) e.classList.toggle('gone', n >= +e.dataset.out);
    sc.classList.add('active');
    sc.insertAdjacentHTML('beforeend', `<span class="pageno">${i + 1} / ${scenes.length}</span>`);
  });
  return scenes.length;
}"""


def main() -> None:
    here = pathlib.Path(__file__).parent
    deck = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else here / "hermes-deck.html").resolve()
    out = pathlib.Path(sys.argv[2] if len(sys.argv) > 2 else deck.with_suffix(".pdf")).resolve()
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome")
        page = browser.new_page(viewport={"width": 1600, "height": 900})
        page.goto(deck.as_uri())
        page.evaluate("document.fonts.ready")
        page.wait_for_load_state("networkidle")
        page.add_style_tag(content=PRINT_CSS)
        n = page.evaluate(FINAL_STATE_JS)
        page.wait_for_timeout(500)
        page.pdf(path=str(out), width="1600px", height="900px", print_background=True)
        browser.close()
    print(f"{n} pages -> {out}")


if __name__ == "__main__":
    main()
