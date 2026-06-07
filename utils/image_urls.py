def normalize_image_url(image_name):
    if not image_name:
        return "/static/images/default.jpg"

    if image_name.startswith("http://") or image_name.startswith("https://"):
        return image_name

    if image_name.startswith("/static/"):
        return image_name

    if image_name.startswith("images/"):
        return f"/static/{image_name}"

    return f"/static/images/{image_name}"