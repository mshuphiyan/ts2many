from pathlib import Path
from ir.ir_models import IRClass
from .type_mapper import map_ts_type_to_java
from utils.import_optimizer import ImportOptimizer
from utils.type_annotation_helper import TypeAnnotationHelper


class ServiceGenerator:
    def __init__(self, base_package: str = "com.myapp.demo", base_output_dir: Path = Path("out")):
        self.base_package = base_package
        self.base_output_dir = base_output_dir
        self.import_optimizer = ImportOptimizer()
        self.type_helper = TypeAnnotationHelper()

    def generate_and_save(self, ir_class: IRClass):
        print("🧩 Generating service interface and implementation...")
        self._save_interface(ir_class)
        self._save_implementation(ir_class)

    def _save_interface(self, ir_class: IRClass):
        code = self._generate_interface(ir_class)
        path = self._package_to_path("service")
        path.mkdir(parents=True, exist_ok=True)
        file_path = path / f"{ir_class.name}Service.java"
        with open(file_path, "w") as f:
            f.write(code)
        print(f"✅ Interface saved: {file_path}")

    def _save_implementation(self, ir_class: IRClass):
        code = self._generate_implementation(ir_class)
        path = self._package_to_path("service.impl")
        path.mkdir(parents=True, exist_ok=True)
        file_path = path / f"{ir_class.name}ServiceImpl.java"
        with open(file_path, "w") as f:
            f.write(code)
        print(f"✅ Implementation saved: {file_path}")

    def _generate_interface(self, ir_class: IRClass) -> str:
        package = f"{self.base_package}.service"
        lines = [f"package {package};\n"]

        imports = {"org.springframework.stereotype.Service"}
        class_lines = [
            "@Service",
            f"public interface {ir_class.name}Service " + "{",
            "}",
        ]
        code_str = "\n".join(class_lines)
        optimized_imports = self.import_optimizer.optimize(imports, code_str)

        for imp in sorted(optimized_imports):
            lines.append(f"import {imp};")

        lines.append("")  # spacing
        lines.extend(class_lines)

        return "\n".join(lines)

    def _generate_implementation(self, ir_class: IRClass) -> str:
        package = f"{self.base_package}.service.impl"
        lines = [f"package {package};\n"]

        imports = {
            "org.springframework.stereotype.Service",
            "org.springframework.http.ResponseEntity",
            f"{self.base_package}.service.{ir_class.name}Service",
        }

        # DTO imports
        dto_imports = self._get_dto_imports(ir_class)
        imports.update(dto_imports)

        # Body of class
        class_lines = []
        class_lines.append("@Service")
        class_lines.append(f"public class {ir_class.name}ServiceImpl implements {ir_class.name}Service " + "{")

        for method in ir_class.methods:
            return_type = f"ResponseEntity<{map_ts_type_to_java(method.return_type)}>"
            params = ", ".join(f"{map_ts_type_to_java(p.type)} {p.name}" for p in method.parameters)
            class_lines.append("")
            class_lines.append("    @Override")
            class_lines.append(f"    public {return_type} {method.name}({params}) " + "{")
            class_lines.append("        // TODO: Add business logic")
            class_lines.append("        return ResponseEntity.ok().body(null);")
            class_lines.append("    }")

        class_lines.append("}")

        code_str = "\n".join(class_lines)
        optimized_imports = self.import_optimizer.optimize(imports, code_str)

        for imp in sorted(optimized_imports):
            lines.append(f"import {imp};")

        lines.append("")  # spacing
        lines.extend(class_lines)

        return "\n".join(lines)

    def _get_dto_imports(self, ir_class: IRClass) -> set:
        dto_imports = set()
        for method in ir_class.methods:
            for p in method.parameters:
                java_type = map_ts_type_to_java(p.type)
                if java_type[0].isupper() and not java_type.startswith("List"):
                    dto_imports.add(f"{self.base_package}.dto.{java_type}")
        return dto_imports

    def _package_to_path(self, sub_package: str) -> Path:
        full_package = f"{self.base_package}.{sub_package}"
        return self.base_output_dir / "src" / "main" / "java" / Path(*full_package.split("."))
