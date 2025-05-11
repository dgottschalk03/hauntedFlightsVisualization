


import re
from typing import Pattern
from itertools import chain
import datetime 
import datefinder # https://github.com/akoumjian/datefinder
from number_parser import parse # https://github.com/scrapinghub/number-parser
import re

def contains_keywords(text, keywords):
    '''
    Takes plain text and returns groups of tokens separated by "sep". 
    Used to make "Visual_Evidence" and "Audio_Evidence" features. 
    Input:
        [text]       - raw text description
        [keywords]   - List of keywords
    Returns:
        [Bool]       - Wether or not text contains a keyword
    eg. 
    >>> str = "I saw a ghost last night."
    >>> keywords = ['see', 'saw', 'seen', ...etc]
    >>> contains_keywords(str, keywords)
    True

    '''
    if isinstance(text, str):
        for keyword in keywords:
            if re.search(keyword, text, re.IGNORECASE):
                return True  
    return False

def extractSequences(tokens : list[str], sepChar: str) -> list[list[str]]:
    '''
    Takes plain text and returns groups of tokens separated by "sep". 
    For this analysis, sepChar is ".". 
    Input:
        [tokens]    - List of tokens
        [sepChar]   - Character that separates sequences
    Returns:
        Sequences   - list of sentence broken into tokens
    '''
    Sequences = []
    currentSequence = []
    
    for token in tokens:
        # Check for Punctuation #
        if token == sepChar:
        # Append Sentence to Res and Reset CurrentSequence #
            currentSequence.append(token)
            Sequences.append(currentSequence)
            currentSequence = []
        else:
            currentSequence.append(token)
    if currentSequence != []:
        Sequences.append(currentSequence)
    return Sequences

def check_regex(text: str, regex: Pattern, *optional_regex : Pattern) -> tuple[bool, list[str]] | bool:
    '''
    Check regex matches for a body of text. 

    Steps:
    1. Check each regex in order
    2. Return false if any regex does not match
    3. Otherwise return True

    Input:
        [text]                  - raw text with quantifiers converted to digits
        [regex]                 - precompiled regular expression 
        [optional_regex]        - additional precompile regular expressions

    Returns:
        [bool]                  - result of re.search()
        [keywords]              - list of matched keywords for full regex match 
    
    NOTE: Match only returns true if all regexes match. 

    eg.
    >>> check_regex("I went to the store", re.compile(r"\\bi\\b"), re.compile(r"\\bstore\\b"))
    [True, ['I', 'store']]
    '''
    ## Compile regular expressions ##
    # Unpack pattern in case it is stored as tuple 
    if isinstance(regex, tuple):
        patterns = [p for p in regex] + list(optional_regex)  
    else:
        patterns = [regex] + list(optional_regex)

    ## Target number of regex matches ##
    target = len(patterns) - 1
    

    ## Tokenize text and convert to sequences ##
    sequences = extractSequences(text.split(), '.')

    ## Convert sequences to strings ##
    sequences = list(" ".join(chain(sequence)) for sequence in sequences)

    ## Iterate through sequences ##
    for sequence in sequences:

        ## Initialize keyword output ##
        keywords = []

        ## Iterate through regex ##
        for i, pattern in enumerate(patterns):

            # Add matched keyword to output
            match = re.search(pattern, sequence)

            # Break loop if regex does not match
            if not match:
                break

            # Return True and matched keywords if all regexes match    
            elif i == target:
                keywords.append(match.group())
                return True, keywords
            
            # otherwise add match to keywords and continue checking regex
            keywords.append(match.group())

    ## Return False if no matches ##
    return False, []

