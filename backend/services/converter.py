import xml.etree.ElementTree as ET
from schemas import SDiagramData,SEdge,ICOMTypeEnum


class IDEF0Converter:
    def __init__(self):
        self.BLOCK_WIDTH=140
        self.BLOCK_HEIGHT=80
        self.START_X=120
        self.START_Y=100
        self.OFFSET_X=180
        self.OFFSET_Y=120

    def convert_to_xml(self,data=SDiagramData)->str:
        mx_graph = ET.Element("mxGraphModel", {
            "dx": "1000", "dy": "1000", "grid": "1", "gridSize": "10", 
            "guides": "1", "tooltips": "1", "connect": "1", "arrows": "1", 
            "fold": "1", "page": "1", "pageScale": "1", 
            "pageWidth": "827", "pageHeight": "1169", "background": "#ffffff"
        })

        root=ET.SubElement(mx_graph,"root")

        ET.SubElement(root, "mxCell", {"id": "0"})
        ET.SubElement(root, "mxCell", {"id": "layer_1", "parent": "0"})

        node_coords:dict[int,tuple[int,int]]={}
        
        for index,node in enumerate(data.nodes):
            x,y=self._create_node_element(root,node,index)
            node_coords[node.id]=(x,y)

        for edge in data.edges:
            self._create_edge_element(root,edge,node_coords)


        ET.indent(mx_graph,space="  ",level=0)
        return ET.tostring(mx_graph,encoding='unicode',method='xml')
    
    def _create_node_element(self,root:ET.Element,node,index:int)->tuple[int,int]:

        x=self.START_X+(index*self.OFFSET_X)
        y=self.START_Y+(index*self.OFFSET_Y)

        style = "rounded=0;whiteSpace=wrap;html=1;shadow=0;"

        full_label=f"{node.label}"
        if node.node_number:
            full_label=f"{node.node_number}\n{full_label}"
        
        node_xml=ET.SubElement(root,"mxCell",{
            "id":str(node.id),
            "value":full_label,
            "style":style,
            "parent":"layer_1",
            "vertex":"1" # it's a block (arrow will be 0)
        })

        ET.SubElement(node_xml,"mxGeometry",{
            "x":str(x),
            "y":str(y),
            "width":str(self.BLOCK_WIDTH),
            "height":str(self.BLOCK_HEIGHT),
            "as":"geometry"
        })

        return x,y
    
    def _create_edge_element(self,root:ET.Element,edge:SEdge,node_coords:dict[int,tuple[int,int]]):
        
        style_parts=[
            "edgeStyle=orthogonalEdgeStyle", 
            "rounded=0", 
            "orthogonalLoop=1", 
            "jettySize=auto", 
            "html=1"
        ]

        # Target Entry 
        if edge.target_id is not None:
            if edge.type==ICOMTypeEnum.input:
                style_parts.append("entryX=0;entryY=0.5") #Left
            elif edge.type==ICOMTypeEnum.control:
                style_parts.append("entryX=0.5;entryY=0") #Top
            elif edge.type==ICOMTypeEnum.mechanism:
                style_parts.append("entryX=0.5;entryY=1") #Bottom
            else:
                style_parts.append("entryX=0;entryY=0.5") #TODO test when arrow comes from right block to left    

        # Source Exit
        if edge.source_id is not None:
            style_parts.append("exitX=1;exitY=0.5")

        edge_xml=ET.SubElement(root,"mxCell",{
            "style":";".join(style_parts),
            "parent":"layer_1",
            "edge":"1",
            "value":edge.label
        })

        # Binding Block IDs
        if edge.source_id is not None:
            edge_xml.set("source",str(edge.source_id))
        if edge.target_id is not None:
            edge_xml.set("target",str(edge.target_id))

        geometry=ET.SubElement(edge_xml,"mxGeometry",{"relative":"1","as":"geometry"})

        # Case: Source=None -> to Block
        if edge.source_id is None and edge.target_id is not None:
            target_x,target_y=node_coords.get(edge.target_id,(0,0))
            start_x,start_y=target_x,target_y

            if edge.type == ICOMTypeEnum.input:
                start_x -= 60; start_y += self.BLOCK_HEIGHT / 2
            elif edge.type == ICOMTypeEnum.control:
                start_x += self.BLOCK_WIDTH / 2; start_y -= 60
            elif edge.type == ICOMTypeEnum.mechanism:
                start_x += self.BLOCK_WIDTH / 2; start_y += self.BLOCK_HEIGHT + 60    

            ET.SubElement(geometry, "mxPoint", {"x": str(start_x), "y": str(start_y), "as": "sourcePoint"})

        # Case: Target=None -> to Border
        elif edge.target_id is None and edge.source_id is not None:
            source_x, source_y = node_coords.get(edge.source_id, (0,0))
            
            end_x = source_x + self.BLOCK_WIDTH + 60
            end_y = source_y + self.BLOCK_HEIGHT / 2
            
            ET.SubElement(geometry, "mxPoint", {"x": str(end_x), "y": str(end_y), "as": "targetPoint"})
