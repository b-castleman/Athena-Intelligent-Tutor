import openai
import random

# Insert Open AI API key below
API_KEY = ''

openai.api_key = API_KEY

human_name = input("Please enter your name: ")
ai_name = 'Athena'

######################################################## START: Initial Functions Used ############################################################
def aiResponse(conversation):
    # Specify parameters we allow for change
    model_id = "text-davinci-003"
    max_tokens = 200
    
    # Obtain Response
    response = openai.Completion.create(
    model=model_id,
    temperature=0.9,
    max_tokens=max_tokens,
    top_p=1,
    frequency_penalty=0.0,
    presence_penalty=0.6,
    stop=[" Human:", " " + ai_name + ":"],
    prompt = conversation
    )
    
    # Make sure the response is nonzero length
    assert(len(response.choices) > 0), "Response is zero-length"

    # Return only the text (and ensure the AI's name is always spelled correctly)
    return response.choices[0].text

# Function to generate a topics list
def generateTopics(overallLearningGoal,subtopicAmount):
    # Make prompt
    prompt = 'You are an AI system whose sole purpose is to come up with subtopics within a high-level, overarching topic. Specifically, you are to come up with subtopics for a human trying to learn more about' + overallLearningGoal + '.'
    prompt = prompt + '\n\n' + "Human: Please give me " + str(subtopicAmount) + " subtopics about " + overallLearningGoal + ". Output this list in the fashion of an array, like [<topic 1>,<topic 2>,...]."

    # Obtain properly formatted response
    response = aiResponse(prompt)
    assert(response.count('[') == 1 and response.count(']') == 1), "The subtopic list is not properly formatted."
    
    # Return a processed/proeprly formatted topics list
    bracketStart = response.find('[')
    bracketEnd = response.find(']')
    
    substring = response[bracketStart+1:bracketEnd]
    topicsList = substring.split(',')
    
    return topicsList

######################################################## END: Initial Functions Used ############################################################
# Goals of this specific lesson
# Insert what the lesson goal is
overallLearningGoal = 'what the history of AI is' # the user is trying to learn WHAT as an umbrella end goal? (i.e. 'what a Faster R-CNN is', 'what unicorns are', 'why atoms are stable','what the basic biology behind eukaryotic is')


# MC Settings (alter as you wish, default is 50% FR-50% MC)
multipleChoiceChance = .5

# Automatic Topic Generation Settings
# Should topics be automatically generated? Default is False
automaticTopicGeneration = False 

# If topics are automatically generated, how many should be?
subtopicAmount = 3  # how many topics should be automatically generated? (only applicable if automaticTopicGeneration == True)