def extract_dates(text):
    """
    Extract dates from a given text using three different methods:
    - `datefinder`
    - Two-digit regex patterns (e.g., "20's", "30s")
    - Four-digit regex patterns (e.g., "1920s", "1970's")

    Steps:
        1. Parse using datefinder.find_dates()
        2. Parse 4 digit and 2 digits regex
        3. Clean false positives
            - dates of the form [2025, 1, x] 
                - These are stray quantifiers that datefinder thinks are numbers
             - years < 1677 (landing at Plymouth Rock). These are likely 3 digit hotel rooms and other non-date objects.
                - eg. {index: 3} = "In the 1970's, one room, **room 211** ..." -> datetime([211, 1, 1]).
    Args:
        text (str): The input text containing potential date references.

    Returns:
        dict: A dictionary containing:
            - dates (list of datetime): Extracted date objects.
            - datefinder_count (int): Number of dates found using datefinder.
            - two_digit_pattern_count (int): Number of dates found using two-digit patterns.
            - four_digit_pattern_count (int): Number of dates found using four-digit patterns.

    """
    holiday_patterns = {
    r"new\s*years?(?:\s*day)?": (1, 1),
    r"valentines?(?:\s*day)?": (2, 14),
    r"st\.?\s*patricks?(?:\s*day)?": (3, 17),
    r"april\s*fools?(?:\s*day)?": (4, 1),
    r"easter": (4, 20),  
    r"independence(?:\s*day)?": (7, 4),
    r"halloween": (10, 31),
    r"thanksgiving": (11, 23),  
    r"christmas\s*eve": (12, 24),
    r"christmas\s*": (12, 25),
    r"new\s*years?\s*eve": (12, 31)
    }

    ## Datefinder ##
    # Remove Years < 1620 #
    matched_dates = [date.date() for date in datefinder.find_dates(text, base_date = datetime.datetime(2025, 1, 1)) 
                    if isinstance(date, datetime.datetime) and 1677 < date.year < 2026]
    datefinder_count = len(matched_dates)

    ## REGEX ##
    matched_years = []

    # 2 Digit Pattern eg. "20's" -> "1920's" #

    two_digit_pattern = [r"\b(?:in\s+the\s+)'?(\d{2})\s*'?s\b", # eg. "in the 20's" (in + the) optional
                         r"\b(?:in\s+)?'?(\d{2})\s*'?s\b",  # eg. "in 20 's ("in" optional and optional white spaces)
                         r"\b(?:the\s+)?'?(\d{2})\s*'?s\b"] # eg. "the 20s" ("the" optional, optional white spaces, optional apostrophes)
    for pattern in two_digit_pattern:
        matched_years.extend(
            [re.sub(r"in the|'|s", "", year.lower()).strip() for year in re.findall(pattern, text, re.IGNORECASE)]
        )
    matched_years = ["19" + year for year in matched_years]


    # Century Pattern eg. "20th Century" -> "1900" #

    century_patterns = [r"\b(\d{1,2})(?:st|nd|rd|th)?\s*century\b"] # eg. "3rd century". 

    for pattern in century_patterns:
        matched_centuries = re.findall(pattern, text, re.IGNORECASE)
        for century in matched_centuries:
            matched_years.append(str((int(century)-1) * 100))

    two_digit_pattern_count = len(matched_years)

    # 4 Digit Pattern eg. "in the 1970's" #
    four_digit_pattern = [r"\b(?:in\s+the\s+)(\d{4})(?:\s*'?\s*s)?\b", r"\b(?:in\s+)?(\d{4})(?:\s*'?\s*s)?\b", r"\b(?:the\s+)?(\d{4})(?:\s*'?\s*s)?\b"]

    for pattern in four_digit_pattern:
        matched_years.extend(
            [re.sub(r"in the|'|s", "", year.lower()).strip() for year in re.findall(pattern, text, re.IGNORECASE)]
        )
    four_digit_pattern_count = len(matched_years) - two_digit_pattern_count

    # Holidays #
    for pattern, val in holiday_patterns.items():
        month, day = val
        if check_regex(text, re.compile(pattern, re.IGNORECASE))[0]:
            matched_dates.append(datetime.date(1000, month, day))

    # Add Regex matches to Matched_Dates #
    for year in matched_years:
        matched_dates.append(datetime.date(int(year), 1, 1)) 

    # Remove Duplicates #
    matched_dates = list(set(matched_dates))

    matched_dates = [date for date in matched_dates if not ((date.year == 2025) and (date.day != 1))] # Remove dates of form [2025, 1, x] where x != 1 

    if matched_dates == []: # If No Dates Matched, Return [2025, 1, 1] 
        matched_dates.append(datetime.date(2025, 1, 1))

    res = {
        "dates" : matched_dates,
        "datefinder_count" : datefinder_count,
        "two_digit_pattern_count" : two_digit_pattern_count,
        "four_digit_pattern_count" : four_digit_pattern_count  
    }

    return res

