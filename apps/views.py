import re

from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView

from apps.models import Category, Product, User


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
    template_name = 'apps/product/product_detail.html'
    context_object_name = "product"


class ProductListByCategoryListView(ListView):
    queryset = Product.objects.order_by('-created_at')
    template_name = 'apps/product/category_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        qs = super().get_queryset()
        slug = self.kwargs.get('slug')
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

    def post(self, request, *args, **kwargs):  # noqa
        phone = re.sub(r'\D', '', request.POST.get('phone'))
        user = User.objects.filter(phone=phone).first()
        if not user:
            user = User.objects.create_user(phone=phone, password=request.POST['password'])
            login(request, user)
            return redirect('main_base')
        else:
            user = authenticate(request, username=user.phone, password=request.POST['password'])
            if user:
                login(request, user)
                return redirect('main_base')
        return render(request, template_name='apps/auth/login.html', context={"messages_error": ["Invalid password"]
                                                                              })


class FavoriteView(ListView):
    queryset = Product.objects.all()
    template_name = 'apps/product/favorite.html'


class CustomLogautView(LoginRequiredMixin, View):
    template_name = 'apps/auth/login.html'

    def get(self, request, *args, **kwargs):
        logout(request)

        return redirect('main_base')


class CoinsView(TemplateView):
    template_name = 'apps/coins.html'


class PaymentView(TemplateView):
    template_name = 'apps/payment.html'


class DiagramView(TemplateView):
    template_name = 'apps/diagram.html'


class CompetitionView(TemplateView):
    template_name = 'apps/competition.html'
