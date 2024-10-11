from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView

from apps.models import Category, Product, Stream


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


class ProductOrStreamDetailView(DetailView):
    template_name = 'apps/products/product_detail.html'
    context_object_name = 'product'

    def get_object(self, queryset=None):
        slug = self.kwargs.get('slug')
        pk = self.kwargs.get('pk')
        self._cache_stream = None
        if pk:
            self._cache_stream = get_object_or_404(Stream, pk=pk)  # noqa
            self._cache_stream.visit_count += 1
            self._cache_stream.save()
            return self._cache_stream.product
        else:
            return get_object_or_404(Product, slug=slug)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        price = self.object.price
        if self._cache_stream:
            price -= self._cache_stream.discount
        ctx['stream_id'] = self.kwargs.get(self.pk_url_kwarg, '')
        ctx['price'] = price
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
