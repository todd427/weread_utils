from bs4 import BeautifulSoup

with open("toddReads/page2.htm", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")
titles_of_interest = [
    "Vibe Coding by Example",
    "Beginning Django API with React: Build Django 4 Web APIs with React Full Stack Applications",
    "Django 5 By Example: Build powerful and reliable Python web applications from scratch"
]

for tag in soup.find_all(["span", "a"]):
    text = tag.get_text(strip=True)
    if text in titles_of_interest:
        print(f"Tag: {tag.name}, Classes: {tag.get('class')}, Text: {text}")
