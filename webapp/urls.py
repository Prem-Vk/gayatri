from django.urls import path
from webapp.views import HomePage, ProductPage,CategoryWiseProduct, search, add_client

urlpatterns = [
    path("", HomePage.as_view(), name="home_page"),
    path("product/<int:id>/", ProductPage.as_view(), name="product"),
    path("category/<int:id>/", CategoryWiseProduct.as_view(), name="category"),
    path('search/', search, name='search_product'),
    path('add-client', add_client, name="add_client")
]