# backend/test_run.py
from schemas import SDiagramData, SNode, SEdge, ICOMTypeEnum
from services.converter import IDEF0Converter

# 1. Создаем тестовые данные: Процесс работы кофейни
fake_data = SDiagramData(
    name="Процесс обслуживания в кофейне",
    nodes=[
        # Блок 1: Прием заказа
        SNode(id=1, label="Принять и оплатить заказ", node_number="A1"),
        # Блок 2: Приготовление
        SNode(id=2, label="Приготовить напиток", node_number="A2"),
        # Блок 3: Выдача
        SNode(id=3, label="Выдать заказ клиенту", node_number="A3"),
    ],
    edges=[
        # --- ВХОДЫ (Inputs - Слева) ---
        # Вход из границы -> в А1
        SEdge(source_id=None, target_id=1, type=ICOMTypeEnum.input, label="Заказ клиента"),
        # Вход из границы -> в А2
        SEdge(source_id=None, target_id=2, type=ICOMTypeEnum.input, label="Кофейные зерна, Молоко"),
        # Вход из границы -> в А3
        SEdge(source_id=None, target_id=3, type=ICOMTypeEnum.input, label="Упаковка (Стаканчик)"),

        # --- УПРАВЛЕНИЕ (Controls - Сверху) ---
        # Правила действуют на все блоки, но для примера направим в разные
        SEdge(source_id=None, target_id=1, type=ICOMTypeEnum.control, label="Прейскурант цен"),
        SEdge(source_id=None, target_id=2, type=ICOMTypeEnum.control, label="Рецептура кофе"),
        SEdge(source_id=None, target_id=3, type=ICOMTypeEnum.control, label="Стандарты сервиса"),

        # --- МЕХАНИЗМЫ (Mechanisms - Снизу) ---
        # Кто выполняет работу?
        SEdge(source_id=None, target_id=1, type=ICOMTypeEnum.mechanism, label="Кассир / POS-терминал"),
        SEdge(source_id=None, target_id=2, type=ICOMTypeEnum.mechanism, label="Бариста"),
        SEdge(source_id=None, target_id=2, type=ICOMTypeEnum.mechanism, label="Кофемашина"), # В один блок можно несколько механизмов

        # --- СВЯЗИ МЕЖДУ БЛОКАМИ (Internal Flow) ---
        # Выход А1 (Чек) -> Вход А2 (Основание для готовки)
        SEdge(source_id=1, target_id=2, type=ICOMTypeEnum.control, label="Оплаченный чек"), 
        # Выход А2 (Кофе) -> Вход А3 (Товар для выдачи)
        SEdge(source_id=2, target_id=3, type=ICOMTypeEnum.input, label="Готовый кофе"),

        # --- ВЫХОДЫ (Outputs - Справа в никуда) ---
        # Результат всего процесса
        SEdge(source_id=3, target_id=None, type=ICOMTypeEnum.output, label="Довольный клиент"),
    ]
)

# 2. Запускаем конвертер
converter = IDEF0Converter()
xml_output = converter.convert_to_xml(fake_data)

# 3. Печатаем результат
print("=== XML GENERATED SUCCESSFULLY ===")
print(xml_output)