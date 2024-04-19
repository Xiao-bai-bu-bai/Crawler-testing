from threading import Thread

# 多线程简单运用一
# def func(name):
#     for i in range(100):
#         print(name, i)
#
# if __name__ == '__main__':
#     # 创建线程
#     t1 = Thread(target=func, args=('张三',))  # args是一个元组
#     t2 = Thread(target=func, args=('李四',))
#
#     # 启动线程
#     t1.start()
#     t2.start()
#
#     # 等待线程结束
#     t1.join()
#     t2.join()
#     print('主线程结束')


# 多线程简单运用二----面向对象
class MyThread(Thread):  # 继承Thread类
    def __init__(self, name):  # 重写构造方法
        super().__init__()  # 调用父类的构造方法
        self.name = name

    def run(self):
        for i in range(100):
            print(self.name, i)

if __name__ == '__main__':
    t1 = MyThread('张三')
    t2 = MyThread('李四')

    t1.start()
    t2.start()

    t1.join()
    t2.join()
    print('主线程结束')