def greet(name):
    return f"Hello, {name}!"

class Calculator:
    def add(self, a, b):
        return a + b
    
class Person:
    def __init__(self, name):
        self.name = name

    def greet(self):
        return "Hello " + self.name

person1 = Person("Alex")
print(person1.greet())