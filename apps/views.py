from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView

from apps.models import Category, Product


class MainBaseView(ListView):
    queryset = Category.objects.all()
    template_name = 'apps/product/product_list.html'
    context_object_name = "categories"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['products'] = Product.objects.all()
        return context


class ProductDetailView(DetailView):
    queryset = Product.objects.all()
    template_name = 'apps/product/product_list.html'
    context_object_name = "product"


class ProductListByCategoryListView(DetailView):
    queryset = Product.objects.order_by('-created_at')
    template_name = 'apps/parts/_category_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        qs = super().get_queryset()
        slug = self.kwargs.get(self.slug_url_kwarg)
        if slug is not None:
            qs = qs.filter(category__slug=slug)

        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['categories'] = Category.objects.all()
        return context


class CustomLoginView(LoginView):
    template_name = 'apps/auth/login.html'
    redirect_authenticated_user = True
    next_page = reverse_lazy('main_base')


class CustomRegisterView(TemplateView):
    pass


class CustomLogautView(LoginRequiredMixin, View):
    pass