def clean_dates(lst):
    '''
    Clean output from `extract_dates` function.

    Steps:
        1. Remove default date: "datetime.datetime(2025, 1, 1)" if list is longer than length 2. 
        2. Remove duplicate years if there exists another date with the same year. 
    
    Input:
        [lst]     - list of datetime objects

    Returns:
        [None] - Modifies list of dates

    eg. 
    >>> lst = [datetime.date(1970, 1, 1), datetime.date(1970, 3, 1)]
    >>> clean_dates([datetime.date(1970, 1, 1), datetime.date(1970, 1, 1)])
    >>> lst
    [datetime.date(1970, 3, 1)]
    
    '''
    # sort list in date order #
    lst.sort()

    # remove [2025, 1, 1] if list is longer than length 2 #
    if (len(lst) > 1) and (datetime.date(2025,1,1) in lst):
        lst.remove(datetime.date(2025, 1, 1))
    elif (len(lst) > 1) and (datetime.datetime(2025,1,1) in lst):
        lst.remove(datetime.datetime(2025, 1, 1))
    
    # remove duplicate years if month == 1 #
    cleaned_dates = []
    i = 0
    while i < len(lst):
        date = lst[i]
        if date.month == 1:
            curr_year = date.year
            if any(d.year == curr_year for d in lst[i+1:]):
                i += 1
                continue
        cleaned_dates.append(date)
        i += 1
    lst.clear()
    lst.extend(cleaned_dates)

    return cleaned_dates

def classify_hours(text):
    """
    Classify numeric time into time of day categories. 
    Inputs:
        [text]              | string you want to parse   

    Returns:
        [str]               | Time of day (default: "Unknown")
                            | Values: ["Night", "Morning", "Evening", "Afternoon", "Dusk", "Unknown"]
    Steps:
        1. Parse numbers and ordinals to integers using number_parser.parse
        2. split text into sequences and tokens
        3. check if sequence contains "a.m." or "p.m."
            3a. check if previous token is a time of the form "hh:mm", "hh", or "h"
        4. return one of "Night", "Morning", "Evening", "Afternoon", "Dusk", "Unknown"
  
    eg:
    >>> classify_hours("It was 2:00 pm")
    "Afternoon"
    """
    
    # pattern to capture a.m., p.m., and hour
    am_pattern = re.compile(r'^(a\.?m\.?)$', re.IGNORECASE)
    pm_pattern = re.compile(r'^(p\.?m\.?)$', re.IGNORECASE)
    
    # split text into sequences by all periods not adjacent to a.m. or p.m. 
    text = re.sub(r'(?<!a|p)\.(?!m)', ' . ', text)
    text = parse(text)

    tokens = text.lower().split()
    sequences = extractSequences(tokens, ".")
    
    for seq in sequences:

        for i, token in enumerate(seq):

            if am_pattern.match(token):
                # check if previous token is a time of the form "hh:mm", "hh", or "h". 
                prev_token = re.match(r'^([0-1]?\d|2[0-3])(:[0-5]\d)?$', seq[i-1])

                # Convert to int if we have match
                if prev_token:
                    prev_token = int(prev_token.group(1)) 

                    if prev_token < 4:
                        return "Night"
                    
                    elif 4 <= prev_token <= 12:
                        return "Morning"

            elif pm_pattern.match(token):
                prev_token = re.match(r'^([0-1]?\d|2[0-3])(:[0-5]\d)?$', seq[i-1])

                # Convert to int if we have match
                if prev_token:
                    prev_token = int(prev_token.group(1)) 

                    if 1 <= prev_token < 7 or prev_token == 12:
                        return "Afternoon"

                    elif 7 <= prev_token < 10:
                        return "Dusk"

                    elif 10 <= prev_token < 12:
                        return "Evening"
                
    return "Unknown"
                
