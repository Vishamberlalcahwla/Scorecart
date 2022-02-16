
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from rest_apis import views

urlpatterns = [
    path('admin/',          admin.site.urls),
    path(r'register',       views.register_api),
    path(r'login',          views.Login),
    path(r'Home',           views.Home),
    path('usertodolist',views.ListTodoAPIView.as_view(),name='todo'),
    path('detail/<str:pk>/',views.TodoDetailAPIView.as_view(),name='detail'),
    path('create',views.CreateTodoAPIView.as_view(),name='create'),
    path('complete',views. CompleteTodoTask.as_view(),name='complete'),
    path('update/<str:pk>/',views.UpdateTodoAPIView.as_view(),name='update'),
    path('delete/<str:pk>/',views.DeleteTodoAPIView.as_view(),name='delete'),
]
