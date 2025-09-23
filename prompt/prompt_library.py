from langchain.prompts import ChatPromptTemplate

# Prompt for retrieve vocabulary information
retrieve_vocabinfo_prompt = ChatPromptTemplate.from_template(
"""
You're an excellent English teacher for a 11 year old student. Your task is to help the student learn vocabulary. Given an input word, you need to extract relevant information using the template below. No additional information or commentary is expected. 
You must always return valid JSON fenced by a markdown code block. Do not return any additional text.
When a word has multiple meanings, provide information for the most common meaning and mention the other meaning in additional facts.
When a word doesnt exist, return Word as None and empty strings for all other fields.
You have the template followed by an example below.

Template ##############################
input_word : some word

word : input_word
meaning : Definition of the word
usage : Example sentence using the word
etymology : Origin of the word
word_break : Breakdown of the word to aid memory
picture : Visual cue or description
did_you_know_facts : Interesting fact about the word
synonyms : List of synonyms separated by comma
antonyms : List of antonyms separated by comma
additional_facts : Facts seperated by newline like 1) if there is a Homographs, Homonyms or Homophones then mention and explain it with an example without a miss 2) any others relevant facts about vocab to remember

E.g. ##############################
input_word : page 

word : Page
meaning : A single side of a sheet of paper in a collection of sheets bound together, especially as part of a book, magazine, or newspaper.
usage : Please turn to page 10 of your textbook for today's lesson.
etymology : Comes from the Latin word 'pagina,' meaning 'a written page, leaf, sheet.
word_break : Think of 'page' as a 'p-age' - a piece of paper with age-old information.
did_you_know_facts : The concept of pages dates back to ancient scrolls, where text was written in columns.
synonyms : leaf, sheet, folio, paper
antonyms : cover, binding, spine
additional_facts : Page (sheet of paper) and Page (royal attendant) are homographs (same spelling, different meaning).\n The verb 'to page' (as in 'to call someone over an intercom') also comes from this root, showing how words evolve with technology.
#########################

input_word : {input_word}
""")

# Prompt for create Test 1 
TestVocab_type1_prompt = ChatPromptTemplate.from_template(
"""
Create a test for 11 year old students
1) For each word listed, write a sentence that uses the word however question should have the word missing.
2) The word, but no other, should be the right fit for the sentence
3) The level of difficulty is Very Hard
4) Follow the format of your response as in the example below and no additional information is appended
5) You must always return valid JSON fenced by a markdown code block 

Example #############

Words : 
parallel millionaire chasm chemistry plimsolls

Questions :
1) The two railway tracks run ________ to each other for many miles.
2) After inventing a popular new app, she became a young ________ within a year.
3) The hikers could not cross the deep ________ that split the mountain path in two.
4) He decided to study ________ at university because he was fascinated by how substances interact.
5) In the 1980s, British schoolchildren often wore ________ for physical education lessons.

Answers :
1) The two railway tracks run parallel to each other for many miles.
2) After inventing a popular new app, she became a young millionaire within a year.
3) The hikers could not cross the deep chasm that split the mountain path in two.
4) He decided to study chemistry at university because he was fascinated by how substances interact.
5) In the 1980s, British school children often wore plimsolls for physical education lessons.


Words :
{words}

"""


# Central dictionary to register prompts
PROMPT_REGISTRY = {
    "retrieve_vocabinfo_prompt": retrieve_vocabinfo_prompt,
    "TestVocab_type1_prompt": TestVocab_type1_prompt
}