import requests

def get_category_data():
    page_number = 1
    category_names = []
    category_ids = []
    cat_url = "https://qriusity.com/v1/categories?page={}&limit=20".format(page_number)
    category_data = requests.get(cat_url).json()

    while category_data != []:
        names = [cat["name"] for cat in category_data]
        ids = [cat["id"] for cat in category_data]
        category_names += names
        category_ids += ids
        page_number +=1
        cat_url = "https://qriusity.com/v1/categories?page={}&limit=20".format(page_number)
        category_data = requests.get(cat_url).json()

    categories = dict(zip(category_names, category_ids))
    return categories

def get_questions_by_category(category_id):
    questions = []
    page_number = 1
    questions_url = "https://qriusity.com/v1/categories/{}/questions?page={}&limit=20".format(category_id,page_number)
    questions_data = requests.get(questions_url).json()

    while questions_data!=[]:
        questions += questions_data
        page_number += 1
        questions_url = "https://qriusity.com/v1/categories/{}/questions?page={}&limit=20".format(category_id,page_number)
        questions_data = requests.get(questions_url).json()

    return questions

def clean_cat_name(cat_name):
    clean_name = cat_name.lower().split()
    clean_name = "_".join(clean_name)

    return clean_name

def parse_questions(questions,cat_name):
    with open("data/trivia/{}.txt".format(cat_name),"w") as trivia_file:
        for question_data in questions:
            question = question_data["question"]
            answer_nbr = str(question_data["answers"])
            answer = question_data["option"+answer_nbr]
            answer_formatted = '`'+answer
            q_and_a_line = question+answer_formatted+"\n"
            trivia_file.write(q_and_a_line)

if __name__=="__main__":

    print("Downloading category names")
    categories = get_category_data()
    for cat_name in categories.keys():
        cat_id = categories[cat_name]
        print("Downloading data for {} category".format(cat_name))
        questions_raw = get_questions_by_category(cat_id)
        print("Parsing questions for {} category".format(cat_name))
        parse_questions(questions_raw,clean_cat_name(cat_name))




