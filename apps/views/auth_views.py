from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import UpdateView, DetailView, ListView

from apps.forms import UserAuthenticatedForm, UserSettingsForm, UserChangePasswordForm, OperatorUpdateForm
from apps.mixins import GetObjectMixins
from apps.models import User, Region, Product, Order, SiteSettings


class UserLoginView(LoginView):
    template_name = 'apps/auth/login.html'
    redirect_authenticated_user = True
    form_class = UserAuthenticatedForm

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return redirect('main_base')


class UserLogautView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        logout(request)

        return redirect('main_base')


class UserChangeImageView(LoginRequiredMixin, GetObjectMixins, UpdateView):
    queryset = User.objects.values('image')
    template_name = 'apps/auth/settings.html'
    success_url = reverse_lazy('settings_page')
    fields = 'image',


class UserSettingsView(LoginRequiredMixin, GetObjectMixins, UpdateView):
    queryset = User.objects.all()
    template_name = 'apps/auth/settings.html'
    success_url = reverse_lazy('settings_page')
    form_class = UserSettingsForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['regions'] = Region.objects.all()
        return context


class UserChangePasswordView(LoginRequiredMixin, GetObjectMixins, UpdateView):
    queryset = User.objects.all()
    template_name = 'apps/auth/settings.html'
    success_url = reverse_lazy('settings_page')
    form_class = UserChangePasswordForm

    def form_valid(self, form):
        user = form.save(commit=False)
        login(self.request, user=user.save())
        return redirect(self.success_url)


class OperatorOrderListView(ListView):
    queryset = Order.objects.all()
    template_name = 'apps/operators/operator.html'
    context_object_name = 'orders'

    def get_queryset(self):
        qs = super().get_queryset()
        status = self.request.path.split('/')[-2]
        if status:
            qs = qs.filter(status=status)
        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['regions'] = Region.objects.all()
        context['products'] = Product.objects.all()

        return context


class OperatorDetailView(DetailView, UpdateView):
    queryset = Order.objects.all()
    template_name = 'apps/operators/operator_detail.html'
    context_object_name = 'order'
    form_class = OperatorUpdateForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['regions'] = Region.objects.all()
        context['site_settings'] = SiteSettings.objects.all()
        return context
