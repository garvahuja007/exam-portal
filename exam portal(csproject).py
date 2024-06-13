import mysql.connector
print('\t\t\t\t\tEXAM PORTAL')


def utype():
    print('1. Teacher Login')
    print('2. Student Login')
    print('3. Exit')
    user_type=input()
    if user_type not in ('1','2','3'):
        print('Invalid entry')
        print('\n')
        utype()
    elif user_type=='1':
        print('\n')
        t_signup()
    elif user_type=='2':
        print('\n')
        stu_login()
    elif user_type=='3':
        print('Exiting portal, please wait...')
        return 532
def t_signup():
    print('1. New User')
    print('2. Existing User')
    print('3. Main Menu')
    t_user=input()
    if t_user not in ('1','2','3'):
        print('Invalid entry')
        print('\n')
        t_signup()
    elif t_user=='1':
        print('   INSTRUCTIONS-')
        print('1. Account ID must not have space in between the characters and must contain at least one letter.')
        print('2. Account ID must not contain any special characters.')
        print('3. Password must contain at least 8 characters.')
        print('4. Note that IDs are not case sensitive.')
        print('5. Enter \'EXIT\' in the field to go back to Main Menu.')
        print('\n')
        new_user()
    elif t_user=='2':
        print('\n')
        existing_user()
    elif t_user=='3':
        print('\n')
        utype()
def new_user():
    mydb=mysql.connector.connect(host='localhost',user='root',password='garv007')
    cur=mydb.cursor()
#inputing name
    acc_name=input('Enter full name: ')
    if acc_name=='EXIT':
        print('\n')
        utype()
#inputing id
    acc_id=input('Enter ID for your account: ')
    for i in range(len(acc_id)):
        if acc_id[i].isspace():
            print('Error:ID must not contain space between characters')
            print('\n')
            mydb.close()
            new_user()
    if acc_id=='EXIT':
        print('\n')
        mydb.close()
        utype()
    d=0
    for i in range (len(acc_id)):
        if acc_id[i].isalnum():
            if acc_id[i].isalpha():
                d+=1
                
            elif acc_id[i].isdigit():
                continue
        else:
            print('Error: Account ID must not contain special characters')
            mydb.close()
            new_user()
    if d==0:
        print('Error: Account ID must contain at least one letter')
        mydb.close()
        new_user()
            
#inputing password
    acc_pass=input('Enter password: ')
    if acc_pass=='EXIT':
        print('\n')
        utype()
    if len(acc_pass)<8:
        print('Error:Password must be more than 8 characters')
        print('\n')
        mydb.close()
        new_user()
    acc_passconfirm=input('Confirm password: ')
    if acc_pass!=acc_passconfirm:
        print('Error:Passwords do not match')
        print('\n')
        mydb.close()
        new_user()
#creating dtabase and table
    
    try:
        #syntax to enter variable as database/table name
        cur.execute('create database '+str(acc_id)+';')
    except mysql.connector.Error as error:
        if error.sqlstate=='HY000':
            print('Error:ID already exists')
            print('\n')
            mydb.close()
            new_user()
    
    cur.execute('use '+str(acc_id)+';')
    cur.execute('create table account(name varchar(30),ID varchar(50) primary key,password varchar(50));')
    #syntax to enter variables into table
    cur.execute('insert into account values(%s, %s, %s);',(str(acc_name), str(acc_id), str(acc_pass)))
    mydb.commit()
    mydb.close()
    print('Account successfully created!')
    print('\n')
    utype()

def existing_user():
    
    acc_id=input('Enter account ID(Enter \'EXIT\' to go back to Main Menu): ')
    if acc_id=='EXIT':
        utype()
    mydb=mysql.connector.connect(host='localhost',user='root',password='garv007')
    cur=mydb.cursor()
    try:
        cur.execute('use '+acc_id+';')
    except mysql.connector.Error as err:
        if err.sqlstate=='42000':
            print('Error:ID does not exist')
            print('\n')
            mydb.close()
            existing_user()
    password=input('Enter password(Enter \'EXIT\' to go back to Main Menu): ')
    if password=='EXIT':
        mydb.close()
        utype()
    cur.execute('select password from account;')
    passw=cur.fetchone()
    if password==passw[0]:
        print('login succesful')
        cur.execute('select name from account')
        n=cur.fetchone()
        print()
        print('Welcome back '+n[0])
        print()
        t_actions(acc_id)
        mydb.commit()
        mydb.close()
        
    else:
        print('Incorrect password')
        mydb.close()
        print('\n')
        existing_user() 
