from __future__ import annotations

from typing import List, Tuple
from lark import Lark, Transformer, exceptions


class PermutationParser:
    """
    Парсер циклической записи перестановки.

    Преобразует строки вида "(1, 2, 3)(4,6)(5)" в список кортежей чисел.
    Обрабатываются варианты с пробелами и без, а также пустые скобки "()".
    """

    def __init__(self):
        """
        Инициализирует парсер с грамматикой Lark и трансформером.

        Грамматика определяет:
          - start: одна или более групп "group"
          - group: скобки с нуля или более чисел, разделённых запятыми
          - number: целое число

        Пробелы игнорируются.
        """
        self._grammar = r"""
            start: group+                 // строка должна состоять из одной или более групп
            group: "(" [number ("," number)*] ")"  // группа: скобки с числами через запятую, может быть пустой
            number: INT                   // целое число
            %import common.INT
            %import common.WS
            %ignore WS                    // игнорируем пробельные символы
        """
        # Используем LALR-парсер и свой Transformer для получения Python-структур
        self._parser = Lark(
            self._grammar,
            parser='lalr',
            transformer=self._ListTransformer()
        )

    class _ListTransformer(Transformer):
        """
        Преобразует построенное дерево в список кортежей.
        """

        def number(self, token_list: List[str]) -> int:
            """
            Преобразует токен числа в int.

            Args:
                token_list (List[str]): Список токенов (обычно один элемент).

            Returns:
                int: Преобразованное целое число.
            """
            return int(token_list[0])

        def group(self, items: List[int]) -> Tuple[int, ...]:
            """
            Преобразует содержимое одной группы в кортеж.

            Args:
                items (List[int]): Список чисел в текущих скобках.

            Returns:
                Tuple[int, ...]: Кортеж чисел группы.
            """
            return tuple(items)

        def start(self, groups: List[Tuple[int, ...]]) -> List[Tuple[int, ...]]:
            """
            Объединяет все группы в итоговый список.

            Args:
                groups (List[Tuple[int, ...]]): Список всех кортежей.

            Returns:
                List[Tuple[int, ...]]: Итоговый список кортежей перестановки.
            """
            return list(groups)

    def parse(self, input_str: str) -> List[Tuple[int, ...]]:
        """
        Парсит строку с записью перестановки и возвращает список кортежей.

        Args:
            input_str (str): Строка вида "(1,2,3)(4,5)()".

        Returns:
            List[Tuple[int, ...]]: Список кортежей, соответствующих каждой группе.

        Raises:
            exceptions.LarkError: При ошибках синтаксического разбора.
        """
        # Передаём строку парсеру и возвращаем результат трансформации
        return self._parser.parse(input_str)