if not automaticTopicGeneration: # If we want to manually fill in the topics to cover & information about it
    userLearningPlatform = 'watched a video' # how did the user initially learn the information? (i.e. 'read a textbook','watched a video','watched a lecture','talked to a professor')
    # Insert a topic list
    topicsList = ['the Gestation of AI',
                  'Early Enthusiasm and Expectations',
                  'Knowledge-based AI',
                  'AI Becomes Scientific']
    
    # Insert keyword dictionary informaton below
    keyWordDict = {("gestation","ai","artificial intelligence"):'The period of time called the "Gestation of AI" was between the 1940s-1950s. It included McCulloch and Pitts, who proposed the first neural network for boolean functions, modeled after a neuron (a biological nerve cell representing a functional unit in the brain; Neurons receive and send nerve impulses). In 1950, Alan Turing published "Computing Machinery and Intelligence", where he proposed the AI agenda and the Turing Test.',
                   ("early enthusiasm","expectations"):'The period of time called "Early Enthusiasm and Expectations" was between the 1950s-1970s. In 1956, the Dartmouth Summer Research Project on AI boosted interest and it was largely recognized as the event that kicked off the interest in AI. John McCarthy coiled the term "Artificial Intelligence". In 1956, Arthur Samuel''s checkers playing program (developed at IBM; used reinforcement learning) was presented to the public. It was able to outperform the average player. In 1958, McCarthy invented Lisp, a programming language common for AI (for 30 years). From 1963-1970, Minsky''s students at MIT worked on Microworlds (solving integrals, algebra, and geometry problems). The most Microworld famous was SHRDLU, a block world that could perform simple actions (pick up block, move, place elsewhere) from natural language requests. The early 60''s included the development of the first neural network. From 1960-1962, Bernie Widrow and his student invented Adaline, and in 1962 Frank Rosenblatt invented the Perceptron. From 1966-1972, Shakey the Robot was invented as the first general purpose mobile robot that used logical reasoning. Lastly, interest for AI in the 1960 began to wane as AI systems were not scalable and were limited.',
                   ("knowledge-based","ai","artificial intelligence"):'The period of time called "Knowledge-based AI" was between the 1960s-1990s. An idea began to immerge: incorporating domain knowledge to encode information about the world. Led to the creation of expert systems, simulationing human decision making processes using rules. As a result, in the 1980s, AI became an industry. However, expert systems were limited as they couldnt handle uncertainty or learn from experience. Consequently, AI research slowed down and let to the AI winter.',
                   ("scientific","ai","artificial intelligence"):'The period of time called "AI Becomes Scientific" started in the 1990s and is still ongoing. Subfields came together to make AI a success. First, neural networks returned with backpropagation. They address imperfections of the world and learn from data. Failure of expert systems also led to probabilistic models rather than boolean logic. Allowed AI to make a huge leap. Machine learning (learning from experience and data) also rised. Benchmark data sets and repositories (i.e. MNIST, ImageNet) helped scientists develop more powerful models. From 2001 and ongoing, the World Wide Web facilitated a large amount of data. Facilitating events included the 2011 IBM Watson (in Jeopardy!), which renewed public interest. From 2011 and ongoing, deep learning began to take over (great machinery allowed this to occur). Now, we are in the AI Spring as a result.'}

else:
    userLearningPlatform = 'been asked to learn from me'
    topicsList = generateTopics(overallLearningGoal,subtopicAmount)
    print(topicsList)

######################################################## START: AI Backgrounds ############################################################
# Concatenate topics for reuse
topicConcatenation = ''
for i in range(len(topicsList)-1):
    topicConcatenation = topicConcatenation + topicsList[i] + ', '
topicConcatenation = topicConcatenation + ', and ' + topicsList[-1] + '.' # uniquely concatenate last topic & the end of the background prompt

# Create each background
background_prompt = 'You are an AI tutor (named ' + ai_name + '), whose goal is to teach a human (named ' + human_name + ') about ' + overallLearningGoal + '. Specifically, ' + human_name + ' has just ' + userLearningPlatform.replace("me","you") + ' detailing ' + topicConcatenation + ' You should always respond to what ' + human_name + ' says as yourself, the AI tutor ' + ai_name + '.'

changepoint_prompt = 'You are a classifier, attempting to decern whether a user is either asking a question (i.e. getting clarification), or b) does not need help or is finished learning (i.e. says they don''t need any help, are fine, are finished with explanations, have no more questions, makes an unrelated comment).'

ranking_prompt = 'You are a ranking system. You will be given a conversation with ' + ai_name + ' (an AI tutor) whose goal is to teach a human (named ' + human_name + ') about ' + overallLearningGoal + ', and then you will rank how accurate their response is to real definitions and accurate responses. Specifically, questions ' + human_name + ' will respond to relates to ' + topicConcatenation + '. You will pay specific attention to the wording of each question and answer to observe the correctness.'

q_and_a_prompt = 'You are a Q&A AI system. You will answer various given by a human with the most precise and accurate response. You should pay very close attention to specific words detailing each question before formulating your response.'

questionCreation = 'You are an AI system (named ' + ai_name + ') built solely to ask easy, non-ambiguous questions about certain topics. Specifically, current topics are surrounding ' + topicConcatenation

