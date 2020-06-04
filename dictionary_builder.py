import os

# Build dictionary of data
# selector:     选择合法的文件名 is_valid = lambda(filename)
#                   filename: (string) 文件名
#                   is_valid: (bool) 文件名是否合法
# editor:      编辑数据字典 item = lambda(item)
#                   item: (str:(int,int)) 数据字典每一项
# foldername:   数据目录
def build_dict(selector, editor, foldername="./data"):
    fileList = os.listdir(foldername)
    data_dict = {}
    for filename in fileList:
        if selector(filename):
            sid = filename[:7]
            syear = int(filename[8:12])
            if sid not in data_dict:
                data_dict[sid] = (syear, syear + 1)
            else:
                (prev_start, prev_end) = data_dict[sid]
                if syear >= prev_end:
                    data_dict[sid] = (prev_start, syear + 1)
                elif syear < prev_start:
                    data_dict[sid] = (syear, prev_end)
    return {k:editor(v) for k, v in data_dict.items()}

# 编辑器 删除2005年以前的数据 删除2020年的数据
def delete_b2005_2020(item):
    (start, end) = item
    start += 1
    if start < 2005:
        start = 2005
    if end > 2020:
        end = 2020
    return (start, end)

if __name__ == "__main__":
    data_dict = build_dict(lambda fn: fn[0:6] == "060000", delete_b2005_2020)
    print(data_dict)