from django.test import TestCase
from .models import *
from .serializers import *


class TestAircraftsModel(TestCase):

    def setUp(self):
        self.aircrafts_attributes = {'aircraft_code': '311',
                                     'model': 'Airbus 311',
                                     'range': 5000
                                     }
        self.aircrafts = Aircrafts.objects.create(**self.aircrafts_attributes)
        self.serializer = AircraftsSerializer(instance=self.aircrafts)

    def test__str__(self):
        aircraft_actual = str(Aircrafts.objects.get(aircraft_code = '311'))
        aircraft_to_expect = "Code: 311 Model: Airbus 311 Range: 5000"
        self.assertEqual(aircraft_actual, aircraft_to_expect)

    def test_create(self):
        aircraft_actual = Aircrafts.objects.create(aircraft_code = '777', model = 'Boeing 777', range= 7900)
        self.assertEqual(aircraft_actual.model, 'Boeing 777')

    def test_update(self):
        aircraft = Aircrafts.objects.get(aircraft_code = '311')
        aircraft.aircraft_code = '310'
        aircraft.model = 'NewModel'
        aircraft.range= 3000
        self.assertIsInstance(aircraft, Aircrafts)
        self.assertEqual(aircraft.aircraft_code, '310')
        self.assertEqual(aircraft.model, 'NewModel')
        self.assertEqual(aircraft.range, 3000)

    def test_delete(self):
        aircraft = Aircrafts.objects.filter(aircraft_code='311')
        aircraft.delete()
        self.assertQuerysetEqual([], aircraft)

    def test_data_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), {'aircraft_code', 'model', 'range'})

    def test_model_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['model'], self.aircrafts_attributes['model'])


class AirportsTest(TestCase):

    def setUp(self):
        self.airports_attributes = {
            'airport_code': 'MJZ',
            'airport_name': 'Boryspil',
            'city': 'Kyiv',
            'longitude': 86.8772,
            'latitude': 53.8114,
            'timezone': 'Europe/Kyiv'
        }

        self.airports = Airports.objects.create(**self.airports_attributes)
        self.serializer = AirportsSerializer(instance=self.airports)

    def test_create(self):
        airport_actual = Airports.objects.create(airport_code='MKZ', airport_name= 'Boryspil', city='Kyiv',
                                                 longitude=86.8772, latitude=53.8114, timezone='Europe/Kyiv')
        self.assertEqual(airport_actual.city, 'Kyiv')

    def test_update(self):
        airport = Airports.objects.get(city='Kyiv')
        airport.airport_code = 'AAA'
        self.assertIsInstance(airport, Airports)
        self.assertEqual(airport.airport_code, 'AAA')
        self.assertEqual(airport.airport_name, 'Boryspil')

    def test_delete(self):
        airport = Airports.objects.filter(city='Kyiv')
        airport.delete()
        self.assertQuerysetEqual([], airport)

    def test_data_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), {'airport_code', 'airport_name', 'city', 'longitude', 'latitude', 'timezone'})

    def test_model_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['city'], self.airports_attributes['city'])