######################################################## END: AI Backgrounds ############################################################


######################################################## START: Stage Functions Used ############################################################
    


def addKeyWordPhrases(conversation): # add keyword phrases to the conversation prior to prompting
    # If automatic mode, we don't have any prior information. Just skip this step then!
    if automaticTopicGeneration:
        return conversation
    
    # Iterate through all the keys
    for tup in keyWordDict.keys():
        keyWordCount = 0
        
        # If all the keywords from this tuple exist, then we should include the extra information
        for keyword in tup:
            if keyword.lower() in conversation.lower():
                keyWordCount += 1
        
        # If every key word was present, add the extra information to the background prompting (well, before it? same deal)
        if keyWordCount/len(tup) >= .5:
            conversation = keyWordDict[tup] + "\n" + conversation
    
    return conversation
                      

def changepointOccurred(human_prompt):
    # Obtain response
    response = aiResponse(changepoint_prompt + 'The user just responded, "' + human_prompt + '". Please respond TRUE if the user does not have any questions, TRUE if the user does not have any questions or clarifications needed, TRUE if the user is only making a comment or exclaimation, or FALSE if and only if the user is asking for questions or knowledge (i.e. asking a question or for clarification). Do not respond anything else other than this TRUE or FALSE response.')
    
    # Check if the change has occurred from our classifier
    text = response.lower()
    assert("true" in text or "false" in text), "Text does not contains TRUE or FALSE (capitalization-agnostic) from the changepoint check."
    if "true" in text:
        return True
    return False

def getQuestion(questionType,currentTopic):
    assert(questionType == "free response" or questionType == "multiple choice"), "Invalid questionType variable"
    if questionType == "free response": # FR
        curPrompt = questionCreation + "\n\n" + "Human: Give an easy, free response question with a nonambiguous (straight-forward) answer about " + currentTopic + "." 
    else: # MC
        curPrompt = questionCreation + "\n\n" + "Human: Give an easy, multiple choice question about " + currentTopic + '. Don''t ask any question along the lines of "which is most common", "which has been a major", etc because these are too open-ended. The question should have only one very clear, possible solution as the answer. Ensure the answer choices are nonambiguous so that the best answer choice is obvious. Do NOT state what the solution is.'
        
    return aiResponse(addKeyWordPhrases(curPrompt))
    
def rankUserResponse(curQuestion,human_response,questionType):
    # First, get the model's own response to this question
    assert(questionType == "free response" or questionType == "multiple choice"), "Invalid questionType variable"
    if questionType == "free response": # FR
        ask_question_to_model_prompt = q_and_a_prompt + "\n\n" + 'Human: I have this question: "' + curQuestion.replace("\n","") + '". Please BRIEFLY answer this question as ACCURATELY as possible. You should pay SPECIFIC attention to the WORDING of each question and possible answers.'
    else: # MC
        ask_question_to_model_prompt = q_and_a_prompt + "\n\n" + 'Human: I have this question: "' + curQuestion.replace("\n","") + '". Please answer this question as ACCURATELY as possible and ONLY respond with the BEST letter choice (nothing more). You should pay SPECIFIC attention to the WORDING of each question and all other possible answers to decide which is the best choice.'
    
    ask_question_to_model_prompt = addKeyWordPhrases(ask_question_to_model_prompt) # add any keyword definitions that may be useful to the ranking
    models_answer = aiResponse(ask_question_to_model_prompt).replace("\n","")
    
    # Choose the prompt based on the questionType being FR or MC
    if questionType == "free response":
        curClassification_prompt = ranking_prompt + "\n\n" + 'Human: The AI just asked the free response question: "' + curQuestion.replace("\n","") + '". I just responded: "' + human_response.replace("\n","") + '". A possible answer from a third party could be along the lines of "' + models_answer + '". Based on MY response (and comparing it to the suggested thirty party response), rank MY response quality and correctness on an integer scale from 1-5. Return "1" if I do not give an answer to the question in my response. Do not include any other words or tokens aside from my response quality.'
    else:
        curClassification_prompt = ranking_prompt + "\n\n" + 'Human: The AI just asked the multiple choice question: "' + curQuestion.replace("\n","") + '". I just responded: "' + human_response.replace("\n","") + '". A suggested answer from a third party is "' + models_answer + '". Based on MY response (and comparing it to the suggested thirty party response), say ONE if my response is NOT the best single most accurate answer choice (or if I do not give an answer) or FIVE if my response is the best single answer to choose. Do not include any other words or tokens aside from my response quality.'
    
    curClassification_prompt = addKeyWordPhrases(curClassification_prompt) # add any keyword definitions that may be useful to the ranking
    response = aiResponse(curClassification_prompt)
    
    # Check what the ranking is
    text = response.lower()
    assert("one" in text or "two" in text or "three" in text or "four" in text or "five" in text or "1" in text or "2" in text or "3" in text or "4" in text or "5" in text), "A valid number was not returned."
    if "one" in text or "1" in text:
        return 1
    if "two" in text or "2" in text:
        return 2
    if "three" in text or "3" in text:
        return 3
    if "four" in text or "4" in text:
        return 4
    if "five" in text or "5" in text:
        return 5
    return None # shouldnt be possible

