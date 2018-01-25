# import csv
# from bs4 import BeautifulSoup
# import requests
# from requests.adapters import HTTPAdapter
# from requests.packages.urllib3.poolmanager import PoolManager
# from multiprocessing import Pool
# import ssl
#
#
# class SSLAdapter(HTTPAdapter):
#     '''An HTTPS Transport Adapter that uses an arbitrary SSL version.'''
#
#     def __init__(self, ssl_version=None, **kwargs):
#         self.ssl_version = ssl_version
#
#         super(SSLAdapter, self).__init__(**kwargs)
#
#     def init_poolmanager(self, connections, maxsize, block=False):
#         self.poolmanager = PoolManager(num_pools=connections,
#                                        maxsize=maxsize,
#                                        block=block,
#                                        ssl_version=self.ssl_version)
#
#
# def getMatches(soup, type):
#     try:
#         matches = []
#         table = soup.find('table', {'class': 'stats-table no-sort'}).tbody
#         for row in table.find_all('tr'):
#             m = {}
#             matchDate = row.find('td', class_='time').a.text
#             matchDate = matchDate.split('/')
#             m['matchDate'] = matchDate[2] + '-' + matchDate[1] + '-' + matchDate[0]
#             m['event'] = row.find('td', class_='gtSmartphone-only').text
#             m['map'] = row.find('td', class_='statsMapPlayed').text
#             score = row.find('td', class_='gtSmartphone-only text-center ').span.text
#             score = score.split('-')
#             m['score'] = score[0]
#             m['opponentScore'] = score[1]
#             opponent = row.contents[7].a.text
#             m['opponent'] = opponent
#             matchId = row.find('td', class_='time').a.get('href')
#             matchId = matchId.split('/')[4]
#             m['matchId'] = matchId
#             if int(score[0]) > int(score[1]):
#                 m['result'] = 'W'
#             elif int(score[0]) == int(score[1]):
#                 m['result'] = 'T'
#             else:
#                 m['result'] = 'L'
#             m['type'] = type
#             matches.append(m)
#         return matches
#     except requests.ConnectionError as e:
#         print(str(e))
#         raise e
#     except requests.Timeout as e:
#         print(str(e))
#         raise e
#     except requests.RequestException as e:
#         print(str(e))
#         raise e
#     except (AttributeError, KeyError) as e:
#         print(str(e))
#         raise e
#     except KeyboardInterrupt as e:
#         print(str(e))
#         raise e
#
#
# def exportMatchStats(team, s):
#     try:
#         matches = []
#         url = 'https://www.hltv.org/stats/teams/matches/{}/{}/?minLineupMatch={}' \
#             .format(team['teamId'], team['name'], str(len(team['lineup'])))
#         for name, playerId in team['lineup'].items():
#             url += '&lineup=' + playerId
#
#         response = s.get(url + '&matchType=Online')
#         html = response.content
#         soup = BeautifulSoup(html, 'html.parser')
#
#         matches += getMatches(soup, 'online')
#
#         response = s.get(url + '&matchType=Lan')
#         html = response.content
#         soup = BeautifulSoup(html, 'html.parser')
#         matches += getMatches(soup, 'lan')
#
#         myFile = open(team['name'] + '*match-stats.csv', 'w')
#         with myFile:
#             # myFields = ['matchDate', 'event', 'map', 'score', 'opponent','opponentScore', 'result', 'type', 'matchId']
#             myFields = matches[0].keys()
#             writer = csv.DictWriter(myFile, fieldnames=myFields)
#             writer.writeheader()
#             writer.writerows(matches)
#     except requests.ConnectionError as e:
#         print(str(e))
#         raise e
#     except requests.Timeout as e:
#         print(str(e))
#         raise e
#     except requests.RequestException as e:
#         print(str(e))
#         raise e
#     except (AttributeError, KeyError) as e:
#         print(str(e))
#         raise e
#     except KeyboardInterrupt as e:
#         print(str(e))
#         raise e
#
#
# def getLineupIds(team, s):
#     try:
#         url = 'https://www.hltv.org/stats/teams/lineups/{}/{}'.format(team['teamId'], team['name'])
#         response = s.get(url)
#         html = response.content
#         soup = BeautifulSoup(html, 'html.parser')
#         ids = {}
#         for player in soup.find('div', {'class': 'grid'}) \
#                 .find_all('div', {'class': 'teammate-info standard-box'}):
#             info = player.find('a', {'class': 'image-and-label'})
#             info = info['href'].split('/');
#             ids[info[4]] = info[3]
#         return ids
#     except requests.ConnectionError as e:
#         print(str(e))
#         raise e
#     except requests.Timeout as e:
#         print(str(e))
#         raise e
#     except requests.RequestException as e:
#         print(str(e))
#         raise e
#     except (AttributeError, KeyError) as e:
#         print(str(e))
#         raise e
#     except KeyboardInterrupt as e:
#         print(str(e))
#         raise e
#
#
# def getPlayerStats(soup):
#     try:
#         stats = []
#         table = soup.find('table', {'class': 'stats-table no-sort'}).tbody
#         for row in table.find_all('tr'):
#             s = {}
#             matchDate = row.find('div', class_='time').text
#             matchDate = matchDate.split('/')
#             s['matchDate'] = matchDate[2] + '-' + matchDate[1] + '-' + matchDate[0]
#             s['rating'] = row.select('td[class*="match"]')[0].text.split(' ')[0]
#             matchId = row.td.a.get('href')
#             matchId = matchId.split('/')[4]
#             s['matchId'] = matchId
#             stats.append(s)
#         return stats
#     except (AttributeError, KeyError) as e:
#         print(str(e))
#         raise e
#     except KeyboardInterrupt as e:
#         print(str(e))
#         raise e
#
#
# def exportPlayerStats(name, teamId, s):  # We will take their rating from HLTV
#     try:
#         url = 'https://www.hltv.org/stats/players/matches/{}/{}'.format(teamId, name)
#         response = s.get(url)
#         html = response.content
#         soup = BeautifulSoup(html, 'html.parser')
#         stats = getPlayerStats(soup)
#         myFile = open(name + '*player-stats.csv', 'w')
#         with myFile:
#             myFields = stats[0].keys()
#             writer = csv.DictWriter(myFile, fieldnames=myFields)
#             writer.writeheader()
#             writer.writerows(stats)
#     except requests.ConnectionError as e:
#         print(str(e))
#         raise e
#     except requests.Timeout as e:
#         print(str(e))
#         raise e
#     except requests.RequestException as e:
#         print(str(e))
#         raise e
#     except (AttributeError, KeyError) as e:
#         print(str(e))
#         raise e
#     except KeyboardInterrupt as e:
#         print(str(e))
#         raise e
#
#
# def getTop30Teams(s):
#     try:
#         url = 'https://www.hltv.org/ranking/teams/'
#         response = s.get(url)
#         html = response.content
#         soup = BeautifulSoup(html, 'html.parser')
#         teamDirectory = {}
#         for team in soup.findAll('div', class_='ranked-team standard-box'):
#             rank = team.find('span', class_='position').text
#             rank = rank.split('#')[1]
#             info = team.find('span', class_='name js-link').get('data-url')
#             info = info.split('/')
#             name = info[3]
#             teamId = info[2]
#             teamDirectory[name] = dict(name=name, teamId=teamId, rank=rank)
#         return teamDirectory
#     except requests.ConnectionError as e:
#         print(str(e))
#         raise e
#     except requests.Timeout as e:
#         print(str(e))
#         raise e
#     except requests.RequestException as e:
#         print(str(e))
#         raise e
#     except (AttributeError, KeyError) as e:
#         print(str(e))
#         raise e
#     except KeyboardInterrupt as e:
#         print(str(e))
#         raise e
#
#
# def exportTeamRankList(teamDirectory):
#     myFile = open('team-rankings.csv', 'w')
#     with myFile:
#         myFields = ['name', 'rank', 'lineup']
#         writer = csv.DictWriter(myFile, fieldnames=myFields)
#         writer.writeheader()
#         writer.writerows(teamDirectory)
#     print("team-ranking")
#
#
# def getRank(teamName, id, s):
#     try:
#         url = 'https://www.hltv.org/team/{}/{}'.format(id, teamName)
#         response = s.get(url)
#         html = response.content
#         soup = BeautifulSoup(html, 'html.parser')
#         rank = soup.find('div', class_='standard-box profileTopBox clearfix').find('div', class_="").contents[8].text
#         rank = rank.split('#')[1]
#         return rank
#     except requests.ConnectionError as e:
#         print(str(e))
#         raise e
#     except requests.Timeout as e:
#         print(str(e))
#         raise e
#     except requests.RequestException as e:
#         print(str(e))
#         raise e
#     except (AttributeError, KeyError) as e:
#         print(str(e))
#         raise e
#     except KeyboardInterrupt as e:
#         print(str(e))
#         raise e
#
#
# def main():
#     try:
#         s = requests.Session()
#         s.mount('https://', SSLAdapter(ssl.PROTOCOL_TLSv1_2))
#         teamDirectory = {}
#         while True:
#             cmd = input("1. Get stats of top 30 teams \n2. Enter team to be fetched: \nq\n")
#             if cmd == "1":
#                 teamDirectory.update(getTop30Teams(s))
#                 for key, val in teamDirectory.items():
#                     teamDirectory[key]['lineup'] = getLineupIds(val, s)
#                     exportMatchStats(val, s)
#                     print(key)
#                     for name, teamId in teamDirectory[key]['lineup'].items():
#                         print(name)
#                         exportPlayerStats(name, teamId, s)
#             elif cmd == "2":
#                 teamName = input("Team name:")
#                 teamId = input("Hltv team id:")
#                 teamDirectory[teamName] = dict(name=teamName, teamId=teamId)
#                 teamDirectory[teamName]['rank'] = getRank(teamName, teamId, s)
#                 teamDirectory[teamName]['lineup'] = getLineupIds(teamDirectory[teamName], s)
#                 exportMatchStats(teamDirectory[teamName], s)
#                 print(teamName)
#                 for name, teamId in teamDirectory[teamName]['lineup'].items():
#                     exportPlayerStats(name, teamId, s)
#                     print(name)
#             else:
#                 break
#         exportTeamRankList(teamDirectory)
#     except(AttributeError, KeyError) as e:
#         print("End process due to attribute error")
#     except KeyboardInterrupt as e:
#         print("End process by keyboard interruption")
#     except requests.Timeout as e:
#         print("Timeout")
#     except requests.RequestException as e:
#         print('Requests error')
#main()



