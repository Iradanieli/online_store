import yaml
from errors import TooManyMatchesError , ItemNotExistError , ItemAlreadyExistsError

from item import Item
from shopping_cart import ShoppingCart

class Store:
    def __init__(self, path):
        with open(path) as inventory:
            items_raw = yaml.load(inventory, Loader=yaml.FullLoader)['items']
        # list of items
        self._items = self._convert_to_item_objects(items_raw)   
        self._shopping_cart = ShoppingCart()

    @staticmethod
    def _convert_to_item_objects(items_raw):
        return [Item(item['name'],
                     int(item['price']),
                     item['hashtags'],
                     item['description'])
                for item in items_raw]

    def get_items(self) -> list:
        return self._items

    # helper function: checks how many common hashtugs an item has with a list of hashtugs
    def Common_hashtags(self,hashtagslist:list,item: Item) ->int:
        count = 0
        for hashInItem in hashtagslist:
            if hashInItem in item.hashtags:
                count+=1
        return count

    def search_by_name(self, item_name: str) -> list:
        
        first_include = []   #all items which include the string item_name and also not in the shopping cart
        for it in self._items:
            if item_name in it.name and it not in self._shopping_cart.itemList():
                first_include.append(it)
        
        tagsInCart = []   
        for t in self._shopping_cart.itemList():
            for k in t.hashtags:
                tagsInCart.append(k) #    ///no need to handle duplicates!

        touples = [] # is a list of touples, each touple contains an item and the number of matches it has with tagsInCart
        for k in first_include:
            matches_number = self.Common_hashtags(tagsInCart,k)
            touples.append((matches_number,k))

        sorted_tuples = sorted(touples, key=lambda x: (-x[0], x[1].name)) #sort according to matches and then abc
        finalList = [t[1] for t in sorted_tuples]
        return finalList
       
        #same idea as search_by_name
    def search_by_hashtag(self, hashtag: str) -> list:
        
        first_include = []   #all items which have the hashtag hashtag and also not in the shopping cart
        for it in self._items:
            if hashtag in it.hashtags and it not in self._shopping_cart.itemList():
                first_include.append(it)
        
        tagsInCart = []   
        for t in self._shopping_cart.itemList():
            for k in t.hashtags:
                tagsInCart.append(k)
                    
        touples = []
        for k in first_include:
            matches_number = self.Common_hashtags(tagsInCart,k)
            touples.append((matches_number,k))

        sorted_tuples = sorted(touples, key=lambda x: (-x[0], x[1].name))
        finalList = [t[1] for t in sorted_tuples]
        return finalList


    def add_item(self, item_name: str):

        match_by_name = []
        for i in self._items:
            if item_name in i.name:
                match_by_name.append(i)

        if len(match_by_name)==0:
            raise ItemNotExistError()
        if len(match_by_name)>1:
            raise TooManyMatchesError()
        
        for i in self._shopping_cart.itemList():
            if item_name in i.name:
                raise ItemAlreadyExistsError()
            
        it = match_by_name[0]
        self._shopping_cart.add_item(it)


    def remove_item(self, item_name: str):
        match_by_name = []
        for i in self._items:
            if item_name in i.name:
                match_by_name.append(i)

        if len(match_by_name)==0:
            raise ItemNotExistError()
        if len(match_by_name)>1:
            raise TooManyMatchesError()
        
        for i in self._shopping_cart.itemList():
            if item_name in i.name:
                self._shopping_cart.remove_item(i.name)
        

    def checkout(self) -> int:
       return self._shopping_cart.get_subtotal()