class BoardingPassesTest(TestCase):

    def setUp(self):
        booking = Bookings.objects.create(book_ref = "00000F", book_date= '2016-09-01T23:12:00Z',
                                                total_amount= '265700.00')
        ticket = Tickets.objects.create(ticket_no ="0005432054309",
                                             book_ref=booking, passenger_id="7006 290035",
                                             passenger_name="NIKOLAY SERGEEV", contact_data="{phone: +70140120338}")
        airport = Airports.objects.create(airport_code='MKZ', airport_name= 'Boryspil', city='Kyiv',
                                                 longitude=86.8772, latitude=53.8114, timezone='Europe/Kyiv')
        aircraft = Aircrafts.objects.create(aircraft_code='777', model='Boeing 777', range=7900)
        flight = Flights.objects.create(flight_id=1, flight_no='PG0405', scheduled_departure="2016-09-13T05:35:00Z",
                                             scheduled_arrival='2016-09-13T06:30:00Z',departure_airport=airport,
                                             arrival_airport=airport, status='Arrived',
                                             aircraft_code=aircraft)
        ticket_flight = TicketFlights.objects.create(ticket_no=ticket, flight=flight,
                                                          fare_conditions='Business', amount=42100.00)
        self.boarding = BoardingPasses.objects.create(ticket_no=ticket_flight, flight_id=28935,
                                                      boarding_no=10, seat_no='7A')


    def test_one_to_one_field(self):
        boarding_actual = BoardingPasses.objects.get(ticket_no='0005432054309')
        expect = TicketFlights.objects.get(amount=42100.00)
        self.assertEqual(boarding_actual.ticket_no, expect)

    def test_update(self):
        boarding = BoardingPasses.objects.get(seat_no='7A')
        boarding.flight_id = 5
        self.assertIsInstance(boarding, BoardingPasses)
        self.assertEqual(boarding.flight_id, 5)
        self.assertEqual(boarding.seat_no, '7A')

    def test_delete(self):
        boarding = BoardingPasses.objects.filter(seat_no='7A')
        boarding.delete()
        self.assertQuerysetEqual([], boarding)


class BookingsTest(TestCase):

    def setUp(self):
        self.booking = Bookings.objects.create(book_ref="00000F", book_date='2016-09-01T23:12:00Z',
                                                total_amount='265700.00')

    def test_create(self):
        booking = Bookings.objects.create(book_ref="12345A", book_date='2017-07-01T23:12:00Z',
                                          total_amount='233500.00')
        self.assertEqual(booking.book_ref, "12345A")

    def test_update(self):
        booking = Bookings.objects.get(book_ref="00000F")
        booking.total_amount = '2000.00'
        self.assertIsInstance(booking, Bookings)
        self.assertEqual(booking.total_amount, '2000.00')
        self.assertEqual(booking.book_ref, '00000F')

    def test_delete(self):
        booking = Bookings.objects.filter(book_ref='00000F')
        booking.delete()
        self.assertQuerysetEqual([], booking)


class FlightsTest(TestCase):

    def setUp(self):
        airport = Airports.objects.create(airport_code='MKZ', airport_name='Boryspil', city='Kyiv',
                                               longitude=86.8772, latitude=53.8114, timezone='Europe/Kyiv')
        aircraft = Aircrafts.objects.create(aircraft_code='777', model='Boeing 777', range=7900)
        self.flight = Flights.objects.create(flight_id=1, flight_no='PG0405',
                                             scheduled_departure="2016-09-13T05:35:00Z",
                                             scheduled_arrival='2016-09-13T06:30:00Z', departure_airport=airport,
                                             arrival_airport=airport, status='Arrived',
                                             aircraft_code=aircraft)

    def test_foreign_keys(self):
        flight_actual = Flights.objects.get(flight_id=1)
        airport_expect = Airports.objects.get(airport_code='MKZ')
        aircraft_expect = Aircrafts.objects.get(model='Boeing 777')
        self.assertEqual(flight_actual.aircraft_code, aircraft_expect)
        self.assertEqual(flight_actual.arrival_airport, airport_expect)

    def test_update(self):
        flight = Flights.objects.get(flight_id=1)
        flight.flight_no = 'P5'
        self.assertIsInstance(flight, Flights)
        self.assertEqual(flight.flight_no, 'P5')
        self.assertEqual(flight.status, 'Arrived')

    def test_delete(self):
        flight = Flights.objects.filter(flight_id=1)
        flight.delete()
        self.assertQuerysetEqual([], flight)


