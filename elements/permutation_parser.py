from __future__ import annotations

from typing import List, Tuple, cast

from lark import Lark, Transformer


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
        # Инициализируем парсер без трансформера
        self._parser = Lark(
            self._grammar,
            parser='lalr',
        )
        # Отдельно создаём трансформер
        self._transformer = self._ListTransformer()

    class _ListTransformer(Transformer):
        """
        Преобразует построенное дерево в список кортежей.
        """

        def number(self, token_list: List[str]) -> int:
            return int(token_list[0])

        def group(self, items: List[int]) -> Tuple[int, ...]:
            return tuple(items)

        def start(self, groups: List[Tuple[int, ...]]) -> List[Tuple[int, ...]]:
            return list(groups)

    def parse(self, input_str: str) -> List[Tuple[int, ...]]:
        """
        Парсит строку с записью перестановки и возвращает список кортежей.
        """
        # Сначала получаем дерево разбора
        tree = self._parser.parse(input_str)
        # Затем трансформируем и явно приводим тип
        result = self._transformer.transform(tree)
        return cast(List[Tuple[int, ...]], result)
