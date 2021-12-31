import requests
from api.bookparser import BookParser


def is_bestseller_accordion(tag):
    return tag['tag_name'] == 'div' \
           and 'data-component' in tag['attrs'] \
           and tag['attrs']['data-component'] == 'BestsellerAccordionSection'


class OldSpiegelParser(BookParser):
    def __init__(self):
        super().__init__()
        self.current_bestseller_section = None
        self.books_found = []

    def get_bestsellers(self, spiegel_url: str):
        response = requests.get(spiegel_url)
        response.raise_for_status()
        self.feed(response.text)
        return self.books_found

    def tagsToString(self, skip_first=0) -> str:
        return '[' + ''.join(
            [f'[{i + skip_first},{tag["tag"]}], ' for i, tag in enumerate(self.tag_stack[skip_first:])]) + ']'

    def handle_starttag(self, tag_name, attrs):
        tag = {'tag_name': tag_name, 'attrs': dict(attrs)}
        if not tag_name in ['link', 'meta', 'input', 'img', 'br']:
            self.tag_stack.append(tag)

        if is_bestseller_accordion(tag):
            assert (self.current_bestseller_section is None)
            self.current_bestseller_section = {}

    def handle_endtag(self, tag):
        popped_tag = self.tag_stack.pop()
        assert (popped_tag['tag_name'] == tag)
        if is_bestseller_accordion(popped_tag):
            assert (self.current_bestseller_section is not None)
            self.books_found.append(self.current_bestseller_section)
            self.current_bestseller_section = None

    def handle_data(self, data):
        if self.current_bestseller_section is not None:
            string_data = str(data).strip().replace('\n', ' ')
            tag = self.tag_stack[-1]['tag_name']
            attrs = self.tag_stack[-1]['attrs']

            # rank
            if 'class' in attrs:
                if tag == 'p' and attrs['class'] == 'font-sansUI lg:text-3xl md:text-3xl sm:text-2xl leading-normal lg:mb-4 md:mb-4 sm:mb-8':
                    self.current_bestseller_section['rank'] = string_data
                elif tag == 'span' and attrs['class'] == 'align-middle':
                    self.current_bestseller_section['title'] = string_data
                elif tag == 'li' and attrs['class'] == 'text-black dark:text-shade-lightest font-sansUI text-s leading-normal':
                    self.current_bestseller_section['isbn'] = string_data.split(':')[1].strip()

            elif tag == 'p':
                if not 'author' in self.current_bestseller_section:
                    self.current_bestseller_section['author'] = string_data

            elif tag == 'a':
                if 'href' in attrs and str(attrs['href']).find('amazon') != -1:
                    self.current_bestseller_section['amazon_url'] = attrs['href']

    def test_data_handler(self, data):
        titles = ['Never. Die letzte Entscheidung', 'Der Zorn des Oktopus', 'Hast du uns endlich gefunden',
                  'Die Enkelin', 'Morgen, Klufti, wird\'s was geben']
        authors = ['Follett, Ken', 'Rossmann, Dirk; Hoppe, Ralf', 'Selge, Edgar', 'Schlink, Bernhard']

        string_data = str(data).strip().replace('\n', ' ')
        if string_data in titles:
            self.test_title_matches.append({'tag': self.tag_stack[-1], 'title': string_data})
            print(f'test - {self.tagsToString(6)} | title: {string_data}')

        if string_data in authors:
            self.test_author_matches.append({'tag': self.tag_stack[-1], 'author': string_data})
