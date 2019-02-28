from django.urls import path
from .views import Login, Logout, Signup, home
from events import views
from api.views import  (
    EventList,
    EventDetail,
    EventCreate,
    EventUpdate,
    EventDelete,
)


urlpatterns = [
	path('', home, name='home'),
    path('signup/', Signup.as_view(), name='signup'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('<int:event_id>/detail/',views.event_detail, name='event-detail'),
    path('list/', views.event_list, name='event-list'),
    path('<int:event_id>/update/',views.update_event, name='event-update'),
    path('<int:event_id>/delete/',views.delete_event, name='delete-event'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add/', views.add_event, name='add-event'),
    path('ticket/<int:event_id>/', views.add_ticket, name='add-ticket'),
    path('book/', views.book, name='book'),

    path('api/list/', EventList.as_view(), name='api-list'),
    path('api/<int:event_id>/detail/', EventDetail.as_view(), name='api-detail'),
    path('api/add/', EventCreate.as_view(), name='api-create'),
    path('api/<int:event_id>/update/', EventUpdate.as_view(), name='api-update'),
    path('api/<int:event_id>/delete/', EventDelete.as_view(), name='api-delete'),

    
]

