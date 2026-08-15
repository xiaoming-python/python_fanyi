import time
# import pyautogui as pa
import pyperclip as pc
import tkinter as tk
import threading as thr
import keyboard as kb
#from 练习1.翻译工具 import *
import sys
import importlib.util

file_path="D:/Creation/py练习/练习1/翻译工具.py"
module_name="my_demo"

spec=importlib.util.spec_from_file_location(module_name,file_path)
demo=importlib.util.module_from_spec(spec)
sys.modules[module_name]=demo
spec.loader.exec_module(demo)

class Qen:
    option1="en"
    option2="zh-CHS"

    @classmethod
    def click(cls):#用于切换翻译模式，0为英译中，1为中译英

        cls.option1,cls.option2=cls.option2,cls.option1

    def my_fangyi(self,copy):
        result = demo.translate(copy, from_lang=self.option1, to_lang=self.option2)
        return result

#创建窗口
root=tk.Tk()
root.geometry("600x500")
root.title("选取文字翻译")
root.attributes("-topmost",True)


def qen_but1():
    button1.place_forget()
    button2.place(relx=0.94,rely=0.45,anchor="center")
    Qen().click()

def qen_but2():
    button2.place_forget()
    button1.place(relx=0.94,rely=0.45,anchor="center")
    Qen().click()

#创建组件
text1=tk.Text(root,font=("微软雅黑",14),width=40,height=6)
text1.place(relx=0.5,rely=0.1,anchor="n")
text2=tk.Text(root,font=("微软雅黑",14),width=40,height=6)
text2.place(relx=0.5,rely=0.5,anchor="n")
label1=tk.Label(master=root,text="原文",font=("微软雅黑",15))
label1.place(relx=0.06,rely=0.2,anchor="n")
label2=tk.Label(master=root,text="译文",font=("微软雅黑",15))
label2.place(relx=0.06,rely=0.6,anchor="n")
button1=tk.Button(root,text="英\n↓\n中",font=("微软雅黑",15),command=qen_but1)
button1.place(relx=0.94,rely=0.45,anchor="center")
button2=tk.Button(root,text="中\n↓\n英",font=("微软雅黑",15),command=qen_but2)
button2.place(relx=0.94,rely=0.45,anchor="center")
button2.place_forget()

def mymain():
    #将用户选取的文字复制到粘贴板，并在text1中输出
    time.sleep(0.1)
    #pa.hotkey('ctrl','c')
    copy=pc.paste()

    text1.insert(tk.END,copy+"||")
    # 调用其他文件实现的翻译函数
    result=Qen().my_fangyi(copy)
    if result.get("errorCode") == "0":
        #print("翻译后的文本：", result["translation"][0])
        text2.insert(tk.END,result["translation"][0]+"||")
    else:
        #print("翻译失败，错误码：", result.get("errorCode"))
        text2.insert(tk.END,result.get("errorCode")+"||")

def original():
    thr1=thr.Thread(target=mymain)
    thr1.start()

kb.add_hotkey("ctrl+c",original)
root.mainloop()