from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('aircrafts', views.AircraftsView)
router.register('airports', views.AirportsView)
router.register('boarding_passes', views.BoardingPassesView)
router.register('bookings', views.BookingsView)
router.register('flights', views.FlightsView)
router.register('seats', views.SeatsView)
router.register('ticket_flights', views.TicketFlightsView)
router.register('tickets', views.TicketsView)

urlpatterns = [
    path('', include(router.urls))
]