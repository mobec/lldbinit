import lldb


def is_primitive(type):
    if type == "null" or type == "string" or type == "boolean" or type == "number" or type == "binary":
        return True
    return False


def get_value(type, value):
    if type == "null":
        return "null"
    if type == "string":
        return value.GetChildMemberWithName("string")
    if type == "boolean":
        return value.GetChildMemberWithName("boolean")
    if type == "number":
        return value.GetChildMemberWithName("number_float")
    return ""


def json_summary(valobj, internal_dict):
    type_val = valobj.GetChildMemberWithName('m_type')
    value_val = valobj.GetChildMemberWithName('m_value')
    return f"type: {type_val.GetValue()}"


class BasicJsonSyntheticChildren:
    def __init__(self, valobj, internal_dict):
        # this call should initialize the Python object using valobj as the variable to provide synthetic children for
        self.valobj = valobj
        self.type = valobj.GetChildMemberWithName("m_type").GetValue()
        self.value = valobj.GetChildMemberWithName("m_value")
        self.update()

    def num_children(self):
        # this call should return the number of children that you want your object to have
        if is_primitive(self.type):
            return 1
        return 2

    def get_child_index(self, name):
        # # this call should return the index of the synthetic child whose name is given as argument
        if name == "m_value":
            return 0
        return None

    def get_child_at_index(self, index):
        # this call should return a new LLDB SBValue object representing the child at the index given as argument
        # if is_primitive(self.type):
        #     return self.value.GetValue()
        # return "none"
        if is_primitive(self.type):
            return get_value(self.type, self.value)
        return None

    def update(self):
        # this call should be used to update the internal state of this Python object whenever the state of the variables in LLDB changes.[1]
        # Also, this method is invoked before any other method in the interface.
        pass
