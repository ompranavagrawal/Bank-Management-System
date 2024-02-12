import cx_Oracle
from tabulate import tabulate
def sign_up():
  print('enter account type(saving-> s,cuurent-> c)')
  acc_type=input()  
  print('enter account holder name')
  name=input()
  print('enter address')
  address=input()
  print('enter desired password')
  password=input()
  print('enter initial amount')
  balance=int(input())
  con=cx_Oracle.connect("pranav/pranav@xe")
  cur=con.cursor()                          
  cur.execute("""insert into bankdb3 values(customer_id.nextval,account.nextval,:xname,:xpassword,:xaddress,:xbalance,'n',null,:xacc_type,'n',null,CURRENT_TIMESTAMP,sno.nextval,CURRENT_TIMESTAMP,null,null)""",{'xname':name,'xpassword':password,'xaddress':address,'xbalance':balance,'xacc_type':acc_type})
  con.commit()
  print('your account is created successfully')
  cur.execute("select max(customer_id) from bankdb3")
  print('your customer id is ')
  abc=(cur.fetchall())
  tup=abc[0]
  print(tup[0])
  cur.execute("select max(acc_no) from bankdb3")
  print('your account no. is ')
  abc1=(cur.fetchall())
  tup16=abc1[0]
  print(tup16[0])
  
  con.close()
  return 1
  
def addrchange(accno):
  print('enter new address')
  addr=input()
  con=cx_Oracle.connect("pranav/pranav@xe")
  cur=con.cursor()
  cur.execute("update bankdb3 set address=:xaddr where acc_no= :xaccno",{'xaddr':addr,'xaccno':accno})
  print('your new address is ',addr)
  con.commit()
  con.close
  return 1

def moneydeposit(accno):   
  print('enter the amount to deposit')
  amt=int(input())
  con=cx_Oracle.connect("pranav/pranav@xe")
  cur=con.cursor() 
  printnextentry(accno)
  
  cur.execute("select max(sno) from bankdb3 where acc_no= :xaccno",{'xaccno':accno})
  sno1=cur.fetchall()
  tup1=sno1[0]
  #print(tup1[0])
  cur.execute("select balance from bankdb3 where sno= :xtup1",{'xtup1':tup1[0]})
  currentamt=cur.fetchall()
  tup=currentamt[0]
 # print(tup[0])
  amt=amt+tup[0]
  #print(amt)
  
  cur.execute("update bankdb3 set balance= :xamt where sno= :xsno1",{'xamt':amt,'xsno1':tup1[0]})
  con.commit()
  print('new balance is ',amt) 
  con.commit()    
  con.close

def moneywithdrawal(accno):   
  print('enter the amount to withdraw')
  amt=int(input())
  print('enter transaction type (press c->CREDIT,d->DEBIT)')
  tt=input()
  con=cx_Oracle.connect("pranav/pranav@xe")
  cur=con.cursor()
  printnextentry(accno)
  cur.execute("select max(sno) from bankdb3 where acc_no= :xaccno",{'xaccno':accno})
  sno1=cur.fetchall()
  tup12=sno1[0]
  
  cur.execute("select balance from bankdb3 where sno= :xtup12",{'xtup12':tup12[0]})
  currentamt=cur.fetchall()
  tup=currentamt[0]
  if(tup[0]>=amt):      
      amt=tup[0]-amt
      #printnextentry(accno)
      #cur.execute("select max(sno) from bankdb2 where acc_no= :xaccno",{'xaccno':accno})
      #sno1=cur.fetchall()
      #tup1=sno1[0]
      cur.execute("update bankdb3 set balance=:xamt where sno= :xsno",{'xamt':amt,'xsno':tup12[0]})
      
      print('new balance is ',amt) 
      con.commit() 
      
      #cur.execute("select max(sno) from bankdb2 where acc_no= :xaccno",{'xaccno':accno})
      #sno=cur.fetchall()
      #tup=sno[0]
      cur.execute("update bankdb3 set trans_type= :xtt where sno= :xsno",{'xtt':tt,'xsno':tup12[0]})
      con.commit() 
  else:
      print("withdrawal amount is more than balance")
      print("retry again")
  con.close  
  

  
