# generators/repository_generator.py

from pathlib import Path
from ir.ir_models import IRClass
from utils.file_utils import save_java_file
from utils.import_optimizer import ImportOptimizer

class RepositoryGenerator:
    def __init__(self, base_output_dir: Path, base_package: str):
        self.base_output_dir = base_output_dir
        self.base_package = base_package
        self.import_optimizer = ImportOptimizer()

    def generate_and_save(self, ir_class: IRClass):
        print(f"🛠️  Generating Repository: {ir_class.name}")
        class_code = self._generate_repository_code(ir_class)
        file_path = self._get_output_path(ir_class.name)
        save_java_file(file_path, class_code)

    def _generate_repository_code(self, ir_class: IRClass) -> str:
        if not ir_class.name.endswith("Repository"):
            raise ValueError(f"Expected repository class to end with 'Repository', got: {ir_class.name}")

        package_line = f"package {self.base_package}.repository;\n"

        entity_name = ir_class.name[:-10]  # Strip 'Repository'
        imports = {
            "org.springframework.stereotype.Repository",
            "org.springframework.data.jpa.repository.JpaRepository",
            self._get_entity_import(entity_name)
        }

        import_block = "\n".join(f"import {imp};" for imp in sorted(imports))
        interface_decl = (
            f"\n@Repository\n"
            f"/**\n * Repository interface for {entity_name} entity.\n */\n"
            f"public interface {ir_class.name} extends JpaRepository<{entity_name}, Long> {{\n}}\n"
        )

        full_code = f"{package_line}\n\n{import_block}\n{interface_decl}".strip()
        return self.import_optimizer.optimize(imports, full_code)

    def _get_output_path(self, class_name: str) -> Path:
        rel_path = Path(*self.base_package.split(".")) / "repository" / f"{class_name}.java"
        return self.base_output_dir / "src" / "main" / "java" / rel_path

    def _get_entity_import(self, entity_name: str) -> str:
        return f"{self.base_package}.entity.{entity_name}"
