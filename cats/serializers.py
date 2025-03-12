from rest_framework import serializers

from .models import Achievement, AchievementCat, Cat, Owner


class AchievementSerializer(serializers.ModelSerializer):

    class Meta:
        model = Achievement
        fileds = ('id', 'name')


class CatSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)
    achievements = AchievementSerializer(many=True, required=False)

    class Meta:
        model = Cat
        fields = ('id', 'name', 'color', 'birth_year', 'owner', 'achievements')

    def create(self, validate_data):
        if 'achivements' not in validate_data:
            cat = Cat.objects.create(**validate_data)
            return cat

        achivements = validate_data.pop('achivements')
        cat = Cat.objects.create(**validate_data)
        for achivement in achivements:
            current_achivement, status = Achievement.objects.get_or_create(
                **achivement
            )
            AchievementCat.objects.create(
                achivement=current_achivement, cat=cat
            )
        return cat


class OwnerSerializer(serializers.ModelSerializer):
    cats = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Owner
        fields = ('first_name', 'last_name', 'cats')
