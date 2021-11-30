import typer
# import re

def sort_function(data):
    priority = []
    for i in data:
        i = i.split(' ')
        priority.append(int(i[0]))
    priority.sort()
    for i in priority:
        for j in data:
            if str(i) in j:
                index1 = data.index(j)
                index2 = priority.index(i)
                temp = data[index1]
                data[index1] = data[index2]
                data[index2] = temp
    return data

def help():
    print(
"""Usage :-
    $ ./task add 2 hello world     # Add a new item with priority 2 and text \"hello world\" to the list
    $ ./task ls                    # Show incomplete priority list items sorted by priority in ascending order
    $ ./task del NUMBER   # Delete the incomplete item with the given priority number
    $ ./task done NUMBER  # Mark the incomplete item with the given PRIORITY_NUMBER as complete
    $ ./task help                  # Show usage
    $ ./task report                # Statistics""")

def add(priority, task):
    # special = re.compile('@[_!#$%^&*\"()<>?/\|}{~:]')
    # if special.search(task) == None:
    #     i = False
    # else:
    #     i = True
    if priority == " ":
        priority = '\0'

    if task == ''  or task == '\0' or priority == '\0':
        print("Error: Missing tasks string. Nothing added!")
    else:
        file = open('task.txt', 'a')
        file.write(str(priority) + ":" + task + '\n')
        file.close()
        print(f'''Added task: "{task}" with priority {priority}''')

def ls():
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
    else:
        print("Error: no incomplete item with index #0" + str(num) + " exists.")

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
    else:
        print("Error: item with index " + str(num) + "\tdoes not exist. Nothing deleted.")
    
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
    print('Completed : ', completed)
    for i in data_final:
        if 'Completed' in i:
            i = i.replace('Completed', '')
            print(f'''{number}. {i.split(':')[1]}''')
            number += 1
    
def argument(op:str = typer.Argument(" "), val:str = typer.Argument(" "), val2:str = typer.Argument(" ")):
    try:
        if op == 'help':
            help()
        elif op == 'add':
            add(val, val2)
        elif op == 'ls':
            ls()
        elif op == 'done':
            try:
              done(int(val))
            except:
                print("Error: Missing NUMBER for marking tasks as done.")
                # help()
        elif op == 'del':
            try:
                delete(int(val))
            except:
                print("Error: Missing NUMBER for deleting tasks.")
                # help()
        elif op == 'report':
            report()
        else:
            help()
    except TypeError:
        print("Error: Missing tasks string. Nothing added!")

if __name__ == "__main__":
       typer.run(argument)