def printstatement(accno):
    
  try:  
      print('date from (format MM/DD/YYYY)')
      datefrom=input()
      print('date to (format MM/DD/YYYY)')
      dateto=input()
      
      con=cx_Oracle.connect("pranav/pranav@xe")
      cur=con.cursor()
      cur.execute("""select session_date,trans_type,balance from bankdb3 where sdate>=to_date(:xdatefrom,'MM/DD/YYYY') and sdate<=to_date(:xdateto,'MM/DD/YYYY') and ACC_NO=:xaccno order by sno""",{'xdatefrom':datefrom,'xdateto':dateto,'xaccno':accno})
      #print(cur.fetchall())
      print('0->date and time')
      print('1->transaction type')
      print('2->balance')
      print (tabulate(cur.fetchall(), headers="keys"))
  except cx_Oracle.DatabaseError as e:
      print('you entered wrong date')

  finally:
      con.close
      
def TRANSFERMONEY(accno):
  print('enter receiver account no.') 
  rcv=int(input())
  print('enter amount to transfer') 
  trans=int(input())
  
  con=cx_Oracle.connect("pranav/pranav@xe")
  cur=con.cursor()
  
  printnextentry(accno)
  cur.execute("select max(sno) from bankdb3 where acc_no= :xaccno",{'xaccno':accno})
  sno1=cur.fetchall()
  tup12=sno1[0]
  
  cur.execute("select balance from bankdb3 where sno= :xtup12",{'xtup12':tup12[0]})
  currentamt=cur.fetchall()
  tup=currentamt[0]
  #print(tup[0])  
  cur.execute("select max(customer_id) from bankdb3 where acc_no= :xrcv",{'xrcv':rcv})
  cust=cur.fetchall()
  cust1=str(cust)
  #print(cust1)
  if(tup[0] >= trans and cust1 != '[]'): 
      newbal=tup[0]-trans
      #print(newbal)
      cur.execute("update bankdb3 set balance= :xnewbal where sno= :xtup12",{'xnewbal':newbal,'xtup12':tup12[0]})
      #print('yes')
      printnextentry(rcv)
      cur.execute("select max(sno) from bankdb3 where acc_no= :xrcv",{'xrcv':rcv})
      sno2=cur.fetchall()
      tup13=sno2[0]
      #print(tup13[0])
      cur.execute("select balance from bankdb3 where sno= :xtup13",{'xtup13':tup13[0]})
      amt1=cur.fetchall()     
      tup14=amt1[0]
      #print(tup14[0])      
      newbal1=tup14[0]+trans
      #trans=trans+tup14[0] 
      #print('yes1')
      
      cur.execute("update bankdb3 set balance= :xnewbal1 where sno= :xtup13",{'xnewbal1':newbal1,'xtup13':tup13[0]})
      print('ammount transferred')
      #print('new balance is ',newbal1) 
      con.commit()     
  else:
      print("transfer amount is more than balance")
      print("retry again")
  #printnextentry(accno,rcv)

      
def ACCOUNTCLOSURE(accno): 
  con=cx_Oracle.connect("pranav/pranav@xe")
  cur=con.cursor()
  cur.execute("update bankdb3 set ACC_CLOSED='Y',close_date=CURRENT_TIMESTAMP where acc_no= :xaccno",{'xaccno':accno})
  cur.execute("select balance from bankdb3 where acc_no= :xaccno",{'xaccno':accno})
  amt=cur.fetchall()
  con.commit()
  con.close
  print('account no.',accno,'has been closed')
  tup=amt[0]
  print('amount of Rs. ',tup[0],'will be sent to your residence')

