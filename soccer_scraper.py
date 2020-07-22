from bs4 import BeautifulSoup
import requests

class TeamScraper:

    def __init__(self, name, age, grade):
        self.name = name
        self.age = age
        self.grade = grade


    def get_fixtures(self, round=''):
        url = f'http://www.shirefootball.com/ssfixtures.asp?Round={round}&Age={self.age}&Grade={self.grade}&Club={self.name}'
        
        try:
            html = requests.get(url)
        except requests.exceptions.RequestException as e:
            print(e)

        if html.status_code == 200:
            soup = BeautifulSoup(html.text, 'html.parser')
            rows = soup.findChildren('table')[5].findChildren('table')[1].findChildren('tr')[1:]
                    
            fixtures = []            
            
            for row in rows:
                fixture = {}
                fixture['date'] = row('td')[0].text
                fixture['grade'] = row('td')[1].text
                fixture['round'] = row('td')[2].text
                fixture['homeTeam'] = row('td')[3].text
                fixture['awayTeam'] = row('td')[4].text
                fixture['venue'] = row('td')[5].text
                fixture['time'] = row('td')[6].text
                fixtures.append(fixture)

        return fixtures
        

    def get_results(self, round=''):
        url = f'http://www.shirefootball.com/ssresult.asp?Round={round}&Age={self.age}&Grade={self.grade}&Club={self.name}&Date='
        
        try:
            html = requests.get(url)
        except requests.exceptions.RequestException as e:
            print(e)

        if html.status_code == 200:
            soup = BeautifulSoup(html.text, 'html.parser')
            rows = soup.findChildren('table')[5].findChildren('table')[0].findChildren('tr')[1:]
            
            results = []  

            for row in rows:
                result = {}
                result['date'] = row('td')[0].text
                result['round'] = row('td')[2].text
                result['homeTeam'] = row('td')[3].text
                result['homeScore'] = row('td')[4].text
                result['awayScore'] = row('td')[6].text
                result['awayTeam'] = row('td')[7].text
                results.append(result)

        return results


    def get_ladder(self):
        url = f'http://www.shirefootball.com/sstables.asp?Age={self.age}&Grade={self.grade}'

        try:
            html = requests.get(url)
        except requests.exceptions.RequestException as e:
            print(e)

        if html.status_code == 200:
            soup = BeautifulSoup(html.text, 'html.parser')
            rows = soup.findChildren('table')[3].findChildren('tr')[4:-1]
            
            ladder = []           
            
            for row in rows:
                team = {}
                team['position'] = row('td')[1].text[:-1]
                team['name'] = row('td')[2].text
                team['played'] = row('td')[3].text
                team['won'] = row('td')[4].text
                team['drawn'] = row('td')[5].text
                team['lost'] = row('td')[6].text
                team['goalsFor'] = row('td')[7].text
                team['goalsAgainst'] = row('td')[8].text
                team['goalDifference'] = row('td')[9].text
                team['points'] = row('td')[10].text
                ladder.append(team)

        return ladder


def main():
    # Enter team name, age, grade
    team = TeamScraper('Gymea United', 'WS', 'g') 
    
    fixtures = team.get_fixtures()
    keys = fixtures[0].keys()
    with open('fixtures.csv', 'w') as f:        
        w = csv.DictWriter(f, keys)
        w.writeheader()
        w.writerows(fixtures)

    results = team.get_results()
    keys = results[0].keys()
    with open('results.csv', 'w') as f:
        w = csv.DictWriter(f, keys)
        w.writeheader()
        w.writerows(results)

    ladder = team.get_ladder()
    keys = ladder[0].keys()
    with open('ladder.csv', 'w') as f:
        w = csv.DictWriter(f, keys)
        w.writeheader()
        w.writerows(ladder)


if __name__ == '__main__':
    main()