# -*- coding: utf-8 -*-

from rest_framework import serializers

from ..models import ProgramType, ProgramArgumentField, ProgramArgument
from ..models.types_ import TYPES_FOR_DJANGO_FIELDS, DJANGO_FIELDS_FOR_TYPES

class ProgramTypeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramType


class ProgramArgumentFieldSerializer(serializers.ModelSerializer):
    schema = serializers.SerializerMethodField()

    class Meta:
        model = ProgramArgumentField
        exclude = ('program_argument', 'id')

    def get_schema(self, obj):
        schema = {}
        argument = obj.program_argument
        model = argument.content_type.model_class()
        field_name = obj.name
        field = model._meta.get_field(field_name)
        schema['data_type'] = TYPES_FOR_DJANGO_FIELDS[field.__class__]
        print dir(field)

        if field.__class__ in DJANGO_FIELDS_FOR_TYPES['model']:
            model = '{}.{}'.format(field.related_model._meta.app_label,
            field.related_model.__class__.__name__)

            schema['model'] = model
        return schema

class ProgramArgumentSerializer(serializers.ModelSerializer):
    field = ProgramArgumentFieldSerializer(many=True)

    class Meta:
        model = ProgramArgument


class ProgramTypeSerializer(serializers.ModelSerializer):
    argument = ProgramArgumentSerializer(many=True)

    class Meta:
        model = ProgramType