import csv
import multiprocessing
import signal
from multiprocessing import Pool
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
import requests
from bs4 import BeautifulSoup
import ssl
import time


class SSLAdapter(HTTPAdapter):
    '''An HTTPS Transport Adapter that uses an arbitrary SSL version.'''

    def __init__(self, ssl_version=None, **kwargs):
        self.ssl_version = ssl_version

        super(SSLAdapter, self).__init__(**kwargs)

    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(num_pools=connections,
                                       maxsize=maxsize,
                                       block=block,
                                       ssl_version=self.ssl_version)


def getSoup(url):
    s = requests.Session()
    s.mount('https://', SSLAdapter(ssl.PROTOCOL_TLSv1_2))
    response = s.get(url)
    html = response.content
    soup = BeautifulSoup(html, 'html.parser')
    return soup


def getMatches(soup, type):
    try:
        matches = []
        table = soup.find('table', {'class': 'stats-table no-sort'}).tbody
        for row in table.find_all('tr'):
            m = {}
            matchDate = row.find('td', class_='time').a.text
            matchDate = matchDate.split('/')
            m['matchDate'] = matchDate[2] + '-' + matchDate[1] + '-' + matchDate[0]
            m['event'] = row.find('td', class_='gtSmartphone-only').text
            m['map'] = row.find('td', class_='statsMapPlayed').text
            score = row.find('td', class_='gtSmartphone-only text-center ').span.text
            score = score.split('-')
            m['score'] = score[0]
            m['opponentScore'] = score[1]
            opponent = row.contents[7].a.text
            m['opponent'] = opponent
            matchId = row.find('td', class_='time').a.get('href')
            matchId = matchId.split('/')[4]
            m['matchId'] = matchId
            if int(score[0]) > int(score[1]):
                m['result'] = 'W'
            elif int(score[0]) == int(score[1]):
                m['result'] = 'T'
            else:
                m['result'] = 'L'
            m['type'] = type
            matches.append(m)
        return matches
    except requests.ConnectionError as e:
        print(str(e))
        raise e
    except requests.Timeout as e:
        print(str(e))
        raise e
    except requests.RequestException as e:
        print(str(e))
        raise e
    except (AttributeError, KeyError) as e:
        print(str(e))
        raise e
    except KeyboardInterrupt as e:
        print(str(e))
        raise e


