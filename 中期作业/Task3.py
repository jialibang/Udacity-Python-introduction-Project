"""
下面的文件将会从csv文件中读取读取短信与电话记录，
你将在以后的课程中了解更多有关读取文件的知识。
"""
import csv

with open('texts.csv', 'r') as f:
    reader = csv.reader(f)
    texts = list(reader)

with open('calls.csv', 'r') as f:
    reader = csv.reader(f)
    calls = list(reader)


"""
任务3:
(080)是班加罗尔的固定电话区号。
固定电话号码包含括号，
所以班加罗尔地区的电话号码的格式为(080)xxxxxxx。

第一部分: 找出被班加罗尔地区的固定电话所拨打的所有电话的区号和移动前缀（代号）。
 - 固定电话以括号内的区号开始。区号的长度不定，但总是以 0 打头。
 - 移动电话没有括号，但数字中间添加了
   一个空格，以增加可读性。一个移动电话的移动前缀指的是他的前四个
   数字，并且以7,8或9开头。
 - 电话促销员的号码没有括号或空格 , 但以140开头。

输出信息:
"The numbers called by people in Bangalore have codes:"
 <list of codes>
代号不能重复，每行打印一条，按字典顺序排序后输出。

第二部分: 由班加罗尔固话打往班加罗尔的电话所占比例是多少？
换句话说，所有由（080）开头的号码拨出的通话中，
打往由（080）开头的号码所占的比例是多少？

输出信息:
"<percentage> percent of calls from fixed lines in Bangalore are calls
to other fixed lines in Bangalore."
注意：百分比应包含2位小数。
"""
calling_LFB = []  # calling_list_from_Bangalore
called_LFB = []  # called_list_from_Bangalore
for index in range(len(calls)):
    if calls[index][0][:5] == "(080)":
        calling_LFB.append(calls[index][0])
        called_LFB.append(calls[index][1])
target_dic = {}  # build dictionary whose key is being called number list from Bangalore and value is code.
for index in range(len(called_LFB)):
    if called_LFB[index][:2] == "(0":
        target_dic[called_LFB[index]] = called_LFB[index][1:called_LFB[index].find(")")]
    elif (called_LFB[index][0] == "7" or called_LFB[index][0] == "8" or called_LFB[index][0] == "9") and called_LFB[index][5] == " ":
        target_dic[called_LFB[index]] = called_LFB[index][:4]
    elif called_LFB[index][:3] == "140":
        target_dic[called_LFB[index]] = "140"
    target_DVL = sorted(set(target_dic.values()))  # bulid a ordered list of the value of target_dic
print("The numbers called by people in Bangalore has codes :")
for element in target_DVL:
    print(element)
target1_list = []  # build dictionary whose key is calling number list from Bangalore and value is being called number /
#  list from Bangalore
for index in range(len(calls)):
    if calls[index][0][:5] == "(080)" and calls[index][1][:5] == "(080)":
        target1_list.append(calls[index][0])
print("{} percent of calls from fixed lines in Bangalore are callsto other fixed lines in Bangalore.".format(round((100
* len(target1_list) / len(calling_LFB)), 2)))