import json
from config_to_json import ConfigParser


def run_test(test_number, input_data, expected_output=None, expect_error=False):
    # Создаем экземпляр парсера
    config_parser = ConfigParser()

    try:
        # Парсим входные данные
        result = config_parser.parse(input_data)

        # Если ожидается ошибка, но её нет
        if expect_error:
            print(f'Test {test_number}: Failed. Expected an error, but parser succeeded.')
            return False

        # Если есть ожидаемый выход, сравниваем его с результатом
        if expected_output is not None:
            if expected_output == result:
                print(f'Test {test_number}: Passed.')
                return True
            else:
                print(f'Test {test_number}: Failed.')
                print('Expected output:')
                print(json.dumps(expected_output, indent=2))
                print('Actual output:')
                print(json.dumps(result, indent=2))
                return False
        else:
            print(f'Test {test_number}: No expected output provided.')
            return False

    except Exception as e:
        if expect_error:
            print(f'Test {test_number}: Passed (expected error).')
            return True
        else:
            print(f'Test {test_number}: Failed with exception.')
            print(f'Error: {e}')
            return False


def main():
    total_tests = 12
    passed_tests = 0

    # Тест 1: Объявление переменных с числами
    test1_input = '''
    var x := 10
    var y := 20
    var z := { x y + }
    '''
    test1_expected_output = [
        {"var": "x", "value": 10},
        {"var": "y", "value": 20},
        {"var": "z", "value": 30}
    ]
    if run_test(1, test1_input, test1_expected_output):
        passed_tests += 1

    # Тест 2: Массивы и сортировка
    test2_input = '''
    var arr := [3, 1, 4, 1, 5]
    var sorted_arr := { arr sort() }
    '''
    test2_expected_output = [
        {"var": "arr", "value": [3, 1, 4, 1, 5]},
        {"var": "sorted_arr", "value": [1, 1, 3, 4, 5]}
    ]
    if run_test(2, test2_input, test2_expected_output):
        passed_tests += 1

    # Тест 3: Индексирование массивов
    test3_input = '''
    var numbers := [10, 20, 30]
    var first_number := { numbers 0 index() }
    var last_number := { numbers 2 index() }
    '''
    test3_expected_output = [
        {"var": "numbers", "value": [10, 20, 30]},
        {"var": "first_number", "value": 10},
        {"var": "last_number", "value": 30}
    ]
    if run_test(3, test3_input, test3_expected_output):
        passed_tests += 1

    # Тест 4: Вложенные массивы
    test4_input = '''
    var matrix := [ [1, 2], [3, 4] ]
    var first_row := { matrix 0 index() }
    var first_element := { first_row 0 index() }
    '''
    test4_expected_output = [
        {"var": "matrix", "value": [[1, 2], [3, 4]]},
        {"var": "first_row", "value": [1, 2]},
        {"var": "first_element", "value": 1}
    ]
    if run_test(4, test4_input, test4_expected_output):
        passed_tests += 1

    # Тест 5: Математические операции
    test5_input = '''
    var a := 5
    var b := 3
    var sum := { a b + }
    var product := { a b * }
    var difference := { a b - }
    '''
    test5_expected_output = [
        {"var": "a", "value": 5},
        {"var": "b", "value": 3},
        {"var": "sum", "value": 8},
        {"var": "product", "value": 15},
        {"var": "difference", "value": 2}
    ]
    if run_test(5, test5_input, test5_expected_output):
        passed_tests += 1

    # Тест 6: Комментарии
    test6_input = '''
    # Это комментарий
    var x := 100
    (comment
    Многострочный
    комментарий
    )
    var y := { x 50 - } # Вычитаем 50
    '''
    test6_expected_output = [
        {"var": "x", "value": 100},
        {"var": "y", "value": 50}
    ]
    if run_test(6, test6_input, test6_expected_output):
        passed_tests += 1

    # Тест 7: Ошибки синтаксиса
    test7_input = '''
    var x := { 10 20 + + }
    '''
    if run_test(7, test7_input, expect_error=True):
        passed_tests += 1

    # Тест 8: Неопределённая переменная
    test8_input = '''
    var result := { undefined_var 10 + }
    '''
    if run_test(8, test8_input, expect_error=True):
        passed_tests += 1

    # Тест 9: Вложенные выражения
    test9_input = '''
    var x := 2
    var y := 3
    var result := { x y + x y + * }
    '''
    test9_expected_output = [
        {"var": "x", "value": 2},
        {"var": "y", "value": 3},
        {"var": "result", "value": 25}
    ]
    if run_test(9, test9_input, test9_expected_output):
        passed_tests += 1

    # Тест 10: Вложенные функции
    test10_input = '''
    var numbers := [5, 2, 8, 3]
    var sorted_numbers := { numbers sort() }
    var second_number := { sorted_numbers 1 index() }
    '''
    test10_expected_output = [
        {"var": "numbers", "value": [5, 2, 8, 3]},
        {"var": "sorted_numbers", "value": [2, 3, 5, 8]},
        {"var": "second_number", "value": 3}
    ]
    if run_test(10, test10_input, test10_expected_output):
        passed_tests += 1

    # Тест 11: Глубокая вложенность массивов
    test11_input = '''
    var nested_array := [ [ [1], [2] ], [ [3], [4] ] ]
    var value := { nested_array 1 index() 0 index() 0 index() }
    '''
    test11_expected_output = [
        {"var": "nested_array", "value": [[[1], [2]], [[3], [4]]]},
        {"var": "value", "value": 3}
    ]
    if run_test(11, test11_input, test11_expected_output):
        passed_tests += 1

    # Тест 12: Вложенные комментарии
    test12_input = '''
    (comment
    # var x := 10
    (comment var y := 20 )
    var z := 30 # Это значение должно быть обработано
    '''
    test12_expected_output = [
        {"var": "z", "value": 30}
    ]
    if run_test(12, test12_input, test12_expected_output):
        passed_tests += 1

    print(f'\nTotal tests passed: {passed_tests} out of {total_tests}')


if __name__ == '__main__':
    main()