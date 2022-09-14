from django.contrib import admin
from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('',views.home, name="home-page"),
    
    path('',views.home, name="home-page"),
    path('login',views.login_page,name='login-page'),
    path('Signupview',views.admin_signup,name='adminsign-page'),
    # path('adminsignup',views.admin_signup,name='admin-page'),
    path('studentclick',views.studentclick_view,name='student-page'),
    path('register',views.userregister,name='register-page'),
    path('save_register',views.save_register,name='register-user'),
    path('user_login',views.login_user,name='login-user'),
    path('home',views.home,name='home-page'),
    path('logout',views.logout_user,name='logout'),
    path('profile',views.profile,name='profile-page'),
    path('update_password',views.update_password,name='update-password'),
    path('update_profile',views.update_profile,name='update-profile'),
    path('users',views.users,name='user-page'),
    path('books',views.books,name='book-page'),
    path('studentbookview',views.studentbooks,name='book-page1'),
    path('manage_book',views.manage_book,name='manage-book'),
    path('manage_book/<int:pk>',views.manage_book,name='manage-book-pk'),
    path('view_book/<int:pk>',views.view_book,name='view-book-pk'),
    path('save_book',views.save_book,name='save-book'),
    path('delete_book/<int:pk>',views.delete_book,name='delete-book'),
    
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
