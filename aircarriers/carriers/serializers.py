from rest_framework import serializers
from .models import *


class AircraftsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aircrafts
        fields = ('aircraft_code', 'model', 'range')


class AirportsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airports
        fields = ('airport_code', 'airport_name', 'city', 'longitude', 'latitude', 'timezone')


class BoardingPassesSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardingPasses
        fields = ('ticket_no', 'flight_id', 'boarding_no', 'seat_no')


class BookingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookings
        fields = ('book_ref', 'book_date', 'total_amount')


class FlightsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flights
        fields = ('flight_id', 'flight_no', 'scheduled_departure', 'scheduled_arrival', 'departure_airport',
                  'arrival_airport', 'status', 'aircraft_code', 'actual_departure', 'actual_arrival')


class SeatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seats
        fields = ('aircraft_code', 'seat_no', 'fare_conditions')


class TicketFlightsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketFlights
        fields = ('ticket_no', 'flight', 'fare_conditions', 'amount')


class TicketsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tickets
        fields = ('ticket_no', 'book_ref', 'passenger_id', 'passenger_name', 'contact_data')