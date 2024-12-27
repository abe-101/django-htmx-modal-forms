"""Django HTMX Modal Forms - Class-based views for HTMX-powered Bootstrap modals."""

from typing import Any, Optional

from django.forms import BaseForm
from django.http import HttpResponse
from django.http.request import HttpRequest
from django.shortcuts import render
from django.views.generic.base import View
from django.views.generic.edit import CreateView, UpdateView
from django_htmx.http import (
    HttpResponseClientRefresh,
    reswap,
    retarget,
    trigger_client_event,
)


class HtmxModalFormMixin(View):
    """
    Base mixin for modal form handling with HTMX and Bootstrap.

    This mixin provides the core functionality for handling forms in Bootstrap modals
    using HTMX for dynamic updates.

    Attributes:
        template_name (str): Template for the full modal structure
        form_template_name (str): Template for just the form content
        modal_size (str): Bootstrap modal size class (sm, lg, xl)
        modal_title (str): Custom modal title override

    """

    template_name = "htmx_modal_forms/_modal_form.html"
    form_template_name = "htmx_modal_forms/_form_content.html"
    modal_size: str = "lg"
    modal_title: Optional[str] = None

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Handle GET requests and trigger modal show."""
        response = super().get(request, *args, **kwargs)
        return trigger_client_event(response, "modal:show", after="swap")

    def get_modal_title(self) -> str:
        """
        Get the title for the modal.

        Override this method to customize the modal title.
        """
        if self.modal_title:
            return self.modal_title
        if hasattr(self, "object") and self.object:
            return f"Edit {self.object}"
        return f"Add {self.model._meta.verbose_name.title()}"

    def get_modal_size(self) -> str:
        """
        Get the Bootstrap modal size class.

        Override this method to customize the modal size.
        """
        return self.modal_size

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Add modal-specific context."""
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "modal_title": self.get_modal_title(),
                "modal_size": self.get_modal_size(),
                "form_url": self.request.path,
            }
        )
        return context

    def form_invalid(self, form: BaseForm) -> HttpResponse:
        """Handle invalid form submission."""
        context = self.get_context_data(form=form)
        response = render(self.request, self.form_template_name, context)
        response = reswap(response, "outerHTML")
        return retarget(response, "[data-form-content]")


class HtmxModalCreateView(HtmxModalFormMixin, CreateView):
    """
    View for creating objects via modal forms.

    On successful form submission, the page will be refreshed to show
    the newly created object.
    """

    def form_valid(self, form: BaseForm) -> HttpResponse:
        """Save form and refresh page on success."""
        self.object = form.save()
        return HttpResponseClientRefresh()


class HtmxModalUpdateView(HtmxModalFormMixin, UpdateView):
    """
    View for updating objects via modal forms.

    On successful form submission, the target element will be updated
    with the new object details.

    Attributes:
        detail_template_name (str): Template for rendering updated object details

    """

    detail_template_name: Optional[str] = None

    def get_detail_template_name(self) -> str:
        """
        Get the template name for rendering object details.

        Override this method to customize the template selection.
        """
        if self.detail_template_name is None:
            raise ValueError("detail_template_name is required for HtmxModalUpdateView")
        return self.detail_template_name

    def form_valid(self, form: BaseForm) -> HttpResponse:
        """Save form and update the page with new object details."""
        self.object = form.save()

        # Render updated object details
        context = self.get_context_data()
        detail_html = render(
            self.request, self.get_detail_template_name(), context
        ).content.decode()

        # Create response with out-of-band swap
        response = HttpResponse(
            f"""
            <div id="{self.model._meta.model_name}-{self.object.pk}"
                 hx-swap-oob="true">
                {detail_html}
            </div>
            """
        )

        # Trigger modal close
        return trigger_client_event(response, "modal:close", after="swap")
