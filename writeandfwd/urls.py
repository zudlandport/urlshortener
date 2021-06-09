
from django.urls import path
from . import views

urlpatterns = [
	path('', views.HomePageView.as_view()),
	path('addfwd', views.addfwd.as_view()),
	path('addfwdcustom', views.addfwdcustom.as_view()),

	path('see/<str:fwdurlstring>', views.seeafwd.as_view()),

	path('testfus', views.testfus.as_view()),

	path('listfwds', views.listfwds.as_view()),
]
