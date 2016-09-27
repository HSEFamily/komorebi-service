from abc import abstractmethod
from grab import Grab
import pprint
import re
import os


debug = False


class Parser:

    @abstractmethod
    def find_film(self, name, info_elements):
        pass

    @abstractmethod
    def search_film(self, name):
        pass


class ParserImpl(Parser):
    def __init__(self):
        self._g = Grab()
        if debug:
            self._g.setup(log_dir=os.path.dirname(os.path.abspath(__file__)) + '/logs')

    def find_film(self, name, info_elements):
        if not info_elements:
            info_elements = [
                'год',
                'страна',
                'режиссер',
                'слоган',
                'сценарий',
                'продюсер',
                'оператор',
                'композитор',
                'художник',
                'монтаж',
                'жанр',
                'бюджет',
                'маркетинг',
                'сборы в США',
                'сборы в мире',
                'сборы в России',
                'зрители',
                'премьера (мир)',
                'премьера (РФ)',
                'релиз на DVD',
                'возраст',
                'рейтинг MPAA',
                'время',
                'актеры',
                'дублеры'
            ]

        self._g.setup(url='https://www.kinopoisk.ru/index.php')
        self._g.setup(post={
            'first': 'yes',
            'kp_query': name
        })

        self._g.request()
        pq = self._g.doc.pyquery

        if pq('h1.moviename-big').length == 0:
            if debug:
                print('No film(')
            return {'found': False}

        film = {}
        film['found'] = True
        film['id'] = re.search('(?<=/)\d+', self._g.response.url).group(0)
        film['name'] = pq('h1.moviename-big').text()
        film['picture'] = pq('div.film-img-box')('img').attr('src')
        film['description'] = {
            'paragraphs': list(filter(None,
                                      pq('div[itemprop="description"]')
                                      .html()
                                      .split('<br />')))
        }

        film['info'] = {}

        def item_found(i, item):
            try:
                info_name = pq(item)('td.type').text()
                if info_name not in info_elements:
                    return

                info_item_list = []
                if debug:
                    print(info_name)

                def list_item_found(j, item):
                    content = pq(item).text()
                    block = ['...', 'слова']
                    if content in block:
                        return

                    if debug:
                        print('\t' + pq(item).text())
                    info_item_list.append(pq(item).text())

                if info_name == 'слоган':
                    if debug:
                        print('\t' + pq(item)('td[style]').text())
                    film['info'][info_name] = pq(item)('td[style]').text()

                elif info_name == 'сборы в мире':
                    if debug:
                        print('\t' + pq(item)('a').not_('.wordLinks').text())
                    film['info'][info_name] = pq(item)('a').not_('.wordLinks').text()

                elif info_name == 'сборы в России':
                    if debug:
                        print('\t' + pq(item)('div').text())
                    film['info'][info_name] = pq(item)('div').text()

                elif info_name == 'зрители':
                    values = pq(item)('div[style="margin-left: -20px"]').text().split(',')
                    countries = []
                    pq(item).find('img').each(lambda i, item:(
                        countries.append(pq(item).attr('alt'))
                    ))
                    film['info'][info_name] = {}
                    for i in range(len(countries)):
                        if debug:
                            print('\t' + countries[i])
                            print('\t\t' + values[i])
                        film['info'][info_name][countries[i]] = values[i]

                elif info_name == 'возраст':
                    if debug:
                        print('\t' + pq(item)('span').text())
                    film['info'][info_name] = pq(item)('span').text()

                elif info_name == 'рейтинг MPAA':
                    if debug:
                        print('\t' + pq(item)('span').text())
                    film['info'][info_name] = pq(item)('span').text()

                elif info_name == 'время':
                    if debug:
                        print('\t' + pq(item)('td.time').text())
                    film['info'][info_name] = pq(item)('td.time').text()

                else:
                    pq(item).find('a').each(list_item_found)
                    if len(info_item_list) == 1:
                        film['info'][info_name] = info_item_list[0]
                    else:
                        film['info'][info_name] = info_item_list

            except Exception as e:
                if debug:
                    raise Exception(e)

        if 'актеры' in info_elements:
            try:
                film['info']['актеры'] = []
                pq('#actorList').find('ul').eq(0).children('li').each(lambda i, item: (
                    film['info']['актеры'].append(pq(item).text())
                ))
                if film['info']['актеры'][-1] == '...':
                    film['info']['актеры'].remove(film['info']['актеры'][-1])
                if debug:
                    print('актеры')
                    for i in film['info']['актеры']:
                        print('\t' + i)
            except Exception as e:
                if debug:
                    raise e

        if 'дублеры' in info_elements:
            try:
                film['info']['дублеры'] = []
                pq('#actorList').find('ul').eq(1).children('li').each(lambda i, item: (
                    film['info']['дублеры'].append(pq(item).text())
                ))
                if film['info']['дублеры'][-1] == '...':
                    film['info']['дублеры'].remove(film['info']['дублеры'][-1])
                if debug:
                    print('дублеры')
                    for i in film['info']['дублеры']:
                        print('\t' + i)
            except Exception as e:
                if debug:
                    raise e

        pq('table.info').children('tr').each(item_found)
        film['info'] = dict((k, v) for k, v in film['info'].items() if v)

        if debug:
            pprint.pprint(film)

        return film

    def search_film(self, name):
        self._g.setup(url='https://www.kinopoisk.ru/index.php?level=7&m_act%5Bwhat%5D=content&m_act%5Bfind%5D=' + name)
        self._g.request()
        pq = self._g.doc.pyquery

        elements = []

        def parse_element(i, el):
            try:
                pqel = pq(el)
                new_el = {}
                new_el['name'] = pqel('p.name a').text()
                new_el['id'] = pqel('p.name a').attr('data-id')
                new_el['picture'] = 'https://st.kp.yandex.net/images/film/' + new_el['id'] + '.jpg'
                new_el['year'] = pqel('span.year').text()
                new_el['time'] = pqel('div.info span').eq(1).text().split(',')[-1]
                new_el['director'] = pqel('i.director').text()
                try:
                    new_el['genre'] = pqel('div.info span').eq(2).text().split('(')[1][:-1].split(',')
                except Exception as e:
                    new_el['genre'] = []
                new_el['actors'] = []
                try:
                    pqel('div.info span').eq(3)('a.lined').each(lambda i, item: (
                        new_el['actors'].append(pq(item).text())
                    ))
                    if len(new_el['actors']) > 0 and new_el['actors'][-1] == '...':
                        new_el['actors'].remove(new_el['actors'][-1])
                except Exception as e:
                    pass

                elements.append(new_el)
            except Exception as e:
                if debug:
                    raise e

        pq('div.element').each(parse_element)
        return elements


class Test:
    def __init__(self):
        self.parser = ParserImpl()

    def test_film_request(self):
        pprint.pprint(self.parser.find_film('Поймай меня если сможешь', None))

    def test_search_request(self):
        pprint.pprint(self.parser.search_film('привет'))

if __name__ == '__main__':
    tester = Test()
    tester.test_search_request()