def t_actions(acc_id):
    print('1. Create question paper')
    print('2. Modify existing question paper')
    print('3. Delete question paper')
    print('4. Display question paper')
    print('5. Log out')
    qp=input()
    if qp not in ('1','2','3','4','5'):
        print("Invalid entry")
        print('\n')
        t_actions(acc_id)
    if qp=='1':
        create_qp(acc_id)
    elif qp=='2':
        mod_qp(acc_id)
    elif qp=='3':
        del_qp(acc_id)
    elif qp=='4':
        show_qp(acc_id)
    
        
    else:
        print('\n')
        utype() 

def create_qp(acc_id):
     
    mydb=mysql.connector.connect(host='localhost',user='root',password='garv007',database=''+acc_id+'')
    cur=mydb.cursor()
    print('   Instructions:')
    print('1. Questions should be MCQ, Fill in the blanks or one word answer type.')
    print('2. In field \'Question Type\' enter \'MCQ\' for MCQ questions and \'OW\' for one word answer, fill in blanks questions.')
    print('3. Marks for each question must be integers.')
    print('4. Question paper name must not have space in it')
    while True:
        qp_name=input('Enter question paper name(Enter \'EXIT\' to go back to Main Menu): ')
        if qp_name=='EXIT':
            print()
            mydb.close()
            utype()
        x=0
        for i in qp_name:
            if i==' ':
                x=1
                break
        if x==1:
            print('Error: Question paper name must not contain space')
            continue
        try:
            cur.execute('create table '+qp_name+'''(qno int primary key,qtype varchar(3),question varchar(60),
                                                        optionA varchar(60),optionB varchar(60),optionC varchar(60),
                                                        optionD varchar(60),answer varchar(30),MM int);''')
        except mysql.connector.Error as err:
            if err.sqlstate=='42S01':
                print('This question paper already exists')
                continue
        break
    q_no=int(input('Enter number of questions: '))
    print()
    print('ENTER QUESTIONS:')
    print()
    i=0
    while i<q_no:
        print('QUESTION ',i+1)
        qtype=input('Enter question type: ')
        if qtype not in ['MCQ','OW']:
            print('Invalid type')
            continue
        
        if qtype=='MCQ':
            ques=input('Enter question: ')
            a=input('A:')
            b=input('B:')
            c=input('C:')
            d=input('D:')
            ans=input('Answer(A/B/C/D): ')
            if ans not in ['A','B','C','D']:
                print('Invalid answer')
                continue
            try:
                marks=int(input('Enter marks: '))
            except ValueError:
                print('Error:Marks must be integer type')
                continue
        else:
            ques=input('Enter question: ')
            a=b=c=d='NULL'
            ans=input('Enter answer: ')
            try:
                marks=int(input('Enter marks: '))
            except ValueError:
                print('Error:Marks must be integer type')
                continue
        i+=1
        try:
            cur.execute('insert into '+qp_name+' values (%s,%s,%s,%s,%s,%s,%s,%s,%s);',(i,qtype,ques,a,b,c,d,ans,marks))
        except mysql.connector.Error as err:
            print(err.msg)
    mydb.commit()
    mydb.close()
    print('QUESTION PAPER SUCCESSFULLY CREATED')
    print()
    t_actions(acc_id)

