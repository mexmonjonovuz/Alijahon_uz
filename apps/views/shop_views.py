from datetime import timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q, Sum
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, CreateView

from apps.forms import OrderCreateForm, StreamForm
from apps.models import Order, SiteSettings, Product, Stream, Favorite, Competition, User


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
        context['site_settings'] = SiteSettings.objects.first()
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
    queryset = User.objects.all()
    template_name = 'apps/statistics/competition.html'
    context_object_name = 'users'

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data(object_list=object_list, **kwargs)
        ctx['competition'] = Competition.objects.filter(is_active=True).first()
        return ctx

    def get_queryset(self):
        qs = super().get_queryset().exclude(type=User.Type.ADMIN)
        competition = Competition.objects.filter(is_active=True).first()
        if competition:
            start_date = competition.start_date
            end_date = competition.end_date

            qs = qs.annotate(
                order_product_count=Sum(
                    'streams__orders__quantity',
                    filter=Q(streams__orders__status=Order.StatusType.DELIVERED) &
                           Q(streams__orders__created_at__range=(start_date, end_date))
                )
            ).filter(order_product_count__isnull=False).order_by('-order_product_count')

        return qs


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
            new=Count('orders', filter=Q(orders__status=Order.StatusType.NEW)),
            ready=Count('orders', filter=Q(orders__status=Order.StatusType.READY)),
            deliver=Count('orders', filter=Q(orders__status=Order.StatusType.DELIVERING)),
            delivered=Count('orders', filter=Q(orders__status=Order.StatusType.DELIVERED)),
            cant_phone=Count('orders', filter=Q(orders__status=Order.StatusType.CANT_PHONE)),
            broken=Count('orders', filter=Q(orders__status=Order.StatusType.BROKEN)),
            canceled=Count('orders', filter=Q(orders__status=Order.StatusType.CANCELED)),
            archived=Count('orders', filter=Q(orders__status=Order.StatusType.ARCHIVED)),
        )
        qs.stream = qs.aggregate(
            total_visit_count=Sum('visit_count'),
            total_new_count=Sum(Order.StatusType.NEW),
            total_ready_count=Sum(Order.StatusType.READY),
            total_deliver_count=Sum(Order.StatusType.DELIVERING),
            total_delivered_count=Sum(Order.StatusType.DELIVERED),
            total_cant_phone_count=Sum(Order.StatusType.CANT_PHONE),
            total_broken_count=Sum(Order.StatusType.CANCELED),
            total_canceled_count=Sum(Order.StatusType.CANCELED),
            total_archived_count=Sum(Order.StatusType.ARCHIVED),
        )
        return qs



