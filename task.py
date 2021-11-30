import typer # for clt property

# function used to sort tasks based on their priority
def sort_function(data):
    priority = []
    for i in data:
        i = i.split(' ')
        priority.append(int(i[0]))
    priority.sort()
    #for loop to sort list of tasks
    for i in priority:
        for j in data:
            if str(i) in j:
                index1 = data.index(j)
                index2 = priority.index(i)
                temp = data[index1]
                data[index1] = data[index2]
                data[index2] = temp
    return data #returning the sorted list of tasks

#to display help table
def help():
    print("""Usage :-
    $ ./task add 2 hello world     # Add a new item with priority 2 and text \"hello world\" to the list
    $ ./task ls                    # Show incomplete priority list items sorted by priority in ascending order
    $ ./task del NUMBER   # Delete the incomplete item with the given priority number
    $ ./task done NUMBER  # Mark the incomplete item with the given PRIORITY_NUMBER as complete
    $ ./task help                  # Show usage
    $ ./task report               # Statistics""")

# to add tasks with priority to task.txt
def add(priority, task):
    if priority == " ":
        priority = '\0'

    if task == ' '  or task == '\0' or priority == '\0':
        print("Error: Missing tasks string. Nothing added!")
    else:
        try:
            int(priority)
            file = open('task.txt', 'a')
            file.write(str(priority) + ":" + task + '\n')
            file.close()
            print(f'''Added task: "{task}" with priority {priority}''')
        except:
            print("Error: Missing priority number. Nothing added!")

#to list tasks from task.txt based on priority 
def ls():
    empty = 0
    data = []
    data_final = []
    file = open('task.txt', 'r')
    num = 1
    for i in file:
        data.append((i.replace(":", ' ')))
    file.close()
    data = sort_function(data)
    for i in data:
        i = i.split(' ')
        string = i[0]+':'
        del i[0]
        i = ' '.join(elm for elm in i)
        string = string + i
        data_final.append(string)
    for i in data_final:
        if 'Completed' in i:
            pass
        else:
            i = i.split(':')
            priority = i[0]
            task = i[1].replace('\n', '')
            print(str(num) + '. ' + task +" " + '[' + priority + ']')
            num += 1
            empty = 1
    #works if there is no pending tasks
    if empty==0:
        print("There are no pending tasks!")
# to mark completed tasks
def done(num):
    num = int(num)
    id = 1
    data = []
    dic = {}
    completed = []

    file = open('task.txt', 'r')
    for i in file:
        data.append((i.replace(":", ' ')))
    file.close()
    data = sort_function(data)
    #here check if the task is completed or not
    for i in data:
        if 'Completed' in i:
            completed.append(i)
        else:
            dic[id] = i
            id += 1
    if len(dic) >= num:
        dic[num] = (dic[num].replace('\n', '')) + ' ' + 'Completed\n'
        
        file = open('task.txt', 'w')
        file.write('')
        file.close()

        file = open('task.txt', 'a')
        for i in dic:
            file.write(dic[i])
        for i in completed:
            file.write(i)
        file.close()

        print("Marked item as done.")
    #it works when the index number that user entered is not exists
    else:
        print("Error: no incomplete item with index #0" + str(num) + " exists.")

#to delete incompleted task from task.txt
def delete(num):
    num = int(num)
    id = 1
    data = []
    dic = {}

    file = open('task.txt', 'r')
    for i in file:
        data.append((i.replace(":", ' ')))
    file.close()
    data = sort_function(data)
    #here check if the task is completed or not
    for i in data:
        if 'Completed' in i:
            pass
        else:
            dic[id] = i
            id += 1
    if len(dic) >= num:
        for i in data:
            if dic[num] == i:
                index = data.index(i)
                data[index] = ''
        file = open('task.txt', 'w')
        file.write('')
        file.close()
        file = open('task.txt', 'a')
        for i in data:
            file.write(i)
        file.close()
        print('Deleted task #'+ str(num))
    #it works when the index number that user entered is not exists
    else:
        print(f'''Error: task with index #{str(num)} does not exist. Nothing deleted.''')
#to display overall report of user's task   
def report():
    pending = completed = 0
    data = []
    data_final = []
    file = open('task.txt', 'r')
    for i in file:
        data.append((i.replace(":", ' ')))
    file.close()
    data = sort_function(data)
    for i in data:
        i = i.split(' ')
        string = i[0]+':'
        del i[0]
        i = ' '.join(elm for elm in i)
        string = string + i
        data_final.append(string)
    #counting
    for i in data_final:
        if 'Completed' in i:
            completed += 1
        else:
            pending += 1
    #print pending task
    number = 1
    print('Pending : ', pending)
    for i in data_final:
        if 'Completed' in i:
            pass
        else:
            i = i.replace('\n', '')
            print(f'''{number}. {i.split(':')[1]} [{i.split(':')[0]}]''')
            number += 1
    #print completed task
    number = 1
    print('\nCompleted : ', completed)
    for i in data_final:
        if 'Completed' in i:
            i = i.replace('Completed', '')
            print(f'''{number}. {i.split(':')[1]}''')
            number += 1

# the starting function; here call other function based on user's command   
def argument(op:str = typer.Argument(" "), val:str = typer.Argument(" "), val2:str = typer.Argument(" ")):
    if op == 'help':
        help()
    elif op == 'add':
        add(val, val2)
    elif op == 'ls':
        ls()
    elif op == 'done':
        try:
            if val == "0":
                print("Error: no incomplete item with index #0 exists.")
            else:
                done(int(val))
        except:
            print("Error: Missing NUMBER for marking tasks as done.")
    elif op == 'del':
        try:
            if val == "0":
                print("Error: task with index #0 does not exist. Nothing deleted.")
            else:
                delete(int(val))
        except:
            print("Error: Missing NUMBER for deleting tasks.")
    elif op == 'report':
        report()
    else:
        help()

if __name__ == "__main__":
       typer.run(argument) #calling the function argument when user excecute "./task"(in linux terminal)