#! /usr/bin/env python
# -*- coding: utf-8 -*-
import gspread

gc = gspread.service_account(
    filename="protean-booth.json")

with open('url.txt') as f:
    url = f.readline()
f.close()

sh = gc.open_by_url(url)
worksheet = sh.sheet1

table = worksheet.get_all_values()

students_number = 153


def get_data_from_list(col_number):
    new_marks = []
    for i in range(students_number):
        new_marks.append(table[i + 1][col_number])
    return new_marks


# заменяю пустые клетки на '0'/ у дробных чисел ',' меняю на '.' и привожу к int
def cleaning_data(data):
    for i in range(0, students_number):
        if str(data[i]) == '':
            data[i] = 0
        if str(data[i]) == 'н':
            data[i] = 0
    for i in range(0, students_number):
        for j in range(len(str(data[i]))):
            if (str(data[i])[j] == ','):
                data[i] = (str(data[i])[: j] + '.' +
                           str(data[i])[j+1: len(str(data[i]))])
        data[i] = int(float(data[i]) + 0.5)


def mlta_script():

    marks = []
    for i in range(students_number):
        marks.append(table[i + 1][23])

    cleaning_data(marks)

    for colum in range(25, 47):
        newdata = get_data_from_list(colum)
        cleaning_data(newdata)
        for row in range(0, students_number):
            marks[row] += newdata[row]

    my_data = marks[26]

    # ищу наибольший балл
    m_value = 0
    for i in range(0, students_number):
        if int(marks[i]) <= m_value:
            continue
        m_value = int(marks[i])
    
    message = ('Максимальный балл: ' + str(m_value) + '.\n')
    message += ('Твой балл: ' + str(my_data) + '.\n') 	
    
    # считаю количество людей у кторых балл больше
    count = 0
    for i in range(0, students_number):
        if int(marks[i]) >= int(my_data):
            count += 1

    message += (str(count) + ' лучше тебя' + '.\n')

    # расчитывю в какой процент студентов вхожу
    percent = (100 / students_number) * count
    message += ('Ты входишь в ' + str(int(percent + 0.5)) + '%' + '.\n')

    # отсортирую значения, чтобы найти медианное значение и посчитать количуство баллов для вхождения в 25% и 10%
    studetns_data = [0] * students_number
    for i in range(0, students_number):
        studetns_data[i - 1] = int(marks[i])

    studetns_data.sort()

    top_10 = studetns_data[-15]
    message += ("Что бы войти в 10% необходимо следующее количество баллов: " +
                str(top_10) + '.\n')

    top_25 = studetns_data[-37]
    message += ("Что бы войти в 25% - " + str(top_25) + '.')

    return message
