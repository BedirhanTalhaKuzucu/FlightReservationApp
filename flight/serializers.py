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
    passenger_id = serializers.IntegerField(source="id", required=False)
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

        #update yapılırken yolcu silmek için
        mevcutIdlist=[Id.id for Id in mevcut ]
        updatedIdlist= [item["id"] for item in passenger_data if "id" in item.keys()]
        for Id in mevcutIdlist:
            if Id in updatedIdlist:
                pass
            else:
                print("yok", Id)
                mevcut = mevcut.exclude(id=Id)
        instance.passenger.set(mevcut)
        # print(instance.passenger.all())
      
        #update yaperken var olan yolcuları güncellemek, olmayanları creat etmek için
        for  passenger in passenger_data:
            #gelen bilgilerde yolcu id si var mı? var ise bu id mevcut rezervasyonda mı yoksa var olan diğer yolcular arasında mı
            if "id" in passenger.keys():
                pas = mevcut.filter(id=passenger["id"])
                if pas:
                    pas = pas.update(**passenger)
                else:
                    pas = Passenger.objects.get(id=passenger["id"])
                    instance.passenger.add(pas)
            else: 
                    pas = Passenger.objects.create(**passenger)
                    print(pas)
                    instance.passenger.add(pas)

    
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




    