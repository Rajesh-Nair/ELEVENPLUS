from src.application.vocab_db_mgr import VocabDBManager
import os
import json
from collections import defaultdict
import random

from logger import GLOBAL_LOGGER as log
from exception.custom_exception import CustomException

from src.application.test_generator import test_generator
from src.application.vocab_db_mgr import VocabDBManager
from src.application.test_db_mgr import TestDBManager

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
            test_summary = self.test_db_mgr.get_test_summary(self.test_type)      
            if not test_summary:
                test_summary = {'testtype': self.test_type,'last_test': 0, 'test_count': 0}
            picked_words = self.generate_random_word_list() 
            log.info(f"Picked words for test: {picked_words}")
            self.test_generator = test_generator(self.test_type)           
            result = self.test_generator.generate_test(picked_words)
            log.info(f"Generated test: {result}")
            query_status = self.db_mgr.updated_words_points_for_test(picked_words)
            if not query_status:
                return {"status": "failed", "error": "Failed to update words points for test"}
            test_no = test_summary['last_test'] + 1
            words = ' '.join([word['word'] for word in picked_words])
            location = os.path.join(self.test_loc, f"test-{self.test_type}-{test_no}.txt")
            with open(location, "w", encoding="utf-8") as f:                
                f.write("\nWords:\n")
                f.write(words)
                f.write("\n\n\n\f")  # page break
                f.write("\nQuestions:\n")
                f.write('\n'.join(f"{i+1}. {question}" for i, question in enumerate(result["Questions"])))
                f.write("\n\n\n\f")  # page break
                f.write('\n'.join(f"{i+1}. {answer}" for i, answer in enumerate(result["Answers"])))
            test_data = {'testtype': self.test_type, 
                         'testno': test_no, 
                         'words': words, 
                         'location': location}
            self.test_db_mgr.insert_test(test_data)
            return {"status": "success", "test_count": test_summary['test_count'] + 1}           

        except Exception as e:
            log.error(f"Error generating vocab test", error=str(e))
            return {"status": "failed", "error": str(e)}
        
    def generate_tests(self):
        self.words_for_test = self.db_mgr.get_all_words_for_test()
        while not self.stop_criteria:
            result = self.generate_vocab_test()
            self.stop_criteria = True ## For testing purpose
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
        picked_indices = random.choices(
            population=list(range(len(self.words_for_test))),
            weights=weights,
            k=num_to_pick
        )
        
        # Ensure distinct items
        picked_words = []
        
        # Reduce points by 5 for picked items
        for item in list(set(picked_indices)):
            self.words_for_test[item]['points'] = max(0, self.words_for_test[item]['points'] - 5)
            picked_words.append(self.words_for_test[item])

        return picked_words
        


    def close(self):
        self.db_mgr.close()

if __name__ == "__main__":
    generator = GenerateVocabTest(test_type=1)
    result = generator.generate_tests()
    print("result : {}".format(result))
    
