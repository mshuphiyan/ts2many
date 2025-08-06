# generators/entity_generator.py

from pathlib import Path
from ir.ir_models import IRClass
from utils.java_utils import to_snake_case
from .type_mapper import map_ts_type_to_java

class EntityGenerator:
    def __init__(self, base_package: str, base_output_dir: Path):
        self.base_package = base_package
        self.base_output_dir = base_output_dir

    def generate_and_save(self, ir_class):
        package_path = self.base_package.replace(".", "/")
        output_dir = self.base_output_dir / "src/main/java" / package_path / "entity"
        output_dir.mkdir(parents=True, exist_ok=True)

        class_code = self._generate_entity_code(ir_class)
        file_path = output_dir / f"{ir_class.name}.java"

        with open(file_path, "w") as f:
            f.write(class_code)
        print(f"✅ Saved: {file_path}")

    def _generate_entity_code(self, ir_class: IRClass) -> str:
        class_name = ir_class.name
        package_line = f"package {self.base_package}.entity;\n"
        imports = set([
            "import jakarta.persistence.*;",
            "import lombok.*;"
        ])

        annotations = [
            "@Entity",
            f"@Table(name = \"{to_snake_case(class_name)}\")",
            "@Data",
            "@NoArgsConstructor",
            "@AllArgsConstructor"
        ]

        fields = []
        for prop in ir_class.properties:
            java_type = map_ts_type_to_java(prop.type)
            field_annotations = []
            if prop.name == "id":
                field_annotations = ["@Id", "@GeneratedValue(strategy = GenerationType.IDENTITY)"]

            field_line = f"{' '.join(field_annotations)}\n    private {java_type} {prop.name};"
            fields.append(field_line)

        class_body = "\n\n    ".join(fields)

        code = "\n".join([
            package_line,
            *sorted(imports),
            "",
            *annotations,
            f"public class {class_name} {{",
            f"    {class_body}",
            "}"
        ])
        return code
