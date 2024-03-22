

from rust.rust_item_name_manager import RustItemNameManager


class RustItemCollection:
    def __init__(self, name_manager: RustItemNameManager):
        self.items = {}
        self.name_manager = name_manager
    
    def insert(self, item_tuple):
        """
        Insert a tuple (item name, id, quantity) into the collection
        If the id is already in the collection, increment the quantity
        """
        item_name, item_id_, quantity = item_tuple
        item_id = str(item_id_)
        if item_id in self.items:
            # update the quantity
            self.items[item_id]['quantity'] += quantity
        else:
            # insert a new entry
            self.items[item_id] = {'item_name': item_name, 'quantity': quantity}
    
    def insert_collection(self, other_collection):
        """
        Insert another RustItemCollection into this collection
        """
        for item_id, data in other_collection.items.items():
            self.insert((data['item_name'], str(item_id), data['quantity']))
    
    def quantity_by_id(self, item_id):
        """
        Get the quantity of the specified item (by id) in the RustItemCollection
        Returns none if we don't know what the alias is
        """
        if str(item_id) in self.items:
            return self.items[str(item_id)]['quantity']
        else:
            return 0 # none of this item
    
    def quantity_by_name(self, name_or_alias):
        """
        Use the name manager to determine the id of a given name or alias, then return
        the quantity of that item (by id) that is in this RustItemCollection
        """
        item_id = self.name_manager.get_item_id(name_or_alias)
        if item_id == -1:
            return -1
        return self.quantity_by_id(item_id) 
    
    def __str__(self):
        if not self.items:
            return "ItemCollection is empty"
        
        items_str = []
        for item_id, data in self.items.items():
            items_str.append(f"Item Name: {data['item_name']}, ID: {item_id}, Quantity: {data['quantity']} aliases = {self.name_manager.get_aliases_for_id(item_id)}")
        return "\n".join(items_str)