def exportMatchStats(team):
    try:
        matches = []
        url = 'https://www.hltv.org/stats/teams/matches/{}/{}/?minLineupMatch={}' \
            .format(team['teamId'], team['name'], str(len(team['lineup'])))
        for name, playerId in team['lineup'].items():
            url += '&lineup=' + playerId

        soup = getSoup(url + '&matchType=Online')
        matches += getMatches(soup, 'online')

        soup = getSoup(url + '&matchType=Lan')
        matches += getMatches(soup, 'lan')

        myFile = open(team['name'] + '*match-stats.csv', 'w')
        with myFile:
            # myFields = ['matchDate', 'event', 'map', 'score', 'opponent','opponentScore', 'result', 'type', 'matchId']
            myFields = matches[0].keys()
            writer = csv.DictWriter(myFile, fieldnames=myFields)
            writer.writeheader()
            writer.writerows(matches)
        print(team + ' stats exported to csv')
    except requests.ConnectionError as e:
        print(str(e))
        raise e
    except requests.Timeout as e:
        print(str(e))
        raise e
    except requests.RequestException as e:
        print(str(e))
        raise e
    except (AttributeError, KeyError) as e:
        print(str(e))
        raise e
    except KeyboardInterrupt as e:
        print(str(e))
        raise e


