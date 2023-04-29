import ast

types_ = ['W', "R"]
type_ = types_[1]
line_ = 2 - 1

if type_ == 'W':
    my_dict = {"homeB": 'Главная страница', "bankB": 'Наш банк', "cardB": 'Твоя кредитка', "loanB": 'Кредиты',
               "hystB": 'История платежей', "abotB": 'О нас', "contB": 'Связь с нами'}
    my_str = ' '.join([k + '=' + v.replace(' ', 'SP') for k, v in my_dict.items()])
    print(my_str)

elif type_ == 'R':
    my_dict = ast.literal_eval(open('langs\\eng.lang', 'r', encoding='utf-8').readlines()[line_].strip())
    print(my_dict)
