from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework import viewsets
from .serializers import *


class BaseModel(viewsets.ModelViewSet):
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_fields = '__all__'


class AircraftsView(BaseModel):
    queryset = Aircrafts.objects.all()
    serializer_class = AircraftsSerializer


class AirportsView(BaseModel):
    queryset = Airports.objects.all()
    serializer_class = AirportsSerializer


class BoardingPassesView(BaseModel):
    queryset = BoardingPasses.objects.all()
    serializer_class = BoardingPassesSerializer


class BookingsView(BaseModel):
    queryset = Bookings.objects.all()
    serializer_class = BookingsSerializer


class FlightsView(BaseModel):
    queryset = Flights.objects.all()
    serializer_class = FlightsSerializer


class SeatsView(BaseModel):
    queryset = Seats.objects.all()
    serializer_class = SeatsSerializer


class TicketFlightsView(BaseModel):
    queryset = TicketFlights.objects.all()
    serializer_class = TicketFlightsSerializer

class TicketsView(BaseModel):
    queryset = Tickets.objects.all()
    serializer_class = TicketsSerializer