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
from commitizen import out
from commitizen.cz.exceptions import CzException


MISSING_CZ_GEMINI_CONFIG = 115
MISSING_CZ_GEMINI_API = 116

gemini_config = {
    'model': 'gemini-2.0-flash-exp',
    'temperature': 0.7,
    'candidate_count': 1,
    'top_k': 40,
    'top_p': 0.95,
    'max_output_tokens': 1024,
}

class CzgeminiException(CzException):
    
    def __init__(self, *args, **kwargs):
        self.output_method = kwargs.get("output_method") or out.error
        self.exit_code = self.__class__.exit_code
        if args:
            self.message = args[0]
        elif hasattr(self.__class__, "message"):
            self.message = self.__class__.message
        else:
            self.message = ""

    def __str__(self):
        return self.message 

class MissingCzGeminiConfigError(CzgeminiException):
    """! Exception class for missing config. """

    exit_code = MISSING_CZ_GEMINI_CONFIG
    message = "fatal: gemini is not set in configuration file."


class MissingCzGeminiAPIError(CzgeminiException):
    """! Exception class for missing or wrong API key. """

    exit_code = MISSING_CZ_GEMINI_API
    message = "fatal: gemini API key is missing or wrong.\n \
               Please add or check 'gemini_api' config or set env variable 'GOOGLE_API_KEY'!"       


