from pathlib import Path
import pytest


PAGES = Path(__file__).resolve().parent.parent / "lab" / "pages"


@pytest.fixture
def open_lab_page(page):
    """Open a lab page by file name, e.g. open_lab_page("pl01_settings.html")."""
    def _open(name: str):
        page.goto((PAGES / name).as_uri())
        return page
    return _open
