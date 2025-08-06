# utils/type_mapper.py

from utils.type_annotation_helper import TypeAnnotationHelper

type_helper = TypeAnnotationHelper()

def map_ts_type_to_java(ts_type: str, wrap_optional: bool = False) -> str:
    ts_type = ts_type.strip()
    nullable = type_helper.is_nullable(ts_type)

    # Base mapping
    mapping = {
        "string": "String",
        "number": "int",
        "boolean": "boolean",
        "any": "Object",
        "unknown": "Object",
        "void": "void",
        "null": "Object",
        "undefined": "Object",
    }

    java_type = mapping.get(ts_type.replace("?", "").strip(), ts_type)

    if nullable and wrap_optional:
        return type_helper.to_optional(java_type)
    return java_type