def printnextentry(accno):
  con=cx_Oracle.connect("pranav/pranav@xe")
  cur=con.cursor()
  cur.execute("""select max(sno) from bankdb3 where acc_no= :xaccno""",{'xaccno':accno})
  a=cur.fetchall()
  b=a[0]
  #print(b[0])
  #cur.execute("""select sno from bankdb2 where sno= :xb""",{'xb':b[0]})
  #c=cur.fetchall()
  #d=c[0]
  
  cur.execute("""select customer_id from bankdb3 where sno= :xb""",{'xb':b[0]})
  x=cur.fetchall()
  tup1=x[0]
  cur.execute("""select acc_holder_name from bankdb3 where sno= :xb""",{'xb':b[0]})
  x=cur.fetchall()
  tup2=x[0]
  cur.execute("""select password from bankdb3 where sno= :xb""",{'xb':b[0]})
  x=cur.fetchall()
  tup3=x[0]
  cur.execute("""select address from bankdb3 where sno= :xb""",{'xb':b[0]})
  x=cur.fetchall()
  tup4=x[0]
  cur.execute("""select balance from bankdb3 where sno= :xb""",{'xb':b[0]})
  x=cur.fetchall()
  tup5=x[0]
  cur.execute("""select acc_closed from bankdb3 where sno= :xb""",{'xb':b[0]})
  x=cur.fetchall()
  tup6=x[0]
  cur.execute("""select close_date from bankdb3 where sno= :xb""",{'xb':b[0]})
  x=cur.fetchall()
  tup7=x[0]
  cur.execute("""select acc_type from bankdb3 where sno= :xb""",{'xb':b[0]})
  x=cur.fetchall()
  tup8=x[0]
  cur.execute("""select blocked from bankdb3 where sno= :xb""",{'xb':b[0]})
  x=cur.fetchall()
  tup9=x[0]
  cur.execute("""select trans_type from bankdb3 where sno= :xb""",{'xb':b[0]})
  x=cur.fetchall()
  tup10=x[0]  
  cur.execute("""select fd_acc_no from bankdb3 where sno= :xb""",{'xb':b[0]})
  x=cur.fetchall()
  tup11=x[0]
  cur.execute("""select loan_acc_no from bankdb3 where sno= :xb""",{'xb':b[0]})
  x=cur.fetchall()
  tup12=x[0]
  cur.execute("""insert into bankdb3 values(:xtup1,:xaccno,:xtup2,:xtup3,:xtup4,:xtup5,:xtup6,:xtup7,:xtup8,:xtup9,:xtup10,CURRENT_TIMESTAMP,sno.nextval,CURRENT_TIMESTAMP,:xtup11,:xtup12)""",{'xtup1':tup1[0],'xaccno':accno,'xtup2':tup2[0],'xtup3':tup3[0],'xtup4':tup4[0],'xtup5':tup5[0],'xtup6':tup6[0],'xtup7':tup7[0],'xtup8':tup8[0],'xtup9':tup9[0],'xtup10':tup10[0],'xtup11':tup11[0],'xtup12':tup12[0]}) 
  con.commit()
  con.close
  

def checkadminsignin():
  print('enter user name')
  usrnm=input()
  print('enter password')
  passwd=input()
  con=cx_Oracle.connect("pranav/pranav@xe")
  cur=con.cursor()
  cur.execute("select usrnm from admintable") 
  data=cur.fetchall()
  tup=data[0]
  cur.execute("select passwd from admintable") 
  data1=cur.fetchall()
  tup1=data1[0]
  con.close
  if(usrnm==tup[0] and passwd==tup1[0]):
      adminsignin()
  else:
      print('USERNAME AND PASSWORD IS INCORRECT')

def fdreport():
  print('enter customer_id')
  cid=int(input())
  con=cx_Oracle.connect("pranav/pranav@xe")
  cur=con.cursor()
  cur.execute("select fd_acc_no,amount,term from fd where customer_id= :xcid",{'xcid':cid})
  print (tabulate(cur.fetchall(), headers="keys"))
  #tup=(cur.fetchall())
  #print(tup)
  con.close

def loanreport():
  print('enter customer_id')
  cid=int(input())
  con=cx_Oracle.connect("pranav/pranav@xe")
  cur=con.cursor()
  cur.execute("select loan_acc_no,amount,term from loan where customer_id= :xcid",{'xcid':cid})
  print (tabulate(cur.fetchall(), headers="keys"))
  #tup=(cur.fetchall())
  #print(tup)
  con.close
      
