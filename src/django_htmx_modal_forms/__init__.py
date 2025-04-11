__version__ = "0.4.0"

from django_htmx_modal_forms.views import (  # noqa
    HtmxModalCreateView,
    HtmxModalUpdateView,
    HtmxModalFormMixin,
)

__all__ = ["HtmxModalCreateView", "HtmxModalFormMixin", "HtmxModalUpdateView"]
