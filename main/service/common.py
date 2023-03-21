def compile_tags(str_tags, option='null'):

    # Define the words to remove as a list
    words_to_remove = ["'", "[", "]", " "]

    # Remove the words using replace()
    for word in words_to_remove:
        str_tags = str_tags.replace(word, "")

    if(option == 'split'):
        str_tags = str_tags.split(',');    

    return str_tags