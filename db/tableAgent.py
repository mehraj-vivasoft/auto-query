import json
from typing import Callable, List, Optional

from utils.getGptClient import get_gpt_client

# Define the TreeGent class
class TreeGent:
    def __init__(self, 
                 name: str, 
                 description: str,                  
                 action: Optional[Callable] = None, 
                 childrenList: Optional[List['TreeGent']] = None):
        self.name = name
        self.description = description
        self.action = action
        self.childrenList = childrenList or []  # Initialize an empty list if None is provided

    def deligate_task(self, query: str):
        print(f"Deligating task from {self.name}...")
        
        descriptions = []
        i = 1
        
        if self.childrenList.__len__() < 1:
            print("No children found")
            return -1
        
        for child in self.childrenList:
            descriptions.append(str(i) + " >> " + child.name + " : " + child.description)
            i += 1        
        
        descriptions.append(str(i) + " >> None of the above can satisfy the query or none of the above is releted to the query given ~ THE QUERY IS INVALID")
        
        completion = get_gpt_client().chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a task delegation agent. You will return only a number. The number you will tell me is the task number you will only return the task_number nothing else. task_number is the number which closest matches with the user query. Please select a task from the following list:" + str(descriptions)},            
                {"role": "user", "content": query},
            ],
        )

        print("GPT RESPONSE: ", completion.choices[0].message.content)

        # choice = json.loads(completion.choices[0].message.content)['selected_choice']
        choice = completion.choices[0].message.content
        
        choice_number = int(choice)
        print(f"AI Selected choice number: {choice_number}")
            
        return choice_number

    # Method to execute the action function, if it exists
    def executeTask(self, query: str) -> str:
        res = self.deligate_task(query)        
        if res == -1:
            print("No children found for deligating so " + self.name + " is performing the action : ")
            if self.action is not None:
                res = self.action(query)
                print("Action performed by " + self.name + " agent : " + res)
                return res
            else:
                print("No action defined for " + self.name + " agent :(")
                return "No action defined for " + self.name + " agent :("
        elif self.childrenList.__len__() >= res:
            res = self.childrenList[res - 1].executeTask(query)                    
        elif res == self.childrenList.__len__() + 1:
            print("THE QUERY CANNOT BE SATISFIED BY ANY OF THE CHILDREN OR THE QUERY IS INVALID")
            return "THE QUERY CANNOT BE SATISFIED BY ANY OF THE CHILDREN OR THE QUERY IS INVALID"
        else:
            print("Invalid choice number by AI")
            return "Invalid choice number by AI"
        return res

    # Method to add a child TreeGent
    def add_child(self, child: 'TreeGent'):
        self.childrenList.append(child)

    # Method to display the tree structure
    def display_tree(self, level=0):
        indent = "  " * level
        print(f"{indent}- {self.name}: {self.description}")
        for child in self.childrenList:
            child.display_tree(level + 1)


