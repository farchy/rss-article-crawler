#! /usr/bin/env python

import sys
import re
import chardet

def asUnicode(text):
    if text is unicode:
        return text

    else:
        try:
            return unicode(text, 'ISO 8859-8')
#            return text.decode('ISO 8859-8')
        except UnicodeDecodeError:
            try:
                return unicode(text, 'ascii')
#                return text.decode('ascii')
            except UnicodeDecodeError:
                try:
                    return unicode(text, 'utf-8')
#                    return text.decode('utf-8')
                except UnicodeDecodeError:
                    print "ERROR: could not infer text encoding"
                    return unicode(text, chardet.detect(text).get('encoding'))

def countOccurrences(text="", keywords=[], foundTerms = {}):#, maxLength=1):
    if not text or not keywords:
        return None

#    termWindow = []
#    foundTerms = {}

    lowerText = text.lower()
    found = 0

    for term in keywords:
        currTerm = " " + term + " "
        if currTerm in lowerText or lowerText.startswith(term) or lowerText.endswith(term):
            found += 1
            if (term in foundTerms):
                foundTerms[term] = foundTerms[term] + 1
            else:
                foundTerms[term] = 1

    return [foundTerms, found]

def cleanText(text=""):
    """
    Cleans a given string from non-alphanumeric characters.
    """
    return re.sub(r'[^\w]', ' ', text)

def splitSentences(text=""):
    return text.replace("!", ". ").replace("?", ". ").split(". ")

def main(argv):
    text = """Later, a 21-year-old woman, Tugba Altinkaynak, was rescued after being trapped beneath rubble for some 27-hours. There was no immediate information on her condition. Her father, Nevzat, said she was at a family lunch with 12 other relatives when the temblor hit. Four of them were pulled out alive earlier.
As over 200 aftershocks rocked the area, rescuers searched mounds of debris for the missing and tearful families members waited anxiously nearby. Cranes and other heavy equipment lifted slabs of concrete, allowing residents to dig for the missing with shovels. Generator-powered floodlights ran all night so the rescues could continue.
Aid groups scrambled to set up tents, field hospitals and kitchens to help the thousands left homeless or too afraid to re-enter their homes. Many exhausted residents spent the night outside, lighting fires to keep warm.
We stayed outdoors all night, I could not sleep at all, my children, especially the little one, was terrified," said Serpil Bilici of her six-year-old daughter, Rabia. "I grabbed her and rushed out when the quake hit, we were all screaming.
The bustling, larger city of Van, about 55 miles (90 kilometers) south of Ercis, also sustained substantial damage, but Interior Minister Idris Naim Sahin said search efforts there were winding down.
Sahin expected the death toll in Ercis to rise, but not as much as initially feared. He told reporters rescue teams were searching for survivors in the ruins of 47 buildings where dozens could be trapped, including a cafe."""
    keywords = ["tugba", "tugba altinkaynak", "ercis", "van"]
    print("unigrams -")
    print countOccurrences(cleanText(text), keywords)[0]
    print("bigrams -")
    print countOccurrences(cleanText(text), keywords)[0]#, 2)
    print("sentences -")
    print(splitSentences(text))

if __name__ == "__main__":
    main(sys.argv)

