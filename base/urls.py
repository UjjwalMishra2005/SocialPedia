from django.urls import path
from . import views
urlpatterns =[
    path('',views.home,name='home'),
    path('rooms/<str:pk>/',views.rooms,name='rooms'),
    path('product',views.product,name='product'),
    path('createroom',views.createroom,name='create-room'),
    path('updateroom/<str:pk>/',views.updateroom,name='update-room'),
    path('deleteroom/<str:pk>',views.deleteroom,name='deleteroom'),
    path('Userregister',views.Userregister,name='register'),
    path('login',views.Userlogin,name='login'),
    path('logout',views.Userlogout,name='logout'),
    path('delete_message/<str:pk1>/<str:pk2>',views.delete_message,name='delete_message'),
    path('edit_message/<str:pk1>/<str:pk2>/',views.edit_message,name='edit_message'),
    path('Profile/<str:pk>',views.userProfile,name='Profile'),
    path('topics',views.topics,name='topics'),
    path('recent-activity',views.activity,name="recent_activity"),
    path('edit-user<str:pk>',views.editUser,name='edit-user'),
    path('photos',views.get_photos,name='photos')

    
]
#test