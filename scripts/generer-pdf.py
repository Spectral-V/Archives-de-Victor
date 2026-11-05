"""Génère un PDF pour chaque lettre de lettres/*.html dans lettres/pdf/.

À relancer après avoir ajouté une nouvelle lettre :
    pip install playwright && playwright install chromium
    python3 scripts/generer-pdf.py              # toutes les lettres
    python3 scripts/generer-pdf.py novembre26   # seulement certaines
"""

import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

RACINE = Path(__file__).resolve().parent.parent
LETTRES = RACINE / "lettres"
SORTIE = LETTRES / "pdf"


def main():
    SORTIE.mkdir(exist_ok=True)
    with sync_playwright() as p:
        navigateur = p.chromium.launch()
        page = navigateur.new_page()
        # Rendu "écran" (et non "impression") pour garder l'allure de la lettre
        page.emulate_media(media="screen")
        choix = sys.argv[1:]
        lettres = [l for l in sorted(LETTRES.glob("*.html")) if not choix or l.stem in choix]
        for lettre in lettres:
            page.goto(lettre.as_uri(), wait_until="networkidle")
            page.evaluate("document.fonts.ready")
            pdf = SORTIE / f"Lettres-Victorieuses-{lettre.stem}.pdf"
            page.pdf(
                path=str(pdf),
                format="A4",
                print_background=True,
                margin={"top": "10mm", "bottom": "10mm", "left": "0", "right": "0"},
            )
            print(f"{lettre.name} -> {pdf.relative_to(RACINE)}")
        navigateur.close()


if __name__ == "__main__":
    main()
