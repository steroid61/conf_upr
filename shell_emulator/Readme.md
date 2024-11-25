Разработать эмулятор для языка оболочки ОС. Необходимо сделать работу
эмулятора как можно более похожей на сеанс shell в UNIX-подобной ОС.
Эмулятор должен запускаться из реальной командной строки, а файл с
виртуальной файловой системой не нужно распаковывать у пользователя.
Эмулятор принимает образ виртуальной файловой системы в виде файла формата
tar. Эмулятор должен работать в режиме CLI.
Конфигурационный файл имеет формат xml и содержит:
• Имя пользователя для показа в приглашении к вводу.
• Путь к архиву виртуальной файловой системы.
• Путь к лог-файлу.
• Путь к стартовому скрипту.
Лог-файл имеет формат xml и содержит все действия во время последнего
сеанса работы с эмулятором. Для каждого действия указан пользователь.
Стартовый скрипт служит для начального выполнения заданного списка
команд из файла.
Необходимо поддержать в эмуляторе команды ls, cd и exit, а также
следующие команды:
1. cp.
2. date.
Все функции эмулятора должны быть покрыты тестами, а для каждой из
поддерживаемых команд необходимо написать 2 теста.

![Снимок экрана 2024-11-25 в 11.39.27.png](..%2F..%2F..%2F..%2F..%2F..%2Fvar%2Ffolders%2F0f%2F1ysfy_wn56q8ng942xvynty40000gn%2FT%2FTemporaryItems%2FNSIRD_screencaptureui_64IZQt%2F%D0%A1%D0%BD%D0%B8%D0%BC%D0%BE%D0%BA%20%D1%8D%D0%BA%D1%80%D0%B0%D0%BD%D0%B0%202024-11-25%20%D0%B2%2011.39.27.png)