def adminsignin():  
  print ('press 1  : CLOSURE HISTORY')
  print ('press 2  : FD REPORT OF A CUSTOMER')
  print ('press 3  : FD REPORT OF A CUSTOMER vis - a - vis ANOTHER CUSTOMER')
  print ('press 4  : FD REPORT W.R.T. A PERTICULAR AMOUNT')
  print ('press 5  : LOAN REPORT OF A CUSTOMER')
  print ('press 6  : LOAN REPORT OF A CUSTOMER vis - a - vis ANOTHER CUSTOMER')
  print ('press 7  : LOAN REPORT W.R.T. A PERTICULAR LOAN AMOUNT')
  print ('press 8  : LOAN FD REPORT OF A CUSTOMER')
  print ('press 9  : REPORT OF CUSTOMER WHO ARE YET TO AVAIL LOAN')
  print ('press 10 : REPORT OF CUSTOMER WHO ARE YET TO OPEN FD ACCOUNT')
  print ('press 11 : REPORT OF CUSTOMER WHO HVE NEITHER HAVE LOAN OR FD WITH THE BANK')
  print ('press 0  : LOGOUT')
  print ('--------------------------------------------------------------')
  n=int(input())

  while(n!=0):
      if(n==1):
        con=cx_Oracle.connect("pranav/pranav@xe")
        cur=con.cursor()
        cur.execute("select ACC_NO,customer_id,close_date from bankdb3 where ACC_CLOSED='Y' order by SESSION_DATE")
       # tup=(cur.fetchall())
       #print(tup)
        print (tabulate(cur.fetchall(), headers="keys"))
        con.close  
      elif(n==2):
        fdreport()
      #elif(n==3):
        #fdreportvisavis()
      #elif(n == 4):
        #fdwrt()
      elif(n==5):
        loanreport()
      #elif(n==6):
        #loanreportvisavis()
      #elif(n==7):
        #loanwrt()
      #elif(n==8):
        #loanfd()
      #elif(n==9):
        #yetloan()
      #elif(n==10):
       # yetfd()
     # elif(n==11):
       # never()
      else:
        print('invalid option')
      print ('press 1  : CLOSURE HISTORY')
      print ('press 2  : FD REPORT OF A CUSTOMER')
      print ('press 3  : FD REPORT OF A CUSTOMER vis - a - vis ANOTHER CUSTOMER')
      print ('press 4  : FD REPORT W.R.T. A PERTICULAR AMOUNT')
      print ('press 5  : LOAN REPORT OF A CUSTOMER')
      print ('press 6  : LOAN REPORT OF A CUSTOMER vis - a - vis ANOTHER CUSTOMER')
      print ('press 7  : LOAN REPORT W.R.T. A PERTICULAR LOAN AMOUNT')
      print ('press 8  : LOAN FD REPORT OF A CUSTOMER')
      print ('press 9  : REPORT OF CUSTOMER WHO ARE YET TO AVAIL LOAN')
      print ('press 10 : REPORT OF CUSTOMER WHO ARE YET TO OPEN FD ACCOUNT')
      print ('press 11 : REPORT OF CUSTOMER WHO HVE NEITHER HAVE LOAN OR FD WITH THE BANK')
      print ('press 0  : LOGOUT')
      print ('--------------------------------------------------------------')
      n=int(input())
  print('logged out')
  
  
