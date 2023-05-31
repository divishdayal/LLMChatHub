import logging
from typing import Optional

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter, Retry

from src.schemas import FetchedContent

logger = logging.getLogger(__name__)


def fetch(url) -> Optional[FetchedContent]:
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
        "referer": "http://localhost:8888/",
    }

    try:
        session = requests.Session()
        retries = Retry(total=5, backoff_factor=1, redirect=1)
        http_adapter = HTTPAdapter(max_retries=retries)
        session.mount("http://", http_adapter)
        session.mount("https://", http_adapter)

        res = session.get(url, headers=headers)

        if res.status_code == 200 and "text/html" in res.headers["content-type"]:
            soup = BeautifulSoup(res.content, "html.parser")

            return FetchedContent(
                url=url,
                title=soup.title.text if soup.title else None,
                html=res.content,
                text=soup.text,
            )
        else:
            logging.error(
                "Failed to fetch %s. Status code: %d, Content-Type: %s",
                url,
                res.status_code,
                res.headers["content-type"],
            )
    except Exception as e:
        logging.exception("Failed to fetch %s", url)
    return None

if __name__ == "__main__":
    print(fetch("https://www.klue.com/"))