def mod_qp(acc_id):
    mydb=mysql.connector.connect(host='localhost',user='root',password='garv007',database=''+acc_id+'')
    cur=mydb.cursor()
    print()
    qp_name=input('Enter name of question paper you want to modify: ')
    cur.execute('show tables;')
    st=cur.fetchall()
    c=0
    for i in st:
        if i[0]==qp_name:
            c=1
            break
        else:
            continue
    if c==1:
        print()
    else:
        print('Error:Paper does not exist')
        print()
        mydb.close()
        mod_qp(acc_id)
    x=0
    while x==0:
        print('1. Change question paper name')
        print('2. Change question')
        print('3. Change answer key')
        mod=input()
        if mod not in ['1','2','3']:
            print('Invalid entry')
            
        else:
            x+=1
        
    if mod=='1':
        qp_new=input('Enter new name: ')
        cur.execute('alter table '+qp_name+' rename to '+qp_new+';')
        print('QUESTION PAPER NAME SUCCESSFULLY CHANGED!')
        print()
        
    elif mod=='2':
        print('Displaying paper ',qp_name)
        print()
        cur.execute('select * from '+qp_name+';')
        qp_l=cur.fetchall()
        #displaying the question paper
        for i in qp_l:
            if i[1]=='OW':
                print('Q.'+str(i[0])+' ',i[2],'(MM:',i[8],')')
                print('Ans.'+i[-2])
                print()
            else:
                print('Q.'+str(i[0])+' ',i[2],'(MM:',i[8],')')
                print('A.',i[3])
                print('B.',i[4])
                print('C.',i[5])
                print('D.',i[6])
                print('Ans.'+i[-2])
                print()
                
        while True:
            qno_mod=int(input('Enter Q.No of the question you want to modify(\'N\' if you dont wish to make more changes): '))
            if qno_mod> len(qp_l):
                print('Invalid question number')
                continue
            if qno_mod=='N':
                break
            qtype=input('Enter new question type(\'OW\' or \'MCQ\'): ')
            if qtype not in ['MCQ','OW']:
                print('Invalid type')
                continue
        
            if qtype=='MCQ':
                ques=input('Enter new question: ')
                a=input('A:')
                b=input('B:')
                c=input('C:')
                d=input('D:')
                ans=input('Answer(A/B/C/D): ')
                if ans not in ['A','B','C','D']:
                    print('Invalid answer')
                    continue
                try:
                    marks=int(input('Enter marks: '))
                except ValueError:
                    print('Error:Marks must be integer type')
                    continue
            else:
                ques=input('Enter new question: ')
                a=b=c=d='NULL'
                ans=input('Enter answer: ')
                try:
                    marks=int(input('Enter marks: '))
                except ValueError:
                    print('Error:Marks must be integer type')
                    continue    
            cur.execute('update '+qp_name+' set qtype= \''+qtype+'\' where qno='+str(qno_mod)+';')
            cur.execute('update '+qp_name+' set question= \''+ques+'\' where qno='+str(qno_mod)+';')
            cur.execute('update '+qp_name+' set optionA= \''+a+'\' where qno='+str(qno_mod)+';')
            cur.execute('update '+qp_name+' set optionB= \''+b+'\' where qno='+str(qno_mod)+';')
            cur.execute('update '+qp_name+' set optionC= \''+c+'\' where qno='+str(qno_mod)+';')
            cur.execute('update '+qp_name+' set optionD= \''+d+'\' where qno='+str(qno_mod)+';')
            cur.execute('update '+qp_name+' set answer= \''+ans+'\' where qno='+str(qno_mod)+';')
            cur.execute('update '+qp_name+' set MM='+marks+' where qno='+str(qno_mod)+';')
            mydb.commit()
        print('QUESTION PAPER UPDATED!')
    else:
        print('Displaying paper',qp_name)
        print()
        cur.execute('select * from '+qp_name+';')
        qp_l=cur.fetchall()
        #displaying the question paper
        for i in qp_l:
            if i[1]=='OW':
                print('Q.'+str(i[0])+' ',i[2],'(MM:',i[8],')')
                print('Ans.'+i[-2])
                print()
            else:
                print('Q.'+str(i[0])+' ',i[2],'(MM:',i[8],')')
                print('A.',i[3])
                print('B.',i[4])
                print('C.',i[5])
                print('D.',i[6])
                print('Ans.'+i[-2])
                print()
        while True:
            qno_mod=int(input('Enter Q.No of the question you want to modify(\'0\' if you dont wish to make more changes): '))
            if qno_mod> len(qp_l):
                print('Invalid question number')
                continue
            if qno_mod==0:
                break
            ans_new=input('Enter new answer: ')
            cur.execute('update '+qp_name+' set answer= \''+ans_new+'\' where qno='+str(qno_mod)+';')
            mydb.commit()
    
        print('ANSWER KEY UPDATED!')
        print()    
    mydb.close()
    t_actions(acc_id)
    


def show_qp(acc_id):
    mydb=mysql.connector.connect(host='localhost',user='root',password='garv007',database=''+acc_id+'')
    cur=mydb.cursor()
    print()
    cur.execute('show tables;')
    st=cur.fetchall()
    while True:
        qp_name=input('Enter name of question paper: ')
       
        c=0
        for i in st:
            if i[0]==qp_name:
                c=1
                break
            else:
                continue
        if c==1:
            print()
            break
        else:
            print('Error:Paper does not exist')
            print()
            mydb.close()
            t_actions(acc_id)
        
    print('Displaying paper',qp_name)
    print()
    cur.execute('select * from '+qp_name+';')
    qp_l=cur.fetchall()
    #displaying the question paper
    for i in qp_l:
        if i[1]=='OW':
            print('Q.'+str(i[0])+' ',i[2],'(MM:',i[8],')')
            print('Ans.'+i[-2])
            print()
        else:
            print('Q.'+str(i[0])+' ',i[2],'(MM:',i[8],')')
            print('A.',i[3])
            print('B.',i[4])
            print('C.',i[5])
            print('D.',i[6])
            print('Ans.'+i[-2])
            print()
    mydb.close()
    while True:
        print('Enter 1 to go back to actions menu')
        gb=input()
        if gb=='1':
            break
        else:
            print('Invalid Input')
            continue
    print()
    t_actions(acc_id)
           
