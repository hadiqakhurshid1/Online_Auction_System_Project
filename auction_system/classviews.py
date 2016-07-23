from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.conf.urls import url
from models import *
from django.views.generic.edit import UpdateView, CreateView
from django.core.urlresolvers import reverse
from django.views.generic.edit import DeleteView
from django.views.generic.edit import FormView
from auction_system.forms import *
from django.http import *
from django.contrib.auth import authenticate, login, logout
from forms import UserCreateForm

class ProductView(ListView):
    model=Product

class AddProductView(CreateView):
    model = Product
    fields = ["product_name", "category", "minimum_price", "bid_end_date", "image", "description"]

    def form_valid(self, form):
        obj = Seller(user_name = self.request.user, product_id = form.save())
        obj.save()
        return super(AddProductView, self).form_valid(form)

    def get_success_url(self):
        return reverse('view_product')

class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'product_list'

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        x = Seller.objects.all()
        context["seller"] = Seller.objects.get(product_id_id=self.kwargs['pk'])
        return context

class UserCreateView(CreateView):
    model = User
    form_class = UserCreateForm

    def get_success_url(self):
        user = authenticate(username=self.request.POST['username'], password=self.request.POST['password1'])
        if user is not None:
            if user.is_active:
                login(self.request, user)
                return reverse('view_product')
        return reverse('register')

class ProductDelete(DeleteView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super(ProductDelete, self).get_context_data(**kwargs)
        context["product_id"] = self.kwargs['pk']
        return context
    def get_success_url(self):
        return reverse('view_product')

class BidderListView(ListView):
    model = Bidder

    def get_queryset(self):
        return Bidder.objects.filter(product_id=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(BidderListView, self).get_context_data(**kwargs)
        context["product_id"] = self.kwargs['pk']
        return context