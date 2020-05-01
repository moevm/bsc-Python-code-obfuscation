# MIT License

# Copyright (c) 2019 Hnfull

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import re
import pathlib

from app.obfuscation import id_generator
from app.obfuscation import obfuscation_settings


# --only for breaking a loop -- #
class BreakLoop(Exception):
    pass


class ObfuscateRenameVars:

    def __init__(self):

        self.settings = obfuscation_settings.settings['semantic']

        self.intensio_dir_path = pathlib.Path(__file__).parent
        self.exclude_dir = self.intensio_dir_path / "exclude"

        self.pythonExcludeDefaultString = self.exclude_dir / "string_to_string_mixed" / "exclude_word_do_not_modify.txt"
        self.pythonExcludeUserString = self.exclude_dir / "string_to_string_mixed" / "exclude_word_by_user.txt"

        self.id_generator = id_generator.UniqueObfuscatedIdGenerator()

    def EachLine(self, line, dictionary, fileNameImport, listModuleImport):
        getIndexLineList = []
        returnLine = []
        charValue = []
        checkCharAfterWord = 1
        wordSetter = 0
        checkGetKey = ""
        checkGetWord = ""
        getLine = ""
        breakLine = ""

        if listModuleImport == True:
            detectChars = r"\.|\:|\)|\(|\=|\[|\]|\{|\}|\,|\+|\s|\*|\-|\%|\/|\^|\'|\""
        else:
            detectChars = r"\.|\:|\)|\(|\=|\[|\]|\{|\}|\,|\+|\s|\*|\-|\%|\/|\^"

        # -- Get list of all letters in line -- #
        for indexLine, letterLine in enumerate(line):
            getIndexLineList.append(letterLine)

        # -- Loop in each letter of line -- #
        for indexLine, letterLine in enumerate(line):
            # -- Add in final line list all chars mixed -- #
            if charValue != []:
                for obfIndex, obfValue in enumerate(charValue):
                    if obfIndex == 0:  # First letter in string mixed are already add in the final line
                        continue
                    returnLine.append(obfValue)
                charValue = []

                # -- If the variable is only a letter, check if the next character is specific so as not to replace it -- #
                if re.match(detectChars, letterLine):
                    returnLine.append(letterLine)

                # -- Count indexes of word to move after it --#
                countDeleteIndex = 0
                for i in getWord:
                    countDeleteIndex += 1
                wordSetter = countDeleteIndex - 2  # -2 Is to letter already append and the letter in progress
            else:
                # -- The index numbers of variable is decremented to add the mixed letters that be replaced -- #
                if wordSetter > 0:
                    wordSetter -= 1
                    continue
                else:
                    try:
                        # -- Loop in the dictionary with already mixed values-- #
                        for key, value in dictionary:
                            for indexKey, letterKey in enumerate(key):
                                for letterValue in value:
                                    # -- Check if letter of word is equal to letter of key -- #
                                    if letterKey == letterLine:
                                        # -- Begin process to check -- #
                                        if indexKey == 0:
                                            indexExplore = indexLine + len(
                                                key
                                            )  # Place index position after the word

                                            # -- If indexError return to next loop -- #
                                            try:
                                                getIndexLineList[indexExplore]
                                            except IndexError:
                                                continue

                                            # -- Check the char after and before the word -- #
                                            if re.match(
                                                detectChars,
                                                getIndexLineList[indexExplore]
                                            ):
                                                # Index check if word finded is not into the other word
                                                indexExploreBefore = indexLine - 1
                                                # Index check char after the end string found with 'detectChars' regex
                                                indexExploreAfter = indexLine + 2

                                                try:
                                                    if not re.match(
                                                        r"\w|\\|\%",
                                                        getIndexLineList[
                                                            indexExploreBefore]
                                                    ):
                                                        # -- Check if it's 'from' and 'import' file in line to avoid replace \
                                                        # name of file if variable is identic name to file -- #
                                                        getLine = "".join(
                                                            getIndexLineList
                                                        )
                                                        if fileNameImport == False:
                                                            if "import" in getLine:
                                                                if "from" in getLine:
                                                                    # -- Cut the line from the current index and check if it is \
                                                                    # not there is the keyword "import" in the line -- #
                                                                    breakLine = getIndexLineList[:
                                                                                                 indexLine
                                                                                                ]
                                                                    breakLine = "".join(
                                                                        breakLine
                                                                    )
                                                                    if not "import" in breakLine:
                                                                        # -- It's file because only 'from'key word -- #
                                                                        checkCharAfterWord = 1
                                                                    else:
                                                                        checkCharAfterWord = 0
                                                                else:
                                                                    checkCharAfterWord = 1
                                                            # -- Check if after char find by 'detectChars' variable it's \
                                                            # not ' or " -- #
                                                            elif re.match(
                                                                r"\"|\'",
                                                                getIndexLineList[
                                                                    indexExploreAfter
                                                                ]
                                                            ):
                                                                if re.match(
                                                                    r"\[|\(|\{",
                                                                    getIndexLineList[
                                                                        indexExploreAfter
                                                                        - 1]
                                                                ):
                                                                    checkCharAfterWord = 0
                                                                else:
                                                                    checkCharAfterWord = 1
                                                            else:
                                                                checkCharAfterWord = 0
                                                        # -- Only for [-rfn, --replacefilsname] feature -- #
                                                        else:
                                                            # -- check if file name is imported - #
                                                            breakLine = getIndexLineList[:
                                                                                         indexLine
                                                                                        ]
                                                            breakLine = "".join(
                                                                breakLine
                                                            )
                                                            # -- If file name is imported after 'import', the file name is not \
                                                            # replaced -- #
                                                            if "import" in breakLine:
                                                                checkCharAfterWord = 1
                                                            else:
                                                                checkCharAfterWord = 0
                                                    else:
                                                        checkCharAfterWord = 1
                                                except IndexError:
                                                    checkCharAfterWord = 0
                                                    pass
                                            else:
                                                checkCharAfterWord = 1

                                            if checkCharAfterWord == 0:
                                                # -- Initialize vars -- #
                                                getCharAllInKey = []
                                                getWord = []

                                                indexExploreStart = indexLine
                                                # -- Delete -1, first letter is already increment -- #
                                                indexExploreEnd = indexLine + len(
                                                    key
                                                ) - 1

                                                # -- List contain all letters of key -- #
                                                for getLetterKey in key:
                                                    getCharAllInKey.append(
                                                        getLetterKey
                                                    )

                                                # -- Check if all letters of key is equal to all letters of word -- #
                                                for indexCheckLetter, checkLetter in enumerate(
                                                    getIndexLineList
                                                ):
                                                    if indexCheckLetter >= indexExploreStart and \
                                                    indexCheckLetter <= indexExploreEnd:
                                                        getWord.append(
                                                            checkLetter
                                                        )

                                                # -- Check if number of chars in key equal number of chars in word -- #
                                                if list(
                                                    set(getCharAllInKey) -
                                                    set(getWord)
                                                ) == []:
                                                    checkGetWord = "".join(
                                                        getWord
                                                    )
                                                    checkGetKey = "".join(
                                                        getCharAllInKey
                                                    )

                                                    # -- Check if key == word -- #
                                                    if checkGetWord == checkGetKey:
                                                        for obfChar in value:
                                                            charValue.append(
                                                                obfChar
                                                            )

                                                        letterLine = letterValue
                                                        raise BreakLoop
                                                    else:
                                                        continue
                                                else:
                                                    continue
                                            else:
                                                continue
                                        else:
                                            continue
                                    else:
                                        continue

                        raise BreakLoop

                    except BreakLoop:
                        returnLine.append(letterLine)

        # -- Rewrite the line -- #
        return "".join(returnLine)

    def rename_vars(self, source):

        if not self.settings['vars_renames']['is_on']:
            return source

        variablesDict = {}
        classesDict = {}
        functionsDict = {}
        allDict = {}
        classFuncDict = {}
        checkWordsMixed = []
        wordsExcludedUser = []
        wordsExcludedUserFound = []
        wordsExcludedDefault = []
        wordsExcludedDefaultFound = []
        checkAllWords = []
        checkWordsError = []
        checkKeyWordsMixed = []
        checkCountWordsMixed = 0
        checkCountWordsValue = 0
        checkQuotePassing = 0
        countRecursFiles = 0

        # -- Catch all variable(s)/class(es)/function(s) name -- #
        functionsDefined = r"def\s+(\w+)"
        classDefined = r"class\s+(\w+)"
        variablesErrorDefined = r"except(\s+\w+\s+as\s+)(\w)"
        variablesLoopDefined = r"for\s+([\w\s\,]+)(\s+in\s+)"
        variablesDefined = r"(^[\s|a-zA-Z_]+[\,\s\w]{0,})+(\s*=\s*[\[|\{\(|\w+|\"|\'])"

        quotesIntoVariable = r".*={1}\s*[\"|\']{3}"
        quotesEndMultipleLines = r"^\s*[\"|\']{3}\)?\.?"
        quotesInRegex = r"={1}\s*r{1}[\"|\']{3}"

        for eachLine in source.splitlines(keepends=True):
            # -- Variables -- #
            search = re.search(variablesDefined, eachLine)
            if search:
                if "," in search.group(1):
                    modifySearch = search.group(1).replace(",", " ")
                    modifySearch = modifySearch.split()
                    for i in modifySearch:
                        if i not in variablesDict:
                            mixer = self.id_generator.get_random_name_random_len(
                                self.settings['vars_renames']['min_len'],
                                self.settings['vars_renames']['max_len']
                            )
                            i = i.strip()
                            variablesDict[i] = mixer
                else:
                    if search.group(1) not in variablesDict:
                        mixer = self.id_generator.get_random_name_random_len(
                            self.settings['vars_renames']['min_len'],
                            self.settings['vars_renames']['max_len']
                        )
                        modifySearch = search.group(1).strip()
                        variablesDict[modifySearch] = mixer

            # -- Error variables -- #
            search = re.search(variablesErrorDefined, eachLine)
            if search:
                mixer = self.id_generator.get_random_name_random_len(
                    self.settings['vars_renames']['min_len'],
                    self.settings['vars_renames']['max_len']
                )
                if search.group(2) not in variablesDict:
                    variablesDict[search.group(2)] = mixer

            # -- Loop variables -- #
            search = re.search(variablesLoopDefined, eachLine)
            if search:
                if "," in search.group(1):
                    modifySearch = search.group(1).replace(",", " ")
                    modifySearch = modifySearch.split()
                    for i in modifySearch:
                        if i not in variablesDict:
                            mixer = self.id_generator.get_random_name_random_len(
                                self.settings['vars_renames']['min_len'],
                                self.settings['vars_renames']['max_len']
                            )
                            variablesDict[i] = mixer
                else:
                    if search.group(1) not in variablesDict:
                        mixer = self.id_generator.get_random_name_random_len(
                            self.settings['vars_renames']['min_len'],
                            self.settings['vars_renames']['max_len']
                        )
                        variablesDict[search.group(1)] = mixer

            # -- Function(s) -- #
            search = re.search(functionsDefined, eachLine)
            if search:
                mixer = self.id_generator.get_random_name_random_len(
                    self.settings['vars_renames']['min_len'],
                    self.settings['vars_renames']['max_len']
                )
                if search.group(1) not in functionsDict:
                    if not "__init__" in search.group(1):
                        functionsDict[search.group(1)] = mixer

            # -- Class(es) -- #
            search = re.search(classDefined, eachLine)
            if search:
                mixer = self.id_generator.get_random_name_random_len(
                    self.settings['vars_renames']['min_len'],
                    self.settings['vars_renames']['max_len']
                )
                if search.group(1) not in classesDict:
                    classesDict[search.group(1)] = mixer

            # -- Delete excluded variables/classes/functions defined from \
            # 'exclude/string_to_string_mixed/exclude_word_do_not_modify.txt' -- #
            with open(self.pythonExcludeDefaultString, "r") as readFile:
                for word in readFile:
                    if "#" in word or word == "\n":
                        continue
                    else:
                        word = word.rstrip()
                        wordsExcludedDefault.append(word)

            # -- Delete excluded variables/classes/functions defined from \
            # 'exclude/string_to_string_mixed/exclude_word_by_user.txt' -- #
            with open(self.pythonExcludeUserString, "r") as readFile:
                for word in readFile:
                    if "#" in word or word == "\n":
                        continue
                    else:
                        word = word.rstrip()
                        wordsExcludedUser.append(word)

            for word in wordsExcludedUser:
                if word in variablesDict.keys():
                    wordsExcludedUserFound.append(word)
                if word in classesDict.keys():
                    wordsExcludedUserFound.append(word)
                if word in functionsDict.keys():
                    wordsExcludedUserFound.append(word)

            for word in wordsExcludedDefault:
                if word in variablesDict.keys():
                    wordsExcludedDefaultFound.append(word)
                if word in classesDict.keys():
                    wordsExcludedDefaultFound.append(word)
                if word in functionsDict.keys():
                    wordsExcludedDefaultFound.append(word)

            for word in wordsExcludedUserFound:
                if word in variablesDict.keys():
                    del variablesDict[word]
                if word in classesDict.keys():
                    del classesDict[word]
                if word in functionsDict.keys():
                    del functionsDict[word]

            for word in wordsExcludedDefaultFound:
                if word in variablesDict.keys():
                    del variablesDict[word]
                if word in classesDict.keys():
                    del classesDict[word]
                if word in functionsDict.keys():
                    del functionsDict[word]

        # -- Merge all dicts -- #

        allDict.update(variablesDict)

        allDict.update(functionsDict)

        allDict.update(allDict, dict2=classesDict)

        classFuncDict.update(classesDict)

        classFuncDict.update(functionsDict)

        result = []

        # -- Change variables/classes/functions to mixed values -- #
        for eachLine in source.splitlines(keepends=True):
            if len(eachLine) < 2:
                continue
            else:
                if re.match(quotesIntoVariable, eachLine):
                    if re.match(quotesInRegex, eachLine):
                        result.append(eachLine)
                    else:
                        checkQuotePassing += 1
                        eachLine = self.EachLine(
                            line=eachLine,
                            dictionary=allDict.items(),
                            fileNameImport=False,
                            listModuleImport=False
                        )
                        result.append(eachLine)
                        continue
                elif re.match(quotesEndMultipleLines, eachLine):
                    if re.match(quotesInRegex, eachLine):
                        result.append(eachLine)
                    else:
                        checkQuotePassing += 1
                        eachLine = self.EachLine(
                            line=eachLine,
                            dictionary=allDict.items(),
                            fileNameImport=False,
                            listModuleImport=False
                        )
                        result.append(eachLine)
                        if checkQuotePassing == 2:
                            checkQuotePassing = 0
                        continue
                if checkQuotePassing == 1:
                    result.append(eachLine)
                elif checkQuotePassing == 2:
                    checkQuotePassing = 0
                else:
                    if re.match(r"\s*__all__\s*=\s*\[", eachLine):
                        eachLine = self.EachLine(
                            line=eachLine,
                            dictionary=classFuncDict.items(),
                            fileNameImport=False,
                            listModuleImport=True
                        )
                        result.append(eachLine)
                    else:
                        eachLine = self.EachLine(
                            line=eachLine,
                            dictionary=allDict.items(),
                            fileNameImport=False,
                            listModuleImport=False
                        )
                        result.append(eachLine)

        return "".join(result)