def opensavingaccount(accno):
  con=cx_Oracle.connect("pranav/pranav@xe")
  cur=con.cursor()
  
  cur.execute("""select max(customer_id) from bankdb3 where acc_no= :xaccno""",{'xaccno':accno})
  x=cur.fetchall()
  cust=x[0]

  cur.execute("""select acc_holder_name from bankdb3 where acc_no= :xaccno""",{'xaccno':accno})
  x=cur.fetchall()
  name=x[0]
  
  cur.execute("""select password from bankdb3 where acc_no= :xaccno""",{'xaccno':accno})
  x=cur.fetchall()
  password=x[0]

  cur.execute("""select address from bankdb3 where acc_no= :xaccno""",{'xaccno':accno})
  x=cur.fetchall()
  address=x[0]

  print("enter initial amount")
  amt=int(input())

  cur.execute("""insert into bankdb3 values(:cust,account.nextval,:xname,:xpassword,:xaddress,:xamt,'n',null,'s','n',null,CURRENT_TIMESTAMP,sno.nextval,CURRENT_TIMESTAMP,null,null)""",{'cust':cust[0],'xname':name[0],'xpassword':password[0],'xaddress':address[0],'xamt':amt})
  #print('your new account no. is ')
  con.commit()
  #con.close
  print('your saving account is created successfully')
  cur.execute("select max(customer_id) from bankdb3")
  print('your customer id is ')
  abc=(cur.fetchall())
  tup=abc[0]
  print(tup[0])
  cur.execute("select max(acc_no) from bankdb3")
  print('your account no. is ')
  abc1=(cur.fetchall())
  tup16=abc1[0]
  print(tup16[0])
  con.close
  
def opencurrentaccount(accno):
  con=cx_Oracle.connect("pranav/pranav@xe")
  cur=con.cursor()
  cur.execute("""select max(customer_id) from bankdb3 where acc_no= :xaccno""",{'xaccno':accno})
  x=cur.fetchall()
  cust=x[0]
  cur.execute("""select acc_holder_name from bankdb3 where acc_no= :xaccno""",{'xaccno':accno})
  x=cur.fetchall()
  name=x[0]
  
  cur.execute("""select password from bankdb3 where acc_no= :xaccno""",{'xaccno':accno})
  x=cur.fetchall()
  password=x[0]

  cur.execute("""select address from bankdb3 where acc_no= :xaccno""",{'xaccno':accno})
  x=cur.fetchall()
  address=x[0]

  print("enter initial amount")
  amt=int(input())

  cur.execute("""insert into bankdb3 values(:xcust,account.nextval,:xname,:xpassword,:xaddress,:xamt,'n',null,'c','n',null,CURRENT_TIMESTAMP,sno.nextval,CURRENT_TIMESTAMP,null,null)""",{'xcust':cust,'xname':name[0],'xpassword':password[0],'xaddress':address[0],'xamt':amt})
  #print('your new account no. is ')
  con.commit()
  #con.close
  print('your current account is created successfully')
  cur.execute("select max(customer_id) from bankdb3")
  print('your customer id is ')
  abc=(cur.fetchall())
  tup=abc[0]
  print(tup[0])
  cur.execute("select max(acc_no) from bankdb3")
  print('your account no. is ')
  abc1=(cur.fetchall())
  tup16=abc1[0]
  print(tup16[0])
  con.close  
  
def openfixeddeposit(accno):
  print('enter the amount to make fixed deposit(amount should not less then Rs.1000)')
  amt=int(input())
  print('enter the term (IN MONTHS) for which you want to make fixed deposit(term should not less then 12 months)')
  term=int(input())
  if(amt>=1000 and term>=12):
      con=cx_Oracle.connect("pranav/pranav@xe")
      cur=con.cursor()
      cur.execute("select max(customer_id) from bankdb3 where acc_no = :xaccno",{'xaccno':accno})
      cust1=cur.fetchall()
      tup=cust1[0]
      cur.execute("insert into fd values(:xtup,sno.nextval,fdaccseq.nextval,:xamt,:xterm)",{'xtup':tup[0],'xamt':amt,'xterm':term})
      cur.execute("select max(fd_acc_no) from fd")
      print('your FD account no. is ')
      facno=(cur.fetchall())
      tup2=facno[0]
      print(tup2[0]) 
      con.commit()        
      con.close
  else:
      print('enter correct value of amount and term')

