from typing import Any, ClassVar

import pytest
from django.forms import ModelForm
from django.test import RequestFactory

from django_htmx_modal_forms.views import (
    HtmxModalCreateView,
    HtmxModalUpdateView,
)
from tests.testapp.models import Blog


# Test Form
class BlogForm(ModelForm):
    """Form for testing modal form functionality with Blog model."""

    class Meta:
        """Meta configuration for BlogForm."""

        model = Blog
        fields: ClassVar[list[str]] = ["name"]


# Mock Views for testing
class MockCreateModalView(HtmxModalCreateView):
    """Mock create view for testing."""

    model = Blog
    form_class = BlogForm
    template_name = "htmx_modal_forms/_modal_form.html"
    form_template_name = "htmx_modal_forms/_form_content.html"

    def __init__(self) -> None:
        """Initialize the view with empty object."""
        super().__init__()
        self.object = None


class MockUpdateModalView(HtmxModalUpdateView):
    """Mock update view for testing."""

    model = Blog
    form_class = BlogForm
    template_name = "htmx_modal_forms/_modal_form.html"
    form_template_name = "htmx_modal_forms/_form_content.html"
    detail_template_name = "testapp/_blog_detail.html"

    def __init__(self) -> None:
        """Initialize the view with empty object."""
        super().__init__()
        self.object = None


@pytest.fixture
def request_factory() -> RequestFactory:
    """Provide a request factory for testing."""
    return RequestFactory()


@pytest.fixture
def blog(db: Any) -> Blog:
    """Create a test blog instance."""
    return Blog.objects.create(name="Test Blog")


@pytest.mark.django_db
class TestHtmxModalFormMixin:
    """Tests for the HtmxModalFormMixin functionality."""

    def test_get_modal_title_default(self, request_factory: RequestFactory) -> None:
        """Test default modal title generation."""
        view = MockCreateModalView()
        view.request = request_factory.get("/")
        assert view.get_modal_title() == "Add Blog"

    def test_get_modal_title_custom(self, request_factory: RequestFactory) -> None:
        """Test custom modal title override."""
        view = MockCreateModalView()
        view.modal_title = "Custom Title"
        view.request = request_factory.get("/")
        assert view.get_modal_title() == "Custom Title"

    def test_get_modal_title_with_object(
        self, request_factory: RequestFactory, blog: Blog
    ) -> None:
        """Test modal title with existing object."""
        view = MockUpdateModalView()
        view.object = blog
        view.request = request_factory.get("/")
        assert view.get_modal_title() == f"Edit {blog}"

    def test_get_modal_size_default(self, request_factory: RequestFactory) -> None:
        """Test default modal size."""
        view = MockCreateModalView()
        view.request = request_factory.get("/")
        assert view.get_modal_size() == "lg"

    def test_get_modal_size_custom(self, request_factory: RequestFactory) -> None:
        """Test custom modal size."""
        view = MockCreateModalView()
        view.modal_size = "xl"
        view.request = request_factory.get("/")
        assert view.get_modal_size() == "xl"

    def test_get_context_data(self, request_factory: RequestFactory) -> None:
        """Test context data includes modal-specific data."""
        view = MockCreateModalView()
        view.request = request_factory.get("/mock-url")
        context = view.get_context_data()

        assert "modal_title" in context
        assert "modal_size" in context
        assert "form_url" in context
        assert context["form_url"] == "/mock-url"


@pytest.mark.django_db
class TestHtmxModalCreateView:
    """Tests for the HtmxModalCreateView functionality."""

    def test_form_valid(self, request_factory: RequestFactory) -> None:
        """Test that form submission creates object and returns refresh response."""
        form_data = {
            "name": "New Blog",
        }
        request = request_factory.post("/mock-url", form_data)
        view = MockCreateModalView()
        view.request = request

        form = BlogForm(data=form_data)
        assert form.is_valid()

        response = view.form_valid(form)

        # Verify response type and status
        assert response.status_code == 200
        assert "HX-Refresh" in response.headers

        # Verify object was created
        assert Blog.objects.filter(name="New Blog").exists()

    def test_form_invalid(self, request_factory: RequestFactory) -> None:
        """Test invalid form submission returns form with errors."""
        form_data = {
            "name": "",  # Invalid - name is required
        }
        request = request_factory.post("/mock-url", form_data)
        view = MockCreateModalView()
        view.request = request

        form = BlogForm(data=form_data)
        assert not form.is_valid()

        response = view.form_invalid(form)

        # Verify response attributes
        assert response.status_code == 200
        assert response.headers.get("HX-Retarget") == "[data-form-content]"
        assert response.headers.get("HX-Reswap") == "outerHTML"


@pytest.mark.django_db
class TestHtmxModalUpdateView:
    """Tests for the HtmxModalUpdateView functionality."""

    def test_get_detail_template_name(self, request_factory: RequestFactory) -> None:
        """Test detail template name validation."""
        view = MockUpdateModalView()
        assert view.get_detail_template_name() == "testapp/_blog_detail.html"

        # Test missing detail template name
        view.detail_template_name = None  # type: ignore[assignment]
        with pytest.raises(ValueError):
            view.get_detail_template_name()

    def test_form_valid(self, request_factory: RequestFactory, blog: Blog) -> None:
        """Test that form submission updates object and returns correct response."""
        form_data = {
            "name": "Updated Blog",
        }
        request = request_factory.post(f"/blog/{blog.pk}/edit", form_data)
        view = MockUpdateModalView()
        view.object = blog
        view.request = request

        form = BlogForm(data=form_data, instance=blog)
        assert form.is_valid()

        response = view.form_valid(form)

        # Verify response type and headers
        assert response.status_code == 200
        assert "blog-" in response.content.decode()
        assert "modal:close" in response.headers.get("HX-Trigger-After-Swap", "")

        # Verify object was updated
        blog.refresh_from_db()
        assert blog.name == "Updated Blog"

    def test_form_invalid_update(
        self, request_factory: RequestFactory, blog: Blog
    ) -> None:
        """Test invalid update form submission."""
        form_data = {
            "name": "",  # Invalid - name is required
        }
        request = request_factory.post(f"/blog/{blog.pk}/edit", form_data)
        view = MockUpdateModalView()
        view.object = blog
        view.request = request

        form = BlogForm(data=form_data, instance=blog)
        assert not form.is_valid()

        response = view.form_invalid(form)

        # Verify response attributes
        assert response.status_code == 200
        assert response.headers.get("HX-Retarget") == "[data-form-content]"
        assert response.headers.get("HX-Reswap") == "outerHTML"
