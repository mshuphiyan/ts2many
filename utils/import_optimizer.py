# utils/import_optimizer.py

import re
from typing import List, Set


class ImportOptimizer:
    def __init__(self):
        self.standard_imports = {
            "List": "java.util.List",
            "Optional": "java.util.Optional",
            "Autowired": "org.springframework.beans.factory.annotation.Autowired",
            "Service": "org.springframework.stereotype.Service",
            "Repository": "org.springframework.stereotype.Repository",
            "Controller": "org.springframework.web.bind.annotation.RestController",
            "GetMapping": "org.springframework.web.bind.annotation.GetMapping",
            "PostMapping": "org.springframework.web.bind.annotation.PostMapping",
            "PutMapping": "org.springframework.web.bind.annotation.PutMapping",
            "DeleteMapping": "org.springframework.web.bind.annotation.DeleteMapping",
            "RequestMapping": "org.springframework.web.bind.annotation.RequestMapping",
            "RequestBody": "org.springframework.web.bind.annotation.RequestBody",
            "PathVariable": "org.springframework.web.bind.annotation.PathVariable",
            "Entity": "jakarta.persistence.Entity",
            "Id": "jakarta.persistence.Id",
            "GeneratedValue": "jakarta.persistence.GeneratedValue",
        }

    def optimize(self, imports: set, code: str) -> set:
        # Detect used classes that need imports
        used_classes = set(self._find_used_classes(code))

        # Deduplicate existing imports
        code_lines = code.splitlines()
        final_lines = []
        existing_imports: Set[str] = set()
        added_imports: Set[str] = set()

        for line in code_lines:
            if line.strip().startswith("import "):
                existing_imports.add(line.strip())
            else:
                final_lines.append(line)

        # Determine needed imports
        needed_imports = []
        for keyword, import_path in self.standard_imports.items():
            if keyword in used_classes and f"import {import_path};" not in existing_imports:
                needed_imports.append(f"import {import_path};")

        # Sort and deduplicate all imports
        all_imports = sorted(existing_imports.union(needed_imports))

        # Reinsert imports after package declaration
        final_code = []
        package_inserted = False
        for line in final_lines:
            final_code.append(line)
            if not package_inserted and line.startswith("package "):
                package_inserted = True
                final_code.extend(all_imports)
                final_code.append("")  # empty line after imports

        return "\n".join(final_code)

    def _find_used_classes(self, code: str) -> List[str]:
        """
        Heuristic: detect all capitalized identifiers which could be class names.
        """
        return re.findall(r'\b([A-Z][A-Za-z0-9_]*)\b', code)
