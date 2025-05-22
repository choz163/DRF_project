from rest_framework import serializers
from urllib.parse import urlparse


def validate_no_external_links(value):

    parsed = urlparse(value)
    domain = parsed.netloc.lower()
    allowed = ("youtube.com", "www.youtube.com")
    if domain and domain not in allowed:
        raise serializers.ValidationError(
            "Сторонние ссылки, кроме youtube.com, запрещены."
        )
    return value
