from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

service = Service('/Users/hiteshchowdarysuryadevara/Desktop/chromedriver-mac-arm64/chromedriver')

driver = Chrome(service=service)

driver.get('https://www.goal.com/en-us/live-scores')

# elements = driver.find_elements(By.CLASS_NAME, 'competition_competition__wbjsu')
soup = BeautifulSoup(driver.page_source,'lxml')

elements = soup.find_all('div',class_ = 'competition_competition__wbjsu')


with open('live_scores.txt', 'w') as file:
    for element in elements:
        games = element.find_all('div',class_ = 'row_row__pwLvU row')
        league = element.a.text
        file.write(f'{league}:\n')

        for game in games:
            if game.a.span :
                time = game.a.span.text 
                team_a = game.a.find('div',class_ = 'team_team__CSYuy team_team-a__KZ1AE').h4.text
                score_a = game.a.find('div',class_ = 'result_result__J9gCz').div.find('p','result_team-a__jx1EM').text
                score_b = game.a.find('div',class_ = 'result_result__J9gCz').div.find('p','result_team-b__kNMbF').text
                team_b = game.a.find('div',class_ = 'team_team__CSYuy team_team-b__6xMTs').h4.text
                file.write(f'{time} {team_a} {score_a} - {score_b} {team_b}\n')
            else :
                break
        file.write('\n')

driver.quit()