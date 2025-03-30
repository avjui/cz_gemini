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
#
# This plugin is strongly based on default customize plugin https://github.com/commitizen-tools/commitizen/blob/master/commitizen/cz/customize/customize.py
#

from __future__ import annotations
import os
import re

try:
    from jinja2 import Template, PackageLoader
except ImportError:
    from string import Template  # type: ignore

from termcolor import colored

from commitizen import cmd, git
from commitizen.config import BaseConfig
from commitizen.cz.base import BaseCommitizen
from commitizen.defaults import Questions

from cz_gemini.gemini_ai import AiGemini
from cz_gemini.gemini_defaults import *
from cz_gemini.gemini_exception import MissingCzGeminiAPIError, MissingCzGeminiConfigError

__all__ = ["GeminiCZ"]

class GeminiCz(BaseCommitizen):


    def __init__(self, config: BaseConfig):
        super().__init__(config)

        # gemini defaults
        self.ai = None
        self.autogenerate = False

        # bump defaults
        self.bump_pattern = BUMP_PATTERN
        self.bump_map = BUMP_MAP
        self.bump_map_major_version_zero = BUMP_MAP_MAJOR_VERSION_ZERO

        # change_type defaults
        self.change_type = CHANGE_TYPES
        self.change_type_map = CHANGE_TYPE_MAP
        self.change_type_order = CHANGE_TYPE_ORDER

        # changelog default pattern
        self.changelog_pattern = CHANGELOG_PATTERN

        # commit parser and template defaults
        self.commit_parser = COMMIT_PARSER

        # example default
        self.example_ = EXAMPLE

        # gemini default
        self.gemini_answer_number = GEMINI_ANSWER_NUMBER
        self.gemini_answer_pattern = GEMINI_ANSWER_PATTERN
        self.gemini_commitizen_pattern = GEMINI_COMMITIZEN_PATTERN
        self.gemini_template = GEMINI_TEMPLATE
        self.gemini_verbose = False
        
        # messages
        self.messages = MESSAGES

        # default question:
        self.question = None
        
        # schema defaults
        self._schema_pattern = SCHEMA_PATTERN
        self.schema_ = SCHEMA

        #scope default
        self.scope = SCOPES
    
        # info defaults
        self.info_ = INFO

        # init config file
        self.ini_config()


    def ini_config(self) -> None:

        # Initial all config and set it to value from config file
        # if it exists!

        if "gemini" not in self.config.settings:
            raise MissingCzGeminiConfigError()
        self.custom_settings = self.config.settings["gemini"]

        autogenerate = self.custom_settings.get('autogenerate')
        if autogenerate:
            self.autogenerate = autogenerate

        custom_bump_pattern = self.custom_settings.get("bump_pattern")
        if custom_bump_pattern:
            self.bump_pattern = custom_bump_pattern

        custom_bump_map = self.custom_settings.get("bump_map")
        if custom_bump_map:
            self.bump_map = custom_bump_map

        custom_bump_map_major_version_zero = self.custom_settings.get(
            "bump_map_major_version_zero"
        )
        if custom_bump_map_major_version_zero:
            self.bump_map_major_version_zero = custom_bump_map_major_version_zero

        custom_change_type_order = self.custom_settings.get("change_type_order")
        if custom_change_type_order:
            self.change_type_order = custom_change_type_order

        commit_parser = self.custom_settings.get("commit_parser")
        if commit_parser:
            self.commit_parser = commit_parser

        changelog_pattern = self.custom_settings.get("changelog_pattern")
        if changelog_pattern:
            self.changelog_pattern = changelog_pattern

        change_type_map = self.custom_settings.get("change_type_map")
        if change_type_map:
            self.change_type_map = change_type_map

        example = self.custom_settings.get("example")
        if example:
            self.example = example

        info_path = self.custom_settings.get("info_path")
        if info_path:
            with open(info_path, encoding=self.config.settings["encoding"]) as f:
                content = f.read()
            self.info = content
        else:
            info = self.custom_settings.get("info")
            if info:
                self.info = info

        gemini_api = self.custom_settings.get("gemini_api")
        if not gemini_api:
            if os.environ.get('GOOGLE_API_KEY') is not None:
                gemini_api = os.environ['GOOGLE_API_KEY']
            else:
                raise MissingCzGeminiAPIError()

        gemini_answer_number = self.custom_settings.get('answer_number')
        if gemini_answer_number:
            self.gemini_answer_number = gemini_answer_number
        
        gemini_answer_patern = self.custom_settings.get('answer_pattern')
        if gemini_answer_patern:
            self.gemini_answer_pattern = gemini_answer_patern

        gemini_commitizen_pattern = self.custom_settings.get('commitzen_pattern')
        if gemini_commitizen_pattern:
            self.gemini_commitizen_pattern = gemini_commitizen_pattern

        gemini_template = self.custom_settings.get("template")
        if gemini_template:
            self.gemini_template = gemini_template

        gemini_verbose = self.custom_settings.get("verbose")
        if gemini_verbose:
            self.gemini_verbose = gemini_verbose

        schema_pattern = self.custom_settings.get("schema_pattern")    
        if schema_pattern:
            self._schema_pattern = schema_pattern

        schema = self.custom_settings.get("schema")
        if schema:
            self._schema = schema
        
        scope = self.custom_settings.get('scopes')
        if scope:
            self.scope = scope
        
        change_type = self.custom_settings.get('types')
        if change_type:
            self.change_type = change_type

        if "templates" not in self.config.settings:
            self.template_loader = PackageLoader("cz_gemini", "templates")

        # init gemini api
        self.ai = AiGemini(gemini_api, self.gemini_answer_pattern, self.gemini_commitizen_pattern, self.gemini_verbose)

    def changelog_message_builder_hook(self, parsed_message: dict, commit: git.GitCommit) -> dict | list | None:
        
        origin_regex = r"(?<=origin\W)(.*)(?=\s\(fetch)"
       
        #from regex101.com https://regex101.com/library/ibVctF?filterFlavors=pcre&filterFlavors=golang&orderBy=RELEVANCE&search=url
        base_url_regex = r"^(https?\:)\/\/(([^:\/?#]*)(?:\:([0-9]+))?)([\/]{0,1}[^?#]*)(\?[^#]*|)(#.*|)$"
        base_url_sub = "\\g<1>//\g<3>/"

        # get remotes from git
        git_hosts = cmd.run("git remote -v").out
        
        # Here we looking only for origin url. We do this because normally
        # we only generate changelog on base repro. In case we forked it we 
        # will push the changes back and there will generate the changelog.
        #
        # TODO: Maybe we add a config to override this behavior
        self.git_host = re.search(origin_regex, git_hosts).group()
        
        if self.git_host:
            for k,v in GIT_COMMITS_URL.items():
                    if k in self.git_host:
                        parsed_message['git_commits_url'] = v

            # in case we origin url git@github:avjui/blabla(.git) we generate https://github.com/avjui/blabla

            match_with_git = re.match(r"git@([^:]+):(.*)\.git", self.git_host)
            match_without_git = re.match(r"git@([^:]+):(.*)", self.git_host)

            if match_with_git:
                self.git_host = f"https://{match_with_git.group(1)}/{match_with_git.group(2)}"
            elif match_without_git:
                self.git_host =  f"https://{match_without_git.group(1)}/{match_without_git.group(2)}"
            else:
                self.git_host = ""

            parsed_message['git_url'] = self.git_host
                
            #parse base url from origin url
            self.git_host = re.sub(base_url_regex, base_url_sub, parsed_message['git_url'])
            parsed_message['git_base_url'] = self.git_host

        else:
            print(colored("Can not parse git host address!\n Note this will skip commit link and user link in changelog!","cyan"))

        # print(colored(f"{parsed_message}", "light_red"))
        return parsed_message

    def questions(self) -> Questions:
        

        self.question = self.custom_settings.get("questions", [{}])

        # In This case we generate autocommit from gemini
        if self.autogenerate:
            self.question = self._auto_question()
    
            
        # otherwise we make it old school manual
        else:
            self.question = self._manual_question()

        return self.question


    def message(self, answers: dict) -> str:
        
        # when we dont use autogenerate we use ai to make a spellcheck
        if not self.autogenerate:
            print(colored(f"Automatic correction spelling with gemini","blue","on_white"))  
            answers['subject'] = self.ai.correct_sentence(answers['subject'] )
        
        # make answer commitizen conform
        else:
            print(f"Answers from input: {answers}")
            if(answers['manual'] != ""):
                answers['body'] = ""
                _answer = answers["manual"].split(":")
                answers["subject"] = _answer[1]
                if ("(" in _answer[0]):
                    answers['change_type'] = _answer[0].split("(")[0]
                    answers['scope'] = _answer[0].split("(",)[1].split(")")[0]
                else:
                    answers['change_type'] = _answer[0]

            else:
                _answer = answers['subject']
                for k,v in self.ai.message[_answer].items():
                    answers[k] = v
        is_breaking_change = answers["is_breaking_change"]
        
        prefix = answers["change_type"]
        scope = answers["scope"]
        subject = answers["subject"]
        body = answers["body"]
        footer = answers["footer"]
        is_breaking_change = answers["is_breaking_change"]

        if scope:
            scope = f"({scope})"
        if body:
            body = f"\n\n{body}"
        if is_breaking_change:
            footer = f"BREAKING CHANGE: {footer}"
        if footer:
            footer = f"\n\n{footer}"

        message = f"{prefix}{scope}: {subject}{body}{footer}"

        return message



    def example(self) -> str | None:
        return self.example


    def schema_pattern(self) -> str | None:
        return self._schema_pattern


    def schema(self) -> str | None:        
        return self.schema


    def info(self) -> str | None:
        return self.info
    
    
    def _create_messages(self, name: str, message: str, choice={}, confirm=False) -> dict:
        c = []
        a = {}
        q = {}

        # type confirm. default always false
        if confirm:
            q = {
                "type": "confirm",
                "message": message,
                "name": name,
                "default": false
                }
        else:
            # if we get a dict we have type choice
            if choice:
                for k,v in choice.items():
                    a = {
                        "value" : k,
                        "name" : v
                        }
                    c.append(a)        
            
                q = {
                    "type" : "list",
                    "name": name,
                    "message" : message,
                    "choices" : c
                    }
            # we have an input type
            else:
                q = {
                    "type": "input",
                    "name": name,
                    "message": message
                    }
        return q
    
    
    def _auto_question(self) -> Questions:

        # we use the diff to send it to gemini for getting results
        gitdiff = cmd.run('git diff --no-ext-diff --cached').out
            
        # set types and scopes dict for gemini
        # note if you want to set custom scopes and types you have to            
        # for compatibility to customize plugin we have a look for 
        # `question`option in config

        if not self.question:
            _types = self.question[0]
            _scopes = self.question[1]

        # we use the new config option
        else:
            _types = self.change_type
            _scopes = self.scope

        # generate prompt for gemini based on template
        # number set how many results gemini give
        gemini_template = Template(self.gemini_template)
        gemini_template = gemini_template.render(number=self.gemini_answer_number, diff=gitdiff, types=_types, scopes=_scopes)
        self.question = self.ai.generate_auto_commit(gemini_template)
            
        # Add breaking question to autogenerate message
        # TODO: Have to test this maybe we don´t need it but for safety we
        #       have to add it.
        _question = self._create_messages("manual", MESSAGES['manual'])
        self.question.append(_question)
        _question = self._create_messages("is_breaking_change", MESSAGES['is_breaking_change'], confirm=False)
        self.question.append(_question)
        _question = self._create_messages("footer", MESSAGES['footer'])
        self.question.append(_question)

        return self.question


    def _manual_question(self) -> Questions:
        # for compatibility to customize plugin
        if not self.question:
            print(f" IS SELF QUESTEN {self.question}")
            return self.question
        # generate with new style
        else:
            message = self.custom_settings.get("messages", "")
            if message:
                self.messages = message
            question = []
            _choice = {}
            _confirm = False
            print(f"Messages : {self.messages}")
            for k,v in self.messages.items():
                
                _add = True
                _confirm = False

                # add types to choice
                if k == "change_type":
                    _choice = self.change_type
                # add scopes to choice
                elif k == "scope":
                    _choice = self.scope
                # no we need no dict anymore
                else:
                    _choice = {}
                
                if k == "manual":
                    _add = False
                
                if(_add):
                    question.append(self._create_messages(k,v, choice=_choice, confirm=_confirm))
        return question
