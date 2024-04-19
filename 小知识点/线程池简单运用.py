from concurrent.futures import ThreadPoolExecutor, wait
import time

# 无返回值
# def func(name):
#     for i in range(100):
#         print(name, i)
#
#
# if __name__ == '__main__':
#     with ThreadPoolExecutor(5) as pool:  # 线程池大小为5
#         for j in range(100):  # 100个任务
#             pool.submit(func, f'第{j}号张三')  # 执行任务

######################################################################

# 接受返回值
def func(name, t):
    time.sleep(t)
    print(f'我是{name}，我睡了{t}秒')
    return name


def fn(res):
    print(res.result())


if __name__ == '__main__':
    with ThreadPoolExecutor(3) as pool:
        # pool.submit(func, '张三', 2).add_done_callback(fn)
        # pool.submit(func, '李四', 1).add_done_callback(fn)
        # pool.submit(func, '王五', 3).add_done_callback(fn)
        '''
        pool.submit().add_done_callback()方法，可以接受线程执行完毕后的返回值
        但是返回值的顺序是不确定的
        '''
        #################################################################################
        result = pool.map(func, ['张三', '李四', '王五'], [2, 1, 3])
        for res in result:
            print(res)
        '''
        map返回的是一个迭代器，可以通过for循环遍历
        返回的内容是按照线程分发的顺序
        '''