def explainBadRanking(curQuestion,human_response):
    explanation_prompt = background_prompt + "\n\n" + 'Human: The AI just asked the question: "' + curQuestion.replace("\n","") + '". I just responded: "' + human_response.replace("\n","") + '". Please explain what about my answer is incorrect and help me understand my misconceptions.'
    explanation_prompt = addKeyWordPhrases(explanation_prompt) # add any keyword phrases that may help explain this better
    response = aiResponse(explanation_prompt) + "\n\nAthena: Does this explanation make sense or do you have any other questions?" + '\n'

    return response

def explainGoodRanking(curQuestion,human_response):
    explanation_prompt = background_prompt + "\n\n" + 'Human: The AI just asked the question: "' + curQuestion.replace("\n","") + '". I just responded: "' + human_response.replace("\n","") + '". Please explain what about my answer was good and what may need improvement.'
    explanation_prompt = addKeyWordPhrases(explanation_prompt) # add any keyword phrases that may help explain this better
    response = aiResponse(explanation_prompt)

    return response

def human_response():
    raw_out = input(human_name + ': ')
    
    # Ensure raw_out is not empty
    while len(raw_out) == 0:
        print("Apologies, but I do not see a response above. Can you please enter one?")
        raw_out = input(human_name + ': ')
    
    # Force punctation on the end so that the prompt never can be autocompleted by the model
    if raw_out[-1] != '.' or raw_out[-1] != '!' or raw_out[-1] != '?':
        raw_out = raw_out + '.'
    
    return raw_out + '\n'
######################################################## END: Stage Functions Used ############################################################    
        
################################################## START: Stage #1 - Background Clarification #############################################
initialStage1AiPrompt = ai_name + ': Hi there, ' + human_name + '! My name is ' + ai_name + " and I am an intelligent tutoring system. I'm here to help you learn about " + overallLearningGoal + ". I have been told that you have " + userLearningPlatform + " on " + overallLearningGoal + "! Do you have any questions about any of the concepts you've just learned?"
net_conversation = background_prompt + '\n\n' + initialStage1AiPrompt + "\n"


print("--Stage #1--")
print('\n' + initialStage1AiPrompt + "\n")
for i in range(20): # threshold the stage 1 prompting at 20
    # Obtain human response
    human_prompt = human_response()
    net_conversation = net_conversation + '\n\nHuman: ' + human_prompt
    
    # Classification: check if the response contains any more question/clarification or if its a changepoint (therefore moving onto stage 2)
    if changepointOccurred(human_prompt):
        break
    
    # Create a response
    conversation_to_prompt = addKeyWordPhrases(net_conversation) # add any keyword definitions that may be useful
    ai_response = aiResponse(conversation_to_prompt) + '\n'
    print(ai_response)
    net_conversation = net_conversation + ai_response
