"""Views"""

from django.forms import BaseModelForm, formset_factory
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormView
from django.utils.translation import gettext_lazy as _
from django.db.models import F

from inventory_autoparts.settings import LOW_QUANTITY

from .models import InventoryItem, Line, Buy, Sell
from .forms import BuyFormSetHelper, InventoryItemForm, LineForm, SellFormSetHelper, UserRegisterForm, BuyForm, SellForm
# from .formsets import BuyFormSet

# Create your views here.


class Index(TemplateView):
    """Index"""

    template_name = "inventory/index.html"


class Dashboard(LoginRequiredMixin, View):
    """Dashboard"""

    def get(self, request):
        """ Dashboard Get """
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


class AddBuy(LoginRequiredMixin, FormView):
    """Add Buy"""

    model = Buy
    form_class = formset_factory(BuyForm, extra=1)
    # helper = BuyFormSetHelper()
    template_name = "inventory/buy_form.html"
    success_url = reverse_lazy("dashboard")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["items"] = InventoryItem.objects.all()
        context["helper"] = BuyFormSetHelper()
        return context

    def form_valid(self, form) -> HttpResponse:
        if form.is_valid():
            print("Formset válido")
            for f in form:
                print("Form válido")
                if f.is_valid():
                    f.save()
                    # print(f.instance.quantity)
                    InventoryItem.objects.filter(name=f.instance.item).update(
                        quantity=F("quantity") + f.instance.quantity
                    )
        return super().form_valid(form)


class AddSell(LoginRequiredMixin, FormView):
    """Add Sell"""

    model = Sell
    form_class = formset_factory(SellForm, extra=1)
    template_name = "inventory/sell_form.html"
    success_url = reverse_lazy("dashboard")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["items"] = InventoryItem.objects.all()
        context["helper"] = SellFormSetHelper()
        return context

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        if form.is_valid():
            print("Formset válido")
            for f in form:
                print("Form válido")
                if f.is_valid():
                    f.save()
                    # print(f.instance.quantity)
                    InventoryItem.objects.filter(name=f.instance.item).update(
                        quantity=F("quantity") - f.instance.quantity
                    )
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
    