def checkloan(accno):
  con=cx_Oracle.connect("pranav/pranav@xe")
  cur=con.cursor()
  cur.execute("select max(customer_id) from bankdb3 where acc_no = :xaccno",{'xaccno':accno})
  cust1=cur.fetchall()
  tup123=cust1[0]
  
  cur.execute("""select max(sno) from bankdb3 where acc_no= :xaccno""",{'xaccno':accno})
  a=cur.fetchall()
  b=a[0] 
  cur.execute("""select balance from bankdb3 where sno= :xb""",{'xb':b[0]})
  x=cur.fetchall()
  bal=x[0]  
  cur.execute("select sum(amount) from loan where customer_id = :xcust",{'xcust':tup123[0]})
  cust1=cur.fetchall()
  tup=cust1[0]
  print('enter the amount to apply for loan(multiple of 1000)')
  amt=int(input())  
  if((tup[0]+amt)<=(2*bal[0])):
      availloan(accno,amt)
  else:
      print('not eligible for loan')
            
def availloan(accno,amt):
  print('enter the repayment term (IN MONTHS) of loan')
  term=int(input())
  if(amt % 1000 == 0):
      con=cx_Oracle.connect("pranav/pranav@xe")
      cur=con.cursor()
      cur.execute("select max(customer_id) from bankdb3 where acc_no = :xaccno",{'xaccno':accno})
      cust1=cur.fetchall()
      tup=cust1[0]
      cur.execute("insert into loan values(:xtup,sno.nextval,loanaccseq.nextval,:xamt,:xterm)",{'xtup':tup[0],'xamt':amt,'xterm':term})
      cur.execute("select max(loan_acc_no) from loan")
      print('your loan senctioned successflly')
      print('your loan account no. is ')
      lacno=(cur.fetchall())
      tup2=lacno[0]
      print(tup2[0]) 
      con.commit()        
      con.close
  else:
      print('enter correct amount')

def opennewaccount(accno):
  print ('press 1 : TO OPEN SAVING ACCOUNT')
  print ('press 2 : TO OPEN CURRENT ACCOUNT')
  print ('press 3 : TO OPEN FIXED DEPOSIT')
  print ('press 4 : TO GO BACK')
  print ('--------------------------------------------------------------')
  n=int(input())
  while(n!=4):
        if(n==1):
            print ("you have selected 1 TO OPEN SAVING ACCOUNT")
            opensavingaccount(accno)
        elif(n==2):
            print ("you have selected 2 TO OPEN CURRENT ACCOUNT")
            opencurrentaccount(accno)
        elif(n==3):
            print ("you have selected 3 TO OPEN FIXED DEPOSIT")
            openfixeddeposit(accno)
        else: 
            print ("invalid option") 
        print ('press 1 : TO OPEN SAVING ACCOUNT')
        print ('press 2 : TO OPEN CURRENT ACCOUNT')
        print ('press 3 : TO OPEN FIXED DEPOSIT')
        print ('press 4 : TO GO BACK')
        print ('--------------------------------------------------------------')
        n=int(input())
  
    
