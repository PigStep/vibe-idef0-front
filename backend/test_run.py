# backend/test_run.py
from schemas import SDiagramData, SNode, SEdge, ICOMTypeEnum
from services.converter import IDEF0Converter

# 1. Создаем тестовые данные (как будто пришли от нейронки)
fake_data = SDiagramData(
    name="Test Process",
    nodes=[
        # A1 - Регистрация
        SNode(id=1, label="Register Order", node_number="A1"),
        # A2 - Проверка
        SNode(id=2, label="Check Availability", node_number="A2"),
        # A3 - Отгрузка
        SNode(id=3, label="Ship Goods", node_number="A3"),
    ],
    edges=[] 
)

# 2. Запускаем конвертер
converter = IDEF0Converter()
xml_output = converter.convert_to_xml(fake_data)

# 3. Печатаем результат
print("=== XML GENERATED SUCCESSFULLY ===")
print(xml_output)