def getLineupIds(team):
    try:
        url = 'https://www.hltv.org/stats/teams/lineups/{}/{}'.format(team['teamId'], team['name'])
        soup = getSoup(url)
        ids = {}
        for player in soup.find('div', {'class': 'grid'}) \
                .find_all('div', {'class': 'teammate-info standard-box'}):
            info = player.find('a', {'class': 'image-and-label'})
            info = info['href'].split('/');
            ids[info[4]] = info[3]
        return ids
    except requests.ConnectionError as e:
        print(str(e))
        raise e
    except requests.Timeout as e:
        print(str(e))
        raise e
    except requests.RequestException as e:
        print(str(e))
        raise e
    except (AttributeError, KeyError) as e:
        print(str(e))
        raise e
    except KeyboardInterrupt as e:
        print(str(e))
        raise e


def getPlayerStats(soup):
    try:
        stats = []
        table = soup.find('table', {'class': 'stats-table no-sort'}).tbody
        for row in table.find_all('tr'):
            s = {}
            matchDate = row.find('div', class_='time').text
            matchDate = matchDate.split('/')
            s['matchDate'] = matchDate[2] + '-' + matchDate[1] + '-' + matchDate[0]
            s['rating'] = row.select('td[class*="match"]')[0].text.split(' ')[0]
            matchId = row.td.a.get('href')
            matchId = matchId.split('/')[4]
            s['matchId'] = matchId
            stats.append(s)
        return stats
    except (AttributeError, KeyError) as e:
        print(str(e))
        raise e
    except KeyboardInterrupt as e:
        print(str(e))
        raise e


def exportPlayerStats(name, teamId):  # We will take their rating from HLTV
    try:
        url = 'https://www.hltv.org/stats/players/matches/{}/{}'.format(teamId, name)
        soup = getSoup(url)
        stats = getPlayerStats(soup)
        myFile = open(name + '*player-stats.csv', 'w')
        with myFile:
            myFields = stats[0].keys()
            writer = csv.DictWriter(myFile, fieldnames=myFields)
            writer.writeheader()
            writer.writerows(stats)
        print(name + ' stats exported to csv')
    except requests.ConnectionError as e:
        print(str(e))
        raise e
    except requests.Timeout as e:
        print(str(e))
        raise e
    except requests.RequestException as e:
        print(str(e))
        raise e
    except (AttributeError, KeyError) as e:
        print(str(e))
        raise e
    except KeyboardInterrupt as e:
        print(str(e))
        raise e


