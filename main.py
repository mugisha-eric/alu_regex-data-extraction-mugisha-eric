import re

PATTERNS = {
    "Email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
    "URL": r"https?://(?:[A-Za-z0-9-]+\.)+[A-Za-z]{2,}(?:/[^\s<>\"']*)?",
    "Phone": r"(?:\(\d{3}\)\s?|\b\d{3}[-.])\d{3}[-.]\d{4}\b",
    "Credit Card": r"\b\d{4}([ -])\d{4}\1\d{4}\1\d{4}\b",
    "Time": r"\b(?:(?:[01]?\d|2[0-3]):[0-5]\d|(?:0?[1-9]|1[0-2]):[0-5]\d\s?[AaPp][Mm])\b",
    "HTML Tag": r"</?[A-Za-z][A-Za-z0-9]*(?:\s+[A-Za-z-]+(?:=\"[^\"]*\")?)*\s*/?>",
    "Hashtag": r"(?<!\w)#[A-Za-z][A-Za-z0-9_]*",
    "Currency": r"\$\d{1,3}(?:,\d{3})*(?:\.\d{2})?|\$\d+(?:\.\d{2})?",
}


def extract_all(text):
    results = {}
    for name, pattern in PATTERNS.items():
        if name == "Credit Card":
            # this pattern has a capture group, so use finditer to get the full match
            results[name] = [m.group(0) for m in re.finditer(pattern, text)]
        elif name == "Time":
            results[name] = [m.group(0) for m in re.finditer(pattern, text, re.IGNORECASE)]
        else:
            results[name] = re.findall(pattern, text)
    return results



if __name__ == "__main__":
    test_test=""
    print("=== Regex Data Extractor ===")
    print("\nEnter your text. Type END on a new line when finished:")
    lines = []
    while True:
        line = input()
        if line.strip().upper() == "END":
            break
        lines.append(line)
    test_text = "\n".join(lines)

    results = extract_all(test_text)
    for category, matches in results.items():
        print(f"\n{category} ({len(matches)} found):")
        for m in matches:
            print(f"   {m}")