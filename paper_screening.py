import io
import json
import logging
import re
from pathlib import Path

import requests
from pypdf import PdfReader
from pypdf.errors import PdfReadError

PROMPT = Path(__file__).with_name("screening_prompt.txt").read_text(encoding="utf-8-sig")
REPO = re.compile(r"https?://(?:www\.)?github\.com/([\w-]+)/([\w.-]+)", re.I | re.ASCII)


def repository_evidence(data):
    evidence = {}
    for page in PdfReader(io.BytesIO(data)).pages:
        text = page.extract_text() or ""
        for match in REPO.finditer(text):
            url = "https://github.com/{}/{}".format(*match.groups()).rstrip(".")
            snippet = text[max(0, match.start() - 350):match.end() + 250]
            evidence.setdefault(url, []).append(snippet)
        for ref in page.get("/Annots", []):
            annotation = ref.get_object()
            action = annotation.get("/A")
            if action:
                uri = str(action.get_object().get("/URI", ""))
                match = REPO.match(uri)
                if match:
                    url = "https://github.com/{}/{}".format(*match.groups()).rstrip(".")
                    evidence.setdefault(url, []).append(text[:3000])
    return evidence


def screen_paper(paper, client, model):
    try:
        response = requests.get(paper["pdf_url"].replace("http://", "https://", 1), timeout=45)
        response.raise_for_status()
        evidence = repository_evidence(response.content)
    except (requests.RequestException, PdfReadError, ValueError, KeyError, TypeError, OSError) as exc:
        logging.warning("Skipping unreadable PDF %s: %s", paper["entry_id"], exc)
        return None
    if not evidence:
        return None
    payload = {
        "title": paper["title"],
        "abstract": paper["abstract"],
        "repositories": {url: snippets[:2] for url, snippets in evidence.items()},
    }
    result = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": PROMPT},
            {"role": "user", "content": json.dumps(payload, ensure_ascii=False)},
        ],
        response_format={"type": "json_object"},
    )
    repo = json.loads(result.choices[0].message.content)["repository"]
    return repo if isinstance(repo, str) and repo in evidence else None
