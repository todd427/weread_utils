from bs4 import BeautifulSoup

with open("toddReads/page2.htm", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

print("\n=== ALL CANDIDATE TITLES ===\n")
for tag in soup.find_all(["a", "span", "div"]):
    txt = tag.get_text(strip=True)
    if txt and len(txt) > 8:
        print(repr(txt))
