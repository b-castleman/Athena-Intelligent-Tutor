# Athena-Intelligent-Tutor
Leveraging GPT-3 for Adaptive and Interactive Intelligent Tutoring for Personalized Learning


1. Clone the repository locally and open up the file "athenaV2.py"
2. Insert your Open AI API key on line 5.
3. On line 58, define the overall learning goal
4. On line 62, define the percentage of questions that should multiple choice vs free response (default is 0.5)
5. Decide if you would like automatic topic generation
  a. If so, change line 66 to "True" to turn it on. Then, on line 69, change the subtopic amount to the number of your choosing.
  b. If not, insert the learning platform in on line 72, the topic list in on line 74, and the key word dictionary in on line 80. It is already prefilled with an example.
6. Everything is set! Go ahead and run the program!


Note that it is suggested to explain your answers for multiple choice as it helps Athena in ranking the responses, which is currently still in beta testing and unperfected. Furthermore, keyword information included should be plentiful for the best results.
