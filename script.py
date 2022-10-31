import gspread

gc = gspread.service_account(
        filename="protean-booth.json")


with open('url.txt') as f:
    url = f.readline()
f.close()

sh = gc.open_by_url(url)
worksheet = sh.sheet1

students_number = 154

def cleaning_data(data): # заменяю пустые клетки на '0'/ у дробных чисел ',' меняю на '.' и привожу к int
    for i in range(1, students_number):
        if str(data[i]) == '':
           data[i] = 0
        if str(data[i]) == 'н':
           data[i] = 0
    for i in range(1, students_number):
        for j in range(len(str(data[i]))):
            if (str(data[i])[j] == ','):
                    data[i] = (buf := str(data[i])[: j] + '.' +
                               str(data[i])[j+1: len(str(data[i]))])
        data[i] = int(float(data[i]) + 0.5)


def mlta_script():
    data = worksheet.col_values(24)

    cleaning_data(data)

    for k in range(26, 48):
        new_data = worksheet.col_values(k)
        cleaning_data(new_data)
        for i in range(1, students_number):
            data[i] += new_data[i]
    
    my_data = data[27]

    f = open(r"message.txt", "w")
    
    # ищу наибольший балл
    m_value = 0
    for i in range(1, students_number):
        if int(data[i]) <= m_value:
            continue
        m_value = int(data[i])
    
    
    f.write('Максимальный балл: ' + str(m_value) + '\n')
    f.write('Твой балл: ' + str(my_data) + '\n') 
    
    # считаю количество людей у кторых балл больше

    count = 0
    for i in range(1, students_number):
        if int(data[i]) >= int(my_data):
            count += 1
    
    f.write(str(count)+ ' лучше тебя' + '\n')
    
    # расчитывю в какой процент студентов вхожу
    percent = (100 / students_number) * count
    f.write('Ты входишь в ' + str(int(percent + 0.5)) + '%' + '\n')
    
    # отсортирую значения, чтобы найти медианное значение и посчитать количуство баллов для вхождения в 25% и 10%
    studetns_data = [0] * students_number
    for i in range(1, students_number):
        studetns_data[i - 1] = int(data[i])
    
    studetns_data.sort()

    top_10 = studetns_data[-15]
    f.write("Что бы войти в 10% необходимо следующее количество баллов: " + str(top_10) + '\n')
    
    top_25 = studetns_data[-37]
    f.write("Что бы войти в 25% - " + str(top_25) + '\n')

    f.close()