class DeltaObject:

    # Must input a single layer dictionary of key value pairs
    def __init__(self, key_values):
        # Holds the changing key value pairs
        self.key_values = key_values
        # Holds the original state of the key value pairs
        self.original_state = dict(key_values)
        # Holds the changes made to the key value pairs
        self.delta_state = {}
        # Set each key to hold an empty array, which will eventually consist of the changes made
        for key in key_values:
            self.delta_state[key] = []
    
    # Adds a new key value pair. Checks to see if it already exists, then adds if it doesn't.
    def add(self, new_key, new_value):
        if new_key not in self.key_values.keys():
            self.set_delta_state(new_key, new_value, "ADD")
            self.key_values[new_key] = new_value

    # Deletes an existing key value pair. Checks to see if the key exists. If it does, deletes it.
    def delete(self, key):
        if key in self.key_values.keys():
            self.set_delta_state(key, self.key_values[key], "DELETE")
            del self.key_values[key]

    # Modifies an existing key value pair. Checks to see if the key exists. If it does, 
    # modifies with the given value.
    def modify(self, key, new_value):
        if key in self.key_values.keys():
            self.set_delta_state(key, new_value, "MODIFY")
            self.key_values[key] = new_value
    
    # Checks if the key exists. If it does, returns the value.
    def get(self, key):
        if key in self.key_values.keys():
            return self.key_values[key]

    # Prints the smallest set of changes to represent the current state
    # Original plan was to just calculate this all at the end, which is much simpler. But the prompt 
    # specified to track this, then output it, so did this instead.
    def deltas(self):
        for key in self.delta_state.keys():
            result_action = ""
            # Check ADDs and DELETEs first since they are most important
            if "ADD" in self.delta_state[key] or "DELETE" in self.delta_state[key]:
                delete = 0
                add = 0
                # Counts the number of each add and delete.
                for action in self.delta_state[key]:
                    if action == "ADD":
                        add += 1
                    elif action == "DELETE":
                        delete += 1
                # If same, result is nothing or modified
                if add == delete:
                    # Case of deleted, then re-added. No case for add, then delete.
                    if key in self.original_state.keys():
                        # If the key is different than the original, count as modified. No action if same.
                        if self.key_values[key] != self.original_state[key]:
                            result_action = "MODIFY"
                # If add is larger, result is add e.g. [ADD, DELETE, ADD, MODIFY] is simply ADD
                elif add > delete:
                    result_action = "ADD"
                # If delete is larger, result is delete e.g. [DELETE, ADD, MODIFY, DELETE] is simply DELETE
                elif delete > add:
                    result_action = "DELETE"
            # If no ADDs or DELETEs, then check MODIFY. No action if nothing exists for the key.
            elif "MODIFY" in self.delta_state[key]:
                result_action = "MODIFY"
            
            # Print the simplified actions
            if result_action == "ADD":
                print "ADD %s = %s" % (key, self.key_values[key])
            elif result_action == "DELETE":
                print "DELETE %s" % key
            elif result_action == "MODIFY":
                print "MODIFY %s = %s" % (key, self.key_values[key])
    
    # Adds an entry in the delta_state array with the change, and the key and value associated
    def set_delta_state(self, key, value, action):
        if key not in self.delta_state.keys():
            self.delta_state[key] = []
        action_dict = {action: {key: value}}
        self.delta_state[key].append(action)

'''
# This is test input. Can be uncommented and changed for testing.
my_delta_obj = DeltaObject({'deer':'park', 'foo':'bar', 'this':'that'})
my_delta_obj.delete('this')
my_delta_obj.add('this','the other')
my_delta_obj.modify('this','that')
my_delta_obj.add('gnu', 'linux')
my_delta_obj.modify('gnu', 'not unix')
print my_delta_obj.get('gnu')
my_delta_obj.modify('deer', 'venison')
my_delta_obj.modify('gnu', 'emacs')
my_delta_obj.deltas()
'''