from datetime import timedelta

from django.contrib.auth import logout, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db.models import Count, Q, Sum
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView, UpdateView, CreateView

from apps.forms import UserSettingsForm, StreamForm, UserChangePasswordForm, UserAuthenticatedForm, OrderCreateForm, \
    OperatorUpdateForm
from apps.models import Category, Product, User, Region, District, Stream, Order, Competition, Favorite, SiteSettings


class MainBaseView(ListView):
    queryset = Product.objects.prefetch_related('category').all()
    template_name = 'apps/products/product_list.html'
    context_object_name = "products"
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['categories'] = Category.objects.all()
        return context


class ProductListByCategoryListView(ListView):
    queryset = Product.objects.select_related('category').order_by('-created_at')
    template_name = 'apps/products/category_list.html'
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


class UserChangeImage(LoginRequiredMixin, UpdateView):
    queryset = User.objects.values('image')
    template_name = 'apps/auth/settings.html'
    success_url = reverse_lazy('settings_page')
    fields = 'image',

    def get_object(self, queryset=None):
        return self.request.user


class UserSettingsView(LoginRequiredMixin, UpdateView):
    queryset = User.objects.all()
    template_name = 'apps/auth/settings.html'
    success_url = reverse_lazy('settings_page')
    form_class = UserSettingsForm

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['regions'] = Region.objects.all()
        return context


class DistrictListView(LoginRequiredMixin, View):
    def get(self, request, region_id):
        districts = District.objects.filter(region_id=region_id).values('id', 'name')
        return JsonResponse(list(districts), safe=False)


class UserChangePasswordView(LoginRequiredMixin, UpdateView):
    queryset = User.objects.all()
    template_name = 'apps/auth/settings.html'
    success_url = reverse_lazy('settings_page')
    form_class = UserChangePasswordForm

    def form_valid(self, form):
        user = form.save(commit=False)
        login(self.request, user=user.save())
        return redirect(self.success_url)

    def get_object(self, queryset=None):
        return self.request.user


class MarketView(ListView):
    queryset = Product.objects.select_related('category').all()
    template_name = 'apps/market.html'
    context_object_name = 'products'
    paginate_by = 5

    def get_queryset(self):
        qs = super().get_queryset()
        slug = self.kwargs.get('slug')
        if slug is not None:
            qs = qs.filter(category__slug=slug)
        search = self.request.GET.get('search')
        if search:
            qs = qs.filter(name__icontains=search)

        return qs


class HeaderSearchView(ListView):
    model = Product
    template_name = 'apps/parts/_header.html'

    def get_queryset(self):
        qs = super().get_queryset()
        search = self.request.GET.get('search')
        if search:
            qs = qs.filter(name__icontains=search, description__icontains=search)

        return qs


class OrderListView(ListView):
    queryset = Order.objects.all()
    template_name = 'apps/orders/order_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class CreatedSuccessOrderedView(CreateView):
    model = Order
    form_class = OrderCreateForm
    template_name = 'apps/orders/success_ordered.html'

    def form_valid(self, form):
        order = form.save()
        context = self.get_context_data(form=form)
        context['order'] = order
        context[
            'site_settings'] = SiteSettings.objects.all().first()
        return render(self.request, self.template_name, context)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class StreamCreateView(LoginRequiredMixin, CreateView):
    queryset = Product.objects.all()
    template_name = 'apps/market.html'
    form_class = StreamForm
    success_url = reverse_lazy('steam_page')


class StreamListView(LoginRequiredMixin, ListView):
    queryset = Stream.objects.all()
    template_name = 'apps/orders/stream_list.html'
    context_object_name = 'streams'

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data(object_list=object_list, **kwargs)
        ctx['product'] = Product.objects.all().first()
        return ctx


# class ProductDetailView(DetailView):
#     queryset = Product.objects.all()
#     template_name = 'apps/products/product_detail.html'
#     context_object_name = "product"


# class StreamDetailView(DetailView):
#     queryset = Product.objects.all()
#     template_name = 'apps/orders/stream_detail.html'
#     context_object_name = 'product'
#
#     def get_object(self, queryset=None):
#         pk = self.kwargs.get(self.pk_url_kwarg)
#         self._cache_stream = None
#         if pk is not None:
#             self._cache_stream = get_object_or_404(Stream.objects.all(), pk=pk)  # noqa
#             self._cache_stream.visit_count += 1
#             self._cache_stream.save()
#             return self._cache_stream.product
#         return super().get_object(queryset)
#
#     def get_context_data(self, **kwargs):
#         ctx = super().get_context_data(**kwargs)
#         price = self.object.price
#         if self._cache_stream:
#             price -= self._cache_stream.discount
#         ctx['stream_id'] = self.kwargs.get(self.pk_url_kwarg, '')
#         ctx['price'] = price
#         return ctx


