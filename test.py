'''
import tkinter   #from…import *语句与import区别在于：. import 导入模块，每次使用模块中的函数都要是定是哪个模块。
                   # from…import * 导入模块，每次使用模块中的函数，直接使用函数就可以了；注因为已经知道该函数是那个模块中的了。.

tk=tkinter.Tk()

# 创建主窗口
#tk = tkinter.Tk()
# 设置窗口大小和位置
tk.geometry('300x210+500+200')
# 不允许改变窗口大小
tk.resizable(False, False)
# 设置窗口标题
tk.title('计算器')

# mainloop 是一个主循环，就是窗口显示出来等待各种消息，比如鼠标 键盘等操作的。
# 自动刷新字符串变量，可用 set 和 get 方法进行传值和取值
contentVar = tkinter.StringVar(tk, '')
# 创建单行文本框
contentEntry = tkinter.Entry(tk, textvariable=contentVar)
# 设置文本框为只读
contentEntry['state'] = 'readonly'
# 设置文本框坐标及宽高
contentEntry.place(x=20, y=10, width=260, height=30)
# 按钮显示内容
bvalue = ['C', '+', '-', '//', '2', '0', '1', '√', '3', '4', '5', '*', '6', '7', '8', '.', '9', '/', '**', '=']
index = 0
# 将按钮进行 5x4 放置
for row in range(5):
    for col in range(4):
        d = bvalue[index]
        index += 1
        btnDigit = tkinter.Button(tk, text=d, command=lambda x=d: onclick(x))
        btnDigit.place(x=20 + col * 70, y=50 + row * 30, width=50, height=20)
        # 点击事件
def onclick(btn):
    # 运算符
    operation = ('+', '-', '*', '/', '**', '//')
    # 获取文本框中的内容
    content = contentVar.get()
    # 如果已有内容是以小数点开头的，在前面加 0
    if content.startswith('.'):
        content = '0' + content  # 字符串可以直接用+来增加字符
    # 根据不同的按钮作出不同的反应
    if btn in '0123456789':
        # 按下 0-9 在 content 中追加
        content += btn
    elif btn == '.':
        # 将 content 从 +-*/ 这些字符的地方分割开来
        lastPart = re.split(r'\+|-|\*|/', content)[-1]
        if '.' in lastPart:
            # 信息提示对话框
            tkinter.messagebox.showerror('错误', '重复出现的小数点')
            return
        else:
            content += btn
    elif btn == 'C':
        # 清除文本框
        content = ''
    elif btn == '=':
        try:
            # 对输入的表达式求值
            content = str(eval(content))
        except:
            tkinter.messagebox.showerror('错误', '表达式有误')
            return
    elif btn in operation:
        if content.endswith(operation):
            tkinter.messagebox.showerror('错误', '不允许存在连续运算符')
            return
        content += btn
    elif btn == '√':
        # 从 . 处分割存入 n，n 是一个列表
        n = content.split('.')
        # 如果列表中所有的都是数字，就是为了检查表达式是不是正确的
        if all(map(lambda x: x.isdigit(), n)):
            content = eval(content) ** 0.5
        else:
            tkinter.messagebox.showerror('错误', '表达式错误')
            return
    # 将结果显示到文本框中
    
    contentVar.set(content)
#tk.messagebox.showerror('错误', '不允许存在连续运算符')
tk.mainloop() 
'''
#  *_* coding:utf8 *_*
import tkinter
from functools import partial

# 按钮输入调用
def get_input(entry, argu):
    # 从entry窗口展示中获取输入的内容
    input_data = entry.get()

    # 合法运算符 : + - * / -- ** // +-
    # ------------ 输入合法性判断的优化 ------------
    # 最后一个字符不是纯数字(已经有算数符号),原窗口值不为空,且输入值为运算符
    # if not input_data[-1:].isdecimal() and (not argu.isdecimal()):
    #     if input_data[-2:] in ["--", "**", "//", "+-"]:
    #         return
    #     if (input_data[-1:] + argu) not in ["--", "**", "//", "+-"]:
    #         return
    # ------------------------------------------------

    # 出现连续+，则第二个+为无效输入，不做任何处理
    if (input_data[-1:] == '+') and (argu == '+'):
        return
    # 出现连续+--，则第三个-为无效输入，不做任何处理
    if (input_data[-2:] == '+-') and (argu == '-'):
        return
    # 窗口已经有--后面字符不能为+或-
    if (input_data[-2:] == '--') and (argu in ['-', '+']):
        return
    # 窗口已经有 ** 后面字符不能为 * 或 /
    if (input_data[-2:] == '**') and (argu in ['*', '/']):
        return

    # 输入合法将字符插入到entry窗口结尾
    entry.insert("end", argu)

