# generators/dto_generator.py

from pathlib import Path
from ir.ir_models import IRClass
from utils.import_optimizer import ImportOptimizer

class DtoGenerator:
    def __init__(self, base_package: str, base_output_dir: Path):
        self.base_package = base_package
        self.base_output_dir = base_output_dir
        self.import_optimizer = ImportOptimizer()

    def generate_and_save(self, ir_class: IRClass):
        code = self.generate_dto_code(ir_class)
        rel_path = Path(*self.base_package.split(".")) / "dto"
        output_path = self.base_output_dir / "src" / "main" / "java" / rel_path
        output_path.mkdir(parents=True, exist_ok=True)

        file_path = output_path / f"{ir_class.name}.java"
        with open(file_path, "w") as f:
            f.write(code)

        print(f"✅ Saved DTO: {file_path.relative_to(self.base_output_dir)}")

    def generate_dto_code(self, ir_class: IRClass) -> str:
        # 1. Package line
        package_line = f"package {self.base_package}.dto;\n"

        # 2. Collect required imports
        imports = {"lombok.Data"}
        for prop in ir_class.properties:
            java_type = self.map_type(prop.type)
            if "List" in java_type:
                imports.add("java.util.List")
            if "Date" in java_type:
                imports.add("java.util.Date")

        # 3. Build import block
        import_block = "\n".join(f"import {imp};" for imp in sorted(imports))

        # 4. Class declaration
        class_decl = f"\n@Data\npublic class {ir_class.name} {{\n"
        fields = self.generate_fields(ir_class)
        class_end = "}\n"

        # 5. Full code before optimization
        full_code = f"{package_line}\n{import_block}\n{class_decl}{fields}{class_end}"

        # ✅ 6. Optimize full code with actual import set
        return self.import_optimizer.optimize(imports, full_code)

    def generate_fields(self, ir_class: IRClass) -> str:
        lines = []
        for prop in ir_class.properties:
            java_type = self.map_type(prop.type)
            lines.append(f"    private {java_type} {prop.name};")
        return "\n".join(lines) + "\n"

    def map_type(self, ts_type: str) -> str:
        mapping = {
            "string": "String",
            "number": "double",
            "boolean": "boolean",
            "any": "Object",
            "Date": "Date",
            "string[]": "List<String>",
            "number[]": "List<Double>",
        }
        return mapping.get(ts_type, "Object")
