
from winreg import REG_NOTIFY_CHANGE_ATTRIBUTES
from xml.dom.minidom import Attr
import psycopg2
from psycopg2 import sql

tables = ["addresses", "applications", "benefits", "companies", "employees", "industries", "postings", "salaries", "scraped", "skills", "specialties"]
columns = {"addresses": ["address", "zip_code"], "applications": ["application_url", "application_type", "applies", "posting_domain"],
           "benefits": ["benefit_id", "inferred", "type"], "companies": ["company_id", "name", "description", "company_size", "url"], 
           "employees": ["company_id", "employee_count", "follower_count", "time_recorded"], "industries": ["industry_id", "industry_name"],
           "postings": ["job_id", "title", "description", "remote_allowed", "views", "formatted_experience_level", "listed_time", "sponsored", "work_type"], 
           "salaries": ["salary_id", "max_salary", "med_salary", "min_salary", "pay_period", "compensation_type"], "skills": ["skill_abr", "skill_name"],
           "scraped": ["job_posting_url", "scraped", "closed_time", "expiry"], "specialties": ["specialty_id", "specialty"]}
integers = set(["applies", "benefit_id", "inferred", "company_id", "company_size", "employee_count", "follower_count", "time_recorded", "industry_id",
                "job_id", "remote_allowed", "views", "sponsored", "salary_id", "max_salary", "med_salary", "min_salary", "scraped", "specialty_id"])

def insert():
    print("\n Please select which table you would like to insert data to: \n")
    for i, table in enumerate(tables): 
       print(str(i) + ". " + table)
    user_input = int(input("\n Your answer: "))
        
    if user_input < 0 or user_input > len(tables) - 1:
        print("\nError: Your input was invalid")
        return
        
    table = tables[user_input]
    attributes = []
        
    for column in columns[table]:
        attributes.append(input("\nEnter a value for " + column + ": "))
            
    sql_query = "INSERT INTO " + table + " VALUES ("
    for attribute in attributes:
        if attribute not in integers:
            sql_query = sql_query + "\'" + attribute + "\', "
        else:
            sql_query = sql_query + attribute + ", "
    sql_query = sql_query[:len(sql_query)-2] + ")"

    return sql_query


def delete():
    print("\n Please select which table you would like to delete data from: \n")
    for i, table in enumerate(tables): 
       print(str(i) + ". " + table)
    user_input = int(input("\n Your answer: "))
        
    if user_input < 0 or user_input > len(tables) - 1:
        print("\nError: Your input was invalid")
        return
        
    table = tables[user_input]
    condition = input("\nEnter a condition for deleting: ")
            
    sql_query = "DELETE FROM " + table + " WHERE " + condition

    return sql_query


def update():
    print("\n Please select which table you would like to update data from: \n")
    for i, table in enumerate(tables): 
       print(str(i) + ". " + table)
    user_input = int(input("\n Your answer: "))
        
    if user_input < 0 or user_input > len(tables) - 1:
        print("\nError: Your input was invalid")
        return
        
    table = tables[user_input]
    attributes = []
        
    print("\n Please select the column you would like to update data in: \n")
    for i, column in enumerate(columns[table]): 
       print(str(i) + ". " + column)
    user_input = int(input("\n Your answer: "))
    
    if user_input < 0 or user_input > len(columns[table]) - 1:
        print("\nError: Your input was invalid")
        return

    column = columns[table][user_input]
    new_col = input("\n Please enter new value for column " + column + ": ")
            
    condition = input("\nEnter a condition for the rows to be updated: ")

    sql_query = "UPDATE " + table + " SET " + column + " = " + new_col + " WHERE " + condition

    return sql_query


def select():
    print("\n Please select which table you would like to select data from: \n")
    for i, table in enumerate(tables): 
       print(str(i) + ". " + table)
    user_input = int(input("\n Your answer: "))
        
    if user_input < 0 or user_input > len(tables) - 1:
        print("\nError: Your input was invalid")
        return
        
    table = tables[user_input]
    condition = input("\nEnter a condition for the rows to be selected: ") 
    sql_query = "SELECT * FROM " + table + " WHERE " + condition
    

    return sql_query


