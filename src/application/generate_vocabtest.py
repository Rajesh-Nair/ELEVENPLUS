from src.application.vocab_db_mgr import VocabDBManager
import os
import json
from collections import defaultdict
import random

from logger import GLOBAL_LOGGER as log
from exception.custom_exception import CustomException

class GenerateVocabTest:
    def __init__(self, test_type=1):
        self.db_mgr = VocabDBManager(db_path=os.path.join("data","vocab_11plus.db"))     
        self.words_for_test = self.db_mgr.get_all_words_for_test()   
        self.stop_criteria = False
        self.test_type = test_type
        self.tests = []
  
    def generate_vocab_test(self):
        try:
            picked_words = self.generate_random_word_list()
            self.tests.append(picked_words)
            return {"status": "success", "test_count": len(self.tests)}           

        except Exception as e:
            log.error(f"Error generating vocab test", error=str(e))
            return {"status": "failed", "error": str(e)}
        
    def generate_tests(self):
        while not self.stop_criteria:
            result = self.generate_vocab_test()
            if result['status'] != "success":
                log.error(f"Error generating vocab test", error=result['error'])
                self.stop_criteria = True
                return {"status": "failed", "error": result['error']}
        return {"status": "success", "test_count": len(self.tests)}
    
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
    