def del_qp(acc_id):
    mydb=mysql.connector.connect(host='localhost',user='root',password='garv007',database=''+acc_id+'')
    cur=mydb.cursor()
    print()
    while True:
        qp_name=input('Enter name of question paper: ')
        cur.execute('show tables;')
        st=cur.fetchall()
        c=0
        for i in st:
            if i[0]==qp_name:
                c=1
                break
            else:
                continue
        if c==1:
            print()
            break
        else:
            print('Error:Paper does not exist')
            print()
            mydb.close()
            t_actions(acc_id)
    
    while True:
        con=input('Are you sure you want to delete '+qp_name+'?(Y/N) ')
        if con=='Y':
            print('Deleting paper '+qp_name)
            cur.execute('drop table '+qp_name+';')
            mydb.commit()
            break
        elif con=='N':
            print('OK, Redirecting to actions menu...')
            break
        else:
            print('Invalid Entry')
            continue
    mydb.close()
    print()
    t_actions(acc_id)


def stu_login():
    name=input('Enter your name: ')
    s_name=''
    i=0
    while i<len(name):
        if name[i].isspace():
            i+=1
            continue
        else:
            s_name+=name[i]
            i+=1
    print('1. Attempt paper')
    print('2. Check previous paper result')
    while True:
        s_ch=input()
        if s_ch not in ['1','2']:
            print('Invalid entry')
            continue
        else:
            break
    if s_ch=='1':
        qp_choose(s_name)
    else:
        t_id=input('Enter ID of examiner: ')
        qp_name=input('Enter name of question paper: ')
        s_table=s_name+'_'+qp_name
        mydb=mysql.connector.connect(host='localhost',user='root',password='garv007')
        cur=mydb.cursor()
        try:
            cur.execute('use '+t_id+';')
    
        except mysql.connector.Error as err:
            if err.sqlstate=='42000':
                print('ID does not exist')
                mydb.close()
                stu_login()
        cur.execute("show tables;")
        qps=cur.fetchall()
        c=0
        for i in qps:
            if i[0]==qp_name:
                c=1
                break
            else:
                continue
        if c==1:
            result(qp_name,s_table,t_id)
        else:
            print('Error:Paper does not exist')
            print()
            mydb.close()
            stu_login()
        
        print()
def qp_choose(s_name):
    t_id=input('Examiner ID(Enter \'EXIT\' to go back to Main Menu): ')
    if t_id=='EXIT':
        utype()
    mydb=mysql.connector.connect(host='localhost',user='root',password='garv007')
    cur=mydb.cursor()
    try:
        cur.execute('use '+t_id+';')
    
    except mysql.connector.Error as err:
        if err.sqlstate=='42000':
            print('ID does not exist')
            mydb.close()
        qp_choose(s_name)
    
    cur.execute("show tables;")
    qps=cur.fetchall()
    while True:
        qp_name=input('Enter name of question paper you wish to attempt: ')
        c=0
        for i in qps:
            if i[0]==qp_name:
                c=1
                break
            else:
                continue
        if c==1:
            print()
            break
        else:
            print('Error:Paper does not exist')
            print()
            mydb.close()
            qp_choose(s_name)
    cur.execute('select * from '+qp_name+';')
    qp_l=cur.fetchall()
    print('   INSTRUCTIONS')
    print('''1. Once the paper starts, the whole paper has to be attempted in
   one go ie. you can not exit from the portal without attempting the entire paper.''')
    print('''2. To skip a question enter \'SKIP\' as the answer.''')
    print('''3. You will have the option of re-attempting the skipped questions once you have
   viewed every question.''')
    print()
    print('BEST OF LUCK!!')
    print()
    while True:
        print('Enter 1 to start test')
        x=input()
        if x=='1':
            print()
            break
        else:
            print('Invalid input')
            continue
    s_table=s_name+'_'+qp_name
    try:
        cur.execute('create table '+s_table+' (qno int primary key, answer_entered varchar(30))')
    except mysql.connector.Error as err:
        if str(err.sqlstate)=='42S01':
            print('You have already attempted this paper once. You cannot attempt a paper more than once.')
            mydb.close()
            stu_login()
            
    mydb.commit()
    mydb.close()
    qp_attempt(qp_l,t_id,s_table,qp_name)
    
    
