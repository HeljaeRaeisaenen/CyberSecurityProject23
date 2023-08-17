from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<pk>/results/', views.results, name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('create/', views.create, name='create' ),
    path('login/', views.login, name='login'),
    path('login_action/', views.loginAction, name='login_action'),
    path('signup/', views.signup, name='signup'),
    path('signup_action/', views.signupAction, name='signup_action'),
    path('logout/', views.logout, name='logout'),
    path('users/<int:pk>/', views.userPage, name='userpage'),
    path('delete_poll/', views.deletePoll, name='delete_poll')

]