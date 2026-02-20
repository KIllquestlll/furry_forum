# Import other library
from slugify import slugify
import uuid


def generate_unique_slug(text:str) -> str:
    base_slug = slugify(text)

    unique_id = uuid.uuid4().hex[:6]
    return f"{base_slug}-{unique_id}"
