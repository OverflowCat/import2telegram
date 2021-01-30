import os
import codecs
import json
import re
import time

generate_files = True
qq_txt_filename = "全部消息记录.txt"
qq_txt_path = qq_txt_filename
data = ""
your_qq_names = ["你的QQ用户名"]
your_telegram_phone_number = ""
  # Please write in the standard format like "+1 (114) 514-1919"

def waDateConverter(qqDateStr): #convert QQ date to WhatsAppish date 
    tup = time.strptime(qqDateStr.strip(), r"%Y-%m-%d %H:%M:%S")
    res = time.strftime(str(tup.tm_mon) +"/"+ str(tup.tm_mday) + r"/%y, %I:%M %p", tup) # 1/29/21, 09:19 AM
    res = res.replace(" 0", " ") # Remove "0" padding on hour 
    # print(res)
    return res
with codecs.open(qq_txt_path, "r+", encoding='utf-8') as h:
    data = h.read()
separator = "=" * (2 ** 6)
group_identifier = "消息分组:"
username_identifier = "消息对象:"
user_identifier = "消息分组:我的好友"
chats_identifier = f"\r\n{separator}\r\n消息分组:"
chats = data.split(chats_identifier)[1:]
print(f"共 {len(chats)} 个对话")
chatsoutput = []
for chat in chats:
    user = ""
    msgDateStr = ""
    msgs = []
    chatobj = {}
    lines = chat.split("\r\n")
    l = lines[2] # 第二行
    if re.match("^" + username_identifier, l):
        user = l.replace(username_identifier, "", 1)
        print(l)
        chatobj["name"] = user
    else:
        print(f"User {user} is invalid.")
        continue
    msg = ""
    for l in lines[5:]:
        isMsgDate = re.match(r"^20[0-9][0-9]-([0]?[1-9]|1[0-2])-[0-3][0-9] [0-2]?[0-9]:[0-6]?[0-9]:[0-6]?[0-9] ", l)
        if isMsgDate:
            msgDateStr = isMsgDate.group()
            # print(msgDateStr)
            # 是新的一行
            if msg.strip() != "": # 跳过空消息
                msgs.append(msginfo + msg.strip())
            username = l.replace(msgDateStr, "")
            if your_telegram_phone_number != "" and username in your_qq_names:
                username = your_telegram_phone_number
            msginfo = f"{waDateConverter(msgDateStr)} - {username}: "
            msg = ""
        elif l == "":
            msg = msg + "\n\n"
            continue
        else: #content
            msg = msg + l +"\n"
    chatobj["content"] = "\n".join(msgs)
    chatsoutput.append(chatobj)
    # print(chatobj)
print([x["name"] for x in chatsoutput])

def filterText(t):
    return t.replace("/", "_")

if generate_files:
    for chatobj in chatsoutput:
        with codecs.open(f"WhatsApp Chat with {filterText(chatobj['name'])}.txt", "w", encoding='utf-8') as writer:
            writer.write("1/29/17, 9:19 AM - Messages and calls are end-to-end encrypted. No one outside of this chat, not even WhatsApp, can read or listen to them. Tap to learn more." + chatobj["content"])

## debug
if False:
    print(waDateConverter("2020-02-18 0:17:10"))
    print(waDateConverter("2020-02-18 12:17:10"))