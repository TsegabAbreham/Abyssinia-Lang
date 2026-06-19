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
To install Abyssinia Lang on you computer go to the releases in the middle-right window and download the latest release. One you do that run the setup in full and open CMD and type Abyss, if it shows a lion ASCII art it means it is successfully installed. One misconception is that since this is written in Python the program needs python to run, however, that is not true, Abyssinia Lang will run even if Python is not installed. Python is needed to access Python libraries through Abyssinia Lang.

<img width="1123" height="669" alt="image" src="https://github.com/user-attachments/assets/1fc7b152-7d57-4e0d-975f-393f05fc5ebb" />



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

## Getting User Input
You can get user input through the keyword `ጠይቅ`.

Example:
```
የ = ጠይቅ("ስምህ ማነዉ")።
አሳይ("ሰላም " + የ)።
```

## Lists 
For creating a list create an ordinary variable and fill in the list using '[]'.
Example:
```
ሃ = [1፣ 2፣ 3፣ 4፣ 5]።
# Display the first element on the list ·
አሳይ(ሃ[0])።
```

## Loops

### While loops
For using a while loop use the keyword `እያለ`.

Example:
```
ገ = 1።

እያለ(ገ != 5){
    አሳይ(ገ)።
    ገ = ገ+1።
}
```
### For loops
For loops have different parts, the keyword (`ለ`) the variable that is changed and the range of change.

Example:
```
ሮ  15።

ለ (ሁ፣ ከ 1 እስከ 10){
    አሳይ(ሁ)።
}
```

## Classes
Classes in this programming language are just a collection of functions and do not contain OOP things like inheritance or encapslation.

Here is how to use it:
```
ክፍል ሃ{
    ተግባር ሙከራ1(){
        አሳይ("ያአህፍህ")።
    }
    ተግባር ሙከራ2(){
        ቁጥሮች = [1፣ 2፣ 3፣ 4፣ 5፣ 6፣ 7፣ 8፣ 9]።
        አሳይ(ቁጥሮች[5])። 
    }
}

# We use '፡' to access a function from a class #
ሃ፡ሙከራ1()።
ሃ፡ሙከራ2()።

```

## Importing Files
To import external variables, functions, or classes from another Abyssinia Lang files all you have to do is use the keyword `አስገባ`
Example:

File 1 (test.aby):
```
ተግባር ነብዩ(ሽ){
    አሳይ(ሽ)።
}
```

File 2 (main.aby):
```
አስገባ "test.aby" እንደ ይይ

አሳይ(ይይ፡ነብዩ("33"))።
```

## Built-in Functions 
There are a wide range of built-in functions including math, string manipulation, list manipulation, file I/O, and requesting (Python is required for this one)

Using these Built-in Functions preview:

```
# File I/O #
f = ፋይል፡ክፈት("test.txt", "w")።
ፋይል፡ጻፍ(f, "Hello Abyss")። 
ፋይል፡ዝጋ(f)።

r = ፋይል፡ክፈት("test.txt", "r")።
text = ፋይል፡አንብብ(r)።
ፋይል፡ዝጋ(r)።

አሳይ(text)።

# Math #

አሳይ(ሂሳብ፡sin(90))።

# String #

መ = "ሃ፣ላ፣ፍ፣ር፣እ፣ቅ"።
አሳይ(ጽሁፍ፡ክፈል(መ፣ "፣"))።
አሳይ(መ[0])።
```

## Using Python's Library in Abyssinia Lang
Using Python's library in Abyssinia Lang is supported. Though the downside here is that you have to install that library you are trying to access beforehand.

This feature is on work right now and will be release when done...


