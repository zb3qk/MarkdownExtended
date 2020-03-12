import re
import copy

class Function():
    # initialized in the Dictionary Parser
    def __init__(self, name, num_params, mandatory_params, content):
        self.name = name # name of the functions

        # Set up names
        self.mandatory_params = mandatory_params # names of each of the unnamed parameters (for replacement via dictionary)
        # self.optional_params = setOptionalParameters(optional_params) # dictionary of named parameters 

        self.num_params = num_params # total number of parameters

        # Set up contents
        self.mandatory_param_contents = []     
        # self.optional_param_content = {} 

        self.content = content # String content pulled directly from the .mded file
    
    def setParameters(self, params):
        self.mandatory_param_contents = params
        
    def addUnnamedParameter(self, content):
        self.mandatory_param_contents.append(content)

    def newContent(self):
        """Fills in the parameters of the content of the .mded Function
        delcaration with the parameter-contents of the .mde function
        
        Returns:
            [str] -- [The new content (replaced parameter calls with content)]
        """
        new_content = copy.deepcopy(self.content)
        if (len(self.mandatory_param_contents) == len(self.mandatory_params)):
            for index, name in enumerate(self.mandatory_params):
                regex = r"{"+name+r"}"

                replacement = self.mandatory_param_contents[index]

                new_content = re.sub(regex, replacement, new_content)
                # print(new_content)
        return new_content
        

# Global Definitions for the Parsers
def star(element):
    """
    Marks an element to be call a single or multiple instances
    """
    return "("+element+")*"

def wrap(element, wrapper):
    """
    Wraps the element with the wrapper element and creates a group of the element
    @param element: regex to be wrapped
    @param wrapper: regex to wrap around the element
    """
    return "("+ wrapper + element + wrapper + ")"

def numOccur(element, num):
    return "{"+str(num)+"}" + element

space = "\s*"
anyChar = ".+"
word = "\s*(\w+)\s+"
reg_or = "|"

"""
.mde parser
"""
class mdeParser():
    """ This is a parser for the .mde file.

        The parser matches function calls that match the functions provided by a .mded file
        and are of one following syntaxes:
        0. Multiple parameters, whitespace delimited, enclosed by parentheses
        1. Single parameter after a system call

        Method calls to this class are used to convert .mde files to their corresponding
        .md equivalents by replacing the .mde function calls with HTML defined in the .mded
        dictionary.

        Use example:
            parser = mdeParser(dictionary) # parameter is a list of functions
            parser.parseFiles(mdeFile, mdFile)
            # Result: a file defined by mdFile will be populated with the markdown and HTML informed by mdeFile
    """
    # function_list is defined from list of functions parsed from a .mded file
    def __init__(self, function_dictionary):
        self.function_dictionary = function_dictionary
        self.function_list = function_dictionary.keys()

        parameter = "(\".+\"|\w+)\s*" # matches for a parameter
        # defined by any set of characters within quotes or a word within quotes (be wary of using quotes within quotes)
        
        """ Parser function matches """
        Regexes = []
        Regexes.append("^\$\s*"+ word + "\((\s*" + star(parameter) + "\s*)\)" ) # match for the full expression
        Regexes.append("^\$\s*" + word + '\s*(\w+)\s*' + '$') # single parameter expression

        self.parameter = re.compile(parameter,re.MULTILINE)

        self.patterns = []
        for regex in Regexes:   
            cur_pattern = re.compile(regex,re.MULTILINE) 
            self.patterns.append(cur_pattern)

    
    def parseFile(self, file, newFile):
        """Abstraction around file interpretation and creating the new file
        
        Arguments:
            file {file} -- [file opened by the user to be interpreted]
            newFile {file} -- [new file opened to dump the interpreter's contents]
        """
        buffer = file.read() # extract text from file
        for patternType in range(len(self.patterns)): # pass through each pattern type 
            pattern = self.patterns[patternType]
            for match in pattern.finditer(buffer): # pass through each match in the file
                # print(match)
                newContent = self.parseFunctionCall(match.groups(), patternType)
                if (newContent == None):
                    newContent = "" # replace all error function calls with a blank line
                    # TODO: Raise error on bad function
                strt, end = match.span()
                replacement_pattern = match.string[strt:end]
                buffer = buffer.replace(replacement_pattern, newContent) # replace function call with new content (in buffer)
        self.buildNewFile(buffer, newFile) # Write new content into the file

    def buildNewFile(self, buffer, newFile):
        """Copies the contents of the old file to the new file
        
        Arguments:
            buffer {str} -- [file contents to be copied]
            newFile {file} -- [file to be copied to]
        """
        newFile.write(buffer)

    def parseFunctionCall(self, functionCall, patternType):
        """Conducts replacement in new file with new text informed by function parameters
        
        Arguments:
            functionCall {(string, list)} -- [Contains the name of the function and the list of parameters]
            patternType {int} -- [integer indicating what pattern was used to parse]
        """
        function_name = functionCall[0]
        if (function_name not in self.function_dictionary.keys()):
            # TODO: Raise error
            return None
        if patternType == 0 or patternType == 1: # parameters passed in parentheses
            # print("success: " + function_name)
            matches = self.parameter.findall(functionCall[1]) # pass through each match in the file
           
            cur_function = self.function_dictionary[function_name]
            cur_function.setParameters(matches)

            return cur_function.newContent() # return content to replace function call
        return None

"""
.mded parser
"""
class mdedParser():
    """Parses a dictionary file and develops the list of functions necessary

    Checks for a pre-compiled version of the dictionary in the same directory (pickled),
    and sees whether or not there have been any changes made
    """
    def __init__(self, function_dictionary={}):
        self.function_dictionary = function_dictionary

        parameter = "\s*(\w+)\s*" # matches for a parameter
        name = "\{(\w+)\}"
        content = "\{(\{\w+\}|\s*.*\s*)\}" # matches the content within the brackets (including name calls and other content, with order of precendece on name calls)
        # content = ""
        
        # defined by any set of characters within quotes or a word within quotes (be wary of using quotes within quotes)
        
        """ Parser function matches """
        Regexes = []
        Regexes.append("^"+ word + "\((\s*" + star(parameter) + "\s*)\)\s*" + content) # match for the full expression

        self.parameter = re.compile(parameter)
        self.name = re.compile(name, re.MULTILINE)
        self.content = re.compile(content, re.MULTILINE)

        self.patterns = []
        for regex in Regexes:
            cur_pattern = re.compile(regex,re.MULTILINE) 
            self.patterns.append(cur_pattern)
    
    def generateFunctionDictionary(self, dictionaryFile):
        buffer = dictionaryFile.read()
        for patternType in range(len(self.patterns)): # pass through each pattern type 
            pattern = self.patterns[patternType]
            for match in pattern.finditer(buffer): # pass through each match in the file
                self.parseFunction(match.groups())
        return self.function_dictionary
        
    def parseFunction(self, match):
        # get parameter names
        function_name = match[0]
        if (function_name in self.function_dictionary.keys()):
            pass # TODO: Raise error

        params = []
        for parameters in self.parameter.finditer(match[1]):
            parameter = parameters.groups()[0] 
            params.append(parameter)
        content = match[-1] 

        # check parameter calls in content is valid
        for names in self.name.finditer(content):
            name = names.groups()[0] 
            if name not in params:
                pass # TODO: Raise Error
        
        curFunction = Function(function_name,len(params),params,content)
        self.function_dictionary[function_name] = curFunction

