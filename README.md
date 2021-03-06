# MarkdownExtended
A Markdown interpreter

## Overview
MarkdownExtended is a Markdown interpreter where users can build custom functions to inject predfined HTML blocks into Markdown files. This works by defining the functions a MarkdownExtended Dictionary file and compiling MarkdownExtended files through these dictionaries.  

## MarkdownExtended file (.mde)
Anything that is not a part of MarkdownExtended will ignored. If a line begins with the $, then it will be compiled by MarkdownExtended.

### Writing Style
Each MarkdownExtended function starts with the '$' character. The following string should be an alpha-numerical word with no whitespace characters defining the function's name. The language supports either a single parameter function call with no parentheses or a multiparameter function call wrappped in parentheses. Each of these parameters are space delimited. These spaces can be any whitespace character including newlines. There must be the same number of parameters written as the function necessitates or else MarkdownExtended will not successfully compile. inputs that require whitespace characters or empty inputs can be enclosed in quotes. 

```
$ a_short_function "My little Pony"
```
```
$ a_long function ("My little Pony" 
    12 
    forty
        ""
    )
```
#### Notes
If double quotes are needed, they can be prepended with a backslash ```"\""```.

## MarkdownExtended Dictionary file (.mded)
For normal compilation, the MarkdownExtended Dictionary file must be in the same directory as the .mke file being compiled. If this is not the case, then the compiler will go up to 3 directories above to find a .mked file. If your project structure is more complicated, then one can include the filepath to the .mked file in one's .mke file. 

For custom build scripts, one can call the following for any number of files:
```
markdownex compile dictionary file1 file2
```

### Writing Style
The writing style is similar to most C-like programming langauges aside from two exceptions. Parameters enclosed in parentheses are space delimited and the values of the parameters can be called using the following brackets enclosed form: ``` {name} ```. All of the contents in the enclosed in the brackets will be pasted into the generated Markdown file on compilation.


```
a_short_function(favorite_cartoon){
    <p>My favorite cartoon is {favorite_cartoon}</p>
}

a_long function (cartoon upper_age lower_age comment){
    <h1>{cartoon}</h1>
    <script>
        var age_up = {upper_age};
        var age_low = {lower_age}; 
    </script>
}
```
#### Notes
If curly brackets are needed, they can be prepended with a backslash ```"\{"```.

## Command Line Interface
Call  ```python markdownex compile``` to get started