def aggregate():
    agg_string = {1: "SUM(", 2: "AVG(", 3: "COUNT(", 4: "MIN(", 5:"MIN("}    

    print("\n Please select which table you would like to select data from: \n")
    for i, table in enumerate(tables): 
       print(str(i) + ". " + table)
    user_input = int(input("\n Your answer: "))
        
    if user_input < 0 or user_input > len(tables) - 1:
        print("\nError: Your input was invalid")
        return
        
    table = tables[user_input]
    print("\n Please select the column you would like to search for data in: \n")
    for i, column in enumerate(columns[table]): 
       print(str(i) + ". " + column)
    user_input = int(input("\n Your answer: "))
    
    if user_input < 0 or user_input > len(columns[table]) - 1:
        print("\nError: Your input was invalid")
        return

    column = columns[table][user_input]
    print("""\n Please select which aggregate function you would like to use: \n\n
          1. Sum\n
          2. Average\n
          3. Count\n
          4. Min\n
          5. Max\n""")
    user_input = int(input("\nYour answer: "))
    
    if user_input < 1 or user_input > 5:
        print("\nError: Your input was invalid")
        return
    
    sql_query = "SELECT " + agg_string[user_input] + column + ") FROM " + table

    return sql_query


def sort():
    print("\n Please select which table you would like to select data from: \n")
    for i, table in enumerate(tables): 
       print(str(i) + ". " + table)
    user_input = int(input("\n Your answer: "))
        
    if user_input < 0 or user_input > len(tables) - 1:
        print("\nError: Your input was invalid")
        return
        
    table = tables[user_input]
    print("\n Please select the column you would like to order the data by: \n")
    for i, column in enumerate(columns[table]): 
       print(str(i) + ". " + column)
    user_input = int(input("\n Your answer: "))
    
    if user_input < 0 or user_input > len(columns[table]) - 1:
        print("\nError: Your input was invalid")
        return

    column = columns[table][user_input]
    user_input = input("\nPlease enter ASC or DESC to order the table in ascending or descending order respectively: ")
    
    if user_input != "ASC" and user_input != "DESC":
        print("\nError: Your input was invalid")
        return
    
    sql_query = "SELECT * FROM " +  table + " ORDER BY " + column + " " + user_input

    return sql_query


def join():
    joins = set(["JOIN", "INNER JOIN", "LEFT JOIN", "RIGHT JOIN", "FULL OUTER JOIN", "FULL JOIN", "LEFT OUTER JOIN", "RIGHT OUTER JOIN", "CROSS JOIN"])

    print("\n Please select the first table you would like to select data from: \n")
    for i, table in enumerate(tables): 
       print(str(i) + ". " + table)
    user_input = int(input("\n Your answer: "))  
    if user_input < 0 or user_input > len(tables) - 1:
        print("\nError: Your input was invalid")
        return
    table1 = tables[user_input]
    
    print("\n Please select the second table you would like to select data from: \n")
    for i, table in enumerate(tables): 
       print(str(i) + ". " + table)
    user_input = int(input("\n Your answer: "))
    if user_input < 0 or user_input > len(tables) - 1:
        print("\nError: Your input was invalid")
        return
    table2 = tables[user_input]
    
    my_join = input("\n Please write in all caps which join function you would like to use: ")
    
    if my_join not in joins:
        print("\nError: Your input was invalid")
        return
    
    key = input("\nPlease enter the key that both tables have in common: ")
    
    sql_query = "SELECT * FROM " +  table1 + " " + my_join + " " + table2 + " ON " + table1 + "." + key + " = " + table2 + "." + key

    return sql_query


def group():
    agg_string = {1: "SUM(", 2: "AVG(", 3: "COUNT(", 4: "MIN(", 5:"MIN("} 

    print("\n Please select which table you would like to select data from: \n")
    for i, table in enumerate(tables): 
       print(str(i) + ". " + table)
    user_input = int(input("\n Your answer: "))
    if user_input < 0 or user_input > len(tables) - 1:
        print("\nError: Your input was invalid")
        return
    table = tables[user_input]
    
    print("\n Please select the column you would like to select and group the data by: \n")
    for i, column in enumerate(columns[table]): 
       print(str(i) + ". " + column)
    user_input = int(input("\n Your answer: "))
    if user_input < 0 or user_input > len(columns[table]) - 1:
        print("\nError: Your input was invalid")
        return
    column1 = columns[table][user_input]
    
    print("""\n Please select which aggregate function you would like to use: \n\n
          1. Sum\n
          2. Average\n
          3. Count\n
          4. Min\n
          5. Max\n""")
    user_input = int(input("\nYour answer: "))
    if user_input < 1 or user_input > 5:
        print("\nError: Your input was invalid")
        return
    agg = agg_string[user_input]
    
    print("\n Please select the column you would like to apply the aggregate function to: \n")
    for i, column in enumerate(columns[table]): 
       print(str(i) + ". " + column)
    user_input = int(input("\n Your answer: "))
    if user_input < 0 or user_input > len(columns[table]) - 1:
        print("\nError: Your input was invalid")
        return
    column2 = columns[table][user_input]
    
    sql_query = "SELECT " + column1 + ", " + agg + column2 + ") FROM " +  table + " GROUP BY " + column1

    return sql_query


