a = float(input('Введите первое число: '))
b = float(input('Введите второе число: '))
print('Резултат', a / b)
def safe_divid(a, b):
if b == 0:
return 'Ошибка: деление на ноль!'
return a / b 