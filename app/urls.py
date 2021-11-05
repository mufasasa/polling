from django.urls import path
from . import views


urlpatterns = [
    path('import_lgas', views.import_lgas, name='import_lgas'),
    path('import_wards', views.import_wards, name='import_wards'),
    path('import_polling_units', views.import_polling_units, name='import_polling_units'),
    path('import_parties', views.import_parties, name='import_parties'),
    path('import_polling_unit_results', views.import_polling_unit_results, name='import_polling_unit_results'),
    path('polling_units_list', views.polling_units_list, name='polling_units_list'),
    path('polling_unit/<int:uniqueid>', views.polling_unit_detail, name='polling_unit'),
    path('select_lga', views.select_lga, name='select_lga'),
    path('add_results', views.add_results, name='add_results'),
    path('', views.index, name='index'),
]