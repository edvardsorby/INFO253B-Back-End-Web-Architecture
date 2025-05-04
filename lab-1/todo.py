class Task:
  def __init__(self, title, description, due_date):
    self.title = title
    self.description = description
    self.due_date = due_date

  def print_task(self):
      print(f"\n{todo_list.index(todo) + 1}. {todo.title}")
      print(todo.description)
      print(f"Due: {todo.due_date.get_date()}")

class Date:
  def __init__(self, year, month, day):
    self.year = year
    self.day = day
    self.month = month

  def get_date(self):
    return f"{self.year}-{self.month}-{self.day}"

todo_list = []
running = True

todo_list.append(Task("Walk the dog", "Take it for a walk around the lake", Date("2025", "02", "10")))
todo_list.append(Task("Buy groceries", "Remember to buy potatoes, rice, salmon and bread", Date("2025", "02", "03")))
todo_list.append(Task("Take car to the dealer", "Yearly warranty inspection", Date("2025", "02", "11")))

print("\nWelcome to the To Do list program :)\n")

while(running):

  print("----------------------------")
  print("\nYour current tasks:")

  if (len(todo_list) < 1):
    print("None\n")
  else:
    for todo in todo_list:
      todo.print_task()
  print("\n----------------------------")

  print("\nSelect action")
  print("(1) Complete a task")
  print("(2) Add new task")
  print("(3) Quit")
  menu_item = int(input())

  if (menu_item == 1):
    index = int(input("Enter task number to mark it as completed: "))
    todo_list.pop(index-1)
  elif (menu_item == 2):
    title = input("Enter new To Do task title: ")
    description = input("Enter task description: ")
    due_date = input("Enter due date (YYYY-MM-DD): ").split("-")

    task = Task(title, description, Date(due_date[0], due_date[1], due_date[2]))
    todo_list.append(task)
  elif (menu_item == 3):
    running = False

