

class RustItemCollection:
    def __init__(self, name_manager):
        self.items = {}
        self.name_manager = name_manager
    
    def insert(self, item_tuple):
        item_name, item_id, quantity = item_tuple
        
        if item_id in self.items:
            # update the quantity
            self.items[item_id]['quantity'] += quantity
        else:
            # insert a new entry
            self.items[item_id] = {'item_name': item_name, 'quantity': quantity}
    
    def insert_collection(self, other_collection):
        for _, data in other_collection.items.items():
            self.insert((data['item_name'], _, data['quantity']))
            
    def get_items(self):
        return [(data['item_name'], item_id, data['quantity']) for item_id, data in self.items.items()]
    
    def get_item_id_by_name(self, name):
        return self.name_manager.get_item_id(name)
    
    def __str__(self):
        if not self.items:
            return "ItemCollection is empty"
        
        items_str = []
        for item_id, data in self.items.items():
            items_str.append(f"Item Name: {data['item_name']}, ID: {item_id}, Quantity: {data['quantity']}")
        return "\n".join(items_str)