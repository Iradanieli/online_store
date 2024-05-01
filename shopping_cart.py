from item import Item
from errors import ItemAlreadyExistsError,ItemNotExistError


class ShoppingCart:
           
    # constructor of shopping cart       
    def __init__(self):
        self.dict = {}

    # adding an item if it didnt exist before
    def add_item(self, item: Item):
       
        if item.name in self.dict:
            raise ItemAlreadyExistsError(f"item '{item.name}' already exist.")
        
        self.dict[item.name] = item
           
    # removing an item, if it doesnt exist throwing an error
    def remove_item(self, item_name: str):
        if item_name in self.dict:
            del self.dict[item_name]
        else:
            raise ItemNotExistError
            

    def get_subtotal(self) -> int:
        
        return sum(x.price for x in self.dict.values())

    #returns a list of the values(items)
    def itemList(self) -> list:
        
        list1 = list(self.dict.values())
        return list1
     