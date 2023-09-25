import pytesseract as pt
import cv2
import numpy as np
import os

### НАСТРОЙКИ ###
path_to_tesseract = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"               # ПУТЬ К ТЕССЕРАКТУ
config = r'-l rus --oem 3 --psm 6'                                                  # КОНФИГУРАЦИЯ ТЕССЕРАКТА
path_to_image = "C:\\Users\\USER\\Documents\\images"                                # ПУТЬ К ИЗОБРАЖЕНИЮ
path_to_output = "C:\\Users\\USER\\Documents\\images\\output.txt"                   # ПУТЬ К ВЫХОДНОМУ ФАЙЛУ
#################

def check_INN10(INN):       # Проверка контрольного числа 10-значного ИНН
    num = []
    INN_copy = INN
    for i in range(10):
        num.append(INN_copy%10)
        INN_copy = int(INN_copy / 10)

    #Весовые коэффициенты: 2 4 10 3 5 9 4 6 8
    control_sum = num[9]*2 + num[8]*4 + num[7]*10 + num[6]*3 + num[5]*5 + num[4]*9 + num[3]*4 + num[2]*6 + num[1]*8
    
    if (control_sum%11) % 10 == num[0]:
        return INN
    else: return -1

def check_INN12(INN):       # Проверка контрольных чисел 12-значного ИНН
    num = []
    INN_copy = INN
    for i in range(12):
        num.append(INN_copy%10)
        INN_copy = int(INN_copy/10)
    
    # Весовые коэффициенты для 11-ой цифры: 7 2 4 10 3 5 9 4 6 8
    control_sum = num[11]*7 + num[10]*2 + num[9]*4 + num[8]*10 + num[7]*3 + num[6]*5 + num[5]*9 + num[4]*4 + num[3]*6 + num[2]*8
    if (control_sum%11) % 10 == num[1]:
        
        # Весовые коэффициенты для 12-ой цифры 3 7 2 4 10 3 5 9 4 6 8
        control_sum = num[11]*3 + num[10]*7 + num[9]*2 + num[8]*4 + num[7]*10 + num[6]*3 + num[5]*5 + num[4]*9 + num[3]*4 + num[2]*6 + num[1]*8
        if (control_sum%11) % 10 == num[0]:
            return INN
        else: return -1
    else: return -1

while True:

    print("Check if path to tesseract.exe is correct:")
    print(path_to_tesseract)
    print("Y/N")
    q = input()
    while True:
        if q == "Y":
            break
        elif q == "N":
            print("Input correct way to tesseract.exe (use // instead of /):")
            path_to_tesseract = input()
            q = "Y"
        else:
            print("Type Y for Yes or N for No!")
            q = input()
    
    print("Check if path to folder with images is correct:")
    print(path_to_image)
    print("Y/N")
    q = input()
    while True:
        if q == "Y":
            break
        elif q == "N":
            print("Input correct way to folder with images (use // instead of /):")
            path_to_image = input()
            q = "Y"
        else:
            print("Type Y for Yes or N for No!")
            q = input()

    print("Check if path to output file is correct:")
    print(path_to_output)
    print("Y/N")
    q = input()
    while True:
        if q == "Y":
            break
        elif q == "N":
            print("Input correct way to output file (use // instead of /):")
            path_to_output = input()
            q = "Y"
        else:
            print("Type Y for Yes or N for No!")
            q = input()

    pt.pytesseract.tesseract_cmd = path_to_tesseract

    output = ""

    os.chdir(path_to_image)
    with os.scandir(path_to_image) as listOfFiles:
        for file in listOfFiles:
            if file.is_file() and (file.name.find(".jpg")!=-1 or file.name.find(".png")!=-1):
                image = cv2.imread(file.name)
                print("================")
                print(file.name)
                print("================")
                text = pt.image_to_string(image, config=config)

                n = text.find("ИНН ")
                if n == -1:
                    print("INN not found")          # Проверка, был ли обнаружен в тексте ИНН
                    output = output + file.name + " INN not found\n"
                else:
                    text = text[n:]
                    i = 0
                    while ord(text[i])<48 or ord(text[i])>57:
                        text = text[1:]
                    INN = text[0:12]            # Выделение 12-ти значного ИНН

                    for i in range(len(INN)-1,len(INN)-3,-1):
                        if ord(INN[i])<48 or ord(INN[i])>57:
                            INN = INN[:i]           # Если ИНН был 10-значный, то убираются лишние символы
                    
                    try:
                        INN = int(INN)
                    except ValueError:
                        INN = -1                    # Если не получилось преобразовать ИНН из строки в число, значит ИНН был распознан неправльно
                    
                    if INN != -1:
                        INN_type = int(np.log10(INN))+1 # Вычисление количества знаков в распознаном ИНН
                        
                        if INN_type == 10:
                            INN = check_INN10(INN)
                        elif INN_type == 12:
                            INN = check_INN12(INN)
                        else: INN = -1

                    if INN == -1:
                        print("Warning! First found INN was not recognized correctly, looking for another one...")

                        text = text[12:]
                        n = text.find("ИНН ")
                        if n == -1:
                            print("INN not found, try another image!")          # Проверка, был ли обнаружен в тексте ИНН
                        else:
                            text = text[n:]
                            i = 0
                            while ord(text[i])<48 or ord(text[i])>57:
                                text = text[1:]
                            INN = text[0:12]            # Выделение 12-ти значного ИНН
                            
                            for i in range(len(INN)-1,len(INN)-3,-1):
                                if ord(INN[i])<48 or ord(INN[i])>57:
                                    INN = INN[:i]           # Если ИНН был 10-значный, то убираются лишние символы
                            
                            try:
                                INN = int(INN)
                            except ValueError:
                                INN = -1                    # Если не получилось преобразовать ИНН из строки в число, значит ИНН был распознан неправльно
                            
                            if INN != -1:
                                INN_type = int(np.log10(INN))+1 # Вычисление количества знаков в распознаном ИНН
                                
                                if INN_type == 10:
                                    INN = check_INN10(INN)
                                elif INN_type == 12:
                                    INN = check_INN12(INN)
                                else: INN = -1

                            if INN == -1:
                                print("Error! There is no INN on the image, which can be recognized correctly. Try another image!")
                                output = output + file.name + " INN not recognized\n"
                            else:
                                print(INN)
                                output = output + file.name + " " + str(INN) + "\n"
                    else:
                        print(INN)
                        output = output + file.name + " " + str(INN) + "\n"

    output_file = open(path_to_output, "w")
    output_file.write(output)
    output_file.close()

    print("Scan another folder?")
    print("Y/N")
    q = input()
    if q == "N":
        break