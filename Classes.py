from datetime import datetime as dt

mon_balance = 1000
cor_passw = 7925
locked_status = True
logged_in = False
oper_list = []
oper_time = []
now = dt.now()

def oper_list_f():
    print("История операций\n")
    i = 0
    if len(oper_list) > 0:
        for id in oper_list:
            if oper_list[i] > 0:
                print('Пополнеие счёта на', oper_list[i], "|", oper_time[i])
                i += 1
            else:
                print("Снятие денег со счёта", oper_list[i], "|", oper_time[i])
                i += 1
        i = 0
    else:
        print("За последнее время вы не проводили никаких операций\n")

def qst():
    b = True
    while b:
        user_answer = input()
        if user_answer == 'Y' or user_answer == 'y':
            b = False
        elif user_answer == 'N' or user_answer == 'n':
            b = False
            global logged_in
            logged_in = False
        else:
            print("Хотите продолжить?\nY - да N - нет")
            continue

class ATM:

    def __init__(self):
        pass

    def pass_code(self, passw):
        global cor_passw
        try:
            if int(passw) == cor_passw:
                print("Пин-код верен\nДобро пожаловать")
                global locked_status
                locked_status = False
                global logged_in
                logged_in = True
            else:
                print("Пин-код неверен\nПопробуйте ещё раз")
        except ValueError:
            print("Пин-код должен состоять только из цифр\nПопробуйте ещё раз")

    def operations(self, cus_input):
        global mon_balance
        if cus_input == "1":
            print(f"Ваш баланс: {mon_balance}")
            print(f"Операция успешно проведена\nХотите продолжить?\nY - да N - нет")

            qst()

        elif cus_input == '2':
            w_amount = int(input("Сколько денег желаете снять с баланса?\n"))
            if w_amount <= mon_balance:
                mon_balance = mon_balance - w_amount
                oper_list.append(-w_amount)
                oper_time.append(f'Время выполнения операции: {now:%d.%m.%Y. %H:%M}')
                print(f"Операция успешно проведена Ваш новый баланс: {mon_balance}"
                      "\nХотите продолжить?\nY - да N - нет")
                qst()
            else:
                print("Не хватает денег на счёте")
                print("Операция не проведена\nХотите продолжить?\nY - да N - нет")
                qst()

        elif cus_input == '3':
            print("Введите кол-во денег на которое желаете пополнить ваш счёт")
            cus_input = int(input())
            print("Ваш счёт был пополнен на", cus_input)
            mon_balance = mon_balance + cus_input
            oper_list.append(cus_input)
            oper_time.append(f'Время выполнения операции: {now:%d.%m.%Y. %H:%M}')
            print("Операция успешно проведена\nХотите продолжить?\nY - да N - нет")

            qst()

        elif cus_input == '4':

            oper_list_f()
            print("Операция успешно проведена\nХотите продолжить?\nY - да N - нет")

            qst()

        elif cus_input == '5':
            global logged_in
            logged_in = False

atm = ATM()

while locked_status:
    passw = input("Введите ваш пин-код\n")
    atm.pass_code(passw)


while logged_in:

    print("Для того чтобы проверить баланс нажмите '1'")
    print("Для того чтобы снять деньги с баланса нажмите '2'")
    print("Для того чтобы пополнить счёт нажмите '3'")
    print("Для того чтобы проверить историю операций нажмите '4'")
    print("Для того чтобы закончить работу нажмите '5'")
    print("")

    atm.operations(cus_input=input("Какую операцию желаете провести?\n"))


print("Спасибо что воспользовались нашими услугами")
