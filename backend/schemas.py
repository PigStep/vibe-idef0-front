from enum import Enum
from pydantic import BaseModel, Field


class DiagramVariantEnum(str, Enum):
    simple = "simple"
    complex = "complex"
    empty = "empty"

class SDiagramQueryParams(BaseModel):
    variant: DiagramVariantEnum = Field(
        default=DiagramVariantEnum.simple,
        description="Type of the IDEF0 diagram to retrieve"
    )