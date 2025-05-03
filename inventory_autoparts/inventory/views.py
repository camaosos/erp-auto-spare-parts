"""Views"""

from django.forms import BaseModelForm, formset_factory
from django.http import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormView
from django.utils.translation import gettext_lazy as _
from django.db.models import F
from django.views.decorators.csrf import csrf_exempt


from inventory_autoparts.settings import LOW_QUANTITY

from .models import InventoryItem, Line, Buy, Sell, BuyItem, SellItem
from .forms import (
    InventoryItemForm,
    LineForm,
    UserRegisterForm,
    BuyForm,
    SellForm,
    BuyItemForm,
    SellItemForm,
)

# Create your views here.
def create_buy_item(request, pk):
    """
    Create buy item
    """
    buy = Buy.objects.get(id=pk)
    buy_items = BuyItem.objects.filter(buy=buy)
    form = BuyItemForm(request.POST or None)
 
    if request.method == "POST":
        if form.is_valid():
            buy_item = form.save(commit=False)
            buy_item.buy = buy
            buy_item.save()

            # Update inventory item quantity
            inventory_item = InventoryItem.objects.get(id=buy_item.item.id)
            inventory_item.quantity = F("quantity") + buy_item.quantity
            inventory_item.save()

            return redirect("detail-buy-item", pk=buy_item.id)
        else:
            return render(request, "inventory/buy_item_form.html", context={
                "form": form
            })
 
    context = {
        "form": form,
        "buy": buy,
        "buy_items": buy_items
    }
 
    return render(request, "inventory/create_buy_item.html", context)


def create_buy_item_form(request):
    """
    Create buy item form
    """
    form = BuyItemForm()
    context = {
        "form": form
    }
    return render(request, "inventory/buy_item_form.html", context)


def detail_buy_item(request, pk):
    """
    Detail buy item
    """
    buy_item = get_object_or_404(BuyItem, id=pk)
    context = {
        "buy_item": buy_item
    }
    return render(request, "inventory/buy_item_detail.html", context)


def update_buy_item(request, pk):
    """
    Update buy item
    """
    buy_item = BuyItem.objects.get(id=pk)
    original_quantity = buy_item.quantity
    form = BuyItemForm(request.POST or None, instance=buy_item)
 
    if request.method == "POST":
        if form.is_valid():
            # Update inventory item quantity
            inventory_item = InventoryItem.objects.get(id=buy_item.item.id)
            inventory_item.quantity = F("quantity") - original_quantity + form.instance.quantity
            form.save()
            inventory_item.save()
            return redirect("detail-buy-item", pk=buy_item.id)
 
    context = {
        "form": form,
        "buy_item": buy_item
    }
 
    return render(request, "inventory/buy_item_form.html", context)

@csrf_exempt
def delete_buy_item(request, pk):
    """
    Delete Buy Item
    """
    buy_item = get_object_or_404(BuyItem, id=pk)

    # Get the inventory item associated with the buy item
    inventory_item = InventoryItem.objects.get(id=buy_item.item.id)

    # Update the inventory item quantity
    inventory_item.quantity = F("quantity") - buy_item.quantity
    inventory_item.save()
 
    if request.method == "POST":
        buy_item.delete()
        return HttpResponse("")
 
    return HttpResponseNotAllowed(
        [
            "POST",
        ]
    )


def create_sell_item(request, pk):
    """
    Create sell item
    """
    sell = Sell.objects.get(id=pk)
    sell_items = SellItem.objects.filter(sell=sell)
    form = SellItemForm(request.POST or None)
 
    if request.method == "POST":
        if form.is_valid():
            sell_item = form.save(commit=False)
            sell_item.sell = sell
            sell_item.save()

            # Update inventory item quantity
            inventory_item = InventoryItem.objects.get(id=sell_item.item.id)
            inventory_item.quantity = F("quantity") - sell_item.quantity
            inventory_item.save()

            return redirect("detail-sell-item", pk=sell_item.id)
        else:
            return render(request, "inventory/sell_item_form.html", context={
                "form": form
            })
 
    context = {
        "form": form,
        "sell": sell,
        "sell_items": sell_items
    }
 
    return render(request, "inventory/create_sell_item.html", context)


def create_sell_item_form(request):
    """
    Create sell item form
    """
    form = SellItemForm()
    context = {
        "form": form
    }
    return render(request, "inventory/sell_item_form.html", context)


def detail_sell_item(request, pk):
    """
    Detail sell item
    """
    sell_item = get_object_or_404(SellItem, id=pk)
    context = {
        "sell_item": sell_item
    }
    return render(request, "inventory/sell_item_detail.html", context)


