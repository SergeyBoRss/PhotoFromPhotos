from defs import *
import os


# Done/NDone (получен/не получен массив средних значений)
status = "NDone"
photoforchange = r"D:\Downloads\2.png" #Путь до изменяемой картинки
papka_Nach_name = r"D:\Downloads\cat"  #Путь до папки с начальными картинками, из которых будет состоять фото
minisize = 20
dir = os.listdir(path=papka_Nach_name)
koleldir = ishkol = len(dir)
print(ishkol)

if status == "NDone":
    # переименовывем все файлы из заданной нам папки в вид 1.png..n.png и проверяем на наличие ошибки существования файла
    for i in range(1, koleldir + 1):
        try:
            os.rename(papka_Nach_name + "\\" + dir[i - 1], papka_Nach_name + "\\" + str(i) + ".png")
        except FileExistsError:
            continue

    # уменьшаем размер фоток
    print("reducing the size of the photos")
    for i in range(1, koleldir + 1):
        uzhim(papka_Nach_name + "/" + str(i) + ".png", i, minisize, papka_Nach_name)
        print(papka_Nach_name + "/" + str(i) + ".png", "success")

    # делаем копии фоток с соседними значениями
    print("creating copies by color")
    for i in range(ishkol):
        mnogoneiborcolor(papka_Nach_name + "\\" + str(i + 1) + ".png", papka_Nach_name, koleldir)
        koleldir += 5
        print(papka_Nach_name + "\\" + str(i + 1) + ".png", "success")

    f = open("d", "w")
    for i in range(1, koleldir + 1):
        p = srchvet(papka_Nach_name + "/" + str(i) + ".png")
        f.write(str(p[0]) + " " + str(p[1]) + " " + str(p[2]) + "\n")
    status = "Done"

if status == "Done":
    masznrgb = []
    f = open("d", "r")
    for i in f.readlines():
        a, b, c = i.split(" ")
        masznrgb.append((int(a), int(b), int(c)))
    change(photoforchange, masznrgb, papka_Nach_name, minisize)
