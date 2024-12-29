(usage)=

# Usage

Assuming that you've followed the {ref}`installations steps <installation>`, you're now ready to use this package.

## Basic Usage

1. First, create your model and form:

```python
from django.db import models
from django import forms

class Person(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['name', 'email']
```

2. Create a view using one of the provided classes:

```python
from django_htmx_modal_forms import HtmxModalCreateView, HtmxModalUpdateView

class PersonCreateView(HtmxModalCreateView):
    model = Person
    form_class = PersonForm
    detail_template_name = "persons/_person_card.html"
    modal_title = "Add New Person"

class PersonUpdateView(HtmxModalUpdateView):
    model = Person
    form_class = PersonForm
    detail_template_name = "persons/_person_card.html"
    modal_title = "Edit Person"
```

3. Create your detail template (`persons/_person_card.html`):

```html
<div id="person-{{ person.id }}" class="card">
  <div class="card-body">
    <h5 class="card-title">{{ person.name }}</h5>
    <p class="card-text">{{ person.email }}</p>
  </div>
</div>
```

4. Add URL patterns:

```python
from django.urls import path

urlpatterns = [
    path('person/new/', PersonCreateView.as_view(), name='person-create'),
    path('person/<int:pk>/edit/', PersonUpdateView.as_view(), name='person-edit'),
]
```

5. Add buttons to trigger the modals:

```html
<!-- Create button -->
<button
  hx-get="{% url 'person-create' %}"
  hx-target="body"
  hx-swap="beforeend"
  class="btn btn-primary"
>
  Add Person
</button>

<!-- Edit button -->
<button
  hx-get="{% url 'person-edit' pk=person.pk %}"
  hx-target="body"
  hx-swap="beforeend"
  class="btn btn-secondary"
>
  Edit Person
</button>
```

## View Options

The modal views support several customization options:

```python
class PersonCreateView(HtmxModalCreateView):
    # Required settings
    model = Person                                    # Your Django model
    form_class = PersonForm                          # Your ModelForm class
    detail_template_name = "persons/_person_card.html"  # Template for rendering single item

    # Optional settings
    modal_title = "Add New Person"                   # Title shown in modal header
    modal_size = "lg"                                # Modal size: "sm", "lg", or "xl"
    form_template_name = "custom_form.html"          # Custom form template
    modal_template_name = "custom_modal.html"        # Custom modal template
```

## Form Templates

Your detail template must include an ID that matches your model instance:

```html
<!-- CORRECT -->
<div id="person-{{ person.id }}" class="card">
  <!-- content -->
</div>

<!-- INCORRECT - Missing ID -->
<div class="card">
  <!-- content -->
</div>
```

This ID is used to update the content after successful form submission.

## Error Handling

Form validation errors are automatically handled:

- Errors are displayed in the modal
- The form is not submitted until valid
- The modal stays open until submission is successful

## JavaScript Events

The package triggers several events you can listen to:

```javascript
// Modal is about to be shown
document.addEventListener("modal:show", (event) => {
  console.log("Modal is opening");
});

// Modal is about to be closed
document.addEventListener("modal:close", (event) => {
  console.log("Modal is closing");
});
```

## Customizing Modal Appearance

You can customize the modal's appearance using the `modal_size` attribute:

```python
class PersonCreateView(HtmxModalCreateView):
    model = Person
    form_class = PersonForm
    detail_template_name = "persons/_person_card.html"
    modal_size = "xl"  # Makes the modal extra large
```

Available sizes:

- `"sm"` - Small modal
- `"lg"` - Large modal (default)
- `"xl"` - Extra large modal
