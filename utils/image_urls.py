import posixpath
import re


SAFE_IMAGE_RE = re.compile(r'^[A-Za-z0-9._/-]+$')


def normalize_image_url(image_name):
    if not image_name:
        return "/static/images/default.jpg"

    if not isinstance(image_name, str):
        image_name = str(image_name)

    image_name = image_name.strip()
    if not image_name:
        return "/static/images/default.jpg"

    if image_name.startswith("http://") or image_name.startswith("https://"):
        return image_name

    if image_name.startswith("/static/"):
        image_name = image_name[len("/static/"):]

    if image_name.startswith("images/"):
        image_name = image_name[len("images/"):]

    sanitized = image_name.lstrip("/")
    if not SAFE_IMAGE_RE.match(sanitized):
        return "/static/images/default.jpg"

    normalized = posixpath.normpath(sanitized)
    if normalized.startswith("../") or normalized == ".." or posixpath.isabs(normalized):
        return "/static/images/default.jpg"

    if normalized.startswith("static/"):
        normalized = normalized[len("static/"):]

    if normalized.startswith("images/"):
        return f"/static/{normalized}"

    return f"/static/images/{normalized}"