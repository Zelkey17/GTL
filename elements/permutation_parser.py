from lark import Lark, Transformer


class PermutationParser:
    """
    Парсер строк вида "(1, 2, 3)(4, 6)(5, 7)" в list[tuple[int]].
    Обрабатывает варианты:
    - (1, 2, 3)(4, 6)(5, 7)
    - (1,2,3)(4,6)(5,7)
    - (1, 2,3)(4,6)(5, 7)
    - ()  # пустые скобки
    """

    def __init__(self):
        self._grammar = r"""
            start: group+
            group: "(" [number ("," number)*] ")"
            number: INT
            %import common.INT
            %import common.WS
            %ignore WS
        """
        self._parser = Lark(
            self._grammar,
            parser='lalr',
            transformer=self._ListTransformer()
        )

    class _ListTransformer(Transformer):
        def number(self, n):
            return int(n[0])

        def group(self, items):
            return tuple(items)

        def start(self, groups):
            return list(groups)

    def parse(self, input_str: str) -> list[tuple[int]]:
        """
        Парсит входную строку и возвращает список кортежей чисел.

        Args:
            input_str: Строка вида "(1,2)(3,4)"

        Returns:
            list[tuple[int]]: Результат разбора

        Raises:
            lark.exceptions.LarkError: При ошибках парсинга
        """
        return self._parser.parse(input_str)