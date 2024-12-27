from __future__ import annotations

from django import template
from django.conf import settings
from django.templatetags.static import static
from django.utils.html import format_html

register = template.Library()


def htmx_modal_script() -> str:
    """Generate the script tag for htmx modal handlers."""
    debug_attr = ""
    if settings.DEBUG:
        debug_attr = " data-debug=true"

    return format_html(
        '<script src="{}"{}></script>',
        static("htmx_modal_forms/js/modal-handlers.js"),
        debug_attr,
    )


register.simple_tag(htmx_modal_script)
