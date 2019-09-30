
#Написать короткие функции, принимающие один аргумент - список чисел и возвращающие:
#Список квадратов чисел;

my_list = list(map(int, input().split()))
def my_square(my_list):
    result = []
    for i in my_list:
        result.append(i**2)
    return(result)
print(my_square(my_list))

#Каждый второй элемент списка;

my_list = list(map(int, input().split()))
def my_second_elem(my_list):
    result = []
    for elem in range(0, len(my_list), 2):
        result.append(my_list[elem])
    return result
print(my_second_elem(my_list))

#Квадраты чётных элементов на нечётных позициях.

my_list = list(map(int, input().split()))
def my_func(my_list):
    result = []
    for elem in range(0, len(my_list), 2):
        if my_list[elem] %2 == 0:
            result.append(my_list[elem]**2)
    return result
print(my_func(my_list))

#Написать функцию, которая на вход принимает словарь, и возвращает словарь, в котором ключи со значениями
# поменяны местами. В случае если это невозможно сделать - выводит об этом сообщение.

my_dict = {1:234, 2:'dog', 3:'duck'}
def my_func_dict(my_dict):
    try:
        result ={}
        for key,value in my_dict.items():
            result[value] = key
        return result
    except TypeError:
        print('В качестве ключа может использоваться только неизменяемый тип данных')
print(my_func_dict(my_dict))

#Написать собственную реализацию zip();

def my_func_zip(*args):
    len_of_row = []
    for row in args:
        len_of_row.append(len(row))
        min_len_of_row = min(len_of_row)
    result = ([row[i] for row in args] for i in range(min_len_of_row))
    return result
print(my_func_zip([1, 2, 1, 2], [2, 4, 5, 6], [7, 8, 9]))

#Написать собственную реализацию xrange().

def my_range(stop, start = None, step = 1):
    result = []
    if start == None:
        c = 0
        while c < stop:
            result.append(c)
            c += step
    else:
        while start < stop:
            result.append(start)
            start += step
    my_generator_object = (elem for elem in result)
    return my_generator_object
print(my_range(8, start = 2, step = 2))

#Написать «вечный» генератор, который выдаёт всё время одно значение;

def my_gen(n):
    while n or n == 0:
        yield n
f = my_gen(23)
print(next(f))
print(next(f))
print(next(f))

