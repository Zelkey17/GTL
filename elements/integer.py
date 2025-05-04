from __future__ import annotations
from elements.base import Element
from groups.base import Group

class IntegerElement(Element[int]):
    """
    Представляет элемент группы с целочисленными значениями.

    Реализация интерфейса `Element[int]`, где все операции
    (умножение, возведение в степень, взятие обратного)
    делегируются соответствующей группе.

    Attributes:
        _value (int): Внутреннее целочисленное представление элемента.
        _reference_to_group (Group[int, IntegerElement]):
            Ссылка на группу, к которой принадлежит элемент.
    """

    def __init__(self, value: int, reference_to_group: Group[int, IntegerElement]):
        """
        Инициализирует новый элемент целочисленной группы.

        Args:
            value (int): Целочисленное значение элемента.
            reference_to_group (Group[int, IntegerElement]):
                Экземпляр группы, реализующей операции над элементами.
        """
        self._value = value
        self._reference_to_group = reference_to_group

    @property
    def value(self) -> int:
        """
        Внутреннее значение элемента.

        Returns:
            int: Целое число, хранящееся в элементе.
        """
        return self._value

    @property
    def group(self) -> Group[int, IntegerElement]:
        """
        Группа, к которой принадлежит этот элемент.

        Returns:
            Group[int, IntegerElement]: Ссылка на соответствующую группу.
        """
        return self._reference_to_group

    def __eq__(self, other: object) -> bool:
        """
        Проверяет равенство двух элементов одной группы.

        Args:
            other (object): Другой объект для сравнения.

        Returns:
            bool: True, если оба — IntegerElement той же группы и имеют одинаковое value.

        Raises:
            TypeError: Если other не является элементом или принадлежит другой группе.
        """
        if not isinstance(other, Element) or self.group != other.group:
            raise TypeError("Несовместимые элементы для сравнения")
        return self._value == other.value

    def __mul__(self, other: IntegerElement) -> IntegerElement:
        """
        Групповая операция: умножение (произведение) двух элементов.

        Делегирует реализацию методу op() группы.

        Args:
            other (IntegerElement): Элемент той же группы для умножения.

        Returns:
            IntegerElement: Результат op(self, other) из группы.

        Raises:
            TypeError: Если элементы из разных групп.
        """
        if not isinstance(other, Element) or self.group != other.group:
            raise TypeError("Несовместимые элементы для умножения")
        return self._reference_to_group.op(self, other)

    def __pow__(self, power: int, modulo=None) -> IntegerElement:
        """
        Возведение элемента в целую степень.

        Поддерживаются отрицательные степени за счёт inverse().

        Args:
            power (int): Показатель степени.
            modulo: Не используется (для соответствия сигнатуре Python).

        Returns:
            IntegerElement: Результат возведения в степень.
        """
        # Игнорируем параметр modulo, т.к. группа сама обрабатывает обратные степени
        return self._reference_to_group.pow(self, power)

    def inv(self) -> IntegerElement:
        """
        Возвращает обратный к элементу элемент.

        Делегирует реализацию методу inverse() группы.

        Returns:
            IntegerElement: Элемент b, такой что self * b == identity.
        """
        return self._reference_to_group.inverse(self)

    def __repr__(self) -> str:
        """
        Строковое представление элемента — его значение.

        Returns:
            str: Строка с числовым значением элемента.
        """
        return str(self._value)

    def __hash__(self) -> int:
        """
        Хэш-функция для использования в множествах и словарях.

        Returns:
            int: Хэш от внутреннего значения.
        """
        return hash(self._value)
