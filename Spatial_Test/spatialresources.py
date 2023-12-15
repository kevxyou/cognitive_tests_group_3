# added by PWL to force images to be downloaded before test starts
import glob
from IPython.display import HTML
png_list = glob.glob("*.jpg")
image_list = ""
for png in png_list:
    image_list+=f"<image src='{png}' width='1px' >"
display(HTML('<p>'+image_list+'</p>'))

from IPython.display import display, Image, clear_output, HTML
import time
import random

'''dictionary that assigns each cube to a question. 
this will be used as an arguement in the question function
ticks and grid are set to true so gridlines and ticks will be seen in the qustion'''
imagedict = {'q1':'image1.png',
             'q2' : 'image2.png',
             'q3' : 'image3.png',
             'q4' : 'image4.png',
             'q5' : 'image5.png',
             'q6' : 'image6.png'    
            }

def question(qnumber, choice1, choice2, choice3, correctchoice):
    '''first arguement takes the filename of the 3D image as a string. the next 4 arguements take the 2D image options also as a string'''
    optionlist = ['A', 'B', 'C', 'D']
    qlist = [choice1, choice2, choice3, correctchoice]
    qlistr= qlist.copy()
    seed_value = len(results)
    '''the same seed value cannot be used for all questions otherwise all the correct answers will be under the same option.
    therefore by adding one to the seed value after each question, the option with the correct answer will be different.
    also because the seed value restarts(since results is wiped after each run of spatial), all recipients of the test will get the same set of randomized options'''
    random.seed(seed_value)
    random.shuffle(qlistr)
    #qlist with the 4 options are copied and randomized
    from IPython.display import Image, display
    #image of 3d image is reduced so the 3d image and the 4 options can be viewed together with minimal scrolling
    display(Image(imagedict[qnumber], width=400, height=40))

    #the following code displays the 4 options in a 2 by 2 grid.
    images_html = '<div style="display:flex; flex-wrap:wrap;">'
    image_width = 150
    image_height = 150
    for i, img in enumerate(qlistr[:4]):
        images_html += f'<div style="flex:50%;">{chr(97+i)}.<br><img src="{img}" style="width:{image_width}px; height:{image_height}px;"/></div>'
        if img == qlist[-1]:
            correctans = optionlist[i]
            #the correct answer is the option in which the image appears under
    display(HTML(images_html))   
    start_time = time.time()
    ans = input("Enter the correct option:")
    while ans.upper() not in optionlist:
        print("Enter the correct option:")
        ans = input(">")
    #makes sure test taker will only enter a single letter e.g B for option B and not 'Option B' or othrer variants
    score = 0
    if ans.upper() != correctans.upper():
        print(f"Incorrect. your get {score} marks")
    else:  
        score += 1
        print(f"Correct. you get {score} mark") 
        total_score_list.append('Correct')
    end_time = time.time()
    time_taken = end_time - start_time
    results.append(str(ans.upper()))
    time_taken_for_each_question.append(time_taken)
    #kees a log of answers provided by recipient
    time.sleep(0.5)
    clear_output(wait=False)
    #the question will be cleared after attempt
    return score


