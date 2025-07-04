from urllib.parse import urlparse


def is_valid_url(url: str) -> bool:
    """
    Простая и эффективная проверка HTTP/HTTPS URL.
    Возвращает True, если:
      - схема — http или https
      - есть нетлок (домен или IP)
    Иначе — False.
    """
    try:
        parsed = urlparse(url)
    except Exception:
        return False

    return parsed.scheme in ("http", "https") and bool(parsed.netloc)
