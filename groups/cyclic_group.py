from elements.element import IntegerElement
import sympy

from groups.finite_group import FiniteGroup
from groups.Subgroup import SubGroup


class CyclicGroup(FiniteGroup[int,IntegerElement]):
    """
    Класс, реализующий циклическую группу целых чисел по модулю заданного порядка.

    Циклическая группа — это группа, все элементы которой могут быть получены
    путем последовательного применения групповой операции к образующему элементу.
    Данная реализация использует целые числа от 0 до (порядок - 1) с операцией
    сложения по модулю порядка.

    Аргументы:
        order (int): Порядок группы (количество элементов). Должен быть положительным.

    Исключения:
        Exception: Если порядок меньше или равен нулю.
    """

    def __contains__(self, item:IntegerElement)->bool:
        return isinstance(item, IntegerElement) and item.group == self

    def __iter__(self)->Iterator[IntegerElement]:
        return (IntegerElement(i,self) for i in range(len(self)))

    def __init__(self, order: int):
        if order <= 0:
            raise Exception("Порядок группы положительное число")
        self._order = order

    def identity(self) -> IntegerElement:
        """
        Возвращает нейтральный элемент группы (ноль по модулю порядка).

        Пример:
            Для порядка 5: identity() -> 0.

        Возвращает:
            IntegerElement: Нулевой элемент.
        """
        return IntegerElement(0, self)

    def op(self, a: IntegerElement, b: IntegerElement) -> IntegerElement:
        """
        Выполняет групповую операцию (сложение по модулю порядка).

        Аргументы:
            a (IntegerElement): Первый элемент.
            b (IntegerElement): Второй элемент.

        Возвращает:
            IntegerElement: Результат сложения элементов по модулю порядка.
        """
        return IntegerElement((a.value + b.value) % self._order, self)

    def inverse(self, a: IntegerElement) -> IntegerElement:
        """
        Возвращает обратный элемент для `a`.

        Аргументы:
            a (IntegerElement): Элемент, для которого ищется обратный.

        Возвращает:
            IntegerElement: Обратный элемент.
        """
        return IntegerElement(-a.value % self._order,self)

    def __len__(self):
        """
        Возвращает порядок группы (количество элементов).

        Возвращает:
            int: Порядок группы.
        """
        return self._order

    def is_lagrangian(self) -> bool:
        """
        Проверяет, удовлетворяет ли группа обратной теореме Лагранжа.

        Для циклических групп всегда верно, так как для любого делителя порядка
        существует подгруппа такого порядка.

        Возвращает:
            bool: Всегда True.
        """
        return True

    def is_abelian(self) -> bool:
        """
        Проверяет, является ли группа абелевой.

        Все циклические группы абелевы.

        Возвращает:
            bool: Всегда True.
        """
        return True

    def is_simple(self) -> bool:
        """
        Проверяет, является ли группа простой (не имеет нетривиальных нормальных подгрупп).

        Для циклических групп группа является простой тогда и только тогда,
        когда её порядок — простое число или 1.

        Возвращает:
        bool: True, если порядок группы является простым числом или 1, False в противном случае.
        """
        return self._order == 1 or sympy.isprime(self._order)

    def is_solvable(self) -> bool:
        """
        Проверяет, является ли группа разрешимой.

        Все абелевы группы разрешимы.

        Возвращает:
            bool: Всегда True.
        """
        return True

    def comutator(self) -> SubGroup:
        """
        Возвращает коммутант группы (подгруппу, порождённую коммутаторами).

        Для абелевых групп коммутант тривиален.

        Возвращает:
            SubGroup: Тривиальная подгруппа.
        """
        return SubGroup.trivial_identity(self)

    def center(self) -> SubGroup:
        """
        Возвращает центр группы.

        Для абелевых групп центр совпадает с самой группой.

        Возвращает:
            SubGroup: Тривиальная подгруппа.
        """
        return SubGroup.trivial_all(self)

    def __getitem__(self, item: int) -> IntegerElement:
        return IntegerElement(item%self._order, self)
