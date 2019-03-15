# define the correct username and password
username = "Ali-Ibrahim"
password = "Ali-Ibrahim"

# user authentication
while True:
    login_username = raw_input('Enter your username: ')
    login_password = raw_input('Enter your password: ')
    if username == login_username and password == login_password:
        print('Successfully Logged In! ')
        break
    # keep looping until correct username and password are used
    print('Invalid username or password !')
# questins and answers files
questins = open('Questions.txt', 'r')
answers  = open('Answers.txt', 'r')
correct = 0
question_count = 0
# read the questions file
q_lines = questins.readlines()
for q_line in q_lines:
    if q_line[0] == '-':
        # questins are seperated by a line of dashes -
        question_count += 1
        user_answer = raw_input('Enter your answer: ')
        user_answer+='\n'
        correct_answer = answers.readline()
        if user_answer == correct_answer:
            # correct answer :D
            correct += 1
        continue
    # print the question:
    print (q_line)
# print (correct)
# calculate percentage grade
grade = correct * 100.0 / question_count
# print the result
if grade >= 50:
    print("Good")
else:
     print('Not Good')
