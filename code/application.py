import database
from database import ApplicationQueries

def run_app(user_name):
    inp = 'y'

    print("\nWelcome to our Database Project, select the options to choose what you'd like to see.\n")
    
    print("Enter:\n")
    
    print("""1: Identify hospitals in counties with river flood or coastal flood risk index above a user-defined threshold.\n""")
    
    print("""2: Identify hospitals in counties with river flood or coastal flood risk index above a user-defined threshold
    and show average monthly rainfall.\n""")
    
    print("""3: Identify hospitals in counties with river flood risk index above a user-defined
    threshold. For each high-risk hospital, identify hospitals of the same type with river flood risk index below a user-defined
    threshold within a user-defined mile radius.\n""")
    
    print("""4: List states in order of largest population living in counties with composite risk index above a user-defined threshold.\n""")
    
    print("""5: Display the number of hospitals per county in counties with composite risk index above a user-defined threshold
    and with population above a user-defined threshold, ordered by descending population.\n""")

    print("""x: Exit.\n""")
    
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


def set_up():
    log = 1 
    while(log == 1):
        
        print("Hello User! Login/Register?:\n")

        
        print("1. Login:")
            
        print("2. Register:\n")
        


        log=input()

        
        if(log == '1'):
            user_name = input("\nEnter User Name : ")
            y = ApplicationQueries.login(user_name)
            if(y == 1):
                run_app(user_name)
            elif(y == 0):
                print("Incorrect User Name")
    return log

if __name__ == "__main__":
    
    log = set_up()

    if(log == '2'):
        user_name = input("\nEnter User Name : ")
        y = ApplicationQueries.register(user_name)
        if(y == 1):
            set_up()
        elif(y == 0):
            print("Error!")
    elif(log == '1'):
        print("\nThank You!")
    else:
        print("Incorrect choice, please select again! ")
