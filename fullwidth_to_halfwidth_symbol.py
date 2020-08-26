def full_width_to_half_width(ustring):
    """全角转半角"""
    rstring = ""

    # 中文逗号就是英文逗号的全角，这里不希望把中文逗号改成英文符号，所以加了一个filter
    # 这几个都是中文标点
    filter = {65281, 65288, 65289, 65292, 65294, 65306, 65307, 65311}

    for uchar in ustring:
        inside_code = ord(uchar)
        if inside_code == 12288:  # 全角空格直接转换
            inside_code = 32
        elif inside_code not in filter and 65281 <= inside_code <= 65374:  # 全角字符（除空格）根据关系转化
            inside_code -= 65248
        rstring += chr(inside_code)
    return rstring