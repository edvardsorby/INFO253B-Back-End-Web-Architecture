class Task:
  def __init__(self, title, description, due_date):
    self.title = title
    self.description = description
    self.due_date = due_date

todo_list = []

todo_list.append(Task("Walk the dog", "Take it for a walk around the lake", "2025-02-10"))
todo_list.append(Task("Buy groceries", "Remember to buy potatoes, rice, salmon and bread", "2025-02-03"))
todo_list.append(Task("Take car to the dealer", "Yearly warranty inspection", "2025-02-11"))

print("\nWelcome to the To Do list program :)\n")

while(True):

  print("----------------------------")
  print("\nYour current tasks:")

  if (len(todo_list) < 1):
    print("None\n")
  else:
    for todo in todo_list:
      print(f"\n{todo_list.index(todo) + 1}. {todo.title}")
      print(todo.description)
      print(f"Due: {todo.due_date}")
  print("\n----------------------------")

  print("\nSelect action")
  print("(1) Complete a task")
  print("(2) Add new task")
  menu_item = int(input())

  if (menu_item == 1):
    index = int(input("Enter task number to mark it as completed: "))
    todo_list.pop(index-1)
  elif (menu_item == 2):
    title = input("Enter new To Do task title: ")
    description = input("Enter task description: ")
    due_date = input("Enter due date: ")

    task = Task(title, description, due_date)
    todo_list.append(task)

