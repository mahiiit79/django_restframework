from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)



router = DefaultRouter()
router.register('',views.TodoViewSetApiView)

urlpatterns=[
    path('',views.all_todos),
    path('<int:todo_id>',views.todo_detail_view),
    path('cbv/',views.TodosListApiView.as_view()),
    path('cbv/<int:todo_id>',views.TodosDetailApiView.as_view()),
    path('mixins/',views.TodosListMixinApiView.as_view()),
    path('mixins/<pk>',views.TodosDetailMixinApiView.as_view()),
    path('generics/', views.TodoGenericApiView.as_view()),
    path('generics/<pk>', views.TodosGenericDetailView.as_view()),
    path('viewsets/',include(router.urls)),
    path('users/',views.UsersGenericApiView.as_view()),

]
