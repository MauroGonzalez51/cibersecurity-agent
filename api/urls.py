from django.urls import path

from .views import agent

urlpatterns = [path("agent/", agent, name="agent")]
