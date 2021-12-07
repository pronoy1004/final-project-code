import database
def run_app():
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
    if(inp == 'x'):
        return
    elif(inp == '1'):
        query.query1()

    elif(inp == '2'):
        query.query2()

    elif(inp == '3'):
        query.query3()

    elif(inp == '4'):
        query.query4()

    elif(inp == '5'):
        query.query5()

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
            y = query.login()
            if(y == 1):
                run_app()
            elif(y == 0):
                print("Incorrect User Name")
    return log

if __name__ == "__main__":
    query = database.ApplicationQueries()

    #### Login/Register ####

    log = set_up()

    if(log == '2'):
        y = query.register()
        if(y == 1):
            set_up()
        elif(y == 0):
            print("Error!")
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


