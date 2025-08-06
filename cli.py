import typer
from ts_parser.ts_runner import extract_ts_ast
from ir.ir_builder import build_ir
from generators.java_generator import generate_java_code

def convert(path: str, target_lang: str = "java"):
    ast = extract_ts_ast(path)
    ir_objects = build_ir(ast)
    if target_lang == "java":
        generate_java_code(ir_objects)

app = typer.Typer()
app.command()(convert)

if __name__ == "__main__":
    app()
