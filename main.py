# from parsers.oldspiegelparser import OldSpiegelParser
# from parsers.amazonparser import AmazonParser
from newparsers import spiegelparser as sp


def main():
    # amazon_parser = AmazonParser()
    spiegel_parser = sp.SpiegelParser()
    #print('download spiegel bestsellers')
    #spiegel_parser = OldSpiegelParser()
    #bestsellers = spiegel_parser.get_bestsellers('https://www.spiegel.de/kultur/bestseller-buecher-belletristik'
    #                                             '-sachbuch-auf-spiegel-liste-a-458623.html')

    #for book in bestsellers:
    #    print(book)
    #    print(amazon_parser.get_details(book['amazon_url'])[:2])

    # screwjack test:
    # print(meta('0-684-87321-4', SERVICE))
    # print(desc('0-684-87321-4'))

    # another list to fetch maybe
    # buecherat_url = 'https://www.buecher.at/bestseller-belletristik/'



if __name__ == '__main__':
    main()
