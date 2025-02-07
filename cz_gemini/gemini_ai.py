# Copyright (C) 2024 Juen Rene´
# 
# This file is part of cz_gemini.
# 
# cz_geminis free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# cz_geminis distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with cz_gemini.  If not, see <https://www.gnu.org/licenses/>.

import google.generativeai as genai
import re

from termcolor import colored

from cz_gemini.gemini_defaults import GEMINI_CONFIG, GEMINI_SAEFTY


class AiGemini():

    
    def __init__(self, api_key: str, answer_pattern: str, commitizen_pattern: str, verbose: bool) -> None:
        self.api_key = api_key
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")
        self.answer_pattern = answer_pattern
        self.commitizen_pattern = commitizen_pattern
        self.message = {}  
        self.verbose = verbose

    
    def correct_sentence(self, text: str) -> str:    
        """! Function for spellchecking

        @parm text  Commit text 

        @return     The corrected commit text
        
        """
        
        # Prompt for correcting the grammar
        prompt_correction = f"Correct grammar and spelling errors in the following commit message:\n\
                              Original: {text}\n \
                              Return only corrected commit in lowercase letters without any other text or quotes"

        # Assuming the API call returns the corrected text
        response_correction = self.model.generate_content(contents=prompt_correction, 
                                                          generation_config=GEMINI_CONFIG, 
                                                          safety_settings=GEMINI_SAEFTY)
        # Extract the corrected sentence
        corrected_text = response_correction.text
        return corrected_text
    
    
    def generate_auto_commit(self, template: str) -> dict:
        """! Function to generate the auto commit
        
            @param template     Template for question generation

            @return             Question dict following commitzen rules with the answers.
        """

        # Local variables
        choices = []
        #self.verbose = True
        _l = 0
        
        if self.verbose:
            print(colored(f" Following question should be answered from gemini: \n\n{template}", "green"))

        # Create answer from gemini api
        # Note: We have set HARM_DANGEROUS_CONTENT to BLOCK_NONE. Otherwise we don´t get any answer
        get_answer = False
        while not get_answer:
            answered = self.model.generate_content(contents=template,
                                                   generation_config=GEMINI_CONFIG,
                                                   safety_settings=GEMINI_SAEFTY)

            if self.verbose:
                print(colored(f"Raw answer getting from gemini: \n {answered}","green"))
            # Sometimes the api return a numbers list with answers 
            # Dirty hack to act on that behavior
            a = re.findall("\*{2}(.*?)\*{2}", answered.text)
            if a:
                for _a in a:
                    answer += _a
            # Only the commits come from api
            else:
                answer = re.sub(self.answer_pattern, "", answered.text)

            
            # Get different pieces from autogenerate message for later processing
            m = re.compile(self.commitizen_pattern, flags=re.MULTILINE)
            pieces = m.findall(answer)
            if pieces:
                # When we got answers we go ahead with the processing
                get_answer = True

        if self.verbose:
            print(colored(f"Answer after gemini_pattern: \n{answer}\n","green"))
            print(colored(f"List of answers [type, scope, subject, body] after commitizen_pattern: \n{pieces}\n","green"))

        # First we build choices from autogenerated answers
        # After that we build dict for later processing
        for a in answer.split("\n"):  

            # TODO: make regex better because sometimes we can not parse all answer
            # then this may failed
            try:
            # remove empty line if one exist
                if "(" in a:
                    # create dict so we can later build the message dict for commit template
            
                    self.message[a] = { "change_type": pieces[_l][0], "scope": pieces[_l][1], "subject": pieces[_l][2], "body": pieces[_l][3]}
                    c = {
                        "value": a,
                        "name": a,
                        "key": f"{_l}"
                        }
                    
                    choices.append(c)
                    _l += 1

            except Exception as e:
                print(colored(f"Failed to handle all messages!", "red"))

        # generate message list
        questions =  [{
          "type": "list",
          "name": "subject",
          "message": "Select one of the autogenerated commit message",
          "choices": choices
        }]

        return questions
    

    def set_config(self, config: dict) -> None:
        
        # Set config for gemini api request
        self.gemini_config = config
        return