# Ассемблер и Интерпретатор для Учебной Виртуальной Машины

## Описание

В этом проекте реализованы ассемблер и интерпретатор для учебной виртуальной машины (УВМ), поддерживающие операции загрузки констант, работы с памятью и выполнения побитовых операций. Задание заключается в разработке системы команд и соответствующих инструментов для работы с виртуальной машиной.

В рамках задания реализована операция побитового "или" (OR) над вектором длиной 7 и числом 167. Результат операции записывается в новый вектор.

## Реализация

### Операция побитового "или"

Для выполнения операции побитового "или" используется следующая последовательность команд:

1. **Загрузка константы 167 в регистр R0:**
    ```asm
    LOAD_CONSTANT R0, #167
    MEMORY_WRITE [R1 + 0], R0
    ```

2. **Загрузка других констант:**
    ```asm
    LOAD_CONSTANT R0, #200
    LOAD_CONSTANT R1, #300
    LOAD_CONSTANT R2, #400
    LOAD_CONSTANT R3, #500
    LOAD_CONSTANT R4, #600
    LOAD_CONSTANT R5, #700
    LOAD_CONSTANT R6, #800
    ```

3. **Выполнение операции побитового "или" (OR) для каждого регистра:**
    ```asm
    OR R0, [0] | R0
    OR R1, [0] | R1
    OR R2, [0] | R2
    OR R3, [0] | R3
    OR R4, [0] | R4
    OR R5, [0] | R5
    OR R6, [0] | R6
    ```

4. **Запись результатов в память:**
    ```asm
    MEMORY_WRITE [R7 + 0], R0
    MEMORY_WRITE [R7 + 1], R1
    MEMORY_WRITE [R7 + 2], R2
    MEMORY_WRITE [R7 + 3], R3
    MEMORY_WRITE [R7 + 4], R4
    MEMORY_WRITE [R7 + 5], R5
    MEMORY_WRITE [R7 + 6], R6
    ```

Каждая команда преобразуется в бинарный формат и выполняется виртуальной машиной.

### Входные и выходные данные

- **Входные данные:** YAML-файл с командами на языке ассемблера.
- **Выходные данные:** YAML-файл, содержащий результат выполнения программы, включая состояние памяти после выполнения команд.

## Запуск

1. **Запуск ассемблера:**
   Ассемблер принимает три аргумента:
    - Путь к входному файлу с командами на языке ассемблера.
    - Путь к выходному файлу для записи скомпилированного бинарного кода.
    - Путь к лог-файлу для записи информации об обработанных инструкциях.

   Пример запуска:
    ```bash
    ./assembler ../files/input.asm ../files/output.bin ../files/log.yaml
    ```

2. **Запуск интерпретатора:**
   Интерпретатор принимает следующие аргументы:
    - Путь к бинарному файлу с закодированными командами.
    - Путь к выходному YAML-файлу для записи значений памяти.
    - Начальный и конечный индексы диапазона памяти, который нужно сохранить.

   Пример запуска:
    ```bash
    ./interpreter ../files/output.bin ../files/result.yaml 0 100
    ```

## Структура файлов

- **assembler.cpp** — точка входа в программу для ассемблера.
- **Assemble.cpp** — основной файл с логикой ассемблера, который выполняет парсинг и генерацию бинарных команд.
- **Assemble.h** — заголовочный файл, содержащий определения классов и функций для работы с командами.
- **interpreter.cpp** — файл для интерпретации бинарных команд и работы с памятью.
- **Interpret.h** — заголовочный файл для интерпретатора, содержащий определения функций и данных для выполнения команд.

## Формат YAML

- **Лог-файл (log.yaml):** Содержит информацию о каждой выполненной инструкции.
- **Результат (result.yaml):** Содержит значения памяти в формате YAML, с указанием адресов и значений.

Пример файла памяти:
```yaml
memory:
  - ID: 0
    VALUE: 239
  - ID: 1
    VALUE: 431
  - ID: 2
    VALUE: 439
  - ID: 3
    VALUE: 503
  - ID: 4
    VALUE: 767
  - ID: 5
    VALUE: 703
  - ID: 6
    VALUE: 935
  - ID: 7
```