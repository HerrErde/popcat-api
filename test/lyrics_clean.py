import html
import json
import re


def js_unescape(js_str):
    js_str = js_str.replace(r"\'", "'").replace(r"\"", '"').replace(r"\/", "/")
    return bytes(js_str, "utf-8").decode("unicode_escape")


def extract_lyrics(content):
    match = re.search(r"JSON\.parse\('(.+?)'\)", content, re.DOTALL)
    if not match:
        raise ValueError("Lyrics JSON not found")

    escaped_js = match.group(1)
    unescaped = js_unescape(escaped_js)
    html_content = json.loads(unescaped)

    end_pos = html_content.find("</p>")
    if end_pos != -1:
        html_content = html_content[: end_pos + 4]

    html_content = re.sub(r"Powered by Genius\s*", "", html_content)

    html_content = html.unescape(html_content)

    text = re.sub(r"<[^>]+>", "", html_content)

    return text.strip()


with open("embed.js", "r", encoding="utf-8") as f:
    file_content = f.read()

lyrics = extract_lyrics(file_content)
print(lyrics)