def getTop30Teams():
    try:
        url = 'https://www.hltv.org/ranking/teams/'
        soup = getSoup(url)
        teamDirectory = {}
        for team in soup.findAll('div', class_='ranked-team standard-box'):
            rank = team.find('span', class_='position').text
            rank = rank.split('#')[1]
            info = team.find('span', class_='name js-link').get('data-url')
            info = info.split('/')
            name = info[3]
            teamId = info[2]
            teamDirectory[name] = dict(name=name, teamId=teamId, rank=rank)
        return teamDirectory
    except requests.ConnectionError as e:
        print(str(e))
        raise e
    except requests.Timeout as e:
        print(str(e))
        raise e
    except requests.RequestException as e:
        print(str(e))
        raise e
    except (AttributeError, KeyError) as e:
        print(str(e))
        raise e
    except KeyboardInterrupt as e:
        print(str(e))
        raise e


def exportTeamRankList(teamDirectory):
    myFile = open('team-rankings.csv', 'w')
    with myFile:
        myFields = ['name', 'rank', 'lineup']
        writer = csv.DictWriter(myFile, fieldnames=myFields)
        writer.writeheader()
        writer.writerows(teamDirectory)
    print("team-ranking")


def getRank(teamName, id):
    try:
        url = 'https://www.hltv.org/team/{}/{}'.format(id, teamName)
        soup = getSoup(url)
        rank = soup.find('div', class_='standard-box profileTopBox clearfix').find('div', class_="").contents[8].text
        rank = rank.split('#')[1]
        return rank
    except requests.ConnectionError as e:
        print(str(e))
        raise e
    except requests.Timeout as e:
        print(str(e))
        raise e
    except requests.RequestException as e:
        print(str(e))
        raise e
    except (AttributeError, KeyError) as e:
        print(str(e))
        raise e
    except KeyboardInterrupt as e:
        print(str(e))
        raise e


def init_worker():
    signal.signal(signal.SIGINT, signal.SIG_IGN)

def main():
    try:
        p = multiprocessing.Pool(10, init_worker)
        teamDirectory = {}
        while True:
            cmd = input("1. Get stats of top 30 teams: \n2. Enter team to be fetched: \nq\n")
            if cmd == "1":
                teamDirectory.update(getTop30Teams())
                listLineups = p.map(getLineupIds, teamDirectory.values())
                x = 0
                for team in teamDirectory.keys():
                    teamDirectory[team]['lineup'] = listLineups[x]
                    x += 1
                playerIdTuple = []
                for lineup in listLineups:
                    playerIdTuple.extend([(name, playerId) for name, playerId in lineup.items()])
                p.starmap(exportPlayerStats, playerIdTuple)
                p.map(exportMatchStats, teamDirectory.values())
            elif cmd == "2":
                teamName = input("Team name:")
                teamId = input("Hltv team id:")
                teamDirectory[teamName] = dict(name=teamName, teamId=teamId)
                teamDirectory[teamName]['rank'] = getRank(teamName, teamId)
                teamDirectory[teamName]['lineup'] = getLineupIds(teamDirectory[teamName])
                exportMatchStats(teamDirectory[teamName])
                for name, teamId in teamDirectory[teamName]['lineup'].items():
                    exportPlayerStats(name, teamId)

            else:
                break
        exportTeamRankList(teamDirectory)
    except(AttributeError, KeyError) as e:
        print("End process due to attribute error")
    except KeyboardInterrupt as e:
        print("End process by keyboard interruption")
    except requests.Timeout as e:
        print("Timeout")
    except requests.RequestException as e:
        print('Requests error')
    finally:
        p.terminate()
        p.join()

start_time = time.time()
main()
print("--- %s seconds ---" % (time.time() - start_time))