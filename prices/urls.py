from django.urls import path
from prices import views


urlpatterns = [
    path('', views.IndexView.as_view(template_name='prices/index.html'), name='series'),
    path('<int:series_id>/', views.GetView.as_view(template_name='prices/get.html'), name='series_data'),
]