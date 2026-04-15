import requests, json
from bs4 import BeautifulSoup

URL = "https://www.rbi.org.in/commonman/english/scripts/FAQs.aspx?Id=1167"

def scrape():
    r = requests.get(URL, timeout=10)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")

    # This page contains the Q/A in the main text body; strategy: extract the main content text then split by question numbers.
    content = soup.get_text(separator="\n")
    # A simple split: find the section header "A. Definitions" (or the page title) and then split into q&a entries.
    # This is a heuristic — verify and edit manually.
    start = content.find("A. Definitions")
    text = content[start:]
    lines = [l.strip() for l in text.splitlines() if l.strip()]

    # Simple heuristic: questions often look like "1. What is ..."
    qa = []
    current_q = None
    current_a = []
    for line in lines:
        if line.split()[0].endswith(".") and line.split()[0][:-1].isdigit() and line.endswith("?"):
            # new question
            if current_q:
                qa.append({"question": current_q, "answer": " ".join(current_a).strip()})
            current_q = line
            current_a = []
        elif current_q:
            current_a.append(line)
    if current_q:
        qa.append({"question": current_q, "answer": " ".join(current_a).strip()})

    # Save a subset (or full)
    with open("evaluation/faq_dataset.json", "w", encoding="utf-8") as f:
        json.dump(qa[:50], f, indent=2, ensure_ascii=False)
    print(f"Saved {min(50,len(qa))} Q/A pairs to evaluation/faq_dataset.json")

if __name__ == "__main__":
    scrape()
