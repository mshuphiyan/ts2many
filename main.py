# main.py

import os
import argparse
import json
import subprocess
from pathlib import Path
from ir.ir_builder import build_ir_from_json
from generators.controller_generator import ControllerGenerator
from generators.service_generator import ServiceGenerator
from generators.dto_generator import DtoGenerator
from generators.entity_generator import EntityGenerator
from detectors.repository_detector import is_repository_class
from generators.repository_generator import RepositoryGenerator


from scaffolder.gradle_scaffolder import scaffold_gradle_project

TS_PARSER_PATH = Path("ts_parser/ts_morph_bridge.js")

def parse_typescript_file(ts_file: str) -> list:
    """Parse a single TypeScript file or pre-parsed JSON."""
    if ts_file.endswith(".json"):
        with open(ts_file, "r") as f:
            return json.load(f)
    else:
        result = subprocess.run(
            ["node", str(TS_PARSER_PATH), "--input", ts_file],
            capture_output=True,
            text=True,
            check=True
        )
        return json.loads(result.stdout)

def collect_ts_files(inputs: list) -> list:
    """Recursively collect all .ts files from given files/directories."""
    ts_files = []
    for input_path in inputs:
        path = Path(input_path)
        if path.is_dir():
            ts_files.extend(path.rglob("*.ts"))
        elif path.is_file() and path.suffix == ".ts":
            ts_files.append(path)
    return list(map(str, ts_files))

def main():
    parser = argparse.ArgumentParser(description="Convert TypeScript to IR and target code.")
    parser.add_argument("--input", nargs="+", required=True, help="Paths to TypeScript files or directories")
    parser.add_argument("--lang", required=False, default="ir", choices=["ir", "java", "python"], help="Target language (default: IR only)")
    parser.add_argument("--output-dir", required=False, help="Output directory for generated code.")
    parser.add_argument("--package", required=False, help="Java package name (e.g., com.example.app)")

    args = parser.parse_args()

    ts_files = collect_ts_files(args.input)
    if not ts_files:
        print("🚫 No TypeScript files found.")
        return

    print(f"📁 Found {len(ts_files)} TypeScript files to parse.")

    all_ir_classes = []
    for ts_file in ts_files:
        print(f"🔍 Parsing: {ts_file}")
        ts_ast = parse_typescript_file(ts_file)
        ir_classes = build_ir_from_json(ts_ast)
        all_ir_classes.extend(ir_classes)

    if args.lang == "ir":
        print("✅ IR Output:")
        for ir_cls in all_ir_classes:
            print(ir_cls)

    elif args.lang == "java":
        print("🛠️  Generating Java Code (Phase 4.5)...\n")
        output_dir = Path(args.output_dir) if args.output_dir else Path("out/java")
        package = args.package or "com.example.demo"

        scaffold_gradle_project(output_dir, package)

        controller_generator = ControllerGenerator(base_package=package, base_output_dir=output_dir)
        service_generator = ServiceGenerator(base_package=package, base_output_dir=output_dir)
        dto_generator = DtoGenerator(base_package=package, base_output_dir=output_dir)
        entity_generator = EntityGenerator(base_package=package, base_output_dir=output_dir)
        repository_generator = RepositoryGenerator(output_dir, package)


        for ir_class in all_ir_classes:
            print("🔍 Debug IRClass:", ir_class.name)
            # print("    Base classes:", ir_class.base_classes)
            print("    Decorators:", [d.name for d in ir_class.decorators])

            name_lower = ir_class.name.lower()
            decorator_names = [d.name.lower() for d in ir_class.decorators]

            print(f"📦 Scanning: {ir_class.name}, decorators={decorator_names}")

            # Controller
            if "controller" in decorator_names:
                print(f"📦 Detected Controller: {ir_class.name}")
                controller_generator.generate_and_save(ir_class)

            # Repository (by name or decorator)
            elif is_repository_class(ir_class):
                print(f"📦 Detected Repository: {ir_class.name}")
                repository_generator.generate_and_save(ir_class)

            # Service
            elif "service" in decorator_names or "injectable" in decorator_names:
                print(f"📦 Detected Service: {ir_class.name}")
                service_generator.generate_and_save(ir_class)

            # DTO
            elif ir_class.name.endswith("Dto") and not decorator_names:
                print(f"📦 Detected DTO: {ir_class.name}")
                dto_generator.generate_and_save(ir_class)

            # Entity
            elif "entity" in decorator_names:
                print(f"📦 Detected Entity: {ir_class.name}")
                entity_generator.generate_and_save(ir_class)

            # No match
            else:
                print(f"⚠️  No matching generator for: {ir_class.name}")


if __name__ == "__main__":
    main()
