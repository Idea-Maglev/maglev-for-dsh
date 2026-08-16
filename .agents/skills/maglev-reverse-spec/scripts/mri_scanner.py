import argparse
import ast
import json
import os
import re


class PythonRouteScanner:
    HTTP_METHODS = {"get", "post", "put", "delete", "patch"}

    def scan(self, file_path):
        routes = []
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                tree = ast.parse(f.read())
        except Exception:
            return routes

        for node in ast.walk(tree):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            for decorator in node.decorator_list:
                if not isinstance(decorator, ast.Call):
                    continue
                func = decorator.func
                method = None
                if isinstance(func, ast.Attribute):
                    method = func.attr.lower()
                elif isinstance(func, ast.Name):
                    method = func.id.lower()
                if method not in self.HTTP_METHODS:
                    continue
                path = "unknown"
                if decorator.args:
                    arg = decorator.args[0]
                    if isinstance(arg, ast.Constant):
                        path = arg.value
                    elif isinstance(arg, ast.Str):
                        path = arg.s
                routes.append({"method": method.upper(), "path": path, "func": node.name})
        return routes


class PythonStructureScanner:
    def scan(self, file_path):
        structures = []
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                tree = ast.parse(f.read())
        except Exception:
            return structures

        for node in ast.walk(tree):
            if not isinstance(node, ast.ClassDef):
                continue
            fields = []
            for child in node.body:
                if isinstance(child, ast.AnnAssign) and isinstance(child.target, ast.Name):
                    field_type = ast.unparse(child.annotation) if hasattr(ast, "unparse") else "unknown"
                    fields.append({"name": child.target.id, "type": field_type})
                elif isinstance(child, ast.Assign):
                    for target in child.targets:
                        if isinstance(target, ast.Name):
                            fields.append({"name": target.id, "type": "unknown"})
            if fields:
                structures.append({"name": node.name, "fields": fields})
        return structures


class TsJsScanner:
    API_PATTERN = re.compile(r"(?:http|api|axios)\.(get|post|put|delete|patch)\([\"']([^\"']+)[\"']")
    FETCH_PATTERN = re.compile(r"fetch\([\"']([^\"']+)[\"']")
    INTERFACE_PATTERN = re.compile(r"interface\s+([a-zA-Z0-9_]+)\s*\{")
    TYPE_PATTERN = re.compile(r"type\s+([a-zA-Z0-9_]+)\s*=")

    def scan(self, file_path):
        findings = {"api_calls": [], "interfaces": [], "types": []}
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception:
            return findings

        for method, path in self.API_PATTERN.findall(content):
            findings["api_calls"].append({"method": method.upper(), "path": path})
        for path in self.FETCH_PATTERN.findall(content):
            findings["api_calls"].append({"method": "FETCH", "path": path})
        for name in self.INTERFACE_PATTERN.findall(content):
            findings["interfaces"].append(name)
        for name in self.TYPE_PATTERN.findall(content):
            findings["types"].append(name)
        return findings


def iter_files(roots, suffixes):
    for root in roots:
        if not root or not os.path.exists(root):
            continue
        for current_root, _, files in os.walk(root):
            for file_name in files:
                if file_name.endswith(suffixes):
                    yield os.path.join(current_root, file_name)


def main():
    parser = argparse.ArgumentParser(description="Generic MRI scanner for reverse engineering.")
    parser.add_argument("--backend", action="append", default=[], help="Backend root path, repeatable.")
    parser.add_argument("--frontend", action="append", default=[], help="Frontend root path, repeatable.")
    args = parser.parse_args()

    py_scanner = PythonRouteScanner()
    py_structure_scanner = PythonStructureScanner()
    ts_scanner = TsJsScanner()
    results = {"backend": {}, "frontend": {}}

    for path in iter_files(args.backend, (".py",)):
        rel_path = os.path.relpath(path)
        routes = py_scanner.scan(path)
        structures = py_structure_scanner.scan(path)
        if routes or structures:
            results["backend"][rel_path] = {}
            if routes:
                results["backend"][rel_path]["routes"] = routes
            if structures:
                results["backend"][rel_path]["structures"] = structures

    for path in iter_files(args.frontend, (".ts", ".tsx", ".js", ".jsx", ".vue")):
        rel_path = os.path.relpath(path)
        findings = ts_scanner.scan(path)
        if findings["api_calls"] or findings["interfaces"] or findings["types"]:
            results["frontend"][rel_path] = findings

    print(json.dumps(results, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
