# Quiz Title
 
**Name:** Zara J. Barte
**Section:** BSINFOTECH SE-3A 
**Topic:** Science Quiz
 
## Features Completed
✅10 multiple-choice questions
✅Random question order
✅15-second countdown timer
✅Answer checking and time-out handling
✅Score and percentage
✅Answer review
✅High score saved in a text file
✅Restart button
 
## How the Questions Are Stored and Shuffled
So, the questions are stored in a list called QUESTIONS and each question is a dictionary. It has three parts: the question text, four choices, and the correct answer letter. For example, one question has the question text, choices A to D, and then "answer": "B" because Roots is the correct answer. So then when the quiz starts, the program uses random.sample() to shuffle the questions and this will makes a new copy of the question list in a different order every time. So, the original QUESTIONS list is not changed.


 
## How the Timer Works
So, the timer starts at 15 seconds for every question. The function update_timer() uses root.after(1000, update_timer). Basically, this means the function runs again after 1,000 milliseconds, or 1 second.
So, every second, the timer goes down by 1. Then, when the timer reaches 0, the function time_up() runs. The question is marked as unanswered and the correct answer is shown, and then the user can go to the next question.
So, when the user clicks Submit Answer, the program calls stop_timer() and this cancels the scheduled timer using timer_job, so the countdown stops right away. Then, the variable answered becomes True and the timer cannot run again for that question.


 
## How the Program Identifies the Correct Answer
In this program, each question dictionary has an "answer" key and this key stores the correct letter, like "B" or "C". So, when the user submits an answer, the program gets the selected letter from selected_answer.get(). Then, it compares that letter with the correct answer letter:
//if choice == question["answer"]://
So, if they are the same, the answer is correct and the score goes up by 1 and a “Correct!” message appears, and then the confetti animation starts. Basically, if the answers are not the same, the program adds the question, the user’s answer, and the correct answer to the wrong_answers list. So, these wrong answers are shown in the review section at the end.


 
## How the Score and High Score Work
First, the score starts at 0 and every time the user answers correctly, the score increases by 1.
Then, at the end of the quiz, the program calculates the percentage using this formula:
//percentage = (score / total) * 100//
So, for example, if the user gets 8 out of 10 correct, the percentage is 80%. The program also gives a message based on the percentage. Basically:
90% or higher: “Excellent work!”
70% or higher: “Good job!”
50% or higher: “Not bad. Keep practicing!”
Below 50%: “Review the topic and try again.”

When it comes to the high score, the high score is saved in a text file called high_score.txt and the file is saved in the same folder as the Python program. The function get_high_score() reads the file. So, if the file does not exist, or if the text inside cannot be turned into a number, the program returns 0. Then, the function save_high_score(new_score) saves the score only if it is higher than the old high score. Basically, it opens the file in write mode and saves the new score as text. So, after finishing a quiz, the user can close the program and open it again. The high score will still be there because it was saved in the text file. Then, a screenshot of the start screen after reopening the program should be added here to prove that the high score was saved.


 
## Function Explanations
1. Function:`get_high_score()`  
Purpose: This function reads the high score from the text file called `high_score.txt`. So, if the file is not there or the number inside is not valid, it just returns 0.  
Called when: This function is called when the start screen opens and when the results screen needs to show the high score.

2. Function:`save_high_score(new_score)`  
Purpose: This function checks if the new score is higher than the old high score. So, if it is, the new score is saved in the text file. Basically, if not, nothing is saved.  
Called when: This function is called after the user finishes the quiz and the results screen appears.

3. Function: `start_quiz()`  
Purpose: This function starts or restarts the quiz. It shuffles the questions and then resets the score, current question, and wrong answers. And then after that, it shows the first question.  
Called when: This function is called when the user clicks Start Quiz or Restart Quiz.

4. Function: `show_question()`  
Purpose: This function shows one question on the screen. Basically, it clears the old screen and shows the question, choices, timer, progress bar, and buttons. Then, it resets the timer to 15 seconds.  
Called when: This function is called when the quiz starts or when the user goes to the next question.

5. Function: `submit_answer()`  
Purpose: This function checks the answer that the user selected. So, it stops the timer, locks the choices, checks if the answer is correct, updates the score, and then shows feedback.  
Called when: This function is called when the user clicks the **Submit Answer** button.

6. Function: `show_results()`  
Purpose: This function shows the final score, percentage, message, high score, and review of the wrong answers. Basically, it also shows the buttons to restart or exit the program.  
Called when: This function is called after the user finishes the last question.



## Screenshots
![Start screen](screenshots/start.png)
![Question screen](screenshots/question.png)
![Answer feedback](screenshots/feedback.png)
![Results screen](screenshots/results.png)
![High score after reopening](screenshots/high_score.png)
 
## Challenges I Faced
The difficult part was making the confetti animation because the confetti did not move properly, so I used a list to store the confetti pieces and then I use `root.after()` to move them every few milliseconds. I also added `stop_confetti()` so the animation would stop and the confetti would be cleared.