def qp_attempt(qp_l,t_id,s_table,qp_name):
    
    l=[]
    i=0
    
    while i<len(qp_l):
        if qp_l[i][1]=='OW':
            print('Q.'+str(qp_l[i][0])+' ',qp_l[i][2],'(MM:',qp_l[i][8],')')
            s_ans=input('Enter answer: ')
            if s_ans=='SKIP':
                l.append(qp_l[i][0])
                i+=1
            else:
                enter_answer(qp_l[i][0],s_ans,s_table,t_id)
                i+=1
            print()
        else:
            print('Q.'+str(qp_l[i][0])+' ',qp_l[i][2],'(MM:',qp_l[i][8],')')
            print('A.',qp_l[i][3])
            print('B.',qp_l[i][4])
            print('C.',qp_l[i][5])
            print('D.',qp_l[i][6])
            while True:
                s_ans=input('Enter answer(A/B/C/D): ')
                if s_ans not in ['A','B','C','D']:
                    print('Invalid answer, pls enter one of the options')
                    continue
                else:
                    break
            if s_ans=='SKIP':
                l.append(qp_l[i][0])
                i+=1
            else:
                enter_answer(qp_l[i][0],s_ans,s_table,t_id)
                i+=1
            print()
    if l!=[]:
        print('You have skipped the following questions- ')
        print(l)
        print('Enter 1 to re-attempt them(any other input will take you to the submitting page)')
        c=input()
        if c=='1':
            for j in qp_l:
                if j[0] in l:
                    if j[1]=='OW':
                        print('Q.'+str(j[0])+' ',j[2],'(MM:',j[8],')')
                        r_ans=input('Enter answer: ')
                        enter_answer(j[0],r_ans,s_table,t_id)
                        print()
                    else:
                        print('Q.'+str(j[0])+' ',j[2],'(MM:',j[8],')')
                        print('A.',j[3])
                        print('B.',j[4])
                        print('C.',j[5])
                        print('D.',j[6])
                        while True:
                            r_ans=input('Enter answer(A/B/C/D): ')
                            if r_ans not in ['A','B','C','D']:
                                print('Invalid answer, pls enter one of the options')
                                continue
                            else:
                                break
                        enter_answer(j[0],r_ans,s_table,t_id)
                        print()
    print('PAPER ATTEMPTED')
    print('Press any key to submit ')
    sub=input()
    print('PAPER SUBMITTED')
    print('Redirecting to result page...')
    result(qp_name,s_table,t_id)

def enter_answer(qno,ans,s_table,t_id):
    mydb=mysql.connector.connect(host='localhost',user='root',password='garv007',database=''+t_id+'')
    cur=mydb.cursor()
    cur.execute('insert into '+s_table+' values(%s,%s);',(qno,ans))
    mydb.commit()
    mydb.close()

def result(qp_name,s_table,t_id):
    mydb=mysql.connector.connect(host='localhost',user='root',password='garv007',database=''+t_id+'')
    cur=mydb.cursor()
    cur.execute('select MM from '+qp_name+','+s_table+' where '+qp_name+'.answer='+s_table+'.answer_entered;')
    m_list=cur.fetchall()
    totalmarks=0
    for i in m_list:
        totalmarks+=i[0]
    print()
    print('Total marks obtained is',totalmarks)
    print()
    choice=input('Enter \"Yes\" to get a detailed result(any other input will redirect you to main menu) ')
    print()
    if choice=="Yes":
        cur.execute('select * from '+qp_name+','+s_table+' where '+s_table+'.qno='+qp_name+'.qno;')
        det_result=cur.fetchall()
        print(' Q.No. | Question | A | B | C | D | answer | MM | answer entered |')
        for i in det_result:
            print(' ',i[0],' |',i[2],'|',i[3],'|',i[4],'|',i[5],'|',i[6],'|',i[7],'|',i[8],'|',i[10])
        mydb.close()
        while True:
            print('Enter 1 to go back to main menu')
            x=input()
            if x=='1':
                print('Redirecting to main menu...')
                break
            else:
                print('Invalid input')
                continue
        print()
        utype()
    else:
        mydb.close()
        utype()
    
c=utype()
if c==532:
    print()
