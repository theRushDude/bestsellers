from html.parser import HTMLParser


class Tag:
    def __init__(self, tag_name: str, attrs: dict):
        self.name: str = tag_name
        self.attrs: dict = attrs
        self.tag_stack: list[Tag] = []

    def __getitem__(self, name):
        if name in self.attrs:
            return self.attrs[name]
        else:
            return ''

    def __contains__(self, item):
        return item in self.attrs

class BookParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tag_stack = []

    @staticmethod
    def has_closing_tag(tag: Tag):
        return tag.name not in ['link', 'meta', 'input', 'img', 'br']

    def tags_as_str(self, sep: str = ' ', fill=5):
        if not self.tag_stack:
            return ''.ljust(fill)
        else:
            strings = [tag.name.ljust(fill) + sep for tag in self.tag_stack]
            return ''.join(strings)
