# ExcelTool
1. <a href="#功能介绍">功能介绍</a>
2. <a href="#安装教程">安装教程</a>
3. <a href="#数据库结构">数据库结构</a>
4. <a href="#源文件结构">源文件结构</a> 
5. <a href="#输入输出设置">输入输出设置</a> 
6. <a href="#运行操作指南">运行操作指南</a> 
7. <a href="#业务逻辑指南">业务逻辑指南</a> 

Notice：该项目是由python写成的excel数据处理工具，同时引入sqlite实现数据的读取/存储过程。此repo只上传Python代码，数据应存放于input文件夹和output文件夹中，现为空，请按照该文档中的<a href="#源文件结构">【文件结构和命名规则】</a>放置文件。此repo尚未上传数据库文件，请根据table schemma建立，存放于本地 c:/sqlite/db/xxxx.db

## 可能造成程序跑不了的问题
1. excel 文件命名/拓展名没按规则： 
    * newReg.xlsx
    * newAcc.xlsx 
    * simTrade.xlsx 
2. clientLogin 文件夹中的所有excel文档名字必须和其内部sheet名字名字相同, 而且文件格式都是xlsx
3. newAcc.xlsx 中只有一张sheet, 名字叫做 Sheet1

## 功能介绍
1. 生成sheet2: 输出（全量）新用户奇点当月（增量）登陆到SHEET2
* 基于input/newAcc.xlsx中记录的【当期】新开户用户，1）补充营销关系 2）通过对clientLoginEvent中登陆记录的计算，补充该用户对应的当前月的登陆天数，没有登入记录的记为0
* 营销关系补充规则： 
``` html 
    # checkMarketRelation 函数检查营销人员编号是不是填写，如果没有填写，用以下方法找【离职人员的营销关系】：
    # 1. 查看QDBM字段
    # 1）如果该字段是以'_'隔开的形式，那么被隔开的第3个字符串, 可能是空字符串/4位营销编码/8位营销编码，如果是一个8位的营销人员编码，则说明该人员因为离职才没有填写，营销人员编码直接写营销部代码.
    # * marketperid = 取该字段前4位编码
    # * marketdepid = 该字段前4位编码
    # * marketdepname = 营销营业部代码对应的营销部名称（在input/《营销人员和营业部列表》excel的branchlist表单中查找到对应的支行名称 //在db的marketdep表中查找）
    # 2）如果QDBM字段中得不到这个4位编码
    #       2.查看newacc表格中TJRSJ字段
    #       1）如果该字段是8位编码，那么说明这个员工已经离职，营销人员编码直接写写营业部代码： 
    #       * marketperid = 该字段的前4位编码
    #       * marketdepid = 该字段的前4位编码 
    #       * marketdepname = 营销营业部代码对应的营销部名称（在input/《营销人员和营业部列表》excel的branchlist表单中查找到对应的支行名称 //在db的marketdep表中查找）
    #       2）如果不是8位编码，什么都不做，marketperid, marketdepid, marketdepname 都空着
```
``` html
   还有一些用用户特殊处理，营销关系给写死的值
```

2. 生成sheet3: 输出新注册模拟交易天数到SHEET3 (全量）
* 基于input/newreg.xlsx中记录的【当期】新注册用户，根据input/simTrade.xlsx中的记录，关联到他对应的模拟交易天数，如果没有交易天数，空格

3 生成ACC+VAL：输出开户用户转换价值红包微信
* 营销人员离职对应的用户: 根据sheet2中修改了哪些来确定

## 安装教程
### 安装SQLite
本地数据库选用轻量级别SQL数据库引擎‘SQLite’。

##### 下载安装SQLite
1. 下载官网 https://www.sqlite.org/index.html （根据操作系统下载）
2. 安装SQLite: C盘中创建sqlite文件夹，把解压缩出的运行文件放入该文件夹

##### 下载安装SQLite可视化工具(选择）
1. 下载官网 https://sqlitestudio.pl/index.rvt
2. 解压缩 C:\sqlite\gui\

##### 数据库.db文件存放
1. 下载 .db文件
2. 放入c:\sqlite\db中

##### SQLite数据库命令行操作
* SQlite包括一个名为 sqlite3 的命令行工具能够让用户使用SQL命令和数据库交互

##### 开启sqlite
```bash
   c:\sqlite>
   c:\sqlite>sqlite3 db/xxx.db
```
看到 sqlite> 显示

##### 基本命令
```bash
  1. sqlite> .tables
  2. sqlite> .open c:\sqlite\chinook.db
  3. sqlite> .exit
  4. sqlite> .schema albums
  5. sqlite>：.table [tableName]
```
----
### 安装Python 
  1. 本项目使用python 3.7.4,请按教程安装

##### 使用python安装拓展包pandas，xlrd，xlwt 
* pandas 用于数据结构封装
* xlrd 用于excel读取
* xrwt 用于excel写入

```python
  py -m pip install pandas
  py -m pip install xlrd
  py -m pip install xlwt 
```
----
### 安装vim(选择)
----
## 数据库结构
#### newreg 
* 该表记录【当期】（input/newReg.xlsx 中记录的）新注册的用户
* 由input/newreg.xlsx 表格导入数据到数据库数据库库时，会删除数据库原有的数据
* 【TODO】: 新添historyreg表格，每一次导入新的注册用户的时候，把遗留在数据库中的原有数据导入到historyreg中}

