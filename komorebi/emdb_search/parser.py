from grab import Grab
import pprint
import re
import os


debug = False


class Parser:
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


class Test:
    def __init__(self):
        self.parser = Parser()

    def test_request(self):
        pprint.pprint(self.parser.find_film('Три типа и скрипач', None))

if __name__ == '__main__':
    tester = Test()
    tester.test_request()
