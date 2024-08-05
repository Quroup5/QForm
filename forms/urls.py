from django.urls import path

from forms.views import CreateFormView, UpdateFormView

urlpatterns = [
    path('create/form/', CreateFormView.as_view(), name='create_form'),
    path('update/form/', UpdateFormView.as_view(), name='update_form')
]