def classify_time_of_day_v2(text):
    """
    Classify time of day from a piece of text
    
    Inputs:
        [text]              | string you want to parse   

    Returns:
        [res]               | Time of day (default: "Unknown")
                            | Values: ["Night", "Morning", "Evening", "Afternoon", "Dusk", "Unknown"]
    Steps:
        1. run classify_hours and return result if not "Unknown"
        2. run regex check for each time of day category ["Night", "Morning", "Evening", "Afternoon", "Dusk"]
        3. return "Unknown" if all fail
        4. check if sequence contains "a.m." or "p.m."

    eg:
    >>> classify_hours("It was late at night")
    "Evening"
    """

    time_patterns_v2 = {
    # "mornings", "dawns", etc.  #
    "Morning": [r"\bmorning('?s)?[a-z]*\b", r"\bdawn('?s)?\b", r"\bsunrise('?s)?\b"],

    # "evenings", "midnights", etc.  #
    "Evening": [r"\bevening('?s)?\b", r"\bnight('?s)?\b", r"\bmidnight('?s)?\b", r"\bnighttime('?s)?\b", r"\blate('?s)?\b"],

    # "afternoon", "school hours", etc.  #
    "Afternoon": [r"afternoon('?s)?\b", r"\bnoon('?s)?\b", r"\b(?:school|business|work|day|closing|opening|lunch|dinner|daytime)\s*hours?\b", r"\blate('?s)?\b"],

    # "dusks", "susnets", etc. #
    "Dusk": [r"\bdusk('?s)?\b", r"\bsunset('?s)?\b", r"\btwilight('?s)?\b"], 

    # "all day", "entire day", "whole day", "all (of) (the) time" #
    "All Day": [r"\ball\s?(day|hours)('?s)?\b", r"\bentire\s?day('?s)?\b" , r"\bwhole\s?day('?s)?\b", r"\ball\s?(of)?\s?(the)?\s?time('?s)?\b"] 
    
    }


    if not isinstance(text, str):
        return "Unknown"
    
    # run classify hours and check if it found something
    res = classify_hours(text)

    # return result if it is not "Unknown"
    if res != "Unknown":
        return res

    # Iterate through each time of day category
    for label, patterns in time_patterns_v2.items():

        for p in patterns:

            # check if regex matches
            if check_regex(text, re.compile(p, re.IGNORECASE))[0]:

                # return time of day category if match found
                res = label
                return res
    
    return res

def first_person_witness_check(text: str, witness_verbs: dict) -> int:
    '''
    Check sequence for first person witnesses.

    Steps:
    1. Break text into tokens and sequences  
    2. Check first person regex pattern
    3. If found, check rest of sentence for a witness verb
    4. if verb found, return 2 for "we" or 1 for "i"

    Input:
        [text]            - raw text with quantifiers converted to digits
    Returns:
        [witness_counts]  - Number of witnesses
        [witnesses]       - token flagged as witness

    eg: 
    >>> extract_eyewitness_counts("I felt my legs pulled sitting bleachers.")
    1
    '''
    ## Extract sequences
    tokens = text.split()
    sequences = extractSequences(tokens, '.')

    ## Regex checks for "we" and "i"
    pattern = r"\bi\b|\bwe\b" 

    ## Init verb set ##
    verb_set = set(chain(*witness_verbs.values())) 

    ## Iterate through sequences
    for sequence in sequences:
        ## Iterate though tokens in sequence
        for idx, token in enumerate(sequence):
            
            # If "i" or "we" found
            if re.search(pattern, token, re.IGNORECASE):
                try:
                    # Check rest of sentence for overlap 
                    if any(word in verb_set for word in sequence[idx:]):

                        # First person Plural
                        if token == "we":
                            return 2
                        
                        # First person singular
                        elif token == 'i':
                            return 1


                except IndexError:
                    pass
    return 0

def parse_ambiguous_quantifiers(text: str) -> str:
    '''
    Parses Ambiguous quantifiers like "several" and "many" and replaces them with numbers
    
    Input:
        [text]  - raw text
    Returns:
        [text]  - text with quantifiers replaced with numbers
    
    eg: 
    >>> parse_ambiguous("several girls names elizabeth evelyn felt legs pulled sitting bleachers.")
    "3 girls names elizabeth evelyn felt legs pulled sitting bleachers."
    '''

    quantifiers = {
    "2" : ['pair', 'couple'], 
    "3" : ['many', 'several', 'some', 'few', 'group', 'groups']
    }
    
    quantifiers = {word: number for number, words in quantifiers.items() for word in words}

    # Parse Quantifiers #
    tokens = text.split()
    tokens = [quantifiers.get(token, token) for token in tokens]
    return " ".join(tokens)

