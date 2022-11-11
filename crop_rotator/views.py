from django.utils.functional import cached_property
from django.views.generic import UpdateView


class CreateOrUpdateMixin:
    """
    A mixin to make an ``UpdateView`` behave like an ``CreateView`` when the ID argument is missing.
    The ``is_add`` attribute allows views to make small changes depending on the way the view is called.
    Note this mixin is designed to save code. When the create and update logic differs a lot,
    write them as separate views.
    """

    @cached_property
    def is_add(self):
        return self.pk_url_kwarg not in self.kwargs and self.slug_url_kwarg not in self.kwargs

    def get_object(self, queryset=None):
        if self.is_add:
            return None
        else:
            return super().get_object(queryset=queryset)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_add'] = self.is_add
        return context


class CreateOrUpdateView(CreateOrUpdateMixin, UpdateView):
    """
    Merging the logic of Django's
    :class:`~django.views.generic.edit.CreateView` and
    :class:`~django.views.generic.edit.UpdateView`.
    This provides the class to inherit from for standard views.
    """
    template_name_suffix = '_form'