# Decibel Project #

[README English](README.md) | [SQLite](https://sqlite.org/) | [PEP-249 DB-API 2.0](https://www.python.org/dev/peps/pep-0249/) | [Python Docs: SQLite3](https://docs.python.org/3/library/sqlite3.html) | [MySQL Connectors](https://www.mysql.com/products/connector/)

## About the Decibel Library ##

本库是一个对Python DB-API兼容的数据库管理器，或者更准确的说，是一个thin wrapper。除了数据库原有的方法外，本库提供了三个方法用于存储和执行SQL指令：`reg` 用来存储命名的SQL指令，`run`用来执行以存储的命名指令一次或多次，`__call__`用来执行未存储的指令。

这个wrapper类可以用来注册指令，将指令以`{'key': 'statment'}`的形式存入内存当中,用户便可以使用'key'来执行指令而不是使用超长的statement。这样的话，用户可以将所有可能用到的指令集中存放到其他地方，比如`config.ini`。所以后期对指令的更改并不会对程序的功能产生影响。[Utilize库](https://www.github.com/copyrighthero/Utilize)提供了程序设置(config/settings)集中管理的功能，并且使用了`Decibel`来提供数据库功能，敬请使用。

除了指令集中管理和执行功能外，本库还使用了`Result`类来管理执行结果。`result`类是`list`的子类，并且提供了两个常用属性: `lastrowid` 和 `rowcount`。

所有使用`Decibel`来执行的命令都会被自动commit到数据库中，所以用户不必担心数据丢失；但是需要注意的是所有的执行结果都会被`fetchall`方法来获取，所以本库并不适合用来执行会产生超长结果的指令。

所有的数据库实例方法都还可以被调用，所以用户可以使用本库高效率地完成工作。

## How to Use Decibel Library ##

在使用`pip install Decibel`安装完本库之后，import Decibel，将数据库实例作为第一个参数传入。第二个参数可选，将指令集以`dict` `{'key': 'statement'}`形式传入。

新的指令可以使用`reg`方法来注册，第一个参数是指令名称，第二个参数是具体的指令。可选的，用户可以提供任意长度的keyword argument(`**kwargs`)并会把它们当作`key - statement`对来存入内存当中。

用户可以调用`run`方法来执行一条已存的指令，第一个参数是指令的名称，第二个可选参数是用tuple/list包含的数据。 第三个参数是辨别本次执行是单一的还是多次的(`execute`和`executemany`)，如果为`True`，那么它就认为第二个参数是一个数据组(list/tuple of lists/tuples of values)，并对其中每一个元素执行一遍该命令。

用户可以直接调用实例来执行任何一条未存的指令(`__call__` method)，第二个和第三个参数和`run`方法相同。 

```python
from mysql.connector import connect as mysql
from sqlite3 import connect as sqlite
from decibel import Decibel

# create database instances as usual
mysql_db = mysql(host = 'localhost', port = 3306, database = 'test')
sqlite_db = sqlite(':memory:')

# initialize Decibel with database instance and statement repo
mysql_dec = Decibel(mysql_db, {
  'init' : 'create table test (id int(11) not null primary key auto_increment);'
})
# register statements for later use with key `insert` and `select_all`
mysql_dec.reg('insert', 'insert into test values (%s);', select_all = 'select * from test;')
# run a saved statement
mysql_dec.run('init') # [], empty results
# run the saved `insert` statement with values
res = mysql_dec.run('insert', (100, )) # insert a value with single parameter
res.lastrowid # 100, get the last row id
res.rowcount # 1, get the affected row count
# run the saved statement on multiple statements
res = mysql_dec.run('insert', [(200, ), (300, )], True) # [[], []]execute many/insert many
# since executed on many values, each item in the res list is a Result object
res[0].lastrowid  # 200, the first insert command's lastrowid
res[0].rowcount   # 1, the first insert command's rowcount
res[1].lastrowid  # 300, the second insert command's lastrowid
res[1].rowcount   # 1, the second insert command's rowcount
res = mysql_dec.run('select_all') # [(100, ), (200, ), (300, )] the results
res.lastrowid # 300, access the lastrowid
res.rowcount # -1, access query row count

# 用户可以使用__call__来执行一条未存的SQL指令
res = mysql_dec('select * from test;')
res.lastrowid # 300, access the lastrowid
res.rowcount # -1, access query row count

# 这个wrapper同样可以管理sqlite3或任何DB-API兼容的数据库实例
sqlite_dec = Decibel(sqlite_db)
sqlite_dec('create table test (id integer not null primary key autoincrement, co);')
sqlite_dec.reg(insert = 'insert into test values (?, ?);')
res = sqlite_dec.run('insert', (1, 'content'))
res.lastrowid # 1
res.rowcount # 1
res = sqlite_dec.run('insert', (2, 'content'))
res.lastrowid # 2
res.rowcount # 1
```

## Decibel Class API References ##

本库提供了两个类: `Result`和`Decibel`。`Result`是Python `list`的子类，被用于容纳指令处理后的`fetchall`结果；`Decibel`类则是被用于管理数据库，存入指令，执行指令，`commit`并且返回结果。

### Result Class ###

这个类是Python `list`的子类，并添加了 `lastrowid`和`rowcount`属性。它会对出纳入的cursor执行`fetchall`操作，所以请注意本库在处理会产生超级长结果的SQL指令时变得慢。

头: `Result(cursor)`

- `instance.lastrowid`属性: 会告诉用户最后一条插入指令的row id，对auto increment的表插入操作非常有帮助。
- `instance.rowcount`属性: 会告诉用户有多少条记录被本次执行的指令影响。

### Decibel Class ###

这个类是对DB-API兼容的数据库管理thin-wrapper。该类对数据库实例仅添加了三个方法： `reg`, `run` 和 `__call__`。所有的数据库实例的方法都还可以访问，所以用户并不会觉得会被该管理器限制太多。

头: `Decibel(database, statments = None)`

- `instance.reg(stid = None, stmt = None, **kwargs)`: 存入一个key： statement格式的SQL指令.
- `instance.run(stid, vaulues = None, many = False)`: 执行一条已存的SQL指令.
- `isntance(statement, values = None, many = False)`: 执行一条SQL指令.

## Licenses ##

This project is licensed under two permissive licenses, please chose one or both of the licenses to your like. Although not necessary, bug reports or feature improvements, attributes to the author(s), information on how this program is used are welcome and appreciated :-) Happy coding 

[BSD-2-Clause License]

Copyright 2018 Hansheng Zhao

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

[MIT License]

Copyright 2018 Hansheng Zhao

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
