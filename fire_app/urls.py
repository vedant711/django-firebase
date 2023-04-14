from django.urls import path

from . import views

urlpatterns = [
    path('',views.index),
    path('create',views.post),
    # path('admin',views.admin),
    path('logout',views.logout),
    # path('admin',views.admin),
    path('indi/<id>',views.indi),
    path('credit/<id>',views.credit),
    path('debit/<id>',views.debit),
    # path('transactions')


]