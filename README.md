# A basic text format checker in Python

### Using Python, concept of deterministic finite automata and regex, check whether the text is correctly formatted or not.

After checking and removing valid emails and web urls, the program checks for the following:

1) begins with capital letter
2) ends with proper punctuation
3) contains extra spaces
4) space before `.` or `?`
5) next sentence after `.` or `?` begins with capital letter or not
6) next sentence after (`.` or `?` or `!`) and 1 space starts with capital letter or not
7) match number of opening and closing for different types of brackets, `<` & `>`, `(` & `)`, `{` & `}`, `[` & `]` 


#### TODO: Readjust the indices as per original text having emails/urls
________________________________________________________________________________________________________________________________________

The function, in main.py, takes text to be checked and returns the total count of mistakes along with a dictionary of the mistakes. The values in dictionary are either bool type or list containing indices in text where mistake was recorded. 

Eg:

s = "hello .hoW are you www.abc@xyz.com? i hope all  good"

t, c, d = check_text_format(s)

print('\n', t, '\n', c)

[print(x) for x in d.items()]

#### Output:
-----------------

hello .hoW are you? i hope all  good 

8

('no_space_after_.?!', [7])

('small_case_after_._space', [20])

('capital_case_after_small_case', [9])

('start_letter_not_capital', True)

('extra_spaces', [31])

('end_not_proper', True)

('capital_letter_missed_after_.', [7])

('space_before_.?!', [5])

Note: here each number in list of dictionary refers to the index in the text after removal of emails/urls.
