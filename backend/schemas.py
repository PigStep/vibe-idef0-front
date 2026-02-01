from enum import Enum
from pydantic import BaseModel, Field

# v0.1 mock diagrams
class DiagramVariantEnum(Enum):
    simple = "simple"
    complex = "complex"
    empty = "empty"

class SDiagramQueryParams(BaseModel):
    variant: DiagramVariantEnum

#v0.2 IDEF0 Template
class ICOMTypeEnum(Enum):
    """
    ICOM codes for IDEF0 arrows:
    - Input (Left)
    - Control (Top)
    - Output (Right)
    - Mechanism (Bottom)
    """
    input="input"
    control="control"
    mechanism="mechanism"
    output="output"

class SNode(BaseModel):
    id:int= Field(description="Internal unique ID of the block")
    label:str= Field(description="Name of the activity")
    node_number:str|None=Field(
        default=None,
        description="Node number"
    )

class SEdge(BaseModel):

    source_id:int|None=Field(
        default=None,
        description="Source Node ID. None means 'Boundary Start'")
    target_id:int|None=Field(
        default=None,
        description="Target Node ID. None means 'Boundary End'"
    )
    type:ICOMTypeEnum= Field(description="Arrow role (ICOM)")
    label:str= Field(description="Label on the arrow")

class SDiagramData(BaseModel):
    name:str= Field(description="Context diagram name")
    nodes:list[SNode]
    edges:list[SEdge]

