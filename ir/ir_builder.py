# ir_builder.py

import json
from typing import List
from .ir_models import IRClass, IRProperty, IRMethod, IRParam, IRDecorator

def parse_decorator_string(deco: str) -> IRDecorator:
    if '(' in deco:
        name = deco.split('(')[0].strip('@')
        args = deco[len(name)+2:-1]
        return IRDecorator(name=name, arguments=args)
    else:
        return IRDecorator(name=deco.strip('@'))

def build_ir_from_json(json_data: List[dict]) -> List[IRClass]:
    classes = []

    for cls in json_data:
        ir_class = IRClass(
            name=cls['name'],
            decorators=[parse_decorator_string(d) for d in cls.get('decorators', [])],
            extends=cls.get('extends'),
            implements=cls.get('implements', []),
            properties=[
                IRProperty(
                    name=p['name'],
                    type=p['type'],
                    access_modifier=p.get('access'),
                    is_readonly=p.get('isReadonly', False),
                    decorators=[parse_decorator_string(d) for d in p.get('decorators', [])]
                )
                for p in cls.get('properties', [])
            ],
            constructor_params=[
                IRParam(
                    name=param['name'],
                    type=param['type'],
                    decorators=param.get('decorators', [])
                )
                for param in cls.get('constructorParams', [])
            ],
            methods=[
                IRMethod(
                    name=m['name'],
                    return_type=m['returnType'],
                    decorators=[parse_decorator_string(d) for d in m.get('decorators', [])],
                    parameters=[
                        IRParam(
                            name=p['name'],
                            type=p['type'],
                            decorators=p.get('decorators', [])
                        )
                        for p in m.get('parameters', [])
                    ]
                )
                for m in cls.get('methods', [])
            ]
        )

        classes.append(ir_class)

    return classes

def load_ir_from_file(json_file_path: str) -> List[IRClass]:
    with open(json_file_path, 'r') as f:
        data = json.load(f)
    return build_ir_from_json(data)
