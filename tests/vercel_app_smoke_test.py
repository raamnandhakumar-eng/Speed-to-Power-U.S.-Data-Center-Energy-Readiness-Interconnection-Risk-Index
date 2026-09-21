from pathlib import Path

root = Path(__file__).resolve().parents[1]
html = (root / "index.html").read_text()

assert "<title>Speed-to-Power</title>" in html
assert "Candidate Pathways V4" in html
assert "Northern Virginia transmission development" in html
assert "Utility-level economics" in html
assert "Regional market screening" in html
assert "renderV4()" in html

print("Vercel static dashboard check passed.")
