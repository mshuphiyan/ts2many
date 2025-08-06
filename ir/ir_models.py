# ir_models.py

from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class IRDecorator:
    name: str
    arguments: Optional[str] = None  # e.g., "@Controller('users')"

@dataclass
class IRParam:
    name: str
    type: str
    decorators: List[str] = field(default_factory=list)

@dataclass
class IRMethod:
    name: str
    return_type: str
    parameters: List[IRParam] = field(default_factory=list)
    decorators: List[IRDecorator] = field(default_factory=list)

@dataclass
class IRProperty:
    name: str
    type: str
    access_modifier: Optional[str] = None
    is_readonly: bool = False
    decorators: List[IRDecorator] = field(default_factory=list)

@dataclass
class IRClass:
    name: str
    decorators: List[IRDecorator] = field(default_factory=list)
    extends: Optional[str] = None
    implements: List[str] = field(default_factory=list)
    properties: List[IRProperty] = field(default_factory=list)
    constructor_params: List[IRParam] = field(default_factory=list)
    methods: List[IRMethod] = field(default_factory=list)
