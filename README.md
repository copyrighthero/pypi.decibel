# Decibel Project #

[README中文文档](README.zh-CN.md) | [SQLite](https://sqlite.org/) | [PEP-249 DB-API 2.0](https://www.python.org/dev/peps/pep-0249/) | [Python Docs: SQLite3](https://docs.python.org/3/library/sqlite3.html) | [MySQL Connectors](https://www.mysql.com/products/connector/)

## About the Decibel Library ##


## How to Use Decibel Library ##

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

# one can also execute a statement one by calling the object
res = mysql_dec('select * from test;')
res.lastrowid # 300, access the lastrowid
res.rowcount # -1, access query row count

# wrapper also worked on sqlite3 or any DB-API compliant instances
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

The Decibel module provides two classes: `Result` and `Decibel`. The `Result` class is a subclass of Python `list` and is used to hold the execution result returned by database cursor; the `Decibel` class is the actual wrapper that manages statements, executions and commits.

### Result Class ###

### Decibel Class ###

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
