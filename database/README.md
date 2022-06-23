# Описание

В базе Tarantool можно на языке программирования Lua писать скрипты для запросов и делать бизнес логику.

## Идеи и реализации
Основная идея решения заключается в построении персистентного дерева с категориями и товарами, реализовать это можно с помощью построения одной таблицы <b>items</b> со следующей структурой и индексами 

```mermaid
classDiagram

    Items <|-- IndexPrimary
    Items <|-- IndexDateTimestamp
    Items <|-- IndexParentId
    Items <|-- IndexCreated

    Items:+ string id -not NULL
    Items:+ string name -not NULL
    Items:+ unsigned item_type -not NULL
    Items:+ integer price -NULL
    Items:+ number data_timestamp -not NULL
    Items:+ string parent_id -NULL
    Items:+ boolean is_created -not NULL
    Items:+ number child_nums -not NULL
    Items:- num residuals -not NULL // Не добавлено

    class IndexPrimary{
        + primary, type 'tree', parts = 'id', unique= true
    }
    class IndexDateTimestamp{
        + primary, type 'tree', parts = 'date_timestamp', 'item_type', unique= false
    }
    class IndexParentId{
        + primary, type 'tree', parts = 'parent_id', 'is_created, unique= false
    }
    class IndexCreated{
        + primary, type 'tree', parts = 'is_created', unique= false
    }
```

Если делать 5 запрос ```/node/{id}/statistic```, понадобится вторая таблица, которая будет хранить информацию по изменениям элементов

Она будет выглядет следующим образом:

```mermaid
class Diagram


    Items:+ serial id -not NULL
    Items:+ number child_nums -not NULL
    Items:+ number residuals -not NULL 
    }

```
