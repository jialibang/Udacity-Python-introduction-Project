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
任务4:
电话公司希望辨认出可能正在用于进行电话推销的电话号码。
找出所有可能的电话推销员:
这样的电话总是向其他人拨出电话，
但从来不发短信、接收短信或是收到来电


请输出如下内容
"These numbers could be telemarketers: "
<list of numbers>
电话号码不能重复，每行打印一条，按字典顺序排序后输出。
"""
calling_SNS = set()  # calling num set which might be salesman
called_NS = set()  # called num set
texting_NS = set()  # texting num set
received_TNS = set()  # received text num set
for index in range(len(calls)):
    calling_SNS.add(calls[index][0])
    called_NS.add(calls[index][1])
for index in range(len(texts)):
    texting_NS.add(texts[index][0])
    received_TNS.add(texts[index][1])
calling_SNS -= called_NS  # Update the calling_SNS set, removing elements found in called_NS
calling_SNS -= texting_NS  # Update the calling_SNS set, removing elements found in texting_NS
calling_SNS -= received_TNS  # Update the calling_SNS set, removing elements found in received_TNS
calling_SOL = sorted(calling_SNS)  # ordered list of calling num which might be salesman
print("These numbers could be telemarketers: ")
for element in calling_SOL:
    print(element)
