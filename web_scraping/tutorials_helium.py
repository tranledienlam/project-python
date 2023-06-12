from helium import *

start_firefox('https://store.steampowered.com/search/?filter=topsellers')

press(PAGE_DOWN)

games_list = find_all(S('.title'))

games = [item.web_element.text for item in games_list]
print(games)