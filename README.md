# Introduction
Abyssinia Lang is an interpreted programming language that uses an Amharic syntax rather than a traditional English syntax. Its goal is to make programming/coding more accessible to Ethiopians who can't speak English and teach things like algorithms in a language that is understandable. The programming language uses Python to do the interpreting so it is able to use 
Python libraries inside the language (requires the install of Python to do that). This language supports basic things that teach people the basics of programming, things like:
 - Ouputing and Inputing to console
 - Loops (for and while)
 - Functions
 - Case...Break
 - Classes (not advanced OOP just simple class containing multiple functions)
 - External file importing
 - Built-in functions (math, file read/write/open/close)
 - Access to Python libraries (requires Python and the library you are trying to access installed)


# Installation
To install Abyssinia Lang on you computer go to the releases in the middle-right window and download the latest release. One you do that run the setup in full and open CMD and type Abyss, if it shows a lion ASCII art it means it is successfully installed.


# Basic Usage Guide to Abyssinia Lang
The Syntax for Abyssinia Lang is very similar to Python with language exceptions. Here are some basic usage of the language

## Running a code
To run an Abyssinia Lang code first create a file with the extension `.aby` then on the CMD type `abyss -f yourfilename.aby`.

## Comments 
To do a single line comment start with '#' and when done close with that same '#', example:
    
    # ሙከራ አስታየት #
To do multiline comments start with "~~" and end with those same characters, example:
```
   ~~
   ሙከራ አስታየት 
   ሙከራ አስታየት 1  
   ሙከራ አስታየት 2  
   ~~
```
## Printing
To do a simple hello world program you simple use the keyword 'አሳይ'

Example:
`
አሳይ("Hello World")።

Note: when finishing a line you should always finish with a semicolon (;) or an amharic four dot full stop (።).

## Variables
Creating a variable is simple, unlike C/C++ or other low-level languages you don't to define variable type instead it is like python:

`
ሙከራ_ተልዋዋጭ = 5።
`

## Conditionals
Using conditionals in Abyssinia Lang is simple you just have to know the keywords which are:
 - if -> ከሆነ
 - else if -> ካልሆነ
 - else -> ሌላ

 - and -> እና, it can also be '&&'
 - or '> ወይም, it can also be '||'


An example can be:
```
ሃ = 10።
ለ = 20።

ከሆነ (ሃ > ለ) {
   አሳይ("ሃ ከ ለ ይበልጣል")።
}
ካልሆነ (ሃ < ለ) {
   አሳይ("ለ ከ ሃ ይበልጣል")።
}
ሌላ {
  አሳይ("እኩል ናቸው")።
}
```
## Functions 
Using functions are also simple you define a function by using the keyword `ተግባር` then followed by the name of your function. You can also pass in parameters to the function like any other function. Note when you are passing in parameters using `፣` as a separater of parameters, if you don't want to use that use a regular comma (,) and it will work without any other problem.

Example:
```
ተግባር ሙከራ(ቁጥር1፣ ቁጥር2) {
    አሳይ(ቁጥር1 + 1)።
    አሳይ(ቁጥር2 + 1)።
}

# Use this to call the function back and pass in your parameters #
ሙከራ(1፣ 5)።

```











