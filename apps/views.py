from django.views.generic import ListView

from apps.models import Category, Product


class CategoryListView(ListView):
    queryset = Category.objects.all()
    template_name = 'apps/main_base.html'
    context_object_name = "categories"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['products'] = Product.objects.all()
        return context