# 退格(撤销输入)
def backspace(entry):
    input_len = len(entry.get())
    # 删除entry窗口中最后的字符
    entry.delete(input_len - 1)

# 清空entry内容(清空窗口)
def clear(entry):
    entry.delete(0, "end")

# 计算
def calc(entry):
    input_data = entry.get()
    # 计算前判断输入内容是否为空;首字符不能为*/;*/不能连续出现3次;
    if not input_data:
        return

    clear(entry)

    # 异常捕获，在进行数据运算时如果出现异常进行相应处理
    # noinspection PyBroadException
    try:
        # eval() 函数用来执行一个字符串表达式，并返回表达式的值；并将执行结果转换为字符串
        output_data = str(eval(input_data))
    except Exception:
        # 将提示信息输出到窗口
        entry.insert("end", "Calculation error")
    else:
        # 将计算结果显示在窗口中
        if len(output_data) > 20:
            entry.insert("end", "Value overflow")
        else:
            entry.insert("end", output_data)


if __name__ == '__main__':

    root = tkinter.Tk()
    root.title("Calculator")

    # 框体大小可调性，分别表示x,y方向的可变性；
    root.resizable(0, 0)

    button_bg = 'orange'
    math_sign_bg = 'DarkTurquoise'
    cal_output_bg = 'YellowGreen'
    button_active_bg = 'gray'

    # justify:显示多行文本的时候, 设置不同行之间的对齐方式，可选项包括LEFT, RIGHT, CENTER
    # 文本从窗口左方开始显示，默认可以显示20个字符
    # row：entry组件在网格中的横向位置
    # column：entry组件在网格中的纵向位置
    # columnspan:正常情况下,一个插件只占一个单元;可通过columnspan来合并一行中的多个相邻单元
    entry = tkinter.Entry(root, justify="right", font=1)
    entry.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

    def place_button(text, func, func_params, bg=button_bg, **place_params):
        # 偏函数partial，可以理解为定义了一个模板，后续的按钮在模板基础上进行修改或添加特性
        # activebackground：按钮按下后显示颜place_params色
        my_button = partial(tkinter.Button, root, bg=button_bg, padx=10, pady=3, activebackground=button_active_bg)
        button = my_button(text=text, bg=bg, command=lambda: func(*func_params))
        button.grid(**place_params)

    # 文本输入类按钮
    place_button('7', get_input, (entry, '7'), row=1, column=0, ipadx=5, pady=5)
    place_button('8', get_input, (entry, '8'), row=1, column=1, ipadx=5, pady=5)
    place_button('9', get_input, (entry, '9'), row=1, column=2, ipadx=5, pady=5)
    place_button('4', get_input, (entry, '4'), row=2, column=0, ipadx=5, pady=5)
    place_button('5', get_input, (entry, '5'), row=2, column=1, ipadx=5, pady=5)
    place_button('6', get_input, (entry, '6'), row=2, column=2, ipadx=5, pady=5)
    place_button('1', get_input, (entry, '1'), row=3, column=0, ipadx=5, pady=5)
    place_button('2', get_input, (entry, '2'), row=3, column=1, ipadx=5, pady=5)
    place_button('3', get_input, (entry, '3'), row=3, column=2, ipadx=5, pady=5)
    place_button('0', get_input, (entry, '0'), row=4, column=0, padx=8, pady=5,
                 columnspan=2, sticky=tkinter.E + tkinter.W + tkinter.N + tkinter.S)
    place_button('.', get_input, (entry, '.'), row=4, column=2, ipadx=7, padx=5, pady=5)

    # 运算输入类按钮(只是背景色不同)
    # 字符大小('+','-'宽度不一样,使用ipadx进行修正)
    place_button('+', get_input, (entry, '+'), bg=math_sign_bg, row=1, column=3, ipadx=5, pady=5)
    place_button('-', get_input, (entry, '-'), bg=math_sign_bg, row=2, column=3, ipadx=5, pady=5)
    place_button('*', get_input, (entry, '*'), bg=math_sign_bg, row=3, column=3, ipadx=5, pady=5)
    place_button('/', get_input, (entry, '/'), bg=math_sign_bg, row=4, column=3, ipadx=5, pady=5)

    # 功能输入类按钮(背景色、触发功能不同)
    place_button('<-', backspace, (entry,), row=5, column=0, ipadx=5, padx=5, pady=5)
    place_button('C', clear, (entry,), row=5, column=1, pady=5, ipadx=5)
    place_button('=', calc, (entry,), bg=cal_output_bg, row=5, column=2, ipadx=5, padx=5, pady=5,
                 columnspan=2, sticky=tkinter.E + tkinter.W + tkinter.N + tkinter.S)

    root.mainloop()




