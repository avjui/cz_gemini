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

from google.generativeai.types import HarmCategory, HarmBlockThreshold

from commitizen import defaults
from commitizen.defaults import Questions


# only a dirty fix 
# TODO: have a look into to 
false = "false"

# bump defaults
BUMP_PATTERN= "^(.+!|BREAKING CHANGE|docs|feat|fix|perf|refactor|revert|style|test)"
BUMP_MAP = {
        ".+!": "MAJOR",
        "BREAKING CHANGE": "MAJOR",
        "feat": "MINOR",
        "fix": "PATCH",
        "docs": "PATCH",
        "perf": "PATCH",
        "refactor": "PATCH",
        "revert": "MINOR",
        "style": "PATCH",
        "test": "PATCH"
      }
BUMP_MAP_MAJOR_VERSION_ZERO = defaults.bump_map_major_version_zero

# default change_types
CHANGE_TYPES = {
        "fix" :  "fix: A bug fix. Correlates with PATCH in SemVer.",
        "feat" : "feat: A new feature. Correlates with MINOR in SemVer.",
        "docs" : "docs: Documentation only changes.",
        "refactor" : "refactor: A code change that neither fixes a bug nor adds a feature.",
        "test" : "test: Adding missing or correcting existing tests.",
        "ci/cd" : "ci/cd: Changes to our CI configuration files and scripts (example scopes: GitHub).",
        "build" : "build: Changes that affect the build system or external dependencies (example scopes: pip, docker, npm)."
      }

# change_type defaults
CHANGE_TYPE_ORDER = [
        ":boom: Breaking Changes",
        ":sparkles: Features",
        ":bug: Bug Fixes",
        ":lipstick: Styling",
        ":zap: Performance",
        ":recycle: Refactor",
        ":rewind: Reverted",
        ":memo: Documentation",
        ":construction_worker: CI/CD or developer scripts",
        ":white_check_mark: Test"
      ]
CHANGE_TYPE_MAP= {
        "BREAKING CHANGE": ":boom: Breaking Changes",
        "build": ":construction_worker: CI/CD or developer scripts",
        "ci": ":construction_worker: CI/CD or developer scripts",
        "docs": ":memo: Documentation",
        "feat": ":sparkles: Features",
        "fix": ":bug: Bug Fixes",
        "perf": ":zap: Performance",
        "refactor": ":recycle: Refactor",
        "revert": ":rewind: Reverted",
        "style": ":lipstick: Styling",
        "test": ":white_check_mark: Test"
      }
    
# changelog pattern default
CHANGELOG_PATTERN = "^(.+!|BREAKING CHANGE|build|ci|docs|feat|fix|perf|refactor|revert|style|test)"

# commit parser defaults
COMMIT_PARSER = "^((?P<change_type>build|ci|docs|feat|fix|perf|refactor|revert|style|test|BREAKING CHANGE)(?:\\((?P<scope>[^()\r\n]*)\\)|\\()?(?P<breaking>!)?|\\w+!):\\s(?P<message>.*)?"


# example default
EXAMPLE = "feature(front): adds the header component"

# gemini defaults
GEMINI_ANSWER_NUMBER = 5
GEMINI_ANSWER_PATTERN = r"(?:\```?\n?)"
GEMINI_COMMITIZEN_PATTERN = r"(?P<type>.*?)\((?P<scope>.*?)\)\:\ (?P<subject>.*?)\-\ (?P<body>.*?)\n"
GEMINI_CONFIG = {
                'temperature': 0.7,
                'candidate_count': 1,
                'top_k': 40,
                'top_p': 0.95,
                'max_output_tokens': 1024,
                }
GEMINI_SAEFTY = {
                  HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                  HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
                  HarmCategory.HARM_CATEGORY_HATE_SPEECH:HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
                  HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE 
                }
GEMINI_TEMPLATE = " \
suggest exact {{number}} commit messages based on the following diff: \n\
{{diff}}\n \
commit messages should:\n \
 - Follow conventional commits \n\
 - Message format should be: <type>[scope]: <description> - <detail> \n\
 - Description should not be longer then 50 character \n\
 - Description should be lower case and no period \n\
 - Detail should contain detail information of changes \n\
 - Valid type name (key name is 'value') and description of the type name (key name is 'name') can be found in following dict with the key name 'value' {{types}} \n\
 - Valid scope name (key name 'value') and description of the scope name (key name is 'name') can be found in following dict with the key name 'value' {{scopes}} \n\
 - Avoid the same commits message \n\
 - Reply with JUST the commit message, without quotes, comments, questions, etc! \n\
\
examples:\
 - fix(back): add password regex pattern \n\
 - test(perf): add new test cases \n"

GIT_COMMITS_URL = {
    "github.com" : "/commit/",
    "gitlab" : "/-/commit/",
    "gitea" : "/commit/"
}


