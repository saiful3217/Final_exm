class Bank:
    __user_accounts=[]
    __admin_accounts=[]
    __balance=100000
    __loan_amount=0

    @property
    def account_info(self):
        print("\n ALL User Account Information \n")
        for account in self.__user_accounts:
            print(f"Account Holder Name: {account.name}")
            print(f"Account Holder Email: {account.email}")
            print(f"Account Holder Password: {account.password}")
            print(f"Account Number: {account.acc_no}")
            print(f"Account Type: {account.type}")
            print(f"Account Balance: {account.balance}\n")

    @account_info.setter
    def add_user_accounts(self,user):
        self.__user_accounts.append(user)

    @property
    def number_of_acc(self):
        return len(self.__user_accounts)
    
    def account_delete(self,acn):
        obj=None
        for acc in self.__user_accounts:
            if acc.acc_no==acn:
                obj=acc
                break
        if obj:
            print(f"\nAccount Holder name: {obj.name}")
            print(f"Account Number: {obj.acc_no}")
            Dbbl.detuct_balance=obj.balance
            self.__user_accounts.remove(obj)
            print("\nAccount Deleted Successfully\n")
        else:
            print("\nNO Account Exists in This Account Number\n")

    @property
    def loan_amount(self):
        return self.__loan_amount

    @loan_amount.setter
    def add_loan_amount(self,amount):
        if amount>=0:
            self.__loan_amount+=amount

    @property
    def balance(self):
        return self.__balance

    @balance.setter
    def detuct_balance(self,amount):
        self.__balance-=amount
    
    @balance.setter
    def add_balance(self,amount):
        self.__balance+=amount
    
    def add_admin_acc(self,ac):
        self.__admin_accounts.append(ac)

    def get_admin(self,email, password):
        flag=True
        for adm in self.__admin_accounts:
            if adm.email==email and adm.password==password:
                return adm
                flag=False
        if flag:
            return None
    
    def change_loan_feature(self,acn,cng):
        flag=True
        for acc in self.__user_accounts:
            if acc.acc_no==acn:
                flag=False
                if cng=="ON":
                    acc.loan_feature=True
                    print("\nLoan Feature Turned ON\n")
                elif cng=="OFF":
                    acc.loan_feature=False
                    print("\nLoan Feature Turned OFF\n")
                else:
                    print("\nInvalid Command\n")
        if flag:
            print("\nInvalid Account Number\n")
    
    def get_user(self,email, password):
        flag=True
        for usr in self.__user_accounts:
            if usr.email==email and usr.password==password:
                return usr
                flag=False
        if flag:
            return None
    
    def get_user_t(self,acn):
        flag=True
        for usr in self.__user_accounts:
            if usr.acc_no==acn:
                return usr
                flag=False
        if flag:
            return None
        
    

class Account:
    def __init__(self,name,email,password,type) -> None:
        self.name=name
        self.__email=email
        self.__password=password
        self.type=type
        self.__balance=0
        self.loan_feature=True
        self.loan_cnt=0
        self.trans_history=[]

    @property
    def balance(self):
        return self.__balance

    @balance.setter
    def deposit(self,amount):
        self.__balance+=amount
        Dbbl.add_balance=amount
        trans_h=("Deposit",amount)
        self.trans_history.append(trans_h)
        print(f"\nSuccessfully Deposited Money: {amount} after Deposit Main Balance: {self.__balance} \n")

    @balance.setter
    def add_trnf_money(self,amount):
        self.__balance+=amount

    @balance.setter
    def withdraw(self,amount):
        if amount<=Dbbl.balance:
            if self.__balance<amount:
                print("\nWithdrawal amount exceeded\n")
            else:
                self.__balance-=amount
                Dbbl.detuct_balance=amount
                trans_h=("Wthdraw",amount)
                self.trans_history.append(trans_h)
                print(f"\nSuccessfully Wthdrawed Money: {amount} after Wthdraw Main Balance: {self.__balance}\n")
        else:
            print("\nThe Bank is Bankrupt\n")
    
    def take_loan(self,amnt):
        if self.loan_cnt<2:
            if amnt<=0 or amnt >5000 :
                print("\nYou cant take nagtive or more than 5000 tk Loan\n")
            else:
                if self.loan_feature:
                    Dbbl.detuct_balance=amnt
                    Dbbl.add_loan_amount=amnt
                    trans_h=("Loan",amnt)
                    self.__balance+=amnt
                    self.trans_history.append(trans_h)
                    self.loan_cnt+=1
                    print(f"\nLoan Successfully taken. Loan Amount: {amnt} and Main Balance: {self.__balance} \n")
                else:
                    print("\nLoan Feature is Currently Off For your Account\n")
        else:
            print("\nYou can't Take Loan More than 2 times.\n")    
    
    def transfer_money(self,acn,amount):
        flag=False
        acc=None
        acc=Dbbl.get_user_t(acn)
        if acc!=None:
            if  self.__balance>0 and self.__balance>=amount:
                self.__balance-=amount
                th=("Transferd",amount)
                self.trans_history.append(th)
                tht=("Recived",amount)
                acc.trans_history.append(tht)
                acc.add_trnf_money=amount
                print(f"\n{amount} TK Successfully Transferd to {acc.name} Account ")
                print(f"After Tranfer Main Balance: {self.__balance}\n")
            else:
                print("\nNot Enough Money \n")
        else:
            print("\nAccount does not Exists\n")

    @property
    def email(self):
        return self.__email

    @property
    def password(self):
        return self.__password