class SeatsTest(TestCase):

    def setUp(self):
        aircraft = Aircrafts.objects.create(aircraft_code='777', model='Boeing 777', range=7900)
        self.seat = Seats.objects.create(aircraft_code=aircraft, seat_no='10A', fare_conditions="Business")

    def test_ono_to_one_field(self):
        seat = Seats.objects.get(seat_no='10A')
        expect = Aircrafts.objects.get(model='Boeing 777')
        self.assertEqual(seat.aircraft_code, expect)

    def test_update(self):
        seat = Seats.objects.get(seat_no='10A')
        seat.fare_conditions = 'Economy'
        self.assertIsInstance(seat, Seats)
        self.assertEqual(seat.fare_conditions, 'Economy')
        self.assertEqual(seat.seat_no, '10A')

    def test_delete(self):
        seat = Seats.objects.filter(seat_no='10A')
        seat.delete()
        self.assertQuerysetEqual([], seat)


class TicketFlightsTest(TestCase):

    def setUp(self):
        airport = Airports.objects.create(airport_code='MKZ', airport_name='Boryspil', city='Kyiv',
                                          longitude=86.8772, latitude=53.8114, timezone='Europe/Kyiv')
        aircraft = Aircrafts.objects.create(aircraft_code='777', model='Boeing 777', range=7900)
        flight = Flights.objects.create(flight_id=1, flight_no='PG0405',
                                        scheduled_departure="2016-09-13T05:35:00Z",
                                        scheduled_arrival='2016-09-13T06:30:00Z', departure_airport=airport,
                                        arrival_airport=airport, status='Arrived',
                                        aircraft_code=aircraft)
        booking = Bookings.objects.create(book_ref="00000F", book_date='2016-09-01T23:12:00Z',
                                          total_amount='265700.00')
        ticket = Tickets.objects.create(ticket_no="0005432054309",
                                        book_ref=booking, passenger_id="7006 290035",
                                        passenger_name="NIKOLAY SERGEEV", contact_data="{phone: +70140120338}")
        self.ticket_flight = TicketFlights.objects.create(ticket_no=ticket, flight=flight,
                                                     fare_conditions='Business', amount=42100.00)

    def test_one_to_one_foreign(self):
        ticket_flight = TicketFlights.objects.get(flight=1)
        ticket_expect = Tickets.objects.get(ticket_no="0005432054309")
        flight_expect = Flights.objects.get(flight_no="PG0405")
        self.assertEqual(ticket_flight.ticket_no, ticket_expect)
        self.assertEqual(ticket_flight.flight, flight_expect)

    def test_update(self):
        ticket_flight = TicketFlights.objects.get(flight=1)
        ticket_flight.amount = 55.55
        self.assertIsInstance(ticket_flight, TicketFlights)

    def test_delete(self):
        ticket_flight = TicketFlights.objects.filter(flight=1)
        ticket_flight.delete()
        self.assertQuerysetEqual([], ticket_flight)


class TicketsTest(TestCase):

    def setUp(self):
        booking = Bookings.objects.create(book_ref="00000F", book_date='2016-09-01T23:12:00Z',
                                          total_amount='265700.00')
        self.ticket = Tickets.objects.create(ticket_no="0005432054309",
                                        book_ref=booking, passenger_id="7006 290035",
                                        passenger_name="NIKOLAY SERGEEV", contact_data="{phone: +70140120338}")

    def test_one_to_one(self):
        ticket = Tickets.objects.get(ticket_no="0005432054309")
        booking_expect = Bookings.objects.get(book_ref="00000F")
        self.assertEqual(ticket.book_ref, booking_expect)

    def test_update(self):
        ticket = Tickets.objects.get(ticket_no="0005432054309")
        ticket.passenger_name = "Maria Sergeeva"
        self.assertIsInstance(ticket, Tickets)
        self.assertEqual(ticket.passenger_name, "Maria Sergeeva")
        self.assertEqual(ticket.passenger_id, "7006 290035")

    def test_delete(self):
        ticket = Tickets.objects.filter(ticket_no="0005432054309")
        ticket.delete()
        self.assertQuerysetEqual([], ticket)
