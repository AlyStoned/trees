from django.urls import path

from . import views

app_name = "materialized_paths"

urlpatterns = [
    path("", views.TreeView.as_view(), name="tree"),
    path("<int:node_id>/", views.BranchView.as_view(), name="branch"),
]
