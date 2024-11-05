from django.urls import path
from . import views
from .views import AplicationDetailView, AplicationPhotoUploadView, AplicationPhotoDeleteView, AplicationList

app_name = 'vehicles'
urlpatterns = [
    path('', views.AplicationList.as_view(), name='all'),
    path('load_more/', views.LoadMoreAplicationsView.as_view(), name='load_more_aplications'),
    
    path('aplication/<int:pk>/', AplicationDetailView.as_view(), name='aplication_detail'),
    path('aplication/<int:pk>/upload/', AplicationPhotoUploadView.as_view(), name='upload_photo'),
    path('photo/delete/<int:pk>/', AplicationPhotoDeleteView.as_view(), name='delete_photo'),

    # Application CRUD
    path("main/create/", views.AplicationCreate.as_view(), name="aplication_create"),
    path("main/<int:pk>/update/", views.AplicationUpdate.as_view(), name="aplication_update"),
    path("main/<int:pk>/delete/", views.AplicationDelete.as_view(), name="aplication_delete"),

    # Make CRUD
    path("make/", views.MakeView.as_view(), name="make_list"),
    path("make/create/", views.MakeCreate.as_view(), name="make_create"),
    path("make/<int:pk>/update/", views.MakeUpdate.as_view(), name="make_update"),
    path("make/<int:pk>/delete/", views.MakeDelete.as_view(), name="make_delete"),

    # Year CRUD
    path("year/", views.YearView.as_view(), name="year_list"),
    path("year/create/", views.YearCreate.as_view(), name="year_create"),
    path('year/<int:pk>/update/', views.YearUpdate.as_view(), name='year_update'),
    path("year/<int:pk>/delete/", views.YearDelete.as_view(), name="year_delete"),

    # Model CRUD
    path("model/", views.ModelView.as_view(), name="model_list"),
    path("model/create/", views.ModelCreate.as_view(), name="model_create"),
    path("model/<int:pk>/update/", views.ModelUpdate.as_view(), name="model_update"),
    path("model/<int:pk>/delete/", views.ModelDelete.as_view(), name="model_delete"),

    # Segment CRUD
    path("segment/", views.SegmentView.as_view(), name="segment_list"),
    path("segment/create/", views.SegmentCreate.as_view(), name="segment_create"),
    path("segment/<int:pk>/update/", views.SegmentUpdate.as_view(), name="segment_update"),
    path("segment/<int:pk>/delete/", views.SegmentDelete.as_view(), name="segment_delete"),

    # Category CRUD
    path('category/', views.CategoryView.as_view(), name='category_list'),
    path('category/create/', views.CategoryCreate.as_view(), name='category_create'),
    path('category/<int:pk>/update/', views.CategoryUpdate.as_view(), name='category_update'),
    path('category/<int:pk>/delete/', views.CategoryDelete.as_view(), name='category_delete'),

    # Part CRUD
    path("part/", views.PartListView.as_view(), name="part_list"),
    path("part/create/", views.PartCreate.as_view(), name="part_create"),
    path("part/<int:pk>/update/", views.PartUpdate.as_view(), name="part_update"),
    path("part/<int:pk>/delete/", views.PartDelete.as_view(), name="part_delete"),
    path('aplication/<int:pk>/', views.PartDelete.as_view(), name="part_detail"), #queda pendiente agregar la pagina de part_detail

    #-------------------------------------------URLS para modelo "Property" obsoleto-----------------------------------------------
    # # Property CRUD
    # path("property/", views.PropertyView.as_view(), name="property_list"),
    # path("property/create/", views.PropertyCreate.as_view(), name="property_create"),
    # path("property/<int:pk>/update/", views.PropertyUpdate.as_view(), name="property_update"),
    # path("property/<int:pk>/delete/", views.PropertyDelete.as_view(), name="property_delete"),
    #------------------------------------------------------------------------------------------------------------------------------

]
