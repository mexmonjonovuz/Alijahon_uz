from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, TemplateView, CreateView

from apps.forms import TransactionCreateForm
from apps.mixins import GetObjectMixins
from apps.models import Product, District, Order
from apps.models.shop import Transaction


class InquiriesView(ListView):
    queryset = Order.objects.all().select_related('product', 'stream', 'operator')
    template_name = 'apps/parts/_inquiries.html'
    context_object_name = 'orders'


class CoinsView(TemplateView):
    template_name = 'apps/statistics/coins.html'


class TransactionCreateView(CreateView, GetObjectMixins):
    model = Transaction
    template_name = 'apps/payment.html'
    form_class = TransactionCreateForm
    success_url = reverse_lazy('payment_page')

    def form_valid(self, form):
        messages.add_message(self.request, message="Muvoffaqiyatli (24 soat ichida kiritilgan kartaga o'tkaziladi )!!",
                             level=messages.SUCCESS)
        form.user = self.request.user
        form.save()
        return super().form_invalid(form)

    def form_invalid(self, form):
        messages.add_message(self.request,
                             message="Karta raqami yoki kiritilayotgan Mablag' noto'gri bo'lishi mumkin tekshirib qaytadan uruning !!!",
                             level=messages.ERROR)
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['transactions'] = Transaction.objects.all().order_by('-created_at').filter(user=self.request.user)
        return ctx


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
            qs = Product.objects.filter(
                Q(name__icontains=search) | Q(description__icontains=search)
            )
        return qs

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        paginator = Paginator(queryset, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        results = [{'name': product.name} for product in page_obj]
        return JsonResponse(results, safe=False)
