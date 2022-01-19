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
    if type == "number_integer":
        return value.GetChildMemberWithName("number_integer")
    if type == "number_unsigned":
        return value.GetChildMemberWithName("number_unsigned")
    if type == "number_float":
        return value.GetChildMemberWithName("number_float")
    if type == "object":
        return value.GetChildMemberWithName("object")
    if type == "array":
        return value.GetChildMemberWithName("array")
    return value


def json_summary(valobj, internal_dict):
    evaluated = valobj.EvaluateExpression(
        "dump(1, ' ', false, nlohmann::detail::error_handler_t::strict).c_str()")
    summary = evaluated.GetSummary()
    if summary:
        display_string = summary[1:-1].replace("\\\"", "\"").replace("\\n", "")
        return f"{display_string}"
    return valobj.GetSummary()

    # return f"{valobj.EvaluateExpression('(int) dump(-1, ' ', false, nlohmann::detail::error_handler_t::strict).c_str();')}"


class BasicJsonSyntheticChildren:
    def __init__(self, valobj, internal_dict):
        # this call should initialize the Python object using valobj as the variable to provide synthetic children for
        self.valobj = valobj
        self.update()

    def num_children(self):
        # this call should return the number of children that you want your object to have
        return len(self.synth_children)

    # def get_child_index(self, name):
    #     # # this call should return the index of the synthetic child whose name is given as argument
    #     if name == "m_value":
    #         return 0
    #     return None

    def get_child_at_index(self, index):
        # this call should return a new LLDB SBValue object representing the child at the index given as argument
        # if is_primitive(self.type):
        #     return self.value.GetValue()
        # return "none"
        return self.synth_children[index]

    def update(self):
        # this call should be used to update the internal state of this Python object whenever the state of the variables in LLDB changes.[1]
        # Also, this method is invoked before any other method in the interface.
        self.type = self.valobj.GetChildMemberWithName("m_type")
        self.value = self.valobj.GetChildMemberWithName("m_value")
        self.synth_children = [self.type, get_value(
            self.type.GetValue(), self.value)]
