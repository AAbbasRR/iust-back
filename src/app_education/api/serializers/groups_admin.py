from rest_framework import serializers
from app_education.models import FieldOfStudyModel, FacultyModel, FacultyGroupsModel


class FacultyGroupsSerializer(serializers.ModelSerializer):
    faculty = serializers.PrimaryKeyRelatedField(queryset=FacultyModel.objects.all())
    fields = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=FieldOfStudyModel.objects.all()
    )

    class Meta:
        model = FacultyGroupsModel
        fields = ['id', 'name', 'faculty', 'fields']

    def create(self, validated_data):
        fields_data = validated_data.pop('fields')
        faculty_group = FacultyGroupsModel.objects.create(**validated_data)
        faculty_group.fields.set(fields_data)
        return faculty_group

    def update(self, instance, validated_data):
        fields_data = validated_data.pop('fields', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if fields_data is not None:
            instance.fields.set(fields_data)

        return instance
