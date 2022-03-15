from django.urls import include, path

urlpatterns = [
    path('v1/', include('djoser.urls')),
    path('v1/auth/', include('djoser.urls.authtoken')),
]
