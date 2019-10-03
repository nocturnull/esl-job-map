from django.contrib import admin

from account.models import SiteUser
from .models import Order, Plan, Product, Subscription
from .forms.order import CreateOrderForm
from .forms.plan import CreatePlanForm
from .forms.product import CreateProductForm


class OrderAdmin(admin.ModelAdmin):
    form = CreateOrderForm
    list_display = ['site_user', 'plan', 'code', 'was_consumed']
    
    def render_change_form(self, request, context, *args, **kwargs):
        context['adminform'].form.fields['site_user'].queryset = SiteUser.objects\
            .filter(role=SiteUser.ROLE_RECRUITER)\
            .order_by('email')

        return super(OrderAdmin, self).render_change_form(request, context, *args, **kwargs)


class PlanAdmin(admin.ModelAdmin):
    form = CreatePlanForm
    list_display = ['billing_amount', 'billing_interval', 'currency', 'stripe_plan_id']


class ProductAdmin(admin.ModelAdmin):
    form = CreateProductForm
    list_display = ['internal_name', 'max_jobs', 'stripe_product_id']


class SubscriptionAdmin(admin.ModelAdmin):
    fields = ('is_active',)
    list_display = ['site_user', 'order', 'is_active', 'code_consumed']


admin.site.register(Order, OrderAdmin)
admin.site.register(Plan, PlanAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Subscription, SubscriptionAdmin)

