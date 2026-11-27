import pytest
from main import Product, Category, Smartphone, LawnGrass


@pytest.fixture(autouse=True)
def reset_counters():
    """Автоматически сбрасывает атрибуты класса перед каждым тестом"""
    Category.category_count = 0
    Category.product_count = 0
    yield  # Здесь выполняется сам тест, а после него можно было бы сделать очистку


def test_product_creation():
    """Проверка корректной инициализации объекта Product"""
    product = Product("Смартфон", "Отличный телефон", 50000.0, 10)

    assert product.name == "Смартфон"
    assert product.description == "Отличный телефон"
    assert product.price == 50000.0
    assert product.quantity == 10


def test_category_creation():
    """Проверка корректной инициализации объекта Category"""
    product1 = Product("Смартфон", "Телефон", 50000.0, 10)
    product2 = Product("Ноутбук", "Компьютер", 100000.0, 5)

    category = Category("Электроника", "Гаджеты", [product1, product2])

    assert category.name == "Электроника"
    assert category.description == "Гаджеты"
    assert "Смартфон" in category.products
    assert "Ноутбук" in category.products
    assert category.products == "Смартфон, 50000.0 руб. Остаток: 10 шт.\nНоутбук, 100000.0 руб. Остаток: 5 шт."


def test_category_count():
    """Проверка подсчета количества категорий"""
    product = Product("Телефон", "Тест", 10000.0, 1)

    cat1 = Category("Кат1", "Описание1", [product])
    assert cat1 is not None
    assert Category.category_count == 1

    cat2 = Category("Кат2", "Описание2", [product])
    assert cat2 is not None
    assert Category.category_count == 2


def test_product_count():
    """Проверка подсчета общего количества товаров (по длине списка)"""
    p1 = Product("Товар1", "Описание", 100.0, 5)
    p2 = Product("Товар2", "Описание", 200.0, 3)
    p3 = Product("Товар3", "Описание", 300.0, 1)

    cat1 = Category("Кат1", "Описание", [p1, p2])
    assert cat1 is not None
    assert Category.product_count == 2  # Добавили 2 товара

    cat2 = Category("Кат2", "Описание", [p3])
    assert cat2 is not None
    assert Category.product_count == 3  # Всего стало 3 товара


def test_add_product():
    """Проверка метода add_product"""
    product1 = Product("Смартфон", "Телефон", 50000.0, 10)
    product2 = Product("Ноутбук", "Компьютер", 100000.0, 5)

    category = Category("Электроника", "Гаджеты", [product1])

    # Запоминаем текущее количество продуктов
    initial_count = Category.product_count

    # Добавляем новый продукт
    category.add_product(product2)

    # Проверяем, что продукт добавился (через геттер)
    assert "Ноутбук" in category.products

    # Проверяем, что счётчик увеличился на 1
    assert Category.product_count == initial_count + 1


def test_products_getter():
    """Проверка геттера products"""
    product1 = Product("Смартфон", "Телефон", 50000.0, 10)
    category = Category("Электроника", "Гаджеты", [product1])

    expected = "Смартфон, 50000.0 руб. Остаток: 10 шт."
    assert category.products == expected


def test_new_product_classmethod():
    """Проверка класс-метода new_product"""
    product_data = {
        "name": "Планшет",
        "description": "Удобный планшет",
        "price": 30000.0,
        "quantity": 7
    }

    product = Product.new_product(product_data)

    assert product.name == "Планшет"
    assert product.description == "Удобный планшет"
    assert product.price == 30000.0
    assert product.quantity == 7


def test_price_setter():
    """Проверка сеттера цены"""
    product = Product("Смартфон", "Телефон", 50000.0, 10)

    # Проверяем геттер
    assert product.price == 50000.0

    # Устанавливаем новую положительную цену
    product.price = 60000.0
    assert product.price == 60000.0

    # Пытаемся установить отрицательную цену
    product.price = -100
    assert product.price == 60000.0  # Цена не должна была измениться

    # Пытаемся установить нулевую цену
    product.price = 0
    assert product.price == 60000.0  # Цена не должна была измениться


def test_product_str():
    """Проверка строкового представления Product"""
    product = Product("Смартфон", "Телефон", 50000.0, 10)
    assert str(product) == "Смартфон, 50000.0 руб. Остаток: 10 шт."


def test_category_str():
    """Проверка строкового представления Category"""
    product1 = Product("Смартфон", "Телефон", 50000.0, 10)
    product2 = Product("Ноутбук", "Компьютер", 100000.0, 5)
    category = Category("Электроника", "Гаджеты", [product1, product2])
    assert str(category) == "Электроника, количество продуктов: 15 шт."


def test_product_add():
    """Проверка магического метода сложения"""
    product1 = Product("Смартфон", "Телефон", 100.0, 10)
    product2 = Product("Ноутбук", "Компьютер", 200.0, 2)
    assert product1 + product2 == 1400.0  # 100*10 + 200*2


def test_add_same_types():
    """Проверка сложения объектов одного класса"""
    smartphone1 = Smartphone("Смартфон1", "Описание", 100.0, 10, 95.5, "Модель", 256, "Серый")
    smartphone2 = Smartphone("Смартфон2", "Описание", 200.0, 2, 98.2, "Модель", 512, "Синий")
    assert smartphone1 + smartphone2 == 1400.0  # 100*10 + 200*2


def test_add_different_types():
    """Проверка, что сложение разных типов вызывает TypeError"""
    smartphone = Smartphone("Смартфон", "Описание", 100.0, 10, 95.5, "Модель", 256, "Серый")
    grass = LawnGrass("Трава", "Описание", 500.0, 20, "Россия", "7 дней", "Зеленый")
    try:
        smartphone + grass
        assert False, "Должен был быть TypeError"
    except TypeError:
        pass


def test_add_smartphone_to_category():
    """Проверка, что наследник добавляется в категорию"""
    phone = Smartphone("Смартфон", "Описание", 100.0, 10, 95.5, "Модель", 256, "Серый")
    category = Category("Электроника", "Гаджеты", [])
    category.add_product(phone)
    assert "Смартфон" in category.products


def test_add_not_product():
    """Проверка, что добавление не-продукта вызывает TypeError"""
    category = Category("Электроника", "Гаджеты", [])
    try:
        category.add_product("Not a product")
        assert False, "Должен был быть TypeError"
    except TypeError:
        pass
