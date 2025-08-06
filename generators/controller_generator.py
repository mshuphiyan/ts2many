from pathlib import Path
from ir.ir_models import IRClass
from .type_mapper import map_ts_type_to_java
from utils.import_optimizer import ImportOptimizer


class ControllerGenerator:
    def __init__(self, base_package: str = "com.example.demo", base_output_dir: Path = Path("out")):
        self.base_package = base_package
        self.base_output_dir = base_output_dir
        self.import_optimizer = ImportOptimizer()

    def generate_and_save(self, ir_class: IRClass):
        kind = self._infer_kind(ir_class)
        package = f"{self.base_package}.{kind}"
        java_code, imports = self._generate_class_code(ir_class, package, kind)
        self._save(java_code, ir_class.name, kind, imports)

    def _generate_class_code(self, ir_class: IRClass, package: str, kind: str) -> tuple[str, set[str]]:
        imports = set()
        annotations = []
        lines = [f"package {package};\n"]

        # Decorator-based detection
        for decorator in ir_class.decorators:
            if decorator.name == "Controller":
                annotations.append("@RestController")
                route = decorator.arguments.strip('"').strip("'") if decorator.arguments else ""
                annotations.append(f'@RequestMapping("{route}")' if route else '@RequestMapping("")')
                imports.update({
                    "org.springframework.web.bind.annotation.RestController",
                    "org.springframework.web.bind.annotation.RequestMapping"
                })
            elif decorator.name == "Service":
                annotations.append("@Service")
                imports.add("org.springframework.stereotype.Service")

        # Common controller-related imports
        imports.update({
            "org.springframework.web.bind.annotation.*",
            "org.springframework.http.ResponseEntity"
        })

        # Method-level type imports
        for method in ir_class.methods:
            # Return type
            ret_type = map_ts_type_to_java(method.return_type)
            if ret_type == "List":
                imports.add("java.util.List")

            # Param type imports
            for param in method.parameters:
                param_type = map_ts_type_to_java(param.type)
                if param_type not in {"int", "long", "float", "double", "boolean", "String"}:
                    imports.add(f"{self.base_package}.dto.{param_type}")

        # Import section
        lines.extend(sorted(f"import {imp};" for imp in imports))
        lines.append("")
        lines.extend(annotations)

        # Class declaration
        class_decl = f"public class {ir_class.name}"
        if ir_class.extends:
            class_decl += f" extends {ir_class.extends}"
        if ir_class.implements:
            class_decl += " implements " + ", ".join(ir_class.implements)
        lines.append(class_decl + " {")

        # Constructor injection (only for controllers)
        if kind == "controller":
            service_name = ir_class.name.replace("Controller", "Service")
            service_var = self._camel(service_name)
            lines.append(f"    private final {service_name} {service_var};\n")
            lines.append("    @Autowired")
            lines.append(f"    public {ir_class.name}({service_name} {service_var}) {{")
            lines.append(f"        this.{service_var} = {service_var};")
            lines.append("    }")

        # Method generation
        for method in ir_class.methods:
            lines.append("")
            http_annot = self._map_http_method(method.name)
            if http_annot:
                lines.append(f"    {http_annot}")

            ret_type = map_ts_type_to_java(method.return_type)
            wrapped_ret_type = f"ResponseEntity<{ret_type}>"

            # Parameters
            param_strs = []
            for param in method.parameters:
                java_type = map_ts_type_to_java(param.type)
                is_dto = param.name.lower().endswith("dto")
                annotation = "@RequestBody " if is_dto else "@RequestParam "
                param_strs.append(f"{annotation}{java_type} {param.name}")
            joined_params = ", ".join(param_strs)

            lines.append(f"    public {wrapped_ret_type} {method.name}({joined_params}) {{")
            lines.append("        // TODO: Implement")
            lines.append("        return ResponseEntity.ok().body(null);")
            lines.append("    }")

        lines.append("}")
        return "\n".join(lines), imports

    def _save(self, java_code: str, class_name: str, kind: str, imports: set[str]):
        path = self.base_output_dir / "src" / "main" / "java" / Path(*self.base_package.split(".")) / kind
        path.mkdir(parents=True, exist_ok=True)
        file_path = path / f"{class_name}.java"

        java_code = self.import_optimizer.optimize(imports, java_code)

        with open(file_path, "w") as f:
            f.write(java_code)
        print(f"✅ Saved: {file_path}")

    def _map_http_method(self, method_name: str) -> str:
        name = method_name.lower()
        if name.startswith("get"):
            return "@GetMapping"
        if name.startswith(("create", "post")):
            return "@PostMapping"
        if name.startswith(("update", "put")):
            return "@PutMapping"
        if name.startswith(("delete", "remove")):
            return "@DeleteMapping"
        return ""

    def _infer_kind(self, ir_class: IRClass) -> str:
        for decorator in ir_class.decorators:
            if decorator.name.lower() == "controller":
                return "controller"
            if decorator.name.lower() == "service":
                return "service"
        if ir_class.name.lower().endswith("dto"):
            return "dto"
        if ir_class.name.lower().endswith("entity"):
            return "entity"
        return "common"

    def _camel(self, name: str) -> str:
        return name[0].lower() + name[1:] if name else name
