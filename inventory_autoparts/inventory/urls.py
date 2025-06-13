'''
Inventory URLs
'''
from django.urls import path
from django.contrib.auth import views as auth_views
from django.utils.translation import gettext_lazy as _
from .views import AddItem, EditItem, Index, SignUpView, Dashboard, DeleteItem, AddLine, AddBuy, AddSell, BuyList, SellList, AddThirdParty, ThirdPartyList, create_buy_item, create_buy_item_form, create_sell_item, create_sell_item_form, delete_buy_item, delete_sell_item, detail_buy_item, detail_sell_item, update_buy_item, update_sell_item


urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='inventory/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='inventory/logout.html'), name='logout'),
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('add-item', AddItem.as_view(), name='add-item'),
    path('edit-item/<int:pk>', EditItem.as_view(), name='edit-item'),
    path('delete-item/<int:pk>', DeleteItem.as_view(), name='delete-item'),
    path('add-line', AddLine.as_view(), name='add-line'),
    path('add-third-party', AddThirdParty.as_view(), name='add-third-party'),
    path('add-buy', AddBuy.as_view(), name='add-buy'),
    path('add-sell', AddSell.as_view(), name='add-sell'),
    path('buy-list', BuyList.as_view(), name='buy-list'),
    path('sell-list', SellList.as_view(), name='sell-list'),
    path('third-party-list', ThirdPartyList.as_view(), name='third-party-list'),
    path('buy/<int:pk>/', create_buy_item, name='create-buy-item'),
    path('buy/create-buy-item-form/', create_buy_item_form, name='create-buy-item-form'),
    path('buy/buyitem/<int:pk>/', detail_buy_item, name="detail-buy-item"),
    path('buy/buyitem/<int:pk>/update/', update_buy_item, name="update-buy-item"),
    path('buy/buyitem/<int:pk>/delete/', delete_buy_item, name="delete-buy-item"),
    path('sell/<int:pk>/', create_sell_item, name='create-sell-item'),
    path('sell/create-buy-item-form/', create_sell_item_form, name='create-sell-item-form'),
    path('sell/sellitem/<int:pk>/', detail_sell_item, name="detail-sell-item"),
    path('sell/sellitem/<int:pk>/update/', update_sell_item, name="update-sell-item"),
    path('sell/sellitem/<int:pk>/delete/', delete_sell_item, name="delete-sell-item"),
]