def spatial():
    '''runs the entire test. the question function above is called 6 times, once for each question. no arguements are needed'''
    intro = '''
    Please run all cells above so the test will work.
    This test will asses your spatial reasoning.
    For each question you will be given a 3D shape and 4 2D images. 
    You will have to determine which of the 2D images cannot be produced by rotation of the 3D shape
    Please enter the letter of the correct option if you think that option is correct 
    e.g if you think option C is correct, enter the letter "c" or "C" and press enter 
    '''
    
    id_instructions = """

    Enter your anonymised ID
    
    To generate an anonymous 4-letter unique user identifier please enter:
    - two letters based on the initials (first and last name) of a childhood friend
    - two letters based on the initials (first and last name) of a favourite actor / actress
    
    e.g. if your friend was called Charlie Brown and film star was Tom Cruise
         then your unique identifer would be CBTC
    """
    print(intro)
    print(id_instructions)
    #golobalized variables will be sent to a google form
    global user_id
    user_id = input("> ")
    
    print("User entered id:", user_id)


    print("enter your age")
    global age
    age = input(">")
    print("enter your sex(M/F)")
    global sex
    sex = input(">")
    while sex.lower() != 'm' and sex.lower() != 'f':
        print("enter your sex")
        sex = input(">")
    #makes sure user only inputs M or F
    global results
    global time_taken_for_each_question
    global total_score_list
    results = []
    time_taken_for_each_question=[]
    total_score_list =[]
    #everytime an answer is correct, total_score_list will be appended in the question function
    total_time = 0
    
    #retrieves current time
    question('q1', 'q1a.png','q1b.png','q1c.png','q1correct.png')
    question('q2','q2a.png','q2b.png','q2c.png','q2correct.png')
    question('q3', 'q3a.png','q3b.png','q3c.png','q3correct.png')
    question('q4', 'q4a.png','q4b.png','q4c.png','q4correct.png')
    question('q5', 'q5a.png','q5b.png','q5c.png','q5correct.png')
    question('q6', 'q6a.png','q6b.png','q6c.png','q6correct.png')
    #displays questions after the previous question has been attempted
  
    #retrieves current time again
    
    #calculate total time taken to compete the test
    total_score=len(total_score_list)
    #calculates total score by counting the amount of times total_score_list has been appended
    data_dict = {
    'user_id': user_id.upper(),
    'age': age,
    'sex' : sex.upper(),
    'Q1': results[0],
    'Q2': results[1],
    'Q3': results[2],
    'Q4': results[3],
    'Q5': results[4],
    'Q6': results[5],
    'Q1 time':time_taken_for_each_question[0],
    'Q2 time':time_taken_for_each_question[1],
    'Q3 time':time_taken_for_each_question[2],
    'Q4 time':time_taken_for_each_question[3],
    'Q5 time':time_taken_for_each_question[4],
    'Q6 time':time_taken_for_each_question[5],
    'Total Score': len(total_score_list),
    'Total Time Taken' : sum(time_taken_for_each_question)
    }
    import requests
    from bs4 import BeautifulSoup
    import json
    
    def send_to_google_form(data_dict, form_url):
        ''' Helper function to upload information to a corresponding google form 
            You are not expected to follow the code within this function!
        '''
        form_id = form_url[34:90]
        view_form_url = f'https://docs.google.com/forms/d/e/{form_id}/viewform'
        post_form_url = f'https://docs.google.com/forms/d/e/{form_id}/formResponse'
    
        page = requests.get(view_form_url)
        content = BeautifulSoup(page.content, "html.parser").find('script', type='text/javascript')
        content = content.text[27:-1]
        result = json.loads(content)[1][1]
        form_dict = {}
        
        loaded_all = True
        for item in result:
            if item[1] not in data_dict:
                print(f"Form item {item[1]} not found. Data not uploaded.")
                loaded_all = False
                return False
            form_dict[f'entry.{item[4][0][0]}'] = data_dict[item[1]]
        
        post_result = requests.post(post_form_url, data=form_dict)
        return post_result.ok
    data_consent_info = """DATA CONSENT INFORMATION:

    Please read:
    
    we wish to record your response data
    to an anonymised public data repository. 
    Your data will be used for educational teaching purposes
    practising data analysis and visualisation.
    
    Please type   yes   in the box below if you consent to the upload."""
    
    print(data_consent_info)
    result = input("> ") 
    
    if result == "yes": 
        print("Thanks for your participation.")
        print("Please contact philip.lewis@ucl.ac.uk")
        print("If you have any questions or concerns")
        print("regarding the stored results.")
        form_url = "https://docs.google.com/forms/d/e/1FAIpQLSdiNbsA6F72IAZQasRfW8-EA2XxaDiiTaxS3hzhRC9dF0pj3Q/viewform usp=sf_link"
        send_to_google_form(data_dict, form_url)
        
    else: 
        # end code execution by raising an exception
        raise(Exception("User did not consent to continue test."))


    return total_score, sum(time_taken_for_each_question), results