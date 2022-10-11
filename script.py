import gspread

gc = gspread.service_account(
        filename="protean-booth.json")

with open('url.txt') as f:
    url = f.readline()
f.close()

sh = gc.open_by_url(url)
worksheet = sh.sheet1

def mlta_script():
    data = worksheet.col_values(64)

    # заменяю пустые клетки на '0'/ у дробных чисел ',' меняю на '.' и привожу к int
    for i in range(1, 151):
        if str(data[i]) == '':
            data[i] = 0
        else:
            for j in range(len(str(data[i]))):
                if (str(data[i])[j] == ','):
                    data[i] = (buf := str(data[i])[: j] + '.' +
                               str(data[i])[j+1: len(str(data[i]))])
            data[i] = int(float(data[i]) + 0.5)
    
    # чищу ошибочные данные исходной таблицы
    data[27] -= 12
    data[52] -= 12
    data[57] -= 12
    data[64] -= 12
    data[103] -= 24
    data[124] -= 10
    data[126] -= 12
    data[137] -= 12
    
    my_data = data[27]

    f = open(r"message.txt", "w")
    
    # ищу наибольший балл
    m_value = 0
    for i in range(1, 151):
        if int(data[i]) <= m_value:
            continue
        m_value = int(data[i])
    
    
    f.write('Максимальный балл: ' + str(m_value) + '\n')
    f.write('Твой балл: ' + str(my_data) + '\n') 
    
    # считаю количество людей у кторых балл больше

    count = 0
    for i in range(1, 151):
        if int(data[i]) >= int(my_data):
            count += 1
    
    f.write(str(count)+ ' лучше тебя' + '\n')
    
    # расчитывю в какой процент студентов вхожу
    percent = (100 / 151) * count
    f.write('Ты входишь в ' + str(int(percent + 0.5)) + '%' + '\n')
    
    # отсортирую значения, чтобы найти медианное значение и посчитать количуство баллов для вхождения в 25% и 10%
    studetns_data = [0] * 151
    for i in range(1, 151):
        studetns_data[i - 1] = int(data[i])
    
    studetns_data.sort()

    top_10 = studetns_data[-15]
    f.write("Что бы войти в 10% необходимо следующее количество баллов: " + str(top_10) + '\n')
    
    top_25 = studetns_data[-37]
    f.write("Что бы войти в 25% - " + str(top_25) + '\n')

    f.close()