################################################## END: Stage #1 - Background Clarification #############################################

################################################## START: Stage #2 - Quizzing #############################################
print("--Stage #2--")
initialStage2AiPrompt = ai_name + ": Awesome! Now, let's review some of the concepts you learned about " + overallLearningGoal + ", " + human_name + "." 
net_conversation = background_prompt + '\n\n' + initialStage2AiPrompt

print('\n' + initialStage2AiPrompt)
askQuestion = True
askNewTopic = True
idxNextTopic = 0
for i in range(50): # threshold the question count at 50
    if askQuestion: # ask a question
        askQuestion = False # next, we should check the response
        
        # Check if we're done with all the questions, if so quit
        if idxNextTopic >= len(topicsList):
            break
        
        # If it's not the first question or a redo or the first question, provide a transition into the next question
        if idxNextTopic != 0 or not askNewTopic:
            if askNewTopic:
                ai_response = "\n" + ai_name + ": Great! Let's move onto the next topic!"
            else:
                ai_response = "\n" + ai_name + ": Let's stay on this topic for a bit longer before moving on."
            print(ai_response)
            net_conversation = net_conversation + ai_response
        
        # Get the next question, dependent on MC being on or off
        if random.random() > 1 - multipleChoiceChance:
            questionType = "free response"
        else:
            questionType = "multiple choice"
        curQuestion = getQuestion(questionType,topicsList[idxNextTopic])
        net_conversation = net_conversation + curQuestion # keep newlines for conversation logging
        subconversation = background_prompt + curQuestion
        print(curQuestion + "\n") # print the question we're asking
        
        
    else: # responding to a user response
        askQuestion = True # next, we should ask a question
        
        # Obtain human response
        human_prompt = human_response()
        net_conversation = net_conversation + '\n\nHuman: ' + human_prompt
        subconversation = subconversation + '\n\nHuman: ' + human_prompt
        
        # We need to see if the user response is good or not. Let's rank it with a classifier
        rank = rankUserResponse(curQuestion,human_prompt,questionType)
        if rank >= 3:
            idxNextTopic += 1 # update the question we ask next time since we just exhausted
            askNewTopic = True # we're gonna go to a new topic!
            ai_response = explainGoodRanking(curQuestion,human_prompt)
            print(ai_response)
            net_conversation = net_conversation + ai_response + '\n'
            subconversation = subconversation+ ai_response + '\n'
        else: # The response was not good enough to warrant a new question. Explain why it was bad and ask a new one on the same subject
            askNewTopic = False # we're sticking to the old topic, sorry!
            ai_response = explainBadRanking(curQuestion,human_prompt)
            print(ai_response)
            net_conversation = net_conversation + ai_response + '\n'
            subconversation = subconversation + ai_response + '\n'
            
            # Loop while the user is understanding their misconception and conversing.
            for j in range(10): # threshold the back-and-forward conversing at 10 prompts each
                # Obtain human response
                human_prompt = human_response()
                net_conversation = net_conversation + '\n\nHuman: ' + human_prompt
                subconversation = subconversation + '\n\nHuman: ' + human_prompt           
                
                # Classification: check if the response contains any more question/clarification or if its a changepoint (therefore moving onto stage 2)
                if changepointOccurred(human_prompt):
                    break
                
                # Create a response
                conversation_prompt = addKeyWordPhrases(subconversation) # add any keyword phrases that may help explain this better
                ai_response = aiResponse(conversation_prompt) # only put the current subconversation in as to avoid overwhelming the model with too many tokens
                print(ai_response)
                net_conversation = net_conversation + ai_response 
                subconversation = subconversation+ ai_response
 ################################################## END: Stage #2 - Quizzing #############################################
            
        
        
