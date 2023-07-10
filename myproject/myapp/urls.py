from django.urls import path
from .views import RegisterView,PunchinView,PunchoutView

urlpatterns = [
    path('register/',RegisterView.as_view()),
    path('punchin/',PunchinView.as_view()),
    path('punchout/',PunchoutView.as_view())
]
