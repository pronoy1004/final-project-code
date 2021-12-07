import database
from database import ApplicationQueries 
def run_app(user_name):
    inp = 'y'


    
    print("Welcome to our Database Project, select the options to choose what you'd like to see :   ")
    
    print("Enter")
    
    print("1: ")
    
    print("2: ")
    
    print("3: ")
    
    print("4: ")
    
    print("5: ")
    
    print("Enter x to Exit")
    
    inp = input()

    _ = None
    if(inp == 'x'):
        return
    elif(inp == '1'):
        ApplicationQueries.query1(_,user_name)

    elif(inp == '2'):
        ApplicationQueries.query2(_,user_name)

    elif(inp == '3'):
        ApplicationQueries.query3(_,user_name)

    elif(inp == '4'):
        ApplicationQueries.query4(_,user_name)

    elif(inp == '5'):
        ApplicationQueries.query5(_,user_name)

    else:
        print("Incorrect choice, please select again! ")

    print("Thank you!")


def set_up():
    log = 1 
    while(log == 1):
        
        print("Hello User! Login/Register? : ")

        
        print("1.Login: ")
            
        print("2.Register: ")
        


        log=input()

        
        if(log == '1'):
            user_name = input("Enter User Name : ")
            y = ApplicationQueries.login(user_name)
            if(y == 1):
                run_app(user_name)
            elif(y == 0):
                print("Incorrect User Name")
    return log

if __name__ == "__main__":
    #query = ApplicationQueries()

    #### Login/Register ####

    log = set_up()

    if(log == '2'):
        user_name = input("Enter User Name : ")
        y = ApplicationQueries.register(user_name)
        if(y == 1):
            set_up()
        elif(y == 0):
            print("Error!")
    elif(log == '1'):
        print("Thank You!")
    else:
        print("Incorrect choice, please select again! ")

    # print("Hello User! Login/Register? : ")

    
    # print("1.Login: ")
        
    # print("2.Register: ")

    # log=input()

    
    # if(log == '1'):
    #     y = query.login()
    #     if(y == 1):
    #         run_app()
    #     elif(y == 0):
    #         print("Incorrect User Name")

    # elif(log == '2'):
    #     query.register()
    #     if(y == 1):
    #         ()
    #     elif(y == 0):
    #         print("Error!")

    # else:
    #     print("Incorrect choice, please select again! ")


