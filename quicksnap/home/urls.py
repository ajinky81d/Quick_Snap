
from django.urls import path
from . import views
from .views import DataList,CustomLoginView,CreateData,DeleteData
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
  
urlpatterns = [
   path('',views.index,name='home'),
   path('contact',views.contact,name='contact'),
   path('feature',views.feature,name='feature'),
   path('data',DataList.as_view(),name='data'),
   path('activate/<uidb64>/<token>', views.activate, name='activate'),
   path('signup', views.signup, name='signup'),
   path('login',CustomLoginView.as_view(),name='login'),
   path('logout',LogoutView.as_view(next_page='home'),name='logout'),
   path('add_data',CreateData.as_view(),name='add_data'),
   path('delete_data/<int:data_id>/', DeleteData.as_view(), name='delete_data'),
   path('get_image/<int:data_id>/', views.get_image, name='get_image'),
   path("<path:unknown_path>", views.error_page, name='error_page'),
   path('handle_dns_error/', views.handle_dns_error, name='handle_dns_error'),
    
    

] +  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

