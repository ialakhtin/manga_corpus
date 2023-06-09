## Описание корпуса
Корпус состоит из 500 обзоров на мангу (японские комиксы) с сайта https://readmanga.live. Я выбрал данный сайт, поскольку мне хотелось посмотреть, как существующие методы обработки текстов справляются со сленговыми и малоупотребимыми в обычных текстах словами.
Для индексации использовалась библиотека stanza. Для каждого токена хранится его часть речи, начальная форма, морфологические особенности, зависимости от других токенов, а также некоторая вспомогательная информация
## Техническая информация
Для создания корпуса использовался скрипт `corpus_loader.py`

Для обработки корпуса использовался скрипт `process_corpus.py`

Для создания примеров (которые находтся в `examples/`) использовались функции из `examples.py`

При запуске `examples.py` с параметрами `file_name, line_count`, выведется морфологический разбор первых `line_count` примеров из корпуса, находящихся в файле `file_name`. 
## Примеры
В `examples/` лежат следующие файлы с примерами:
* `lex_h.txt` - примеры лексических омонимов
* `gram_h.txt` - примеры грамматических омонимов
* `morf_analysis.txt` - пример морфологического разбора
* `non_tree_examples.txt` - примеры недревесных структур
* `dependences.txt` - пример построения графа зависимостей
## Выводы
* Поиск грамматических омонимов получилось автоматизировать, в то время как для поиска лексических омонимов нужны другие методы. Например, модели машинного обучения (такие как word2vec)
* В морфологическом разборе присутствуют некоторые ошибки (в `morf_analysis.txt` 'боже' помечено как VERB), но я не увидел зависимость от наличия омонимов в предложении
* Вероятно, ошибки связаны с тем, что большинство авторов не придерживаются какой-либо определенной структуры предложения и употребляют много сленговых слов и выражений