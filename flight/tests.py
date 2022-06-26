from django.test import TestCase

# Create your tests here.


# class PassengerSerializer(serializers.ModelSerializer):
#     passenger_id = serializers.IntegerField(write_only=True, required=False)
#     class Meta:
#         model= Passenger
#         fields=(
#             "first_name",
#             "last_name",
#             "email",
#             "phone_number",
#             "passenger_id",
#         )


#  class ReservationSerializer(serializers.ModelSerializer):
    
#    ...
#    ...

#     def update(self, instance, validated_data):
        
#         passenger_data = validated_data.pop('passenger')
#         mevcut = instance.passenger.all()

#         for index, passenger in enumerate(passenger_data):
        
#             try: 
#                 pas = Passenger.objects.filter(id = passenger.passenger_id)
#                 pas = pas.update(**passenger)
#             except: 
#                 pas = Passenger.objects.create(**passenger)
#                 instance.passenger.add(pas)

    

#         instance.flight_id = validated_data["flight_id"]
#         instance.save()

#         return instance