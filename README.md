## features

This repository offers you some preprocessing operations for NLP tasks.

### 1. conversion from Complicated Chinese to Simple Chinese

the code below depends on two scripts. 

```python
from langconv import *

sentence = ""
sentence = Converter('zh-hans').convert(sentence)
```

### 2. conversion from full-width symbols to half-width symbols

According to the [Unicode Character Table](https://unicode-table.com/en/) and [Baidu Encyclopedia](https://baike.baidu.com/item/%E4%B8%AD%E6%96%87%E5%85%A8%E8%A7%92%E7%AC%A6%E5%8F%B7/7786521), fullwidth ASCII variants begins from 65281(U+FF01) to 65374(U+FF5E), and their counterparts in halfwidth form vary from 33(U+0021) to 126(U+007E), thus the gap is 65248 except for the space character, its fullwidth form and halfwidth form are 12288(U+3000) and 32(U+0020).

There is an excellent solution from cnblogs, but it ignores the fact that some chinese punctuations are the right fullwidth form of english characters, which may lead to unexpected modifications for these chinese punctuations.

```python
def full_width_to_half_width(ustring):
    rstring = ""

    filter = {65281, 65288, 65289, 65292, 65294, 65306, 65307, 65311}

    for uchar in ustring:
        inside_code = ord(uchar)
        if inside_code == 12288:
            inside_code = 32
        elif inside_code not in filter and 65281 <= inside_code <= 65374:
            inside_code -= 65248
        rstring += chr(inside_code)
    return rstring
```
