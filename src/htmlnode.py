class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    def to_html(self):
        raise NotImplementedError
    def props_to_html(self):
        for_str = "href="+self.props["href"]+" target="+self.props["target"]
        return for_str
    def __repr__(self):
        print(self.tag, self.value, self.children, self.props)
    