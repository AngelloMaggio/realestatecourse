from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import string


def main():
    # Declare globals
    global ff

    # Start Driver
    ff = webdriver.Chrome()





    # Credentials
    username = "mena.malek.mccarthy@gmail.com"
    password = "realestate"

    # Open site
    ff.get("https://yescourse.com/course/6661/")
    sleep(3)

    # Get fields
    u_name = ff.find_element_by_name("username")
    u_pass = ff.find_element_by_name("password")

    # Log in
    u_name.send_keys(username)
    u_pass.send_keys(password)
    u_pass.send_keys(Keys.RETURN)
    sleep(3)

    # Find all unread elements
    while True:

        # Lectures
        read_lectures = ff.find_elements_by_css_selector(".yc-menu-entry.lesson.read")
        locked_lectures = ff.find_elements_by_css_selector(".yc-menu-entry.lesson.locked")
        lectures = ff.find_elements_by_css_selector(".yc-menu-entry.lesson")
        lectures = [lecture for lecture in lectures if (lecture not in locked_lectures) and (lecture not in read_lectures)]

        # Do next lecture
        doLecture(lectures[0])
        ff.back()
        sleep(3)

def doLecture(lecture):

    global answers

    print "-Opened function to do lecture."
    # Open the lecture
    lecture.click()
    sleep(2)


    answers = {0:'A', 1:'B', 2:'C', 3:'D', 4:'E', 5:'F',6:'G'}

    time = ff.find_element_by_id("yc-time-display")
    print '--Time: ', time.text


    mark_completed = ff.find_element_by_class_name("yc-mark-lesson-read")

    while True:

        try:
            mark_completed.click()
            print "---done"
            break

        except Exception as e:

            try:
                quiz_button = ff.find_element_by_css_selector('.action.attempt_now')
                print '---Found Quiz Button----' + str(e)
                #doChapterQuiz(quiz_button)
                doDDQuiz(quiz_button)
                break
            except:
                print '----Waiting for time to be done....' + str(e)
                sleep(10)
                pass

def doChapterQuiz(quiz_button):
    quiz_button.click()
    print "Finding answers"
    sleep(3)
    choice_answers = ff.find_elements_by_xpath('//input[@value="A"]')
    for answer in choice_answers:
        answer.click()
    while True:
        try:
            submit_button = ff.find_element_by_id("submit_exam")
            submit_button.click()
            "Clicked activity submit button"
            sleep(3)
            break
        except:
            pass


def doDDQuiz(quiz_button):

    global answers

    quiz_button.click()
    sleep(4)

    dd_numbs = dict.fromkeys(string.ascii_uppercase, 0)
    questions = ff.find_elements_by_class_name("question")
    questions_str = []
    for question in questions:
        questions_str(question.text.split('\n')[0])

    question_count = len(questions)

    print dd_numbs

    print "There are " + str(question_count) + " questions."
    for i in range(0, question_count):
        print "Doing dropdown number", i
        questions[i].click()
        print "Clicked the question."

        dropdown = ff.find_element_by_name("exam_"+str(i))
        dropdown.click()
        print "Clicked the dropdown"
        sleep(1)
        print "Going to look at the value"
        print i
        if questions_str[i] not in answers:
            answers[questions_str[i]] = 'A'
        try:
            value = answers[questions_str[i]]
        except:
            print "AHA!"
        print value
        print '//option[@value="'+ value +'"]'
        choice = dropdown.find_element_by_xpath('.//option[@value="'+ value +'"]')
        choice.click()
        print "Clicked answer"


    while True:
        try:
            submit_button = ff.find_element_by_id("submit_exam")
            submit_button.click()
            "Clicked activity submit button"
            sleep(3)
            break
        except:
            pass

    answers = [ans.text for ans in ff.find_elements_by_tag_name("td")][-10:]
    my_answers = answers[::2]
    correct_answers = answers[1::2]

    for i in range(0, len(correct_answers)):
        answers[i] = correct_answers[i]
    sleep(5)

    #while True:



if __name__ == '__main__':
    main()