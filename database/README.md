# Описание

В базе Tarantool можно на языке программирования Lua писать скрипты для запросов и делать бизнес логику.

## Идеи и реализации
Основная идея решения заключается в построении персистентного дерева с категориями и товарами, реализовать это можно с помощью построения одной таблицы <b>items</b> со следующей структурой и индексами 

```mermaid
classDiagram
    class Items
    Items <|-- IndexPrimary
    Items <|-- IndexDateTimestamp
    Items <|-- IndexParentId
    Items <|-- IndexCreated

    Items : +string id
    Items : +string name
    Items : +unsigned item_type
    Items : +integer price
    Items : +number data_timestamp 
    Items : +string parent_id
    Items : +boolean is_created
    Items : +number child_nums
    Items : +num residuals

    class IndexPrimary{
        + id primary
    }
    class IndexDateTimestamp{
        + date_timestamp date_timestamp
    }
    class IndexParentId{
        + parent_id__is_created parent_id
    }
    class IndexCreated{
        + is_created created 
    }
```

Если делать 5 запрос ```/node/{id}/statistic```, понадобится вторая таблица, которая будет хранить информацию по изменениям элементов

Она будет выглядет следующим образом:

```mermaid
class Diagram
    class Items
    Items : +serial id -not NULL
    Items : +number child_nums -not NULL
    Items : +number residuals -not NULL 


```