class Saving(Account):
    def __init__(self, name, email, password, type) -> None:
        super().__init__(name, email, password, type)
        self.acc_no=10051+Dbbl.number_of_acc
        Dbbl.add_user_accounts=self

class Current(Account):
    def __init__(self, name, email, password, type) -> None:
        super().__init__(name, email, password, type)
        self.acc_no=20051+Dbbl.number_of_acc
        Dbbl.add_user_accounts=self

class Admin:
    def __init__(self,name,email,password) -> None:
        self.name=name
        self.__email=email
        self.__password=password
        Dbbl.add_admin_acc(self)
    @property
    def email(self):
        return self.__email
    @property
    def password(self):
        return self.__password

Dbbl=Bank()

cur=None
while True:
    print("1. Sinup as Admin")
    print("2. Create a new Bank Account")
    print("3.Login ")
    print("4. Exit")
    option=int(input("Enter Option: "))
    if option==1:
        a_pass=input("Enter Autintication code: ")
        if a_pass=="123456789":
            name=input("Enter Name: ")
            email=input("Enter email: ")
            password=input("Enter Password: ")
            re_pass=input("Re-enter Password: ")
            if password==re_pass:
                Admin(name,email,password)
            else:
                print("Password not matched")
        else:
            print("Authentication Error. You can't signup as Admin")
    elif option==2:
        name=input("Enter Name: ")
        email=input("Enter email: ")
        password=input("Enter Password: ")
        re_pass=input("Re-enter Password: ")
        if password==re_pass:
            act=input("Current Account or Saving Account? Enter (CA/SA): ")
            if act=="CA"  :
                Current(name,email,password,"Current")
            elif act=="SA":
                Saving(name,email,password,"Saving")
            else:
                print("Invalid Command")
        else:
            print("Password not matched")
    elif option==3:
        while True:
            print("1.Login as Admin")
            print("2.Login as User")
            print("3. Return to Main Menu")
            op=int(input("Enter option: "))
            if op==1:
                email=input("Enter Email: ")
                password=input("Enter Password: ")
                cur= Dbbl.get_admin(email,password)
                if cur==None:

                    print("Invalid Email or Password")
                else:
                    print(f'\n Welcome {cur.name}\n')
                    while True:
                        print("1. See All User Accounts List")
                        print("2. Check the Total Available Balance of the Bank")
                        print("3. Check the Total Loan Amount.")
                        print("4. Delete any User Account")
                        print("5. Take action Loan feature of the bank.")
                        print("6. Return to Main Menu.")
                        aop=int(input("Enter Option: "))
                        if aop==1:
                            Dbbl.account_info
                        elif aop==2:
                            print ("Total Available Balance of the Bank: ",Dbbl.balance)
                        elif aop==3:
                            print("Total Loan Amount: ",Dbbl.loan_amount)
                        elif aop==4:
                            acn=int(input("Enter Account NO: "))
                            Dbbl.account_delete(acn)
                        elif aop==5:
                            print("What Type of Change You Want?")
                            cng=input("Please Type (ON/OFF): ")
                            acn=int(input("Enter Account NO: "))
                            Dbbl.change_loan_feature(acn,cng)
                        elif aop==6:
                            break
                        else:
                            print("Invalid Command")
            
            elif op==2:
                email=input("Enter Email: ")
                password=input("Enter Password: ")
                cur= Dbbl.get_user(email,password)
                if cur==None:
                    print("Invalid Email or Password")
                else:
                    print(f'\n Welcome {cur.name}\n')
                    while True:
                        print("1. Deposit Money")
                        print("2. Withdraw Money")
                        print("3. Check Available Balance")
                        print("4. Check Transaction History.")
                        print("5. Take Loan.")
                        print("6. Transfer Money.")
                        print("7. Return to Main Menu.")
                        aop=int(input("Enter Option: "))
                        if aop==1:
                            amnt=int(input("Enter Deposit Amount: "))
                            cur.deposit=amnt
                        elif aop==2:
                            amnt=int(input("Enter Withdraw Amount: "))
                            cur.withdraw=amnt
                        elif aop==3:
                            print("\nTotal Balance: ",cur.balance)
                            print()
                        elif aop==4:
                            print(f"Transaction History of {cur.name}\n")
                            for t in cur.trans_history:
                                print(f"Transaction Type: {t[0]}  Amount: {t[1]}")
                            print()
                        elif aop==5:
                            amt=int(input("\nEnter Amount of Loan You want:"))
                            cur.take_loan(amt)
                        elif aop==6:
                            acn=int(input("\nEnter Account Number :"))
                            amnt=int(input("Enter Amount :"))
                            cur.transfer_money(acn,amnt)
                        elif aop==7:
                            break
                        else:
                            print("\nInvalid Command\n")
            elif op==3:
                break
            else:
                print("\nInvalid Command\n")
    elif option==4:
        break
    else:
        print("\nInvalid Command\n")
