"""Typing test implementation"""

from utils import lower, split, remove_punctuation, lines_from_file
from ucb import main, interact, trace
from datetime import datetime


###########
# Phase 1 #
###########


def choose(paragraphs, select, k):
    """Return the Kth paragraph from PARAGRAPHS for which SELECT called on the
    paragraph returns true. If there are fewer than K such paragraphs, return
    the empty string.
    """
    # BEGIN PROBLEM 1
    paragraphs = [x for x in paragraphs if select(x) == True]
    if len(paragraphs) - 1 < k:
        return ''
    return paragraphs[k]
    # END PROBLEM 1


def about(topic):
    """Return a select function that returns whether a paragraph contains one
    of the words in TOPIC.

    >>> about_dogs = about(['dog', 'dogs', 'pup', 'puppy'])
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup!'], about_dogs, 0)
    'Cute Dog!'
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup.'], about_dogs, 1)
    'Nice pup.'
    """
    assert all([lower(x) == x for x in topic]), 'topics should be lowercase.'
    # BEGIN PROBLEM 2
    def word_checker(x):
        x = split(lower(remove_punctuation(x)))
        for element in x:
            for element_2 in topic:
                if element == element_2:
                    return True
        return False
    return word_checker
    # END PROBLEM 2


def accuracy(typed, reference):
    """Return the accuracy (percentage of words typed correctly) of TYPED
    when compared to the prefix of REFERENCE that was typed.

    >>> accuracy('Cute Dog!', 'Cute Dog.')
    50.0
    >>> accuracy('A Cute Dog!', 'Cute Dog.')
    0.0
    >>> accuracy('cute Dog.', 'Cute Dog.')
    50.0
    >>> accuracy('Cute Dog. I say!', 'Cute Dog.')
    50.0
    >>> accuracy('Cute', 'Cute Dog.')
    100.0
    >>> accuracy('', 'Cute Dog.')
    0.0
    """
    typed_words = split(typed)
    reference_words = split(reference)
    # BEGIN PROBLEM 3
    correct_words = 0
    start = len(typed_words)
    while len(typed_words) >= 1 and len(reference_words) > 0:
        if typed_words[0] == reference_words[0] and len(reference_words) > 1:
            correct_words += 1
            typed_words , reference_words = typed_words[1:] , reference_words[1:]
        elif typed_words[0] != reference_words[0] and len(reference_words) > 1:
            typed_words , reference_words = typed_words[1:] , reference_words[1:]
        elif len(reference_words) == 1:
            if typed_words[0] == reference_words[0]:
                correct_words += 1
            typed_words = []
    if start == 0:
        return 0.0
    return (correct_words/start)*100


    # END PROBLEM 3


def wpm(typed, elapsed):
    """Return the words-per-minute (WPM) of the TYPED string."""
    assert elapsed > 0, 'Elapsed time must be positive'
    # BEGIN PROBLEM
    characters = len(typed)
    return (characters/5)/(elapsed/60)
    # END PROBLEM 4

def autocorrect(user_word, valid_words, diff_function, limit):
    """Returns the element of VALID_WORDS that has the smallest difference
    from USER_WORD. Instead returns USER_WORD if that difference is greater
    than LIMIT.
    """
    # BEGIN PROBLEM 5
    limits = {x:diff_function(user_word,x,limit) for x in valid_words}
    min_value = min(limits.values())
    for element in valid_words:
        if element == user_word:
            return user_word
    if min_value <= limit:
        for x in valid_words:
            if limits[x] == min_value:
                return x
    return user_word
    # END PROBLEM 5


def shifty_shifts(start, goal, limit):
    """A diff function for autocorrect that determines how many letters
    in START need to be substituted to create GOAL, then adds the difference in
    their lengths.
    """
    # BEGIN PROBLEM 6
    def helper(start, goal, a):
        if a > limit:
            return limit
        if len(start) == 0 and len(goal) == 0:
            return 0
        elif len(start) == 1 or len(goal) == 1:
            if len(start) == 1:
                if start[0] == goal[0]:
                    return helper([],[],a + len(goal) - 1) + (len(goal)-1)
                else:
                    return helper([],[],a + len(goal)) + len(goal)
            if len(goal) == 1:
                if start[0] == goal[0]:
                    return helper([],[],a + len(start) - 1) + (len(start)-1)
                else:
                    return helper([],[],a + len(start)) + len(start)
        else:
            if start[0] == goal[0]:
                return helper(start[1:],goal[1:],a)
            else:
                return helper(start[1:],goal[1:],a + 1) + 1
    return helper(start , goal, 0)
    # END PROBLEM 6


def pawssible_patches(start, goal, limit):
    """A diff function that computes the edit distance from START to GOAL."""
    if limit < 0:
        return limit + 1
    elif start == goal:
        return 0
    elif len(start) == 0 or len(goal) == 0:
        if len(start) == 0:
            return pawssible_patches('finished' , 'finished' , limit - len(goal)) + len(goal)
        else:
            return pawssible_patches('finished' , 'finished' , limit - len(start)) + len(start)
    elif start[0] == goal[0]:
        return pawssible_patches(start[1:],goal[1:],limit)
    else:
        add_diff = pawssible_patches(goal[0] + start, goal, limit - 1) + 1
        remove_diff = pawssible_patches(start[1:], goal, limit - 1) + 1
        substitute_diff = pawssible_patches(goal[0] + start[1:], goal, limit - 1) + 1
    return min(add_diff , remove_diff , substitute_diff)


