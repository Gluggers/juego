import logging
from app.items import items, item_listing
from lang import language

DEFAULT_MAX_INVENT_SIZE = 120  # 30 #40?


class Inventory(item_listing.ItemListing):
    inventory_name_info = language.MultiLanguageText(en='Inventory', es='Inventario')
    toolbelt_name_info = language.MultiLanguageText(en='Toolbelt', es='Herramientas')

    def __init__(self, max_size=DEFAULT_MAX_INVENT_SIZE):
        # Will be lists of 2-tuple (item_id, quantity).
        # Non-stackable items will have quantity of 1 and will be
        # in separate tuples, while stackable items with the same ID
        # will share the same tuple and can have a quantity value
        # of greater than 1.
        # Quantity should not be less than 1, otherwise item will be
        # removed from the data structure.
        item_listing.ItemListing.__init__(
            self,
            max_size=max_size,
        )

    # Overridden.
    def remove_item_by_index(self, index, quantity=1):
        if quantity > 0 and (index is not None) and 0 <= index <= self.get_last_index():
            item_entry = self._item_listing_data[index]
            item_id = item_entry[0]
            item_obj = items.Item.get_item(item_id)

            if item_obj:
                if item_obj.is_stackable():
                    old_quantity = item_entry[1]
                else:
                    old_quantity = self.get_item_quantity(item_id)

                new_quantity = max(0, old_quantity - quantity)

                if item_obj.is_stackable():
                    if new_quantity > 0:
                        self._item_listing_data[index] = (
                            item_id,
                            new_quantity,
                        )
                    else:
                        self._item_listing_data.pop(index)
                else:
                    # Handle nonstackable item.
                    self._item_listing_data.pop(index)
                    to_remove = old_quantity - new_quantity - 1

                    curr_index = self.get_last_index()

                    while to_remove > 0 and curr_index >= 0:
                        curr_entry = self._item_listing_data[curr_index]
                        if curr_entry[0] == item_id:
                            self._item_listing_data.pop(curr_index)
                            to_remove -= 1

                        curr_index -= 1

                logging.info("Removed {0} x{1}".format(
                    item_obj.get_name(),
                    old_quantity - self.get_item_quantity(item_id)
                ))
            else:
                logging.error("Trying to remove invalid item ID from inventory.".format(item_id))

    # Overridden.
    def get_item_quantity(self, item_id):
        quantity = 0

        item_obj = items.Item.get_item(item_id)

        if item_obj:
            if item_obj.is_stackable():
                obj_index = self.get_item_index(item_id)

                if obj_index >= 0:
                    entry = self._item_listing_data[obj_index]
                    quantity = entry[1]
            else:
                num_found = 0
                for entry in self._item_listing_data:
                    if entry[0] == item_id:
                        num_found += entry[1]
                quantity = num_found
        else:
            logging.error("Invalid item ID {0}".format(item_id))
        return quantity

    # initial_item_dict is mapping of item IDs to quantity. Used to
    # create initial inventory.
    # Returns created inventory.
    @classmethod
    def inventory_factory(cls, max_size=DEFAULT_MAX_INVENT_SIZE, initial_item_dict=None):
        # Create inventory and populate initial items if any.
        ret_invent = Inventory(max_size=max_size)
        if initial_item_dict:
            # Populate initial items if any.
            for item_id, quantity in initial_item_dict.items():
                ret_invent.add_item(item_id, quantity=quantity)
        return ret_invent

    @classmethod
    def get_inventory_name(cls):
        return cls.inventory_name_info.get_text()