def subquery():
    choice = int(input("\nEnter 1 to select from a table or 2 to enter a subquery: "))
    table = ""
    snippet = ""
    
    if choice == 1:
        print("\nPlease select which table you would like to select data from: \n")
        for i, table in enumerate(tables): 
            print(str(i) + ". " + table)
        user_input = int(input("\n Your answer: "))  
        if user_input < 0 or user_input > len(tables) - 1:
            print("\nError: Your input was invalid")
            return
        table = tables[user_input]
    elif choice == 2:
        snippet = input("\nPlease enter a valid sql subquery for a FROM statement: ")
    else:
        print("\nError: invalid input")
        return
       
    condition = input("\nEnter a valid condition or subquery including parentheses for a WHERE statement: ")
    if snippet == "":
        sql_query = "SELECT * FROM " + table + " WHERE " + condition
    else:
        sql_query = "SELECT * FROM (" + snippet + ") WHERE " + condition
        
    return sql_query


def transaction():
    sql_query = "BEGIN TRANSACTION;"
    
    while True:
        user_input = int(input("\nPress 1 to insert a new query, 2 to commit queries or 3 to roll them back: "))
        if user_input == 1:
            sql_query = sql_query + " " + input("\nPlease enter a valid SQL query: ") + ";"
        elif user_input == 2:
            sql_query += " COMMIT;"
            break
        elif user_input == 3:
            sql_query += " ROLLBACK;"
            break
        
    return sql_query


def error_handle():
    sql_query = "BEGIN TRY"
    
    while True:
        user_input = int(input("\nPress 1 to insert a new query or 2 to finish the try block: "))
        if user_input == 1:
            sql_query = sql_query + " " + input("\nPlease enter a valid SQL query: ")
        elif user_input == 2:
            sql_query += " END TRY"
            break
       
    sql_query += " BEGIN CATCH"
    while True:
        user_input = int(input("\nPress 1 to insert a new query or 2 to finish the catch block: "))
        if user_input == 1:
            sql_query = sql_query + " " + input("\nPlease enter a valid SQL query: ") + ";"
        elif user_input == 2:
            sql_query += " END CATCH"
            break
        
    return sql_query
    


def execute_command(cmd, connection, crsr):   
    sql_query = ""
    
    if cmd == 1:
        sql_query = insert()
    elif cmd == 2:
        sql_query = delete()
    elif cmd == 3:
        sql_query = update()
    elif cmd == 4:
        sql_query = select()
    elif cmd == 5:
        sql_query = aggregate()
    elif cmd == 6:
        sql_query = sort()
    elif cmd == 7:
        sql_query = join()
    elif cmd == 8:
        sql_query = group()
    elif cmd == 9:
        sql_query = subquery()
    elif cmd  == 10:
        sql_query = transaction()
    elif cmd == 11:
        sql_query = error_handle()

    print("\nYour query is: " + sql_query)
    crsr.execute(sql_query)
    if 4 <= cmd <= 9:
        records = crsr.fetchall()
        print("\nYour results are:\n")
        for record in records:
            print(record)
    connection.commit()
        


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    try: 
        connection = psycopg2.connect(host = "localhost", port = "5432", database = "LinkedIn", user = "postgres", password = "Laaeg2023")
        crsr = connection.cursor()
        print("Welcome to the LinkedIn Database CLI interface!\n")
        
        while True:
            user_input = input("""\nPlease select one of the following operations: \n\n
            1. Insert Data\n
            2. Delete Data\n
            3. Update Data\n
            4. Search Data\n
            5. Aggregate Functions\n
            6. Sorting\n
            7. Joins\n
            8. Grouping\n
            9. Subqueries\n
            10. Transactions\n
            11. Error Handling\n
            12. Exit\n\n                   
            What would you like to do: """)
            
            if int(user_input) < 1 or int(user_input) > 12:
                print("\nInvalid input, please try again")
            elif int(user_input) == 12:
                break
            else:
                execute_command(int(user_input), connection, crsr)
        
        crsr.close()
        connection.close()
        print("\nDatabase Connection Terminated")
        
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)