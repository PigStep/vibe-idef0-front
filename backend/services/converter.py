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

        for index,node in enumerate(data.nodes):
            self._create_node_element(root,node,index)

        ET.indent(mx_graph,space="  ",level=0)

        return ET.tostring(mx_graph,encoding='unicode',method='xml')
    
    def _create_node_element(self,root:ET.Element,node,index:int):

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

