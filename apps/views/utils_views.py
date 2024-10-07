from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, TemplateView, CreateView

from apps.forms import TransactionCreateForm
from apps.models import Product, District, Order
from apps.models.shop import Transaction


class InquiriesView(ListView):
    queryset = Order.objects.all().select_related('product', 'stream', 'operator')
    template_name = 'apps/parts/_inquiries.html'
    context_object_name = 'orders'


class CoinsView(TemplateView):
    template_name = 'apps/statistics/coins.html'


class PaymentCreateView(CreateView):
    model = Transaction
    template_name = 'apps/payment.html'
    form_class = TransactionCreateForm
    success_url = reverse_lazy('payment_page')

    def form_valid(self, form):
        # form.instance.user = self.request.user
        return super().form_invalid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class PaymentListView(ListView):
    queryset = Transaction.objects.all()
    template_name = 'apps/payment.html'
    context_object_name = 'transactions'


class DiagramView(TemplateView):
    template_name = 'apps/statistics/diagram.html'


class DistrictListView(LoginRequiredMixin, View):
    def get(self, request, region_id):
        districts = District.objects.filter(region_id=region_id).values('id', 'name')
        return JsonResponse(list(districts), safe=False)


class HeaderSearchView(ListView):
    model = Product
    template_name = 'apps/parts/_header.html'

    def get_queryset(self):
        qs = super().get_queryset()
        search = self.request.GET.get('search')
        if search:
            qs = qs.filter(name__icontains=search, description__icontains=search)

        return qs
