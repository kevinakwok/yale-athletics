from athletic_functions import *


output_file = "results.txt"


file_name = 'athletics_homepage.txt'
strip_words = ['Home', 'Coaches']

teams = get_and_clean_list(file_name, strip_words)

output_to_txt(list_all_teams(teams), output_file)
