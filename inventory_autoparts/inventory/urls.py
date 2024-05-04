'''
Inventory URLs
'''
from django.urls import path
from django.contrib.auth import views as auth_views
from django.utils.translation import gettext_lazy as _
from .views import AddItem, EditItem, Index, SignUpView, Dashboard, DeleteItem, AddLine, AddBuy, AddSell, BuyList, SellList


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
    path('add-buy', AddBuy.as_view(), name='add-buy'),
    path('add-sell', AddSell.as_view(), name='add-sell'),
    path('buy-list', BuyList.as_view(), name='buy-list'),
    path('sell-list', SellList.as_view(), name='sell-list'),
]