MESSAGES = {
    "change_type" : "Select the type of change you are committing",
    "scope" : "What is the scope of this change? (class or file name): (press [enter] to skip)",
    "subject" : "Write a short and imperative summary of the code changes: (lower case and no period)\n",
    "body" : "Provide additional contextual information about the code changes: (press [enter] to skip)\n",
    "is_breaking_change" : "Is this a BREAKING CHANGE? Correlates with MAJOR in SemVer. (press [enter] if not)\n",
    "footer" : "Footer. Information about Breaking Changes and reference issues that this commit closes: (press [enter] to skip)\n",
    "manual" : "Maybe you are not happy with geminis answer. Do you wan´t make it old school be hand (press [enter] if you are happy)\n"
}

# default question:
QUESTIONS : Questions = [
        {
          "type": "list",
          "name": "change_type",
          "message": "Select the type of change you are committing",
          "choices": [
            {
              "value": "fix",
              "name": "fix: A bug fix. Correlates with PATCH in SemVer.",
              "key": "x"
            },
            {
              "value": "feat",
              "name": "feat: A new feature. Correlates with MINOR in SemVer.",
              "key": "f"
            },
            {
              "value": "docs",
              "name": "docs: Documentation only changes.",
              "key": "d"
            },
            {
              "value": "style",
              "name": "style: Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc.).",
              "key": "s"
            },
            {
              "value": "refactor",
              "name": "refactor: A code change that neither fixes a bug nor adds a feature.",
              "key": "r"
            },
            {
              "value": "perf",
              "name": "perf: A code change that improves performance.",
              "key": "p"
            },
            {
              "value": "test",
              "name": "test: Adding missing or correcting existing tests.",
              "key": "t"
            },
            {
              "value": "build",
              "name": "build: Changes that affect the build system or external dependencies (example scopes: pip, docker, npm).",
              "key": "b"
            },
            {
              "value": "ci",
              "name": "ci: Changes to our CI configuration files and scripts (example scopes: GitHub).",
              "key": "c"
            }
          ]
        },
        {
          "type": "list",
          "name": "scope",
          "message": "What is the scope of this change? (class or full file name): (press [enter] to skip) ",
          "choices": [
            {
              "value": "front",
              "name": "front: Changes to Svelte and the front end."
            },
            {
              "value": "back",
              "name": "back: Changes to the back end not directly related to Strapi."
            },
            {
              "value": "ci",
              "name": "ci: CI/CD changes like GitHub Workflows etc."
            },
            {
              "value": "github",
              "name": "github: GitHub-specific changes to CI/CD, secrets, etc."
            },
            {
              "value": "perf",
              "name": "perf: Perf testing, configuration, and/or enhancements."
            },
            {
              "value": "project",
              "name": "project: Configuration, CI/CD, Developer Experience, etc."
            },
            {
              "value": "terraform",
              "name": "terraform: Changes to Terraform/Infrastructure."
            },
            {
              "value": "docker",
              "name": "docker: Changes to Dockerfiles/build steps."
            },
            {
              "value": "testing",
              "name": "testing: Changes to testing utils/tests."
            },
            {
              "value": "utils",
              "name": "utils: Changes to developer scripts and utils."
            }
          ]
        },
        {
          "type": "input",
          "name": "subject",
          "message": "Write a short and imperative summary of the code changes: (lower case and no period)\n"
        },
        {
          "type": "input",
          "name": "body",
          "message": "Provide additional contextual information about the code changes: (press [enter] to skip)\n"
        },
        {
          "type": "confirm",
          "message": "Is this a BREAKING CHANGE? Correlates with MAJOR in SemVer",
          "name": "is_breaking_change",
          "default": false
        },
        {
          "type": "input",
          "name": "footer",
          "message": "Footer. Information about Breaking Changes and reference issues that this commit closes: (press [enter] to skip)\n"
        }
      ]
    
# schema defaults
SCHEMA_PATTERN = "^(build|ci|docs|feat|fix|perf|refactor|revert|style|test){1}(\\([\\w\\-\\.]+\\))?(!)?: ([\\w \\-'])+([\\s\\S]*)"
SCHEMA = "<type>(<scope>): <subject>\n \n<body>\n \n(BREAKING CHANGE: )<footer>"

#default scopes
SCOPES = {
        "frontend" : "frontend: Changes make to frontend webgui or display",
        "backend" : "backend: Changes make to backend system",
        "ble" : "ble: Changes make to ble",
        "wifi" : "wifi: Changes make to wifi",
        "component" : "component: Changes on components (example: change version of component)",
        "project" : "project: Configuration, CI/CD, Developer Experience, etc.",
        "Testing" : "testing: Changes to testing utils/tests.",
        "utils" : "utils: Changes to developer scripts and utils."
      }

# info defaults
INFO = "Customize plugin for spellchecking using google gemini ai."

