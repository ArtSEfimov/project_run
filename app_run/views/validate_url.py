import re
from urllib.parse import urlparse

# Компактный, но достаточно надёжный паттерн для HTTP/HTTPS URL:
_URL_REGEX = re.compile(
    r'^(?:http|https)://'  # схема
    r'(?:'  # либо имя хоста...
    r'(?:[A-Za-z0-9-]{1,63}\.)+'  # метки домена, разделённые точками
    r'[A-Za-z]{2,63}'  # TLD (от 2 до 63 букв)
    r'|'  # ...или localhost
    r'localhost'
    r'|'  # ...или IPv4
    r'\d{1,3}(?:\.\d{1,3}){3}'
    r')'
    r'(?::\d{1,5})?'  # опциональный порт
    r'(?:/[^\s]*)?$'  # опциональный путь (без пробелов)
    , re.IGNORECASE)


def is_valid_url(url: str) -> bool:
    """
    Проверяет, является ли строка корректным HTTP/HTTPS URL.

    Алгоритм:
      1. Проверяем, что это строка.
      2. Разбираем через urlparse и убеждаемся, что есть scheme и netloc.
      3. Регексп убеждается, что хост — это либо доменное имя, либо localhost, либо IPv4.
      4. Проверяем опциональный порт и путь.

    Примеры:
      >>> is_valid_url("https://example.com")
      True
      >>> is_valid_url("http://127.0.0.1:8000/path?query=1")
      True
      >>> is_valid_url("ftp://example.com")
      False
      >>> is_valid_url("just some text")
      False
    """
    if not isinstance(url, str):
        return False

    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        return False
    if not parsed.netloc:
        return False

    return bool(_URL_REGEX.match(url))
