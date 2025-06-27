from bs4 import BeautifulSoup

with open("toddReads/page2.htm", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

# Print all text in large spans for manual inspection
for tag in soup.find_all("span"):
    text = tag.get_text(strip=True)
    if text and len(text) > 4:
        print(repr(text))
