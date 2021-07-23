from django.urls import path
from . import views


urlpatterns = [
    path('measurements', views.MeasurementView.as_view()),
    path('tags/<tagid>', views.userView.as_view()),
    path('clear/<tagid>', views.userclear_credits_View.as_view()),
    path('mpesa_stk_push', views.stk_push_api.as_view()),

]