| 名称   | 数据类型  |  默认值 | 备注 |
|  ----  | ----  |  ----  |  ----  |
| usrmobile  | INTEGER | NULL  | 新注册用户的手机号  |
| marketcode | INTEGER | NULL  | 营销人员编号 |
| createtime | TEXT | NULL  | 新用户注册的时间  |
| departmentid  | INTEGER | NULL | 营销营业部代码 |
| refid | | |推荐人的id|
| refnickname | | |推荐人的昵称|
| refrealname | | |推荐人的真实姓名|
| refphone| | |推荐人的手机|
| pageindex | | | ???| 

* usrmobile没有设置成primary key考虑到表格可能出现重复

#### account
* account里存放的是来自newaccount，经过处理过后，不重复的记录的累加总和。
* 初始化：input/datatoolsheet6.xlsx 导入

* 何时更新：
1. 当newaccount的变化直接出发account的变化:
   * 跑sheet2的程序把newaccount的数据全部删除的时候
   * 跑sheet2将处理过的新用户数据写入newaccount时
   * 因为sheet6之后都是基于account里的数据，而sheet2的变化影响account, 所以sheet2和sheet6的变化是同步的

* 如果数据更新：
   * 把销户用户写入【销户人员表】
   * 把用户关联的营销人员（若离职）写入【离职人员表】
   * 【todo】被做出任何修改的那条用户账户的记录，都可以写在【modifiedaccount中】

| 名称   | 数据类型  |  默认值 | 备注 |
|  ----  | ----  |  ----  |  ----  |
| khcode  | INTEGER | NULL  | 开户的交易号  |
| khdate | TEXT | NULL  | 开户日期(NOT NULL) |
| usrnameshort | TEXT | NULL  | 用户简称(NOT NULL)   |
| usrname  | TEXT | NULL | 用户名称(NOT NULL)  |
| khusrmobile  | INTEGER | NULL  | 用户使用的开户手机号(NOT NULL)   |
| lddepid | INTEGER | NULL  | 落地营业部代码(NOT NULL)  |
| lddepname | TEXT | NULL  | 落地营业部名称(NOT NULL)   |
| marketperid | INTEGER | NULL | 营销人员编码 |
| marketpername  | TEXT | NULL | 营销人员名称 |
| marketpertype  | TEXT | NULL  | 营销人员类别  |
| marketpermobile | INTEGER | NULL  | 营销人员手机号 |
| marketdepname | TEXT | NULL  | 营销营业部名称 |
| marketdepid  | INTEGER | NULL | 营销营业部代码 |
| hrid  | INTEGER | NULL  | hr编号 |
| tjrsj | TEXT | NULL  |  |
| qdbm | TEXT | NULL  |  |

* khcode没有设置成primary key考虑到表格可能出现重复


#### newaccount
* 该表记录【当期】(input/newAcc.xlsx 中记录的）新开户用户
* 由input/newreg.xlsx 表格导入数据到数据库数据库库时，会删除数据库原有的数据
* 【TODO】: 新添historyaccount表格，每一次导入新的注册用户的时候，把遗留在数据库中的原有数据导入到historyaccount中}

