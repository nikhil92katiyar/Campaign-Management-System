from django.contrib import admin

from cms.models import (
    Campaign,
    CampaignRules,
    Customer,
    CustomerGroup,
    LocationTierRule,
    MinCartValueRule,
    PaymentMethodRule,
    UserPriorityRule,
)


class CampaignRulesInline(admin.StackedInline):
    model = CampaignRules
    extra = 1
    show_change_link = True


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    inlines = [CampaignRulesInline]
    list_display = ("name", "is_active", "start_date", "end_date")
    search_fields = ("name", "description")
    list_filter = ("is_active", "start_date")
    filter_horizontal = ("target_groups",)


@admin.register(CampaignRules)
class CampaignRulesAdmin(admin.ModelAdmin):
    list_display = (
        "campaign",
        "min_cart_rule",
        "payment_rules",
        "location_rules",
        "priority_rules",
    )
    raw_id_fields = ("campaign",)


@admin.register(PaymentMethodRule)
class PaymentMethodRuleAdmin(admin.ModelAdmin):
    list_display = ("name", "methods_list")

    def methods_list(self, obj):
        return ", ".join(obj.methods)


@admin.register(LocationTierRule)
class LocationTierRuleAdmin(admin.ModelAdmin):
    list_display = ("name", "tiers_list")

    def tiers_list(self, obj):
        return ", ".join(obj.tiers)


@admin.register(UserPriorityRule)
class UserPriorityRuleAdmin(admin.ModelAdmin):
    list_display = ("name", "priorities_list")

    def priorities_list(self, obj):
        return ", ".join(map(str, obj.priorities))


@admin.register(MinCartValueRule)
class MinCartValueRuleAdmin(admin.ModelAdmin):
    list_display = ("name", "min_value", "max_discount")
    list_editable = ("min_value", "max_discount")


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("email", "full_name", "is_active", "created_at")
    readonly_fields = ("id", "created_at", "last_updated")

    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"


@admin.register(CustomerGroup)
class CustomerGroupAdmin(admin.ModelAdmin):
    search_fields = ("name", "description")
    filter_horizontal = ("members",)
    list_display = ("name", "description", "customer_count")

    def customer_count(self, obj):
        return obj.members.count()
