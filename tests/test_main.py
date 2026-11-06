import pytest
from main import Product, Category


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
    assert len(category.products) == 2
    assert category.products[0] == product1


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
