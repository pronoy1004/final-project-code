from database import ApplicationQueries

if __name__ == "__main__":
    # we can call function like this.
    query = ApplicationQueries()

    inp = 'y'

    while(inp != 'x'):
        
        print("Welcome to our Database Project, select the options to choose what you'd like to see :   ")
        
        print("Enter")
        
        print("1: ")
        
        print("2: ")
        
        print("3: ")
        
        print("4: ")
        
        print("5: ")
        
        print("Enter x to Exit")
        
        inp = input()
        if(inp == 'n'):
            break
        elif(inp == "1"):
            query.query1()

        elif(inp == "2"):
            query.query2()

        elif(inp == "3"):
            query.query3()

        elif(inp == "4"):
            query.query4()

        elif(inp == "5"):
            query.query5()

        else:
            print("Incorrect choice, please select again! ")

    print("Thank you!")
