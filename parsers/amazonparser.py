from api.pagecache import PageCache

class AmazonParser(BookParser):
    def __init__(self):
        super().__init__()
        self.in_book_description = False
        self.details = []

    def get_details(self, amazon_url: str):
        headers = {'User-Agent': USER_AGENT}
        response = requests.get(amazon_url, headers=headers)
        response.raise_for_status()
        self.feed(response.text)
        details = self.details
        self.details = []
        return details

    @staticmethod
    def is_book_description_tag(tag: Tag):
        if tag.name == 'div':
            if tag['data-feature-name'] == 'bookDescription':
                return True
            if tag['id'] == 'bookDescription_feature_div':
                return True
        return False

    def handle_starttag(self, tag_name, attrs):
        tag = Tag(tag_name, dict(attrs))
        if BookParser.has_closing_tag(tag):
            self.tag_stack.append(tag)

        if AmazonParser.is_book_description_tag(tag):
            assert not self.in_book_description
            self.in_book_description = True
            print('entered description')

    def handle_endtag(self, tag):
        if not self.tag_stack:
            return

        popped_tag = self.tag_stack.pop()
        if AmazonParser.is_book_description_tag(popped_tag):
            assert self.in_book_description
            self.in_book_description = False
            print('left description')

    def handle_data(self, data):
        string_data = str(data).replace('\n', ' ').strip()

        if string_data and self.in_book_description:
            self.details.append(string_data)