| 名称   | 数据类型  |  默认值 | 备注 |
|  ----  | ----  |  ----  |  ----  |
| khcode  | INTEGER | NULL  | 开户的交易号  |
| khdate | TEXT | NULL  | 开户日期(NOT NULL) |
| usrnameshort | TEXT | NULL  | 用户简称(NOT NULL)   |
| usrname  | TEXT | NULL | 用户名称(NOT NULL)  |
| khusrmobile  | INTEGER | NULL  | 用户使用的开户手机号(NOT NULL)   |
| lddepid | INTEGER | NULL  | 落地营业部代码(NOT NULL)  |
| lddepname | TEXT | NULL  | 落地营业部名称(NOT NULL)   |
| marketperid | INTEGER | NULL | 营销人员编码 |
| marketpername  | TEXT | NULL | 营销人员名称 |
| marketpertype  | TEXT | NULL  | 营销人员类别  |
| marketpermobile | INTEGER | NULL  | 营销人员手机号 |
| marketdepname | TEXT | NULL  | 营销营业部名称 |
| marketdepid  | INTEGER | NULL | 营销营业部代码 |
| hrid  | INTEGER | NULL  | hr编号 |
| tjrsj | TEXT | NULL  |  |
| qdbm | TEXT | NULL  |  |

* khcode没有设置成primary key考虑到表格可能出现重复

#### leftaccount
* 该表记录【当期】基于newacc和存在于sheet6里的老用户的比较得出的注销用户
* 暂时没有表格能够直接导入
* 在比较sheet2和sheet6,也就是所谓新用户和老用户的过程中，会出现存在于sheet2却不存在于sheet6的用户，暂且把这些用户看作是销户用户
* 每次更新都是sheet2(newaccount)的更新引发的sheet6（oldaccount)的更新，比较出来的不同的用户，进入到leftaccount中，所以leftaccount每次被更新的时候不能删除原来的值，而是把新的销户用户加进去。

| 名称   | 数据类型  |  默认值 | 备注 |
|  ----  | ----  |  ----  |  ----  |
| khcode  | INTEGER | NULL  | 开户的交易号  |
| khdate | TEXT | NULL  | 开户日期(NOT NULL) |
| usrnameshort | TEXT | NULL  | 用户简称(NOT NULL)   |
| usrname  | TEXT | NULL | 用户名称(NOT NULL)  |
| khusrmobile  | INTEGER | NULL  | 用户使用的开户手机号(NOT NULL)   |
| lddepid | INTEGER | NULL  | 落地营业部代码(NOT NULL)  |
| lddepname | TEXT | NULL  | 落地营业部名称(NOT NULL)   |
| marketperid | INTEGER | NULL | 营销人员编码 |
| marketpername  | TEXT | NULL | 营销人员名称 |
| marketpertype  | TEXT | NULL  | 营销人员类别  |
| marketpermobile | INTEGER | NULL  | 营销人员手机号 |
| marketdepname | TEXT | NULL  | 营销营业部名称 |
| marketdepid  | INTEGER | NULL | 营销营业部代码 |
| hrid  | INTEGER | NULL  | hr编号 |
| tjrsj | TEXT | NULL  |  |
| qdbm | TEXT | NULL  |  |

* khcode没有设置成primary key考虑到表格可能出现重复

#### marketper
* 记录营销人员信息
* 由input/营销人员和营业部列表.xlsx/SQL Results 表单导入数据到数据库数据库库时，会删除数据库原有的数据

