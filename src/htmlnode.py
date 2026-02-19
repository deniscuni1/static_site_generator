class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    def to_html(self):
        raise NotImplementedError
    def props_to_html(self):
        if self.props == None:
            return ""
        else:
            string_to_return = ""
            for key, value in self.props.items():
                string_to_return += f' {key}="{value}"'
            return string_to_return
    def __repr__(self):
        print(self.tag, self.value, self.children, self.props)
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
    def to_html(self):
        if self.value ==  None:
            raise ValueError
        elif self.tag == None:
            return self.value
        else:
            string_i_need = self.props_to_html()
            return "<"+self.tag+string_i_need+">"+self.value+"</"+self.tag+">"
    def __repr__(self):
        print(self.tag, self.value, self.props)
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
        self.props = props
    def to_html(self):
        if self.children ==  None:
            raise ValueError
        elif self.tag == None:
            raise ValueError
        else:
            string_in_the_middle = ""
            for i in self.children:
                string_in_the_middle = string_in_the_middle + i.to_html()
            return "<"+self.tag+self.props_to_html()+">"+string_in_the_middle+"</"+self.tag+">"