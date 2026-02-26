from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    # path('', views.IndexView.as_view(), name='index'),
    path('', views.ObjectiveListView.as_view(), name='list_objective'),
    path('create/', views.CreateObjectiveView.as_view(), name='create_objective'),
    path('delete/<int:pk>/', views.DeleteObjectiveView.as_view(), name='delete_objective'),
    path('update/<int:pk>/', views.UpdateObjectiveView.as_view(), name='update_objective'),
    path('finished/<int:pk>/', views.FinishedObjectiveView, name='finished_objective'),
]