from rest_framework import serializers
from .models import Flight, Passenger, Reservation


class FlightSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Flight
        fields = (
            "id",
            "flight_number",
            "operation_airlines",
            "departure_city",
            "arrival_city",
            "date_of_departure",
            "etd"
        )
        

class PassengerSerializer(serializers.ModelSerializer):
    # passenger_id = serializers.IntegerField(write_only=True, required=False)
    class Meta:
        model= Passenger
        fields=(
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "passenger_id",
        )

class ReservationSerializer(serializers.ModelSerializer):
    
    passenger = PassengerSerializer(many=True, required=False)
    flight = serializers.StringRelatedField()  # default read_only=True
    user = serializers.StringRelatedField()  # default read_only=True
    flight_id = serializers.IntegerField(write_only=True)
    user_id = serializers.IntegerField(write_only=True, required=False)
    class Meta:
        model = Reservation
        fields =(
            "id",
            "flight",
            "flight_id",
            "user",
            "user_id",
            "passenger"
        )
        
    def create(self, validated_data):
        passenger_data = validated_data.pop('passenger')

        validated_data['user_id'] = self.context['request'].user.id
        reservation = Reservation.objects.create(**validated_data)
        for passenger in passenger_data:
            pas = Passenger.objects.create(**passenger)
            reservation.passenger.add(pas)
        reservation.save()
        return reservation


    def update(self, instance, validated_data):
        
        passenger_data = validated_data.pop('passenger')
        mevcut = instance.passenger.all()

        for index, passenger in enumerate(passenger_data):
        
            if index < len(mevcut):
                pas = Passenger.objects.filter(id = mevcut[index].id)
                pas = pas.update(**passenger)
            else:
                pas = Passenger.objects.create(**passenger)
                instance.passenger.add(pas)

            # try: 
            #     pas = Passenger.objects.filter(id = passenger.passenger_id)
            #     pas = pas.update(**passenger)
            # except: 
            #     pas = Passenger.objects.create(**passenger)
            #     instance.passenger.add(pas)

    

        instance.flight_id = validated_data["flight_id"]
        instance.save()

        return instance




class StaffFlightSerializer(serializers.ModelSerializer):
    
    reservations = ReservationSerializer(many=True, read_only=True)
    
    class Meta:
        model = Flight
        fields = (
            "id",
            "flight_number",
            "operation_airlines",
            "departure_city",
            "arrival_city",
            "date_of_departure",
            "etd",
            "reservations",
        )




    