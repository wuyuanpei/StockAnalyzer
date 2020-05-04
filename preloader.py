# 用来处理从网上复制黏贴的字符串的临时文件
with open('indices.txt') as file:
    content = file.read()
    dictionary = []
    while True:
        idx = content.find("(")
        if idx == -1:
            break
        dictionary.append((content[0:idx],content[idx+1:idx+7]))
        content = content[idx+8:]
    
    with open("stocks2.txt",'w') as fw:
        for item in dictionary:
            if item[1][0] == '6' or item[1][0] == '5' or item[1][0] == '9':
                fw.write("0"+item[1]+"/"+item[0]+'\n')
            else:
                fw.write("1"+item[1]+"/"+item[0]+'\n')


        
        