class ProductOrStreamDetailView(DetailView):
    template_name = 'apps/products/product_detail.html'
    context_object_name = 'product'

    def get_object(self, queryset=None):
        slug = self.kwargs.get('slug')
        pk = self.kwargs.get('pk')
        self._cache_stream = None

        if pk is not None:
            self._cache_stream = get_object_or_404(Stream.objects.all(), pk=pk)
            self._cache_stream.visit_count += 1
            self._cache_stream.save()
            return self._cache_stream.product
        else:
            return get_object_or_404(Product.objects.all().first(), slug=slug)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        price = self.object.price
        if self._cache_stream:
            price -= self._cache_stream.discount
        ctx['stream_id'] = self.kwargs.get(self.pk_url_kwarg, '')
        ctx['price'] = price
        return ctx


class FavouriteListView(ListView):
    model = Favorite
    template_name = 'apps/products/favorite.html'
    context_object_name = 'favorites'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(user=self.request.user)
        return qs


class FavoriteView(LoginRequiredMixin, View):
    template_name = 'apps/products/category_list.html'

    def get(self, request, pk, *args, **kwargs):
        obj, created = Favorite.objects.get_or_create(user=request.user, product_id=pk)
        if not created:
            obj.delete()
        referer = request.META.get('HTTP_REFERER')
        if referer:
            return redirect(referer)
        else:
            return redirect('product_detail', pk=pk)


class CompetitionListView(ListView):
    queryset = Competition.objects.filter(is_active=True).first()
    template_name = 'apps/statistics/competition.html'
    context_object_name = 'competition'

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data(object_list=object_list, **kwargs)
        user = User.objects.filter(orders__status='Delivered').values('first_name')
        return ctx


class ProductStatisticView(DetailView):
    queryset = Product.objects.all()
    template_name = 'apps/products/product_statistic.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        product = self.get_object()
        context = super().get_context_data(**kwargs)
        context['product_stream_count'] = product.streams.count()
        context['owner_stream_count'] = product.streams.filter(owner=self.request.user).count()
        return context


class StatisticView(LoginRequiredMixin, ListView):
    model = Stream
    template_name = 'apps/statistics/statistic.html'
    context_object_name = 'streams'

    def get_queryset(self, *args, **kwargs):
        now = timezone.now()
        period = self.request.GET.get('period')

        periods = {
            'today': now.replace(hour=0, minute=0, second=0),
            'yesterday': now.replace(hour=0, minute=0, second=0) - timedelta(days=1),
            'weekly': now - timedelta(days=now.weekday()),
            'monthly': now.replace(day=30),
            'all': None
        }
        start_date = periods.get(period)

        qs = super().get_queryset().filter(owner=self.request.user)
        if start_date:
            qs = qs.filter(orders__created_at__gte=start_date)
        qs = qs.annotate(
            new=Count('orders', filter=Q(orders__status='new')),
            ready=Count('orders', filter=Q(orders__status='ready')),
            deliver=Count('orders', filter=Q(orders__status='deliver')),
            delivered=Count('orders', filter=Q(orders__status='delivered')),
            cant_phone=Count('orders', filter=Q(orders__status='cant_phone')),
            canceled=Count('orders', filter=Q(orders__status='canceled')),
            archived=Count('orders', filter=Q(orders__status='archived')),
        )
        qs.stream = qs.aggregate(
            total_visit_count=Sum('visit_count'),
            total_new_count=Sum('new'),
            total_ready_count=Sum('ready'),
            total_deliver_count=Sum('deliver'),
            total_delivered_count=Sum('delivered'),
            total_cant_phone_count=Sum('cant_phone'),
            total_canceled_count=Sum('canceled'),
            total_archived_count=Sum('archived'),
        )
        return qs


class InquiriesView(ListView):
    queryset = Order.objects.all()
    template_name = 'apps/parts/_inquiries.html'
    context_object_name = 'orders'


class UserProfileView(TemplateView):
    template_name = 'apps/auth/profile.html'


class CoinsView(TemplateView):
    template_name = 'apps/statistics/coins.html'


class PaymentView(TemplateView):
    template_name = 'apps/payment.html'


class DiagramView(TemplateView):
    template_name = 'apps/statistics/diagram.html'


class AdminsView(TemplateView):
    template_name = 'apps/auth/admin.html'


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
