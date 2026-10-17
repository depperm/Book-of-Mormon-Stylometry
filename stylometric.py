import nltk
nltk.download('punkt')
import matplotlib.pyplot as plt
import math
#nltk.download('punkt_tab')
#%matplotlib inline

bom_books = {
    'Nephi': [1,2], # 1 Nephi, 2 Nephi
    'Jacob': [3],
    'Enos': [4],
    'Jarom': [5],
    'Omni': [6], # Omni...short with a bunch of authors
    'Mormon': [7,8,9,10,11,12,13], # Words of Mormon, Mosiah, Alma, Helaman, 3 Nephi, 4 Nephi
    'Moroni': [14,15] # Mormon chapter 7,8 added to Ether, also Moroni
}
joseph_smith = [1,2,3]
plagiarism_books = {
    'Solomon Spalding': [1], # Manuscript Found
    'Eliakim': [2], # The First Book of Napoleon
    'Ethan Smith': [3], # View of the Hebrews
}
# based mainly on Traditional attribution
# some of the included books are probably too short to be useful for stylometric analysis, but I have included them for completeness and because I've never done stylometrics and think it might be interesting
# I have omitted some books that are not attributed to a single author or many proposals:
#   Judges, Ruth, Kings, Chronicles, Jonah
bible_books = {
    'Moses': [1,2,3,4,5, 10], # torah, job
    'Joshua': [6],
    'Ezra': [7],
    'Nehemiah': [8],
    'Mordecai': [9],
    'King David': [11],
    'King Solomon': [12, 13, 14],# proverbs, ecclesiastes, song of solomon
    'Isaiah': [15],
    'Jeremiah': [16, 17], # jeremiah, lamentations
    'Ezekiel': [18],
    'Daniel': [19],
    'Hosea': [20],
    'Joel': [21],
    'Amos': [22],
    'Obadiah': [23],
    'Michah': [24],
    'Nahum': [25],
    'Habakkuk': [26],
    'Zephaniah': [27],
    'Haggai': [28],
    'Zechariah': [29],
    'Malachi': [30],
    'Matthew': [31],
    'Mark': [32],
    'Luke': [33, 35], # luke, acts
    'John': [34, 53, 54, 55, 57], # john, 1 john, 2 john, 3 john, revelation
    'Paul': [36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48], # romans, corinthians, galatians, ephesians, philippians, colossians, thessalonians, timothy, titus, philemon
    'Hebrews': [49],
    'James': [50],
    'Peter': [51, 52], # 1 peter, 2 peter
    'Jude': [56]
}
other_books = {
    'Jane Austin': [1], # Sense and Sensibility
    'Charles Dickens': [2], # Oliver Twist
    'Mark Twain': [3], # The Adventures of Tom Sawyer
    'James Fenimore Cooper': [4], # The Last of the Mohicans
    'Henry Wadsworth Longfellow': [5] # The Song of Hiawatha
}
js_acquaintances = {
    'Oliver Cowdery': [1,2],
    'Parley P. Pratt': [],
    'Sidney Rigdon': [],
}

def read_files_into_string(filenames, section='BookOfMormon', prefix='bom'):
    strings = []
    for filename in filenames:
        with open(f'data/{section}/{prefix}_{filename}.txt', 'r', encoding='utf-8') as f:
            strings.append(f.read())
    return '\n'.join(strings)

writings_by_author = {}
for author, files in bom_books.items():
    writings_by_author[author] = read_files_into_string(files)

for author, files in bible_books.items():
    writings_by_author[author] = read_files_into_string(files, 'KJV', prefix='bible')

for author, files in plagiarism_books.items():
    writings_by_author[author] = read_files_into_string(files, 'PlagarismSource', prefix='book')

for author, files in other_books.items():
    writings_by_author[author] = read_files_into_string(files, 'OtherBooks', prefix='book')

writings_by_author['Joseph Smith'] = read_files_into_string(joseph_smith, section='JosephSmith', prefix='doc')

# test read of files:
#for author in writings_by_author.keys():
#    print(author, ':',writings_by_author[author][:100])
#print()

###################################################
#
# Mendenhall's Characteristic Curves of Composition
#
###################################################

authors = ('Nephi', 'Jacob', 'Enos', 'Jarom', 'Omni', 'Mormon', 'Moroni', 'Joseph Smith', 'Solomon Spalding', 'Eliakim', 'Ethan Smith', 'Isaiah', 'Paul','Moses')

# transform the author's writings into lists of word tokens
writings_by_author_tokens = {}
writings_by_author_length_distributions = {}
for author in authors:
    tokens = nltk.word_tokenize(writings_by_author[author])

    # filter out punctuation and non-alphabetic tokens
    writings_by_author_tokens[author] = ([token for token in tokens if any(c.isalpha() for c in token)])
    
    # get a distribution of token lengths
    token_lengths = [len(token) for token in writings_by_author_tokens[author]]
    writings_by_author_length_distributions[author] = nltk.FreqDist(token_lengths)

    #fd = writings_by_author_length_distributions[author]
    #fd.plot(15, title=author)
    #plt.show()  # shows multiple graphs one after the other
