# GTL-DEV

структура разработки 

GTL/                         # корневой пакет
├── elements/                # модули представления элементов
│   ├── integer/             # элементы группы Z и Z/n
│   │   └── element.py       # IntegerElement
│   ├── permutation/         # элементы перестановочных групп
│   │   └── element.py       # PermutationElement
│   ├── matrix/              # элементы матричных групп
│   │   └── element.py       # MatrixElement
│   └── word/                # элементы групп по презентации (слова)
│       └── element.py       # WordElement
├── groups/                  # модули групп
│   ├── finite/              # конечные группы
│   │   ├── base.py          # FiniteGroup
│   │   ├── cyclic.py        # CyclicGroup, ZmodGroup
│   │   ├── dihedral.py      # DihedralGroup
│   │   └── symmetric.py     # SymmetricGroup, AlternatingGroup
│   ├── infinite/            # бесконечные группы
│   │   └── integer.py       # IntegerGroup (Z)
│   ├── custom/              # группы по презентации (generators/relations)
│   │   └── presentation.py  # CustomPresentationGroup
│   ├── subgroup/            # подгруппа
│   │   └── subgroup.py      # Subgroup
│   ├── factor/              # фактор-группа
│   │   └── factor.py        # FactorGroup
│   └── products/            # произведения групп
│       ├── direct.py        # DirectProductGroup
│       └── semidirect.py    # SemidirectProductGroup
├── algebra/                 # алгебраические механизмы
│   ├── homomorphisms/       # гомоморфизмы
│   │   └── homomorphism.py  # GroupHomomorphism
│   ├── actions/             # действия групп на множествах
│   │   └── action.py        # GroupAction
│   ├── properties/          # проверка свойств группы
│   │   └── checker.py       # PropertyChecker
│   └── presentations/       # алгоритм упрощения слов по презентации
│       └── reducer.py       # PresentationReducer
├── utils/                   # утилиты
│   ├── visualization/       # визуализация (диаграммы Кэли и т.д.)
│   │   └── viz.py           # CayleyGraphBuilder, CayleyTableBuilder
│   └── tables/              # генерация таблиц умножения
│       └── table.py         # CayleyTableBuilder
└── tests/                   # тесты
    └── ...
