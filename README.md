# Book of Mormon Stylometry

There have been a few stylometric studies on the Book of Mormon (for and against)
- [Book of Mormon Stylometry in Pictures and Tables](https://rationalfaiths.com/book-of-mormon-stylometry-in-pictures-and-tables/), 2016, Rational Faiths
- [Stylometric Analyses of the Book of Mormon: A Short History](https://scholarsarchive.byu.edu/cgi/viewcontent.cgi?article=1492&context=jbms), 2012, Journal of Book of Mormon Studies
- [Book of Mormon Authorship: New Light on Ancient Origins](https://scholarsarchive.byu.edu/cgi/viewcontent.cgi?article=1014&context=mi), 1996, Maxwell Institute Publications
- [A Stylometric Analysis of Mormon Scripture and Related Texts](https://www.physics.smu.edu/scalise/P3333sp08/ScienceReligion/MormonStylometric.pdf), 1992, Journal of the Royal Statistical Society

However I'm unaware of any accessible project that anyone can view the sources, download, and tweak the variables or fine tune the data (spelling).

# Data

Goal of 5,000+ (6,500+) words per author for comparison.

## Comparison Data
Format of `Known author: work (word count)`

### From Book of Mormon (267k)w
- Nephi
- Mormon
- Moroni
- Jacob

### Non Book of Mormon

- Bible: King James Version (793k)
- Isaiah: King James Version (37k)
- Joseph Smith:
  - 1833 Letter to Church Leaders (2.2k)
  - 1839 Letter to Emma Smith (1k)
  - 1842 Wentworth Letter (2.9k)
- Ethan Smith: View of the Hebrews (47k)
- Eliakim: The First Book of Napolean (18k)
- Solomon Spalding: Manuscript Found (39k)
- Oliver Cowdery: TODO
- Sidney Rigdon: TODO
- Parley Pratt: TODO
- Henry Longfellow: TODO
- Jane Austin: TODO
- Charles Dickens: TODO
- Mark Twain: TODO
- James Fennimore Cooper: TODO


# Setup

`pip install nltk pandas numpy scikit-learn faststylometry matplotlib`

# Run

`py ./sylometric.py`

If you want the graphs of basic stylometrics remove the comments (`"""`) surrounding the blocks

# Foundation Stylometry Info/Reference
- https://guides.temple.edu/stylometryfordh
- https://programminghistorian.org/en/lessons/introduction-to-stylometry-with-python#introduction