"""
# comparison
plt.figure()
for author, fd in writings_by_author_length_distributions.items():
    # frequencies = [count for _, count in fd.most_common(15)]
    # normalize the frequency of word based on total words of author
    total_words = fd.N()
    frequencies = [count/total_words * 100 for _, count in fd.most_common(15)]

    ranks = range(1, len(frequencies) + 1)
    plt.plot(ranks, frequencies, marker='o', label=author)
plt.xlabel("Rank")
plt.ylabel("Frequency")
plt.legend()
plt.show()
"""
###################################################
#
# Kilgariff's Chi-Squared Method
#
###################################################
authors = ('Joseph Smith', 'Solomon Spalding', 'Eliakim', 'Ethan Smith', 'Isaiah')
"""
for author in authors:
    writings_by_author_tokens[author]= ([token.lower() for token in writings_by_author_tokens[author]])
#for author in ('Nephi', 'Jacob', 'Enos', 'Jarom', 'Omni', 'Mormon', 'Moroni'):
writings_by_author_tokens['Disputed']= ([token.lower() for token in writings_by_author_tokens['Mormon']])


# Calculate chisquared for each of the candidate authors
for author in authors:

    # First, build a joint corpus and identify the 500 most frequent words in it
    joint_corpus = (writings_by_author_tokens[author] +
                    writings_by_author_tokens["Disputed"])
    joint_freq_dist = nltk.FreqDist(joint_corpus)
    most_common = list(joint_freq_dist.most_common(500))

    # What proportion of the joint corpus is made up
    # of the candidate author's tokens?
    author_share = (len(writings_by_author_tokens[author])
                    / len(joint_corpus))

    # Now, let's look at the 500 most common words in the candidate
    # author's corpus and compare the number of times they can be observed
    # to what would be expected if the author's papers
    # and the Disputed papers were both random samples from the same distribution.
    chisquared = 0
    for word,joint_count in most_common:

        # How often do we really see this common word?
        author_count = writings_by_author_tokens[author].count(word)
        disputed_count = writings_by_author_tokens["Disputed"].count(word)

        # How often should we see it?
        expected_author_count = joint_count * author_share
        expected_disputed_count = joint_count * (1-author_share)

        # Add the word's contribution to the chi-squared statistic
        chisquared += ((author_count-expected_author_count) *
                       (author_count-expected_author_count) /
                       expected_author_count)

        chisquared += ((disputed_count-expected_disputed_count) *
                       (disputed_count-expected_disputed_count)
                       / expected_disputed_count)

    print("The Chi-squared statistic for candidate", author, "(v Mormon) is", chisquared)
"""
###################################################
#
# John Burrows' Delta Method
#
###################################################
authors = ('Joseph Smith', 'Solomon Spalding', 'Eliakim', 'Ethan Smith', 'Isaiah', 'Paul', 'Moses')

for author in authors:
    writings_by_author_tokens[author] = [tok.lower() for tok in writings_by_author_tokens[author]]

whole_corpus = []
for author in authors:
    whole_corpus += writings_by_author_tokens[author]

whole_corpus_freq_dist = list(nltk.FreqDist(whole_corpus).most_common(30))
#print(whole_corpus_freq_dist[ :10])

features = [word for word,_ in whole_corpus_freq_dist]
feature_freqs = {}

for author in authors:
    feature_freqs[author] = {}

    tokens = list(writings_by_author_tokens[author])
    overall = len(tokens)

    for feature in features:
        presence = tokens.count(feature)
        if overall == 0:
            feature_freqs[author][feature] = 0
        else:
            feature_freqs[author][feature] = presence/overall


corpus_features = {}
for feature in features:
    corpus_features[feature] = {}

    feature_avg = 0
    for author in authors:
        feature_avg += feature_freqs[author][feature]
    feature_avg /= len(authors)
    corpus_features[feature]['Mean'] = feature_avg

    feature_stdev = 0
    for author in authors:
        diff = feature_freqs[author][feature] - corpus_features[feature]['Mean']
        feature_stdev += diff*diff
    feature_stdev /= (  len(authors)-1)
    feature_stdev = math.sqrt(feature_stdev)
    corpus_features[feature]['StdDev'] = feature_stdev

feature_zscores = {}
for author in authors:
    feature_zscores[author] = {}

    for feature in features:
        feature_val = feature_freqs[author][feature]
        feature_mean = corpus_features[feature]['Mean']
        feature_stdev = corpus_features[feature]['StdDev']
        if feature_stdev == 0:
            feature_zscores[author][feature] = 0
        else:
            feature_zscores[author][feature] = (feature_val - feature_mean) / feature_stdev


testcase_tokens  = nltk.word_tokenize(writings_by_author['Nephi'])

testcase_tokens  = [token.lower() for token in testcase_tokens if any(c.isalpha() for c in token)]

overall = len(testcase_tokens)
testcase_freqs  = {}

for feature in features:
    presence = testcase_tokens.count(feature)
    testcase_freqs[feature] = presence/overall

testcase_zscores = {}
for feature in features:
    feature_val = testcase_freqs[feature]
    feature_mean = corpus_features[feature]['Mean']
    feature_stdev = corpus_features[feature]['StdDev']
    if feature_stdev == 0:
        testcase_zscores[feature] = 0
    else:
        testcase_zscores[feature] = (feature_val - feature_mean) / feature_stdev
    #print("Test case z-score for feature '", feature, "' is", testcase_zscores[feature])

for author in authors:
    delta = 0
    for feature in features:
        delta += math.fabs((testcase_zscores[feature] - feature_zscores[author][feature]))

    delta /= len(features)
    print("The Delta statistic for candidate", author, "(v Nephi) is", delta)
