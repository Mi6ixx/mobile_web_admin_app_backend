from rest_framework import serializers
from core.models import Lodge, LodgeAmenity


class LodgeAmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = LodgeAmenity
        fields = ['id', 'name']
        read_only_fields = ['id']

class LodgeSerializer(serializers.ModelSerializer):
    amenities = LodgeAmenitySerializer(many=True, required=False)

    class Meta:
        model = Lodge
        fields = [
            'id',
            'name',
            'location',
            'total_rooms',
            'rent_rate',
            'caretaker_number',
            'description',
            'amenities',
        ]
        read_only_fields = ['id']

    def _get_or_create_amenities(self, amenities, lodge):
        """Helper function for getting or creating tags as needed"""
        auth_user = self.context['request'].user
        for amenity in amenities:
            amenity_obj, created = LodgeAmenity.objects.get_or_create(
                user=auth_user,
                **amenity
            )
            lodge.amenities.add(amenity_obj)

    def create(self, validated_data):
        amenities = validated_data.pop('amenities', [])
        lodge = Lodge.objects.create(**validated_data)
        self._get_or_create_amenities(amenities, lodge)
        return lodge

    def update(self, instance, validated_data):
        """Update lodge"""
        amenities = validated_data.pop('amenities', [])
        if amenities is not None:
            instance.amenities.clear()
            self._get_or_create_amenities(amenities, instance)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class LodgeImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lodge
        fields = ['id', 'image']
        read_only_fields = ['id']

