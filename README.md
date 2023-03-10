<<<<<<< HEAD

#### git clone https://github.com/WISEPLAT/QuikPy
#### git clone https://github.com/WISEPLAT/BackTraderQuik

1) для настройки интеграции с Quik (отсюда можно взять последнюю версию
 https://github.com/finsight/QUIKSharp/):
2) в Quik -> Сервисы -> Lua скрипты -> нажимаем кнопку добавить и выбираем
 файл QuikSharp.lua из папки "lua"
3) после добавления файла убеждаемся что он выбран, и нажимаем !!!
 на стрелку около кнопки Запустить,
4) выбираем пункт "Запустить в Lua 5.3.5", после запуска в строке файла
 в поле "Память, КВ" начнут бежать цифры,
5) и теперь нажимаем кнопку "Закрыть" - интеграция сделана

=======
### Здесь выкладываю некие наработки по BackTrader, видосы по ним находятся здесь: 

### https://www.youtube.com/@wiseplat/streams


Почему нужно брать библиотеку BackTrader с WISEPLAT?
====================================================

Потому, что вы можете размещать ваши коммиты в моем репозитории - я применю их ASAP!

Чтобы установить backtrader из моего репозитория::

    pip install git+https://github.com/WISEPLAT/backtrader.git


По этой ссылке https://github.com/WISEPLAT/backtrader вы можете предложить свои коммиты, я применю их ASAP.

1-й коммит: Возможность изменить фон для отображаемых тегов значений для темной темы - чтобы получить темную тему)))
Когда вы используете темную тему, вам нужно изменить фон для отображаемых тегов значений.

2-й коммит: Исправление: В коллекциях последних версий Python.Iterable -> collections.abc.Iterable - для работы с Python 3.11+


Why use BackTrader repo from WISEPLAT?
======================================

Because, you can post your commits in my repository - I will apply them!

To install backtrader from my repository::

    pip install git+https://github.com/WISEPLAT/backtrader.git


By this link https://github.com/WISEPLAT/backtrader you can suggest your commits, I will apply them ASAP.
This suggestion is made here, because of no one here doesn't want to continue this cool project!

1st commit: Option to change background for plotted value tags for dark theme - to get dark theme)))
When you use dark theme you need to change background for plotted value tags.

2nd commit: Fix: In last Python versions collections.Iterable -> collections.abc.Iterable - to work with Python 3.11+
>>>>>>> origin/master
