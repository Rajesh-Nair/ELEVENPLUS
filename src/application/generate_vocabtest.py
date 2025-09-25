from src.application.vocab_db_mgr import VocabDBManager
import os
import json
from collections import defaultdict
import random
import numpy as np

from logger import GLOBAL_LOGGER as log
from exception.custom_exception import CustomException

from src.application.test_generator import test_generator
from src.application.vocab_db_mgr import VocabDBManager
from src.application.test_db_mgr import TestDBManager
from utils.pdf_printer import save_text_to_pdf, save_dict_list_to_pdf

class GenerateVocabTest:
    def __init__(self, test_type=1):
        self.db_mgr = VocabDBManager(db_path=os.path.join("data","vocab_11plus.db"))     
        self.words_for_test = self.db_mgr.get_all_words_for_test()   
        self.stop_criteria = False
        self.test_type = test_type
        self.test_db_mgr = TestDBManager(db_path=os.path.join("data","vocab_testset.db"))
        self.test_loc = os.path.join("data","test_sets")
  
    def generate_vocab_test(self):
        try:    
            # Get test summary based on last run
            test_summary = self.test_db_mgr.get_test_summary(self.test_type)      
            if not test_summary:
                test_summary = {'testtype': self.test_type,'last_test': 0, 'test_count': 0}

            # Generate picked words
            picked_words = self.generate_random_word_list() 
            log.info(f"Picked words for test: {picked_words}")

            # Generate test
            testgenerator = test_generator(self.test_type)           
            result = testgenerator.generate_test(picked_words)
            log.info(f"Generated test: {result}")
            query_status = self.db_mgr.updated_words_points_for_test(picked_words)
            if not query_status:
                return {"status": "failed", "error": "Failed to update words points for test"}
            
            # Generate test pdf
            test_no = test_summary['last_test'] + 1
            word_list = [word['word'] for word in picked_words]
            random.shuffle(word_list)
            words = ' '.join(word_list)
            location = os.path.join(self.test_loc, f"test-{self.test_type}-{test_no}.txt")  

            word_cards = [self.db_mgr.get_word(word['word']) for word in picked_words]
            random.shuffle(word_cards)            
            definition_words_answers = '|'.join(f"{i+1}. {word['word']}" for i, word in enumerate(word_cards))
            definitions_to_print = [{'Meaning': word['meaning'], 'Word': word_list[i]} for i, word in enumerate(word_cards)]         
            usage_questions = '\n'.join(f"{i+1}. {word_question['question']}" for i, word_question in enumerate(result))
            usage_answers = '|'.join(f"{i+1}. {word_question['word']}" for i, word_question in enumerate(result))
            
            questions_to_print = """
            Words : \n{}\n\n\n
            Questions : \n{}\n\n\n
            """.format(words, \
                       usage_questions)
            answers_to_print = """
            Definitions : \n{}\n
            Usage : \n{}\n\n\n
            """.format(definition_words_answers, \
                       usage_answers)
            instructions = f"""{self.test_type}-{test_no}-Match the words with their definitions"""
            
            # Save test pdf
            save_dict_list_to_pdf(definitions_to_print, os.path.join(self.test_loc, f"test-{self.test_type}-{test_no}-definitions.pdf"), instructions)
            save_text_to_pdf(questions_to_print, os.path.join(self.test_loc, f"test-{self.test_type}-{test_no}-usage.pdf"),title=f"test-{self.test_type}-{test_no}-usage")
            save_text_to_pdf(answers_to_print, os.path.join(self.test_loc, f"test-{self.test_type}-{test_no}-answers.pdf"),title=f"test-{self.test_type}-{test_no}-answers")
            
            # Update test db
            test_data = {'testtype': self.test_type, 
                         'testno': test_no, 
                         'words': words, 
                         'location': location}
            self.test_db_mgr.insert_test(test_data)
            
            return {"status": "success", "test_count": test_summary['test_count'] + 1}           

        except Exception as e:
            log.error(f"Error generating vocab test", error=str(e))
            return {"status": "failed", "error": str(e)}

    def retrieve_vocab_cards(self, words):
        vocab_cards = []
        for word in words:
            vocab_card = self.db_mgr.get_word(word)
            vocab_cards.append(vocab_card)
        return vocab_cards
       
    def generate_tests(self):
        self.words_for_test = self.db_mgr.get_all_words_for_test()
        while not self.stop_criteria:
            result = self.generate_vocab_test()
            #self.stop_criteria = True ## For testing purpose - uncomment this for testing purpose
            if result['status'] != "success":
                log.error(f"Error generating vocab test", error=result['error'])
                self.stop_criteria = True
                return {"status": "failed", "error": result['error']}
        return {"status": "success", "test_count": result['test_count']}
    
    def generate_random_word_list(self, num_to_pick=20):
        # Determine eligible items and their weights
        weights = []
        self.stop_criteria = True
        for item in self.words_for_test:
            if item['points'] >= 10:
                weights.append(0.749)
                self.stop_criteria = False
            elif item['points'] == 5:
                weights.append(0.25)
                self.stop_criteria = False
            else:  # item['points'] == 0
                weights.append(0.001)
        
        # Pick num_to_pick distinct items
        weights = np.array(weights)
        weights_normalized = weights / weights.sum()
        picked_indices = np.random.choice(
            a=list(range(len(self.words_for_test))),
            size=min(num_to_pick, len(self.words_for_test)),
            replace=False,  # Ensure distinct items
            p=weights_normalized
            )
        
        # Ensure distinct items
        picked_words = []
        
        # Reduce points by 5 for picked items
        for item in list(set(picked_indices)):
            self.words_for_test[item]['points'] = max(0, self.words_for_test[item]['points'] - 5)
            picked_words.append(self.words_for_test[item])

        return picked_words
        
    def retrieve_test(self):
        return self.test_db_mgr.get_all_tests(self.test_type)
    
    def reset_test(self):
        #reset words points for test
        reset_words_points_for_test = self.db_mgr.reset_words_points_for_test()
        # reset test
        reset_test = self.test_db_mgr.reset_test()
        return {"status": "success", \
                "reset_words_points_for_test": reset_words_points_for_test, \
                "reset_test": reset_test}

    def close(self):
        self.db_mgr.close()

if __name__ == "__main__":
    test_case = 4
    if test_case == 1:
        generator = GenerateVocabTest(test_type=1)
        result = generator.generate_tests()
        print("result : {}".format(result))
    elif test_case == 2:
        generator = GenerateVocabTest(test_type=1)
        reset_test = generator.reset_test()
        print("reset_test : {}".format(reset_test))
    elif test_case == 3:
        vocab_db_mgr = VocabDBManager(db_path=os.path.join("data","vocab_11plus.db"))
        all_words_for_test = vocab_db_mgr.get_all_words_for_test()
        print("all_words_for_test : {}".format(all_words_for_test))
    elif test_case == 4:
        generator = GenerateVocabTest(test_type=1)
        get_all_tests = generator.retrieve_test()
        print("get_all_tests : {}".format(get_all_tests))