def update_sell_item(request, pk):
    """
    Update sell item
    """
    sell_item = SellItem.objects.get(id=pk)
    original_quantity = sell_item.quantity
    form = SellItemForm(request.POST or None, instance=sell_item)
 
    if request.method == "POST":
        if form.is_valid():
            # Update inventory item quantity
            inventory_item = InventoryItem.objects.get(id=sell_item.item.id)
            inventory_item.quantity = F("quantity") + original_quantity - form.instance.quantity
            form.save()
            inventory_item.save()           
            return redirect("detail-sell-item", pk=sell_item.id)
 
    context = {
        "form": form,
        "sell_item": sell_item
    }
 
    return render(request, "inventory/sell_item_form.html", context)

@csrf_exempt
def delete_sell_item(request, pk):
    """
    Delete Sell Item
    """
    sell_item = get_object_or_404(SellItem, id=pk)

    # Update inventory item quantity
    inventory_item = InventoryItem.objects.get(id=sell_item.item.id)
    inventory_item.quantity = F("quantity") + sell_item.quantity
    # Save the inventory item
    inventory_item.save()
 
    if request.method == "POST":
        sell_item.delete()
        return HttpResponse("")
 
    return HttpResponseNotAllowed(
        [
            "POST",
        ]
    )

class Index(TemplateView):
    """Index"""

    template_name = "inventory/index.html"


class Dashboard(LoginRequiredMixin, View):
    """Dashboard"""

    def get(self, request):
        """Dashboard Get"""
        items = InventoryItem.objects.filter(user=self.request.user.id).order_by("id")
        low_inventory = items.filter(
            user=self.request.user.id, quantity__lte=LOW_QUANTITY
        )

        low_inventory_ids = low_inventory.values_list("id", flat=True)
        if low_inventory.count() >= 1:
            messages.error(
                request=request,
                message=_("Items {list_low_inventory_ids} with low inventory").format(
                    list_low_inventory_ids=list(low_inventory_ids)
                ),
                # message = ngettext("Item {the_number} with low inventory".format(the_number = list(low_inventory_ids)[0]),
                #                    "Items {the_list} with low inventory".format(the_list = list(low_inventory_ids)),
                #                    low_inventory_ids.count())
            )

        return render(
            request=request,
            template_name="inventory/dashboard.html",
            context={"items": items, "low_inventory_ids": low_inventory_ids},
        )


class SignUpView(View):
    """Sign Up View"""

    def get(self, request):
        """Get"""
        form = UserRegisterForm()
        return render(
            request=request,
            template_name="inventory/signup.html",
            context={"form": form},
        )

    def post(self, request):
        """Post"""
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password1"],
            )
            login(request, user)
            return redirect("index")

        return render(
            request=request,
            template_name="inventory/signup.html",
            context={"form": form},
        )


class AddItem(LoginRequiredMixin, CreateView):
    """Add Item"""

    model = InventoryItem
    form_class = InventoryItemForm
    template_name = "inventory/item_form.html"
    success_url = reverse_lazy("dashboard")

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context["lines"] = Line.objects.all()
        return context

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.user = self.request.user
        return super().form_valid(form)


class EditItem(LoginRequiredMixin, UpdateView):
    """Edit Item"""

    model = InventoryItem
    form_class = InventoryItemForm
    template_name = "inventory/item_form.html"
    success_url = reverse_lazy("dashboard")


class DeleteItem(LoginRequiredMixin, DeleteView):
    """Delete Item"""

    model = InventoryItem
    template_name = "inventory/delete_item.html"
    success_url = reverse_lazy("dashboard")
    context_object_name = "item"


class AddLine(LoginRequiredMixin, CreateView):
    """Add Item"""

    model = Line
    form_class = LineForm
    template_name = "inventory/line_form.html"
    success_url = reverse_lazy("dashboard")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.user = self.request.user
        return super().form_valid(form)


class AddBuy(LoginRequiredMixin, CreateView):
    """Add Buy"""

    model = Buy
    form_class = BuyForm
    template_name = "inventory/buy_form.html"

    def get_success_url(self):
        return reverse_lazy("create-buy-item", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.user = self.request.user
        return super().form_valid(form)



class AddSell(LoginRequiredMixin, CreateView):
    """Add Sell"""

    model = Sell
    form_class = SellForm
    template_name = "inventory/sell_form.html"

    def get_success_url(self):
        return reverse_lazy("create-sell-item", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.user = self.request.user
        return super().form_valid(form)


class BuyList(LoginRequiredMixin, View):
    def get(self, request):
        buys = Buy.objects.order_by("id")

        return render(
            request=request,
            template_name="inventory/buy_list.html",
            context={"buys": buys},
        )


class SellList(LoginRequiredMixin, View):
    def get(self, request):
        sells = Sell.objects.order_by("id")

        return render(
            request=request,
            template_name="inventory/sell_list.html",
            context={"sells": sells},
        )
