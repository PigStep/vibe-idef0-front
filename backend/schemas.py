from enum import Enum
from pydantic import BaseModel


class DiagramVariantEnum(Enum):
    simple = "simple"
    complex = "complex"
    empty = "empty"

class SDiagramQueryParams(BaseModel):
    variant: DiagramVariantEnum
