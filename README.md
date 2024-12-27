# Django Htmx Modal Forms

<p align="center">
  <a href="https://github.com/abe-101/django-htmx-modal-forms/actions/workflows/ci.yml?query=branch%3Amain">
    <img src="https://img.shields.io/github/actions/workflow/status/abe-101/django-htmx-modal-forms/ci.yml?branch=main&label=CI&logo=github&style=flat-square" alt="CI Status" >
  </a>
  <a href="https://django-htmx-modal-forms.readthedocs.io">
    <img src="https://img.shields.io/readthedocs/django-htmx-modal-forms.svg?logo=read-the-docs&logoColor=fff&style=flat-square" alt="Documentation Status">
  </a>
  <a href="https://codecov.io/gh/abe-101/django-htmx-modal-forms">
    <img src="https://img.shields.io/codecov/c/github/abe-101/django-htmx-modal-forms.svg?logo=codecov&logoColor=fff&style=flat-square" alt="Test coverage percentage">
  </a>
</p>
<p align="center">
  <a href="https://github.com/astral-sh/uv">
    <img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json" alt="uv">
  </a>
  <a href="https://github.com/astral-sh/ruff">
    <img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json" alt="Ruff">
  </a>
  <a href="https://github.com/pre-commit/pre-commit">
    <img src="https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white&style=flat-square" alt="pre-commit">
  </a>
</p>
<p align="center">
  <a href="https://pypi.org/project/django-htmx-modal-forms/">
    <img src="https://img.shields.io/pypi/v/django-htmx-modal-forms.svg?logo=python&logoColor=fff&style=flat-square" alt="PyPI Version">
  </a>
  <img src="https://img.shields.io/pypi/pyversions/django-htmx-modal-forms.svg?style=flat-square&logo=python&amp;logoColor=fff" alt="Supported Python versions">
  <img src="https://img.shields.io/pypi/l/django-htmx-modal-forms.svg?style=flat-square" alt="License">
</p>

---

**Documentation**: <a href="https://django-htmx-modal-forms.readthedocs.io" target="_blank">https://django-htmx-modal-forms.readthedocs.io </a>

**Source Code**: <a href="https://github.com/abe-101/django-htmx-modal-forms" target="_blank">https://github.com/abe-101/django-htmx-modal-forms </a>

---

A Django package that provides class-based views for handling forms in Bootstrap modals using HTMX. This package makes it easy to add create and update functionality to your Django models with a clean modal interface.

## Features

- 🚀 Easy-to-use class-based views for modal forms
- ⚡ HTMX-powered for dynamic updates without page reloads
- 🎨 Bootstrap modal integration with customizable sizes
- ✨ Automatic form validation with error handling
- 🔄 Out-of-band updates for seamless UX
- 🐛 Debug mode for development
- 📱 Mobile-friendly and responsive

## Requirements

- Python 3.8+
- Django 4.2+
- django-htmx
- Bootstrap 5
- django-crispy-forms

## Installation

1. Install via pip:

```bash
pip install django-htmx-modal-forms
```

2. Add to your `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    ...
    "crispy_forms",
    "django_htmx_modal_forms",
]
```

3. Load and include the JavaScript in your base template:

```html
{% load htmx_modal_forms %}

<!doctype html>
<html>
  <head>
    <!-- Required dependencies -->
    <script src="{% static 'js/bootstrap.bundle.min.js' %}"></script>
    <script src="{% static 'js/htmx.min.js' %}"></script>

    <!-- Modal handlers -->
    {% htmx_modal_script %}
  </head>
  <body>
    <!-- Your content -->
  </body>
</html>
```

## Quick Start

1. Create your view:

```python
from django_htmx_modal_forms import HtmxModalUpdateView

class PersonUpdateView(HtmxModalUpdateView):
    model = Person
    form_class = PersonForm
    detail_template_name = "persons/_person_card.html"
    modal_size = "lg"  # Optional: sm, lg, or xl
```

2. Add the URL pattern:

```python
path("persons/<int:pk>/edit/", PersonUpdateView.as_view(), name="person_update"),
```

3. Create your detail template (`_person_card.html`):

```html
<div id="person-{{ person.id }}" class="card">
  <div class="card-body">
    <h5 class="card-title">{{ person.name }}</h5>
    <p class="card-text">{{ person.email }}</p>
  </div>
</div>
```

4. Add a button to trigger the modal:

```html
<button
  hx-get="{% url 'person_update' pk=person.pk %}"
  hx-target="body"
  hx-swap="beforeend"
  class="btn btn-primary"
>
  Edit Person
</button>
```

That's it! When you click the edit button, a modal will appear with your form. On successful submission, the person's card will automatically update with the new information.

## Advanced Usage

### Custom Modal Titles

```python
class PersonCreateView(HtmxModalCreateView):
    model = Person
    form_class = PersonForm
    modal_title = "Add New Team Member"  # Custom title
```

### Different Modal Sizes

```python
class PersonUpdateView(HtmxModalUpdateView):
    model = Person
    form_class = PersonForm
    modal_size = "xl"  # Available: sm, lg, xl
```

### Debug Mode

Debug mode is automatically enabled when `settings.DEBUG = True`. It provides helpful console logging for:

- Modal initialization
- Event triggers
- Bootstrap/HTMX availability
- Error conditions

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. To develop locally:

1. Clone the repository
2. Install dependencies: `uv sync`
3. Run tests: `uv run pytest`

## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- prettier-ignore-start -->
<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://www.habet.dev/"><img src="https://avatars.githubusercontent.com/u/82916197?v=4?s=80" width="80px;" alt="Abe Hanoka"/><br /><sub><b>Abe Hanoka</b></sub></a><br /><a href="https://github.com/abe-101/django-htmx-modal-forms/commits?author=abe-101" title="Code">💻</a> <a href="#ideas-abe-101" title="Ideas, Planning, & Feedback">🤔</a> <a href="https://github.com/abe-101/django-htmx-modal-forms/commits?author=abe-101" title="Documentation">📖</a></td>
    </tr>
  </tbody>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->
<!-- prettier-ignore-end -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!

## Credits

This package was created with
[Copier](https://copier.readthedocs.io/) and the
[browniebroke/pypackage-template](https://github.com/browniebroke/pypackage-template)
project template.
