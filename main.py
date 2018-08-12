import re
import string
import collections

pattern_web_url = re.compile(
    r"""(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))""")

pattern_email = re.compile(r'([a-zA-Z]+[a-zA-Z0-9_.]*@[a-zA-Z._]+?\.(?:com|net|org|edu|gov))')


def get_email_url_indices(txt):
    span_set = set()

    r = pattern_email.finditer(txt)
    if r:
        for item in r:
            span_set.add(item.span())

    r = pattern_web_url.finditer(txt)
    if r:
        for item in r:
            span_set.add(item.span())

    nums = set()
    for start, end in span_set:
        if txt[start - 1] == ' ':
            nums.add((start - 1, end))
        else:
            nums.add((start, end))
    return {i for s, e in nums for i in range(s, e)}


def check_text_format(text):
    text = text.strip()
    mistakes = {}
    count = 0

    # check if the text starts and contains only email/url
    email = pattern_email.match(text)
    url = pattern_web_url.match(text)
    if email:
        s, e = email.span()
        if e - s in [len(text), len(text) - 1]:
            return 0, {}
    if url:
        s, e = url.span()
        if e - s in [len(text), len(text) - 1]:
            return 0, {}

    first = text[0]
    last = text[-1]

    if (first < 'A' or first > 'Z') and (first < '0' or first > '9'):
        mistakes['start_letter_not_capital'] = True
        count += 1
    if last not in ['.', '?', '!']:
        mistakes['end_not_proper'] = True
        count += 1

    mistakes['extra_spaces'] = []
    mistakes['space_used_before_.?!'] = []
    mistakes['no_space_after_.?!'] = []
    mistakes['capital_letter_missed_after_.?!_space'] = []
    mistakes['capital_letter_missed_after_.?!'] = []
    mistakes['capital_case_after_small_case'] = []

    chars_dict = collections.defaultdict(int)
    previous_to_previous_state = previous_state = current_state = 0
    capital_letters = set(string.ascii_uppercase)
    small_letters_digits_special_chars_set = set(string.ascii_lowercase + string.digits + string.punctuation)
    [small_letters_digits_special_chars_set.remove(x) for x in ['.', '?', '!']]

    index = 1
    chars_dict[text[0]] += 1
    length = len(text)

    indices_to_ignore = get_email_url_indices(text)

    while index < length:
        if index in indices_to_ignore:
            index += 1
            continue
        char = text[index]
        chars_dict[char] += 1

        if char in capital_letters:
            current_state = 0

        if char == ' ':
            current_state = 1

        if char in small_letters_digits_special_chars_set:
            current_state = 2

        if char in ['.', '?', '!']:
            current_state = 3

        '''checks for states'''

        # check if space before '.'
        if current_state == 3 and previous_state == 1:
            mistakes['space_used_before_.?!'].append(index - 1)
            count += 1

        # check if space after space -> extra space used
        elif previous_state == current_state == 1:
            mistakes['extra_spaces'].append(index)
            count += 1

        # wrong case usage: abC, 'C' is capital case after small case.
        elif current_state == 0 and previous_state == 2:
            mistakes['capital_case_after_small_case'].append(index)
            count += 1

        # ...blah. abc -> small case after '.' and space
        if previous_to_previous_state == 3 and previous_state == 1 and current_state == 2:
            mistakes['capital_letter_missed_after_.?!_space'].append(index)
            count += 1

        # no space after '.'
        if current_state in [0, 2] and previous_state == 3:
            mistakes['no_space_after_.?!'].append(index)
            count += 1

        # small letter after .
        if current_state == 2 and previous_state == 3:
            mistakes['capital_letter_missed_after_.?!'].append(index)
            count += 1

        index += 1
        previous_to_previous_state = previous_state
        previous_state = current_state

    # while ends

    ''' check the number of pairs for '(' & ')', '{' & '}', '[' & ']', '<' & '>'   '''
    if chars_dict['('] != chars_dict[')']:
        mistakes['(_)_mismatch'] = True
        count += 1

    if chars_dict['{'] != chars_dict['}']:
        mistakes['{_}_mismatch'] = True
        count += 1

    if chars_dict['['] != chars_dict[']']:
        mistakes['[_]_mismatch'] = True
        count += 1

    if chars_dict['<'] != chars_dict['>']:
        mistakes['<_>_mismatch'] = True
        count += 1

    return count, mistakes


if __name__ == '__main__':
    s = "hello .hoW are you www.xyz.com? i hope all  good"
    c, m = check_text_format(s)
    print(s, '\n', c)
    [print(x) for x in m.items()]
