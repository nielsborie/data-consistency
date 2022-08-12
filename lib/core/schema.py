from enum import Enum
from typing import Dict, List, Optional


class FieldType(Enum):
    BOOLEAN = "boolean"
    INTEGER = "integer"
    DOUBLE = "double"
    STRING = "string"
    OBJECT = "object"
    CATEGORY = "category"
    DATE = "date"
    DATETIME = "datetime"

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))

    @staticmethod
    def get_inner_type(field_type: str) -> str:
        match field_type:
            case FieldType.BOOLEAN.value:
                target_type = "bool"
            case FieldType.INTEGER.value:
                target_type = "int"
            case FieldType.DOUBLE.value:
                target_type = "float"
            case FieldType.STRING.value:
                target_type = "str"
            case FieldType.OBJECT.value:
                target_type = "object"
            case FieldType.CATEGORY.value:
                target_type = "category"
            case FieldType.DATE.value | FieldType.DATETIME.value:
                target_type = "datetime64[ns]"
            case _:
                raise ValueError("Unknown field type!")
        return target_type


class Field:
    def __init__(self, name: str, properties: Dict):
        self.name: str = name
        self.type: FieldType = FieldType(properties.get("type"))
        self.description: Optional[str] = properties.get("description")


class DataSchema:
    def __init__(self, raw_schema: Dict):
        self.raw_schema = raw_schema
        fields_dict: Dict = self.raw_schema.get("fields", {})
        self.fields: List[Field] = [Field(key, fields_dict[key]) for key in fields_dict.keys()]
        self.ensure_data_schema_is_valid()

    def get_field_by_name(self, field_name: str) -> Field:
        for field in self.fields:
            if field.name == field_name:
                return field
        error_message = f"Data schema does not contain field {field_name} in 'fields' key"
        raise ValueError(error_message)

    def get_fields_names(self) -> List[str]:
        return [field.name for field in self.fields]

    def get_categorical_fields(self) -> List[Field]:
        return [f for f in self.fields if (f.type == FieldType.CATEGORY or f.type == FieldType.BOOLEAN)]

    def get_numerical_fields(self) -> List[Field]:
        return [f for f in self.fields if (f.type == FieldType.DOUBLE or f.type == FieldType.INTEGER)]

    def get_datetime_fields(self) -> List[Field]:
        return [f for f in self.fields if (f.type == FieldType.DATETIME or f.type == FieldType.DATE)]

    def get_text_fields(self) -> List[Field]:
        return [f for f in self.fields if f.type == FieldType.STRING]

    def ensure_data_schema_is_valid(self):
        if not self.fields:
            raise ValueError(f"Data schema does not contain any field in 'fields' key")
