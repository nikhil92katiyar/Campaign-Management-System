from django.urls import path

from . import views

urlpatterns = [
    path("campaigns/", views.CampaignListCreateView.as_view()),
    path(
        "campaigns/<uuid:pk>/",
        views.CampaignRetrieveUpdateDestroyView.as_view(),
    ),
    path("campaign-rules/", views.CampaignRulesListCreateView.as_view()),
    path(
        "campaign-rules/<int:pk>/",
        views.CampaignRulesRetrieveUpdateDestroyView.as_view(),
    ),
    path("payment-rules/", views.PaymentMethodRuleListCreateView.as_view()),
    path(
        "payment-rules/<int:pk>/", views.PaymentMethodRuleDetailView.as_view()
    ),
    path("location-rules/", views.LocationTierRuleListCreateView.as_view()),
    path(
        "location-rules/<int:pk>/", views.LocationTierRuleDetailView.as_view()
    ),
    path("priority-rules/", views.UserPriorityRuleListCreateView.as_view()),
    path(
        "priority-rules/<int:pk>/", views.UserPriorityRuleDetailView.as_view()
    ),
    path("min-cart-rules/", views.MinCartValueRuleListCreateView.as_view()),
    path(
        "min-cart-rules/<int:pk>/", views.MinCartValueRuleDetailView.as_view()
    ),
    path("groups/", views.CustomerGroupList.as_view(), name="group-list"),
    path(
        "groups/<uuid:id>/",
        views.CustomerGroupDetail.as_view(),
        name="group-detail",
    ),
    path(
        "eligible-campaigns/",
        views.EligibleCampaignsView.as_view(),
        name="eligible-campaigns",
    ),
    path(
        "apply-discount/",
        views.ApplyDiscountView.as_view(),
        name="apply-discount",
    ),
]