def sign_in_submenu(accno):
  print ('press 1 : ADDRESS CHANGE')
  print ('press 2 : OPEN NEW ACCOUNT')
  print ('press 3 : MONEY DEPOSIT')
  print ('press 4 : MONEY WITHDRAWAL')
  print ('press 5 : PRINT STATEMNT')
  print ('press 6 : TRANSFER MONEY')
  print ('press 7 : ACCOUNT CLOSURE(Y/N)')
  print ('press 8 : Avail loan')
  print ('press 0 : CUSTOMER LOGOUT')
  print ('--------------------------------------------------------------')
  n=int(input())
  while(n!=0):
         
        if(n==1):
            print ("you have selected 1 for address change")
            addrchange(accno)
        elif(n==2):
            print ("you have selected 2 to open new account")
            opennewaccount(accno)
        elif(n==3):
            print ("you have selected 3 for MONEY DEPOSIT")
            moneydeposit(accno)           
        elif(n==4):
            print ("you have selected 4 for MONEY WITHDRAWAL")
            moneywithdrawal(accno)
        elif(n==5):
            print ("you have selected 5 for PRINT STATEMNT")
            printstatement(accno)
        elif(n==6):
            print ("you have selected 6 for TRANSFER MONEY")
            TRANSFERMONEY(accno)
        elif(n==7):
            print ("you have selected 7 for ACCOUNT CLOSURE")
            ACCOUNTCLOSURE(accno)
        elif(n==8):
            print("you have selected 8 to avail loan")
            checkloan(accno)
        elif(n==0):
            print ("you have selected 0 for CUSTOMER LOGOUT")
        else: 
            print ("invalid option")  
        print ('press 1 : ADDRESS CHANGE')
        print ('press 2 : OPEN NEW ACCOUNT')
        print ('press 3 : MONEY DEPOSIT')
        print ('press 4 : MONEY WITHDRAWAL')
        print ('press 5 : PRINT STATEMNT')
        print ('press 6 : TRANSFER MONEY')
        print ('press 7 : ACCOUNT CLOSURE(Y/N)')
        print ('press 8 : Avail loan')
        print ('press 0 : CUSTOMER LOGOUT')
        print ('--------------------------------------------------------------')
        n=int(input())
        

def sign_in():
    n=1
    while(n<4):
        print('enter your customer_id')
        cust=int(input())
        print('enter your password')
        pas=input()
        con=cx_Oracle.connect("pranav/pranav@xe")
        cur=con.cursor()
        cur.execute("select acc_closed from bankdb3 where customer_id=:xcust""",{'xcust':cust})
        YorN=cur.fetchall()
        
        cur.execute("select blocked from bankdb3 where customer_id=:xcust""",{'xcust':cust})
        YorNcust=cur.fetchall()
        
        con.close
        print('yes')
        tup=YorN[0]
        #print(tup[0])
        tup1=YorNcust[0]
        #print(tup1[0])
        if(tup[0]=='y'):
            print("your account is closed")
            break
        elif(tup1[0]=='y'):
            print("your account is blocked because of more then 3 incorrect customer id or password")
            break
        else:
            try:       
                con=cx_Oracle.connect("pranav/pranav@xe")
                cur=con.cursor()
                cur.execute("""select acc_no from bankdb3 where customer_id= :xcust and password= :xpas""",{'xcust':cust,'xpas':pas})
                acc=cur.fetchall()
                #check=str(cur.fetchall())
                check=str(acc)
                if(check=='[]'):
                    print("either your customer id incorrect")
                    print("or password incorrect")
                    n=n+1
                
                else:
                    print('your account no. is ')
                    #print(check)
                    tup=acc[0]
                    print(tup[0])                
                    sign_in_submenu(tup[0])
                    break
                #con.close()
            except:
                con.close()
            
    if(n>=4):
        con=cx_Oracle.connect("pranav/pranav@xe")
        cur=con.cursor()
        cur.execute("update bankdb3 set blocked= 'Y' where customer_id=:xcust""",{'xcust':cust})
        #YorNcust=cur.fetchall()
        con.close
        
        
def main_menu():
  print ('press 1 : SIGN UP(new customer)')
  print ('press 2 : SIGN IN(existing customer)')
  print ('press 3 : ADMIN SIGN IN')
  print ('press 4 : EXIT')
  #print ('--------------------------------------------------------------')
  #print ('press 1 to continue')
  n=int(input())
  while(n!=4):
                  
        if(n==1):
            print ("you have selected 1 to SIGN UP")
            sign_up()
        elif(n==2):
            print ("you have selected 2 to SIGN IN")
            sign_in()
        elif(n==3):
            print ("you have selected 3 to ADMIN SIGN IN")
            checkadminsignin()
        elif(n==4):
            print ("you have selected 4 to exit")
        else: 
            print ("invalid option")
        print ('press 1 : SIGN UP(new customer)')
        print ('press 2 : SIGN IN(existing customer)')
        print ('press 3 : ADMIN SIGN IN')
        print ('press 4 : EXIT')
        print ('--------------------------------------------------------------')
        n=int(input())
   

if __name__ == '__main__':
  main_menu()

