---
title: `book`
---

**book name**

The Latin name of the present bible book.

This feature is present on objects of type
[`book`, `chapter`, and `verse`](otype.md).

Below is a list of all books with their number of chapters in the order as encoded in the BHSA dataset.

For book names in other languages: see [`book@ll`](book@ll.md)

book | #chapters
---|---
`Genesis`      | 50
`Exodus`       | 40
`Leviticus`    | 27
`Numeri`       | 36
`Deuteronomium`| 34
`Josua`        | 24
`Judices`      | 21
`Samuel_I`     | 31
`Samuel_II`    | 24
`Reges_I`      | 22
`Reges_II`     | 25
`Jesaia`       | 66
`Jeremia`      | 52
`Ezechiel`     | 48
`Hosea`        | 14
`Joel`         |  4
`Amos`         |  9
`Obadia`       |  1
`Jona`         |  4
`Micha`        |  7
`Nahum`        |  3
`Habakuk`      |  3
`Zephania`     |  3
`Haggai`       |  2
`Sacharia`     | 14
`Maleachi`     |  3
`Psalmi`       |150
`Iob`          | 42
`Proverbia`    | 31
`Ruth`         |  4
`Canticum`     |  8
`Ecclesiastes` | 12
`Threni`       |  5
`Esther`       | 10
`Daniel`       | 12
`Esra`         | 10
`Nehemia`      | 13
`Chronica_I`   | 29
`Chronica_II`  | 35  
  
  
  
### SHEBANQ/MQL Query Example

In the following query we use the node type `book` and the corresponding
feature `book` (`[book book`) in order to count all words (`[word FOCUS]`) that
appear in the Pentateuch (`IN (Genesis, Exodus, Leviticus, Numeri, Deuteronomium)`).

```
select all objects where  
[book book IN (Genesis, Exodus, Leviticus, Numeri, Deuteronomium)  
  [word FOCUS]  
]
```

See this query (with results) on [SHEBANQ]({{shebanq}}/hebrew/query?version=4b&id=1502).
Note that the data version used on SHEBANQ is **4b**, while this documentation
is for version **2016**.