def final_diff(start, goal, limit):
    """A diff function. If you implement this function, it will be used."""
    assert False, 'Remove this line to use your final_diff function'


###########
# Phase 3 #
###########


def report_progress(typed, prompt, user_id, send):
    """Send a report of your id and progress so far to the multiplayer server."""
    # BEGIN PROBLEM 8
    i = 0
    original_length =  len(prompt)
    print_progress = lambda d: print('ID:', d['id'], 'Progress:', d['progress'])
    while i < len(typed):
        if typed[i] == prompt[i]:
            i += 1
        else:
            value = i/original_length
            print_progress({'id': user_id, 'progress': value})
            return value
    value = i/original_length
    print_progress({'id': user_id, 'progress': value})
    return value
    # END PROBLEM 8


def fastest_words_report(times_per_player, words):
    """Return a text description of the fastest words typed by each player."""
    game = time_per_word(times_per_player, words)
    fastest = fastest_words(game)
    report = ''
    for i in range(len(fastest)):
        words = ','.join(fastest[i])
        report += 'Player {} typed these fastest: {}\n'.format(i + 1, words)
    return report


def time_per_word(times_per_player, words):
    """Given timing data, return a game data abstraction, which contains a list
    of words and the amount of time each player took to type each word.

    Arguments:
        times_per_player: A list of lists of timestamps including the time
                          the player started typing, followed by the time
                          the player finished typing each word.
        words: a list of words, in the order they are typed.
    """
    # BEGIN PROBLEM 9
    for element in times_per_player:
        i = 0
        while i + 1 < len(element):
            element[i] = element[i+1] - element[i]
            i += 1
        element = element[0:len(element)-1]
        times_per_player = times_per_player[1:] + [element]
    return game(words, times_per_player)
    # END PROBLEM 9


def fastest_words(game):
    """Return a list of lists of which words each player typed fastest.

    Arguments:
        game: a game data abstraction as returned by time_per_word.
    Returns:
        a list of lists containing which words each player typed fastest
    """
    player_indices = range(len(all_times(game)))  # contains an *index* for each player
    word_indices = range(len(all_words(game)))    # contains an *index* for each word
    # BEGIN PROBLEM 10
    player_count = len(all_times(game))
    word_count = len(all_words(game))
    p_list = []
    w_index = 0
    while w_index < word_count:
        p_index = 0
        fastest_time = 100
        fastest_player = -1
        while p_index < player_count:
            if time(game, p_index, w_index) < fastest_time:
                fastest_time = time(game, p_index, w_index)
                fastest_player = p_index
            p_index += 1
        p_list = p_list + [[w_index,fastest_player]]
        w_index += 1
    p_index = 0
    small_list, real_list = [],[]
    while p_index <=player_count:
        w_index = 0
        while w_index < word_count:
            if p_index == p_list[w_index][1]:
                small_list = small_list + [word_at(game, w_index)]
            w_index += 1
        real_list = real_list + [small_list]
        p_index += 1
        small_list = []
    return real_list[0:len(real_list)-1]
    # END PROBLEM 10


def game(words, times):
    """A data abstraction containing all words typed and their times."""
    assert all([type(w) == str for w in words]), 'words should be a list of strings'
    assert all([type(t) == list for t in times]), 'times should be a list of lists'
    assert all([isinstance(i, (int, float)) for t in times for i in t]), 'times lists should contain numbers'
    assert all([len(t) == len(words) for t in times]), 'There should be one word per time.'
    return [words, times]


def word_at(game, word_index):
    """A selector function that gets the word with index word_index"""
    assert 0 <= word_index < len(game[0]), "word_index out of range of words"
    return game[0][word_index]


def all_words(game):
    """A selector function for all the words in the game"""
    return game[0]


def all_times(game):
    """A selector function for all typing times for all players"""
    return game[1]


def time(game, player_num, word_index):
    """A selector function for the time it took player_num to type the word at word_index"""
    assert word_index < len(game[0]), "word_index out of range of words"
    assert player_num < len(game[1]), "player_num out of range of players"
    return game[1][player_num][word_index]


def game_string(game):
    """A helper function that takes in a game object and returns a string representation of it"""
    return "game(%s, %s)" % (game[0], game[1])

enable_multiplayer = False  # Change to True when you're ready to race.

##########################
# Command Line Interface #
##########################


def run_typing_test(topics):
    """Measure typing speed and accuracy on the command line."""
    paragraphs = lines_from_file('data/sample_paragraphs.txt')
    select = lambda p: True
    if topics:
        select = about(topics)
    i = 0
    while True:
        reference = choose(paragraphs, select, i)
        if not reference:
            print('No more paragraphs about', topics, 'are available.')
            return
        print('Type the following paragraph and then press enter/return.')
        print('If you only type part of it, you will be scored only on that part.\n')
        print(reference)
        print()

        start = datetime.now()
        typed = input()
        if not typed:
            print('Goodbye.')
            return
        print()

        elapsed = (datetime.now() - start).total_seconds()
        print("Nice work!")
        print('Words per minute:', wpm(typed, elapsed))
        print('Accuracy:        ', accuracy(typed, reference))

        print('\nPress enter/return for the next paragraph or type q to quit.')
        if input().strip() == 'q':
            return
        i += 1


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions."""
    import argparse
    parser = argparse.ArgumentParser(description="Typing Test")
    parser.add_argument('topic', help="Topic word", nargs='*')
    parser.add_argument('-t', help="Run typing test", action='store_true')

    args = parser.parse_args()
    if args.t:
        run_typing_test(args.topic)
