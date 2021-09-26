from django.db import models


class Aircrafts(models.Model):
    aircraft_code = models.CharField(primary_key=True, max_length=3)
    model = models.TextField()
    range = models.IntegerField()

    class Meta:
        db_table = 'aircrafts'

    def __str__(self):
        return f"Code: {self.aircraft_code} Model: {self.model} Range: {self.range}"

class Airports(models.Model):
    airport_code = models.CharField(primary_key=True, max_length=3)
    airport_name = models.TextField()
    city = models.TextField()
    longitude = models.FloatField()
    latitude = models.FloatField()
    timezone = models.TextField()

    class Meta:
        db_table = 'airports'


class BoardingPasses(models.Model):
    ticket_no = models.OneToOneField('TicketFlights', on_delete=models.CASCADE, db_column='ticket_no', primary_key=True)
    flight_id = models.IntegerField()
    boarding_no = models.IntegerField()
    seat_no = models.CharField(max_length=4)

    class Meta:
        db_table = 'boarding_passes'
        unique_together = (('flight_id', 'boarding_no'), ('flight_id', 'seat_no'), ('ticket_no', 'flight_id'),)


class Bookings(models.Model):
    book_ref = models.CharField(primary_key=True, max_length=6)
    book_date = models.DateTimeField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'bookings'


class Flights(models.Model):
    flight_id = models.AutoField(primary_key=True)
    flight_no = models.CharField(max_length=6)
    scheduled_departure = models.DateTimeField()
    scheduled_arrival = models.DateTimeField()
    departure_airport = models.ForeignKey(Airports, on_delete=models.CASCADE, db_column='departure_airport', related_name='departure_airport')
    arrival_airport = models.ForeignKey(Airports, on_delete=models.CASCADE, db_column='arrival_airport', related_name='arrival_airport')
    status = models.CharField(max_length=20)
    aircraft_code = models.ForeignKey(Aircrafts, on_delete=models.CASCADE, db_column='aircraft_code')
    actual_departure = models.DateTimeField(blank=True, null=True)
    actual_arrival = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'flights'
        unique_together = (('flight_no', 'scheduled_departure'),)


class Seats(models.Model):
    aircraft_code = models.OneToOneField(Aircrafts, on_delete=models.CASCADE, db_column='aircraft_code', primary_key=True)
    seat_no = models.CharField(max_length=4)
    fare_conditions = models.CharField(max_length=10)

    class Meta:
        db_table = 'seats'
        unique_together = (('aircraft_code', 'seat_no'),)


class TicketFlights(models.Model):
    ticket_no = models.OneToOneField('Tickets', on_delete=models.CASCADE, db_column='ticket_no', primary_key=True)
    flight = models.ForeignKey(Flights, on_delete=models.CASCADE)
    fare_conditions = models.CharField(max_length=10)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'ticket_flights'
        unique_together = (('ticket_no', 'flight'),)


class Tickets(models.Model):
    ticket_no = models.CharField(primary_key=True, max_length=13)
    book_ref = models.ForeignKey(Bookings, on_delete=models.CASCADE, db_column='book_ref')
    passenger_id = models.CharField(max_length=20)
    passenger_name = models.TextField()
    contact_data = models.JSONField(blank=True, null=True)

    class Meta:
        db_table = 'tickets'