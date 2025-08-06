# utils/type_annotation_helper.py

import re

class TypeAnnotationHelper:
    OPTIONAL_TYPES = {"null", "undefined"}

    def is_nullable(self, ts_type: str) -> bool:
        """
        Detect if a TypeScript type is nullable (contains null/undefined or ?)
        """
        ts_type = ts_type.strip()
        if "?" in ts_type:
            return True
        if "|" in ts_type:
            parts = [p.strip() for p in ts_type.split("|")]
            if any(p in self.OPTIONAL_TYPES for p in parts):
                return True
        return False

    def to_optional(self, java_type: str) -> str:
        """
        Wrap a Java type with Optional<> if not already
        """
        if java_type.startswith("Optional<"):
            return java_type
        return f"Optional<{java_type}>"

    def get_nullable_annotation(self) -> str:
        return "@Nullable"

    def get_optional_import(self) -> str:
        return "java.util.Optional"

    def get_nullable_import(self) -> str:
        return "org.jetbrains.annotations.Nullable"

    def get_param_javadoc(self, name: str, ts_type: str) -> str:
        return f" * @param {name} {ts_type} parameter"

    def get_return_javadoc(self, ts_type: str) -> str:
        return f" * @return {ts_type} result"
