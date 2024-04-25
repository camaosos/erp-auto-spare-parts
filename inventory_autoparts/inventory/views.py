"""Views"""

from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View, CreateView, UpdateView, DeleteView
from inventory_autoparts.settings import LOW_QUANTITY

from .models import InventoryItem, Line
from .forms import InventoryItemForm, LineForm, UserRegisterForm

# Create your views here.


class Index(TemplateView):
    """Index"""

    template_name = "inventory/index.html"


class Dashboard(LoginRequiredMixin, View):
    """Dashboard"""

    def get(self, request):
        items = InventoryItem.objects.filter(user=self.request.user.id).order_by("id")
        low_inventory = InventoryItem.objects.filter(
            user=self.request.user.id, quantity__lte=LOW_QUANTITY
        )

        low_inventory_ids = low_inventory.values_list("id", flat=True)
        if low_inventory.count() >= 1:
            messages.error(
                request=request,
                message=(f"Items {list(low_inventory_ids)} with low inventory"),
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