| 名称   | 数据类型  |  默认值 | 备注 |
|  ----  | ----  |  ----  |  ----  |
| marketcode  | INTEGER | NULL  | 营销人员编号(PRIMARY KEY(|
| markettype | TEXT | NULL  | 营销人员类别(NOT NULL) |
| marketname | TEXT | NULL  | 营销人员名称(NOT NULL)   |
| marketmobile  | INTEGER | NULL | 营销人员手机号(NOT NULL)  |

#### leftmarketper
* 记录已经离职的营销人员信息
* 暂时没有表格供导入
* 离职人员表格
1. 在输出sheet2，基于newaccount处理的时候，会发现离职的人员。如果发现，把它加入到离职人员表格内
2. 【todo】如果离职人员变动其实会影响account和marketper里面的记录
3. 离职人员应该和营销人员字段相等

| 名称   | 数据类型  |  默认值 | 备注 |
|  ----  | ----  |  ----  |  ----  |
| marketcode  | INTEGER | NULL  | 营销人员编号(PRIMARY KEY(|
| markettype | TEXT | NULL  | 营销人员类别(NOT NULL) |
| marketname | TEXT | NULL  | 营销人员名称(NOT NULL)   |
| marketmobile  | INTEGER | NULL | 营销人员手机号(NOT NULL)  |

#### marketdep 
* 记录营销营业部信息
* 由input/营销人员和营业部列表xlsx/branchlist 表单导入数据到数据库数据库库时，会删除数据库原有的数据

| 名称   | 数据类型  |  默认值 | 备注 |
|  ----  | ----  |  ----  |  ----  |
| depid  | INTEGER | NULL  | 营销营业部编号  |
| depname | TEXT | NULL  | 营销营业部名称(NOT NULL) |

#### simtrade 
* 该表记录【当期】(input/simTrade.xlsx 中记录的）模拟交易记录
* 由input/simTrade.xlsx 表格导入数据到数据库数据库库时，会删除数据库原有的数据
* 【TODO】: 新添historysimtrade表格，每一次导入新的注册用户的时候，把遗留在数据库中的原有数据导入到historysimtrade中

| 名称   | 数据类型  |  默认值 | 备注 |
|  ----  | ----  |  ----  |  ----  |
| usrmobile  | INT | NULL | 开户的交易号(PRIMARY KEY)|
| createtime | INT | NULL | 开户日期(NOT NULL)|
| tradedays  | INT | NULL  | 用户简称(NOT NULL)|

#### clientloginevent 
* 该表记录【当期】(input/clientLogin/xxxxxx.xlsx 中记录的）用户登陆
* 由input/clientLogin/xxxxxx.xlsx 所有的表格导入数据到数据库数据库库时，会删除数据库原有的数据
* 【TODO】: 新添historyaccount表格，每一次导入新的注册用户的时候，把遗留在数据库中的原有数据导入到historyaccount中

| 名称   | 数据类型  |  默认值 | 备注 |
|  ----  | ----  |  ----  |  ----  |
| eventno  | INTEGER | NULL  |登入事件编号（自增）（仅代表在该表中的序号） (PRIMARY KEY)|
| clientid | TEXT | NULL  | 登入用户的usrid |
| logindate | TEXT | NULL  | 登入的日期(NOT NULL)|
| logintime | TIME | NULL |  登入的时间(NOT NULL)  |
| eventtype | TEXT | NULL  | 事件类型(NOT NULL)   |
| eventmsg | TEXT | NULL  | 事件信息(NOT NULL)  |

#### usrDayInCapital
* 该表记录【当期】（input/capital/capital.xlsx/SQL Results 中记录的）用户入金记录
* 由input/capital/capital.xlsx/SQL Results 导入数据到数据库时，删除数据库原有数据
* 【TODO】：新添historyusrdayincapital表格，每一次导入新的注册用户的时候，把遗留在数据库的苏话剧导入到historyusrdayincapital中

| 名称   | 数据类型  |  默认值 | 备注 |
|  ----  | ----  |  ----  |  ----  |
| date  | TEXT | NULL| 用户入金的日期 |
| khcode | TEXT | NULL  | 用户开户后的交易号 |
| zzc | DOUBLE | NULL | 用户某一天的转入金额| 

#### clienttradeevent
* 该表记录【当期】（input/trade/tradelog.xlsx/SQL Results 中记录的）用户交易记录
* 由 input/trade/tradelog.xlsx/SQL Results 导入数据到数据库时，删除数据库原有数据
* 【TODO】：新添historyclienttradeevent表格，每一次导入新的注册用户的时候，把遗留在数据库的苏话剧导入到historyclienttradeevent中

| 名称   | 数据类型  |  默认值 | 备注 |
|  ----  | ----  |  ----  |  ----  |
| eventno  | INTEGER | NULL  |交易事件编号（自增）（仅代表在该表中的序号） (PRIMARY KEY)|
| khcode | TEXT | NULL  | 用户开户后的交易号 |
| khqz | TEXT | NULL | | 
| wtfs | TEXT | NULL | | 
| tradedate | TEXT | NULL | | 
| wtlb | TEXT | NULL | |
| zqdm | TEXT | NULL | | 
| zqmc | TEXT | NULL | | 
| wtsl | TEXT | NULL | | 
| cjsl | TEXT | NULL | | 
| wtgy | TEXT | NULL | | 
| sbxw | TEXT | NULL | | 
| czzd | TEXT | NULL | | 

#### usrdayatrade 
* 该表记录【当期】（input/atrade.xlsx/Sheet1 中记录的）用户日跟投次数
* 由 input/atrade.xlsx/Sheet1 导入数据到数据库时，删除数据库原有数据
* 【TODO】：新添historyusrdayatrade表格，每一次导入新的用户日跟投次数的时候，把遗留在数据库用户日跟投次数导入到historyusrdayatrade中

| 名称   | 数据类型  |  默认值 | 备注 |
|  ----  | ----  |  ----  |  ----  |
| atradedate | TEXT | NULL  |用户跟投进行的日期|
| khcode | INTEGER | NULL |客户号| 
| atradenumber | INTEGER | NULL | 用户在次日进行跟投的数量（次数） | 




----
## 源文件结构
* 文件夹intput 
   * clientLogin文件夹
   * capital文件夹
   * trade文件夹
   * aTrade.xlsx
   * ?(newAcc + val + wechat) 
   * newAcc.xlsx
   * newReg.xlsx 
   * simTrade.xlsx 
   * 营销人员和营销部列表.xlsx 
   
* 文件夹output 
   * sheet2
   * sheet3 
   
* 文件夹input 
   * 存放input一样的东西，但是出去当前星期的以前的文件的存档

* 文件夹ExcelToSQLite: 
   * exceldoc.py //excel 文档的一些辅助函数
   * importCapitalToSQLite.py 【把input/capital/capital.xlsx的数据导入到数据库，生成usrDayInCapital表格数据】
   * importClientLoginFolderToSQLite.py 【把input/clientLogin/xxxxxx.xlsx 所有的表格导入数据库，生成clientloginevent表格数据】
   * importMarketDepToSQLite.py 【把input/营销人员和营业部列表xlsx/branchlist 表单导入数据库，生成marketdep表格数据】
   * importMarketPerToSQLite.py 【把input/营销人员和营业部列表.xlsx/SQL Results 表单导入数据库，生成marketper表格数据】
   * importNewAccountToSQLite.py 【把input/newAcc.xlsx 表格导入数据库，生成newaccount表格数据】
   * importNewregToSQLite.py 【把input/newReg.xlsx 表格导入数据到数据库数据库库时，生成newreg表格数据】
   * importSimTradeToSQLite.py 【把input/simTrade.xlsx 表格导入数据到数据库数据库库时，生成simtrade表格数据】
   * importTradeLogToSQLite.py 【把input/trade/tradelog.xlsx 表格导入数据库，生成clienttradeevent表格数据】
   * importATradeToSQLite.py 【把input/aTrade.xlsx 表格导入数据库，生成usrdayatrade表格数据】  
   * import模板.py 
 
 * 文件夹SQLiteToExcel 
   * clientLoginEventUtility.py 【统计用户某月登入天数】
   * getSheet2FromSQLite.py 【生成sheet2到output文件夹】
   * getSheet3FromSQLite.py 【生成sheet3到output文件夹】
   * getSheetFromSQLite模板.py 

----
## 运行操作指南
   【TODO】把下面手动跑程序步骤写成程序
   * 生成sheet2: 输出（全量）新用户奇点当月（增量）登陆到SHEET2
      1. 在input/newAcc.xlsx 中放入【当期】新开户用户, 在input/clientLogin/中放入【当月】的登录记录
      2. 运行importNewAccountToSQLite.py 
      3. 运行importClientLoginFolderToSQLite.py，确保所有的login表格都是xlsx格式，里面的sheet名和外部文档名相同。
      4. 把【当期】新添的clientlogin放在hislogin中，运行importHisClientLoginEventToSQLite.py
      5. 保证数据库中的marketdep表格有数据，没有的话运行importMarketDepToSQLite.py 
      6. 运行getSheet2FromSQLite.py
      
   * 生成sheet3: 输出新注册模拟交易天数到SHEET3 (全量）
      1. 在input/newReg.xlsx 中放入【当期】新注册用户; 在input/simTrade.xlsx中放入模拟交易天数表
      2. 运行importMarketDepToSQLite.py （保证更新）
      3. 运行importMarketPerToSQLite.pytidrr （保证更新）
      4. 运行importNewregToSQLite.py （核对数量）
      5. 运行importSimTradeToSQLite.py (核对数量)(保证simTrade文档位xlsx格式，保证里面的sheet叫做simTrade)  
      6. 运行getSheet3FromSQLite.py 
      
  * 生成ACC + VAL，输出新开户用户转化
  1. prerequiste: sheet2 
  2. newACC + clientlogin + capital + aTtrade + ACCVALPrevious.xlsx/ACC+VAL      
  3. 跑完以后找出ACCVAL中的注销人员, 这些注销人员应当能在上一次跑出来的ACCVALPrevious里还有记录。
   对比后，如果登录/入金/跟投/交易少了，可能是因为为注销人员的记录在数据库里删除了,还是保留ACCVALPrevious的值。
   如果登录/入金/跟投/交易的记录多了，可能是销户的那个星期，也就是用户还存在的最后一个星期还进行了某些行为，
   而且虽然销户了但是记录还没来得及删除，保留新的ACCVAL跑出来的结果。
----
## 业务逻辑指南
* [营销关系补充](./notes/营销关系补充.md) 


