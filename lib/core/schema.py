from enum import Enum
from typing import Dict, List, Optional


class FieldType(Enum):
    BOOLEAN = "boolean"
    INTEGER = "integer"
    DOUBLE = "double"
    STRING = "text"
    CATEGORY = "category"
    DATE = "date"
    DATETIME = "datetime"

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


class Mappings:
    def __init__(self, raw_mapping: Dict):
        self.raw_mapping = raw_mapping
        fields_dict: Dict = self.raw_mapping.get("fields", {})
        self.fields: List[Field] = [Field(key, fields_dict[key]) for key in fields_dict.keys()]
        self.ensure_mappings_are_valid()

    def get_field_by_name(self, field_name: str) -> Field:
        for field in self.fields:
            if field.name == field_name:
                return field
        error_message = f"Mapping does not contain field {field_name} in 'fields' key"
        raise ValueError(error_message)

    def get_fields_names(self) -> List[str]:
        return [field.name for field in self.fields]

    def get_categorical_fields(self) -> List[Field]:
        return [f for f in self.fields if f.type == FieldType.CATEGORY]

    def ensure_mappings_are_valid(self):
        if not self.fields:
            raise ValueError(f"Mapping does not contain any field in 'fields' key")
