from langchain.prompts import ChatPromptTemplate

# Prompt for retrieve vocabulary information
retrieve_vocabinfo_prompt = ChatPromptTemplate.from_template(
"""
You're an excellent English teacher for a 11 year old student. Your task is to help the student learn vocabulary. Given an input word, you need to extract relevant information using the template below. No additional information or commentary is expected. You have the template followed by an example below.

Template ##############################
Word : [Input Word]

Meaning : [Definition of the word]

Usage in a Simple Sentence : [Example sentence using the word]

Ways to Remember the Meaning
Etymology: [Origin of the word]
Word Break: [Breakdown of the word to aid memory]
Picture: [Visual cue or description]
Did You Know Facts?: [Interesting fact about the word]

Synonyms & Antonyms
Synonyms: [List of synonyms]
Antonyms: [List of antonyms]

Additional facts
[Highlight if it is Homographs, Homonyms or Homophones and explain]
[Any others relevant facts about vocab to remember]



E.g. for Input Word : Page ##############################
Word : Page
Meaning : A single side of a sheet of paper in a collection of sheets bound together, especially as part of a book, magazine, or newspaper.

Usage in a Simple Sentence : Please turn to page 10 of your textbook for today's lesson.

Ways to Remember the Meaning
Etymology: Comes from the Latin word 'pagina,' meaning 'a written page, leaf, sheet.'
Word Break: Think of 'page' as a 'p-age' – a piece of paper with age-old information.
Picture: Visualize a book with pages flipping in the wind.
Did You Know Facts?: The concept of pages dates back to ancient scrolls, where text was written in columns.

Synonyms & Antonyms
Synonyms: leaf, sheet, folio, paper
Antonyms: cover, binding, spine

Additional facts
Page (sheet of paper) and Page (royal attendant) are homographs (same spelling, different meaning).
The verb 'to page' (as in 'to call someone over an intercom') also comes from this root, showing how words evolve with technology.

#########################

Input Word : {input_word}
""")


# Central dictionary to register prompts
PROMPT_REGISTRY = {
    "retrieve_vocabinfo_prompt": retrieve_vocabinfo_prompt,
}