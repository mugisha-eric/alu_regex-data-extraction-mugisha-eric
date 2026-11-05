# Regex Data Extractor

A Python command-line tool that uses **regular expressions** to extract structured data from large blocks of raw text, such as API responses or scraped web pages.

## Features

The program extracts 8 types of data:

| Data type   | Example formats matched                                                   |
|-------------|---------------------------------------------------------------------------|
| Email       | `user@example.com`, `firstname.lastname@company.co.uk`                    |
| URL         | `https://www.example.com`, `https://subdomain.example.org/page`           |
| Phone       | `(123) 456-7890`, `123-456-7890`, `123.456.7890`                          |
| Credit card | `1234 5678 9012 3456`, `1234-5678-9012-3456`                              |
| Time        | `14:30` (24-hour), `2:30 PM` (12-hour)                                    |
| HTML tag    | `<p>`, `<div class="example">`, `<img src="image.jpg" alt="description">` |
| Hashtag     | `#example`, `#ThisIsAHashtag`                                             |
| Currency    | `$19.99`, `$1,234.56`                                                     |

## Requirements

- Python 3.6 or newer
- No external libraries (uses only the built-in `re` module)

## How to Run

```bash
python main.py
```

(Replace `main.py` with the name of your script file.)

## How to Use

1. Run the script.
2. Paste or type your text. It can span multiple lines.
3. Type `END` on a new line and press Enter.
4. The program prints every match, grouped by data type.

### Using the included `sample.txt`

`sample.txt` contains test text with valid and invalid examples. Instead of typing or pasting, you can feed it to the program through input redirection:

```bash
python main.py < sample.txt
```

Make sure the last line of `sample.txt` is `END`, since the program stops reading input when it sees that word.

### Example input

```
Contact us at user@example.com or firstname.lastname@company.co.uk.
Visit https://www.example.com or https://subdomain.example.org/page
Call (123) 456-7890, 123-456-7890 or 123.456.7890.
Cards: 1234 5678 9012 3456 and 1234-5678-9012-3456.
Meeting at 14:30, lunch at 2:30 PM.
HTML: <p> <div class="example"> <img src="image.jpg" alt="description">
Trending: #example #ThisIsAHashtag
Prices: $19.99 and $1,234.56
END
```

### Example output

```
Email (2 found):
   user@example.com
   firstname.lastname@company.co.uk

URL (2 found):
   https://www.example.com
   https://subdomain.example.org/page

Phone (3 found):
   (123) 456-7890
   123-456-7890
   123.456.7890

Credit Card (2 found):
   1234 5678 9012 3456
   1234-5678-9012-3456

Time (2 found):
   14:30
   2:30 PM

HTML Tag (3 found):
   <p>
   <div class="example">
   <img src="image.jpg" alt="description">

Hashtag (2 found):
   #example
   #ThisIsAHashtag

Currency (2 found):
   $19.99
   $1,234.56
```

## How the Code Works

- **`PATTERNS`** is a dictionary that maps each data type to its regular expression.
- **`extract_all(text)`** runs every pattern against the input text and returns a dictionary of `{data type: [matches]}`.
  - `re.finditer` with `m.group(0)` is used for patterns that contain a capture group (Credit Card), so the full match is returned instead of only the group.
  - `re.IGNORECASE` is applied to Time so `pm`, `PM`, and `Pm` all match.
- The **main block** reads multi-line input until the user types `END`, then prints the results.

## Regular Expression Breakdown

| Type        | Pattern idea                                                                                   |
|-------------|------------------------------------------------------------------------------------------------|
| Email       | local part, then `@`, then domain (dots allowed, so `.co.uk` works), then a TLD of 2+ letters  |
| URL         | `http://` or `https://`, then domain labels, then an optional path with no spaces or quotes    |
| Phone       | `(123) ` or `123-` / `123.`, followed by `456`, a `-` or `.`, and `7890`                       |
| Credit card | 4 groups of 4 digits; `([ -])` captures the separator and `\1` forces the same one every time |
| Time        | 12-hour (`1:00`-`12:59` + AM/PM) or 24-hour (`00:00`-`23:59`)                                  |
| HTML tag    | opening or closing tag, with optional `name="value"` attributes and optional `/`               |
| Hashtag     | `#` followed by a letter, then letters, digits, or underscores                                 |
| Currency    | `$` plus digits, with optional thousands commas and optional 2 decimal places                  |

## Test Cases

### Valid (should match)

| Type        | Input                       |
|-------------|-----------------------------|
| Email       | `user@example.com`          |
| URL         | `https://www.example.com`   |
| Phone       | `(123) 456-7890`            |
| Credit card | `1234-5678-9012-3456`       |
| Time        | `2:30 PM`, `14:30`          |
| HTML tag    | `<div class="example">`     |
| Hashtag     | `#ThisIsAHashtag`           |
| Currency    | `$1,234.56`                 |

### Invalid (should NOT match)

| Type        | Input                                   | Reason                              |
|-------------|-----------------------------------------|-------------------------------------|
| Email       | `bad@email`                             | no top-level domain                 |
| URL         | `htp:/broken.com`                       | malformed scheme                    |
| Phone       | `12-34-5678`                            | wrong digit grouping                |
| Credit card | `1234 5678 9012`, `1234 5678-9012 3456` | too short / mixed separators        |
| Time        | `25:99`                                 | invalid hour and minute             |
| Hashtag     | `#123`                                  | must start with a letter            |

## Limitations

- URLs must start with `http://` or `https://` (for example, `www.example.com` alone is not matched).
- Currency supports only the `$` symbol.
- Credit card matching checks the **format only**; it does not run a Luhn checksum to confirm the number is a real card.
- Phone matching covers US-style 10-digit numbers.
- HTML matching is for simple tags and is not a full HTML parser.

## Project Structure

```
.
├── README.md    # Project documentation
├── main.py      # Regex patterns, extraction function, and CLI
└── sample.txt   # Sample text for testing the extractor
```

## AI Disclosure

This README.md file was written with the assistance of an AI tool (Claude, developed by Anthropic) while codes and programming was written and reviewed entirely by human. The content was reviewed and adapted to describe the code in this project.