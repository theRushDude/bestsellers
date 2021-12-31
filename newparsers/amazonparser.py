import bs4
from api import urls
from api import pagecache


class AmazonParser:
    def __init__(self):
        self.soup: bs4.BeautifulSoup = pagecache.get(urls['spiegel'])
        self.bestsellers = []
        self.get_bestsellers()

    def get_bestsellers(self) -> dict:
        book_divs = self.soup.find_all('div', {'class': 'w-full bg-white dark:bg-dm-shade-darkest'})
        for book_div in book_divs:
            book = {}
            # rank
            cursor = book_div.find('p', {'class': 'font-sansUI lg:text-3xl md:text-3xl'
                                                  ' sm:text-2xl leading-normal lg:mb-4'
                                                  ' md:mb-4 sm:mb-8'})
            book['rank'] = cursor.text.strip()

            # title
            cursor = book_div.find('span', {'class': 'block font-sansUI font-bold lg:text-xl'
                                                     ' md:text-xl sm:text-base mb-4'})
            book['title'] = cursor.text.strip()

            # author
            cursor = book_div.find('li', {'class': 'mr-8 flex items-center'})
            book['author'] = cursor.text.strip()

            # isbn
            cursor = book_div.find('li', {'class': 'text-black dark:text-shade-lightest'
                                                   ' font-sansUI text-s leading-normal'})
            book['isbn'] = cursor.text.split(' ')[-1].strip()
            self.bestsellers.append(book)
            print(book)