def extract_eyewitness_counts(text: str, witness_nouns: dict, witness_verbs: dict) -> int:
    '''
    Extract number of witnesses from a block of text using sliding window.

    Input:
        [text]            - raw text with quantifiers converted to digits
    Returns:
        [witness_counts]  - Number of witnesses
        [witnesses]       - token flagged as witness

    Steps:
    1. Tokenize and sequence text
    2. initialize sentence window
    2. Identify Witness-Specific Nouns
    3. If noun found, check next 3 sentences for witness-specific verbs
    4. If verb found, check previous token for quantifier
    5. Increment witness_count, 
        * (+1) for singular
        * (+3) for plural 
        * (+quantifier) if quantifier found
    6. Move sliding window to sentence following witness-verb
    7. loop until final sentence

    eg: 
    >>> extract_eyewitness_counts("2 girls names elizabeth evelyn felt legs pulled sitting bleachers.")
    (2, [['girls', 2]])
    '''
    
    # Extract Tokens and sequences
    tokens = text.replace('.', ' . ').split()
    sequences = extractSequences(tokens, '.')

    ## Compile noun regex ##
    singular_noun_pattern = re.compile(r"\b(" + "|".join(map(re.escape, list(chain(*witness_nouns['Singular'].values())))) + r")\b", re.IGNORECASE)
    plural_noun_pattern = re.compile(r"\b(" + "|".join(map(re.escape, list(chain(*witness_nouns['Plural'].values())))) + r")\b", re.IGNORECASE)
    
    # Quantify Regex
    regex_dict = {
        '1' : singular_noun_pattern,
        '2' : plural_noun_pattern
    }

    ## Compile verb set ##
    verb_set = set(chain(*witness_verbs.values())) 

    ## Initialize results ##
    witnesses = []
    witness_count = 0 
    num_sequences = len(sequences)

    i = 0 
    while i < num_sequences:
        
        starting_sequence = sequences[i]

        # Check First Person Regex #
        first_person_witnesses = first_person_witness_check(" ".join(starting_sequence))
        if first_person_witnesses != 0:
            witness_count += first_person_witnesses
            witnesses.append(['i|we', '1|2'])
            i += 1
            break
        # Check Singular and Plural Patterns #
        for val, regex_pattern, in regex_dict.items():
            
            default_value = int(val)

            # Iterate through each sentence 
            for idx, token in enumerate(starting_sequence):
                if regex_pattern.match(token):

                    # init sliding window and search
                    for j in range(i, min(i + 2, num_sequences)):
                        ending_sequence = sequences[j] 

                        # If verb found, check starting sentence for quantifier
                        if any(word in verb_set for word in ending_sequence):
                            prev_token = starting_sequence[idx -1] if idx > 0 else None

                            # If digit, use as quantifier.        
                            if prev_token and prev_token.isdigit() and int(prev_token) < 16: # Filter quantifiers over 15
                                count = int(prev_token)
                            # If no quantifier, use default_value 
                            else:
                                count = default_value

                            witness_count += count
                            witnesses.append([token,count])
                            i = min(j+1, num_sequences)
                            break

                    break # Break noun loop after first verb match

        i += 1 # Move to next sentence if no witness was added

    return witness_count, witnesses

def recompile_regex(pattern):
    '''
    Recompile regex patterns in `keywords.json`.
    Supports lists, strings, and tuples.

        Input:
        [pattern]            - regex pattern stored as string.
    Returns:
        [res]                - recompiled regex object.
    '''
    if isinstance(pattern, str):
        return re.compile(rf"\b{pattern}\b", re.IGNORECASE)

    elif isinstance(pattern, tuple):
        return tuple(recompile_regex(x) for x in pattern)

    elif isinstance(pattern, list) and all(isinstance(p, str) for p in pattern) and len(pattern) > 1:
        return tuple(recompile_regex(p) for p in pattern)
    
    elif isinstance(pattern, list):
        return [recompile_regex(x) for x in pattern]
    
def match_groups(text, event_groups):
    '''
    Classify "Event_Type" from raw text using `check_regex` function.

    Input:
        [text]                   - Raw Text
        [groups]                 - Dictionary of groups {group: [regex_patterns]}
    Returns:
        [group1|group2|...]      - matching groups separated by "|". (Default: "Unkown")

    Steps:
    1. Iterate through each event group and their respective regex patterns
    2. return matched event groups. 
    '''
    if not isinstance(text, str):
        return "Unknown"

    triggered_groups = set()

    # Check every keyword in every group
    for group, patterns in event_groups.items():
        for pattern in patterns:

            if check_regex(text, pattern)[0]:
                triggered_groups.add(group)
                break

    if not triggered_groups:
        return "Unknown"

    # Return all matched groups
    return " | ".join(sorted(triggered_groups))