################################################## START: Conclusion #############################################
# End the conversation
endText = ai_name + ": Thank you for learning with me today, " + human_name + ", I had a lot of fun! I'll see you soon in your future lessons!"
print("\n" + endText)
net_conversation = net_conversation + "\n\n" + endText
    

# Finished, print total conversation
print("Here is the net logging of the conversation that occurred: \n\n")
print(net_conversation)
################################################## END: Conclusion #############################################



################################################## NOTES #######################################################

    # overallLearningGoal = 'what the future of AI may be' # the user is trying to learn WHAT as an umbrella end goal? (i.e. 'what a Faster R-CNN is', 'what unicorns are', 'why atoms are stable')
    # userLearningPlatform = 'watched a video' # how did the user initially learn the information? (i.e. 'read a textbook','watched a video','watched a lecture','talked to a professor')
    # topicsList = ['The Components of Ethical AI. The three components are defined as 1. interpretable AI, 2. bias AI, and 3. education of AI.',
    #               'Concerns with AI',
    #               'The Potential Future with AI']
    
    
    # keyWordDict = {("interpretable",):'Interpretable AI aims to interpret the complex and incomprehensable black box models. AI models must be accountable and interpretable in order to (1) ensure they are inclusive, (2) increase our confidence in using them, and (3) gain knowledge',
    #                ("bias",):'The data we use to build AI can include human-bias decisions. An example of AI bias includes phone cameras, which tend to have trouble recognizing darker-skinned individuals. This may be because there are fewer darker-skinned faces than lighter-skinned faces in the training data used to generate the model. Fair AI aims to reduce bias so that decision-making is fair, ethical, and inclusive.',
    #                ("education","ai","artificial intelligence"):'AI education should be promoted to empower the younger generation with AI knowledge as they grow. This means allowing AI education to students regardless of nationality, race, or gender.',
    #                ("ai","artificial intelligence","concerns"):'There is a lot to take into consideration as AI develops into the future. Some of these concerns include: "How will AI impact our jobs, cities, and laws?","Should we be afraid of AI?","Is AI a threat to humankind?"',
    #                ("potential","ai","artificial intelligence","future"):'With AI, the future has the potential to be: clean (cleaning robots, self-driving robots, traffic reduction, renewable energy, smart cities), fair (identify and irraticate injustice and bias, provide healthcare education, employment, and services), and healthy (personalized medicine, fitness, AI physicians, treatment, medicine, and science). They will help humanity be happy.'}
    
    # overallLearningGoal = 'what AI is' # the user is trying to learn WHAT as an umbrella end goal? (i.e. 'what a Faster R-CNN is', 'what unicorns are', 'why atoms are stable')
    # userLearningPlatform = 'watched a video' # how did the user initially learn the information? (i.e. 'read a textbook','watched a video','watched a lecture','talked to a professor')
    # topicsList = ['the possible definitions of AI',  # list all subtopics you want to specifically go over
    #                 'the four schools of thought (thinking rationally, acting rationally, thinking human-like, acting human-like)',
    #                 'the Turing test',
    #                 'why we study AI',
    #                 'common fields in which we can use AI in']
    
    
    # keyWordDict = {("definition","ai","artificial intelligence"):'Many definitions of AI include, "a branch of computer science that allows computers to make predictions and decisions to solve problems", "ability for computer program or machine to think and learn","the science and engineering of making intelligent machines","study and design of intelligent agents to take actions to maximize success".',
    #                ("turing",):"A Turing Test is a general test to determine whether or not a computer can think. It passes the test of intelligence if it can fool a human interrogator into believing its results were human-made.",
    #                ("why","ai","artificial intelligence"):"AI has the potential to free up humanity from a lot of mental drudgery",
    #                ("where","ai","artificial intelligence"):"AI can be implemented to places including but not limited to CV, NLP, Self-Driving Cars, Spoken Language Processing, Robotics, Planning, and Games."}
