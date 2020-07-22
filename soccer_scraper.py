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
        pass


    def get_ladder(self):
        pass


def main():
    # Enter Team name, age, grade
    team = TeamScraper('Gymea United', 'WS', 'G') 
    
    fixtures = team.get_fixtures()
    
if __name__ == '__main__':
    main()