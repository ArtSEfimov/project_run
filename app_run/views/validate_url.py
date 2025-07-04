from urllib.parse import urlparse


import ipaddress
from urllib.parse import urlparse

def is_valid_url(url: str) -> bool:
    """
    Простая и эффективная проверка HTTP/HTTPS URL.
    Возвращает True, если:
      - схема — http или https
      - есть netloc
      - hostname — либо корректный IP (v4/v6), либо домен с точкой, либо 'localhost'
    Иначе — False.
    """
    try:
        parsed = urlparse(url)
    except Exception:
        return False

    # 1) схема и netloc
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        return False

    host = parsed.hostname  # без порта, без credentials
    if not host:
        return False

    # 2) разрешаем localhost
    if host.lower() == "localhost":
        return True

    # 3) если это IP — валидно
    try:
        ipaddress.ip_address(host)
        return True
    except ValueError:
        pass

    # 4) иначе требуем хотя бы одну точку (домен уровня example.com)
    return "." in host