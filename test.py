import random

def get_idnum(num_count,char_count):
    tmp_li = []
    for i in range(num_count):
        num = random.randint(0,9)
        tmp_li.append(str(num))
    for j in range(char_count):
        char = chr(random.randint(97,123))
        tmp_li.append(char)
    print(tmp_li)
    res = random.choices(tmp_li,k=num_count+char_count)
    return ''.join(res)

# print(get_idnum(2,3))

def get_random_id(num):
    num_li = [ str(i) for i in range(10) ]
    char_li = [ chr(i) for i in range(97,123)]
    # print(num_li)
    # print(char_li)
    num_li.extend(char_li)
    # print(num_li)
    res = random.choices(num_li,k=num)
    # print(''.join(res))
    return  ''.join(res)

print(get_random_id(10))