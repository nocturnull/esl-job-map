from django.contrib import admin

from .models import Plan, Product
from .forms.plan import CreatePlanForm
from .forms.product import CreateProductForm


class PlanAdmin(admin.ModelAdmin):
    form = CreatePlanForm
    list_display = ['amount', 'interval', 'currency', 'stripe_plan_id']


class ProductAdmin(admin.ModelAdmin):
    form = CreateProductForm
    list_display = ['name', 'stripe_product_id']


admin.site.register(Plan, PlanAdmin)
admin.site.register(Product, ProductAdmin)

