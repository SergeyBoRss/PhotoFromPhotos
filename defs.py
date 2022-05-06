from PIL import Image
import time


# делаем из квадратной картинки картинку поменьше с размерами minisize
def uzhim(namef, n, minisize, spath):
    image = Image.open(namef)
    newimage = image.resize((minisize, minisize))
    savenew(newimage, n, spath)


# сохарняем файл с учетом его порядкого номера, можно убрать эту функцию
def savenew(f, n, spath):
    f.save(spath + "/" + str(n) + ".png")


# сохранение картинки с привязкой к точной дате и времени
def savepic_withdate(f):
    namewithtime = (time.strftime("%H_%M_%S-%m.%d.%Y", time.localtime()))
    f.save(namewithtime + ".png")


# ищем среднйи цвет каждой маленькой картинки
def srchvet(namef):
    image = Image.open(namef)
    pxmas = image.load()
    # print(pxmas)
    x, y = image.size
    sr, sg, sb = 0, 0, 0
    for i in range(x):
        for j in range(y):
            r, g, b = pxmas[i, j]
            sr += r
            sg += g
            sb += b
    return (sr // (x * x), sg // (x * x), sb // (x * x))


# проверка цвета пикселя на выход за разрешенные грани
def checknewpx(n):
    if n > 255:
        n = 255
    elif n < 0:
        n = 0
    return n


# ищем соседние цвета для картинки, чтобы увелчиить цветовую палитру картинок
def neiborcolor(namef, smech, spath, ldir):
    image = Image.open(namef)
    pxmas = image.load()
    x, y = image.size
    # print(x, y)
    newpic = Image.new("RGB", (x, y), (0, 0, 0))
    pxnewmas = newpic.load()
    for i in range(x):
        for j in range(y):
            r, g, b = pxmas[i, j]
            newr = checknewpx(r + smech[0])
            newg = checknewpx(g + smech[1])
            newb = checknewpx(b + smech[2])
            pxnewmas[i, j] = newr, newg, newb
    newpic.save(spath + "/" + str(ldir) + ".png")


# много раз применяем функцию соседних цветов
def mnogoneiborcolor(namef, spath, ldir):
    k = [(-20, -20, -20), (20, 20, 20), (20, 0, 0), (0, 20, 0), (0, 0, 20)]
    for i in range(5):
        neiborcolor(namef, k[i], spath, ldir + i + 1)


# изменение пикселей в полученной картинке на картинки из файла
def change(namef, masznrgb, spath, minisize):
    image = Image.open(namef)
    pxmas = image.load()
    x, y = image.size
    # print(x, y)
    xnew = x - x % minisize
    ynew = y - y % minisize
    newpic = Image.new("RGB", (xnew, ynew), (0, 0, 0))
    # pxnewmas = newpic.load()
    for i in range(0, xnew, minisize):
        for j in range(0, ynew, minisize):
            sr, sg, sb = 0, 0, 0
            # print(i, j)
            for ix in range(i, i + minisize):
                for jy in range(j, j + minisize):
                    r, g, b = pxmas[ix, jy]
                    sr += r
                    sg += g
                    sb += b
            sr //= (minisize * minisize)
            sg //= (minisize * minisize)
            sb //= (minisize * minisize)
            minzn = 1000000
            imin = 1
            for p in range(len(masznrgb)):
                r, g, b = masznrgb[p]
                if ((r - sr) ** 2 + (g - sg) ** 2 + (b - sb) ** 2) ** 0.5 < minzn:
                    minzn = ((r - sr) ** 2 + (g - sg) ** 2 + (b - sb) ** 2) ** 0.5
                    imin = p + 1
            im2 = Image.open(spath + "\\" + str(imin) + ".png")
            newpic.paste(im2, (i, j))
    newpic.show()
    savepic_withdate(newpic)
