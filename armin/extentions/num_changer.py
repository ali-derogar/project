def number_changer(x):

    number_list = {
        '0' : '۰',
        '1' : '۱',
        '2' : '۲',
        '3' : '۳',
        '4' : '۴',
        '5' : '۵',
        '6' : '۶',
        '7' : '۷',
        '8' : '۸',
        '9' : '۹',
        '10' : '۱۰',
        '11' : '۱۱',
        '12' : '۱۲'
    }
    for z ,c in number_list.items():
         if z in list(x):
             x = x.replace(z,c)
    return x