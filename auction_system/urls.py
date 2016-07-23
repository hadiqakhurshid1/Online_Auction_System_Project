from django.conf.urls import url, include
from django.contrib import admin
import auction_system.views
from classviews import *
from django.contrib.auth.decorators import login_required
from django.conf.urls.static import static
from django.conf import settings





urlpatterns = [
    url(r'^$', auction_system.views.index, name="index"),
    url(r'^viewproduct/', login_required(ProductView.as_view()), name="view_product"),
    url(r'^addproduct/', login_required(AddProductView.as_view()), name="add_product"),
    url(r'^productdetails/(?P<pk>[0-9]+)', login_required(ProductDetailView.as_view()), name="product_detail"),
    url(r'^save_bid/', login_required(auction_system.views.save_bid), name="save_bid"),
    url(r'^register_user/', UserCreateView.as_view(), name="register"),
    url(r'^deleteproduct/(?P<pk>[0-9]+)', login_required(ProductDelete.as_view()), name="delete_product"),
    url(r'^bidderlist/(?P<pk>[0-9]+)', login_required(BidderListView.as_view()), name="bidder_list"),
    url(r'^logout/', 'django.contrib.auth.views.logout_then_login')
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
