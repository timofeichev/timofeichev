
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

my_list = []
for elem in range(int(input())):
    elem = list(map(int, input().split()))
    my_list.append(elem)

def my_func_zip(my_list):
    len_of_row = []
    for row in my_list:
        len_of_row.append(len(row))
        min_len_of_row = min(len_of_row)
    result = ([row[i] for row in my_list] for i in range(min_len_of_row))
    return result
print(my_func_zip(my_list))

