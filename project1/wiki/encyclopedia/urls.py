from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:name>", views.wiki_page, name="greet"),
    path("add",views.add,name="add"),
    path("random",views.random_page,name="random"),
    # path("",views.search,name="search"),
    # path('search/', view.SearchResultsView.as_view(), name='search_results'),
]
