#!/usr/bin/env python3

import pickle
import Parser
import fire # for CLI
import os # for file system parsing
import glob # for file system searching

def setupDictionary(mdedFile):
    parser = Parser.mdedParser()
    return parser.generateFunctionDictionary(mdedFile)

def listmdeFiles():
    return [f for f in glob.glob("*.mde")]

def listmdedFiles():
    return [f for f in glob.glob("*.mded")]

def generateFile(mdeFile, mdFile, function_dictionary):
    parser = Parser.mdeParser(function_dictionary)
    parser.parseFile(mdeFile, mdFile)

# parser = mdeParser(functions)
class CLI(object):
    """ A class to create workflows for .mde and .mded files """

    def compile(self, nameMDE=None, nameMD=None):
        """Compile MDE files in current directory using a MDED file either in the current directory
        or in the global dictionary
        
        Keyword Arguments:
            nameMDE {string} -- [Name of the MarkdownExtended file to be interpreted] (default: {None})
            nameMD {string} -- [Name of the output markdown file] (default: {None})
        """
        function_dictionary = setupDictionary(open(listmdedFiles()[0])) # retrieves first .mded file in the directory

        if (nameMDE != None): # compile all in current directory
            with open(nameMDE+".mde") as mdeFile:
                if (nameMD == None): # name MD file same as the 
                    with open(nameMDE+".md") as mdFile:
                        generateFile(mdeFile, mdFile, function_dictionary)
                else:
                    with open(nameMD+".md") as mdFile:
                        generateFile(mdeFile, mdFile, function_dictionary)
        else:
            listOfFiles = listmdeFiles()
            for filename in listOfFiles:
                with open(filename) as mdeFile:
                    with open(filename[:-4]+".md", "w") as mdFile:
                        generateFile(mdeFile, mdFile, function_dictionary)
                print("Compiled: ", mdeFile.name, " into ", mdFile.name)
        print("Finished")
        pass

if __name__ == "__main__":
    fire.Fire(CLI)