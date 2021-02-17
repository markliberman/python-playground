#
# Compares two text files (file1.txt and file2.txt) and scores their similarity between 0 (no-similarity) and 1 (identical)
# Note: cannot include sys or getopt libraries to read command-line arguments
#

class textCompare():
    # commonwords are all lower case
    commonWords = ["is", "a", "of", "an", "to", "with", "the", "and", "any", "if", "you", "for", "on"]
    punctuation = [".", "?", ",", "!"]
    precision = 2
    minPhraseLength = 3
    maxPhraseLength = 5

    def removePunctuation(self, sample: str):
      sample = ''.join(ch for ch in sample if ch not in self.punctuation)
      return sample

    def removeCommonWords(self, words: [str]):
      words = [item for item in words if item not in self.commonWords]
      return words

    # Returns an list of lower case words from the sample.  Duplicates included
    def getLowerCaseWords(self, sample):
      sample = self.removePunctuation(sample)
      words = sample.split()
      words = [each_string.lower() for each_string in words]
      return words

    def extractWords(self, sample: str):
      wordsDict = {}
      words = self.getLowerCaseWords(sample)
      # For individual word comparison lets remove common words
      words = self.removeCommonWords(words)

      for i in range(len(words)):
        if words[i] in wordsDict:
          wordsDict[words[i]] += 1
        else:
          wordsDict[words[i]] = 1

      return wordsDict

    def getAllElements(self, dict1, dict2):
      mergedDict = {**dict1, **dict2}
      keysList = list(mergedDict.keys())
      return keysList

    def compareDictionaries(self, dict1, dict2):
      distinctElements = self.getAllElements(dict1, dict2)
      distinctItems = 0
      commonItems = 0
      for i in range(len(distinctElements)):
        key = distinctElements[i]
        if key in dict1 and key in dict2:
          if dict1[key] == dict2[key]:
            # same item used same number of times. Increment numerator and denominator
            commonItems += dict1[key]
            distinctItems += dict1[key]
          else:
            # e.g. used 1 time in sample1 2 in sample2 ... 1/2
            commonItems += abs(dict1[key] - dict2[key])
            if dict1[key] > dict2[key]:
              distinctItems += dict1[key]
            else:
              distinctItems += dict2[key]
        elif key in dict1:
            # only in dict1
            distinctItems += dict1[key]
        else:
          distinctItems += dict2[key]

      print("commonItems: ", commonItems, "distinctItems: ", distinctItems)
      return commonItems/distinctItems

    def createListOfSentences(self, sample):
      sentenceTerminators = [".","!","?"]
      # Parse on any of ., !, ? and create a list of sentences
      for i in range(len(sentenceTerminators)):
        sample = sample.replace(sentenceTerminators[i],"|")
      sample = sample.replace("| ", "|")
      sentences = sample.lower().split('|')
      # Remove empty list element after last punctuation mark
      sentences.remove('')
      return sentences

    def extractSentences(self, sample):
      sentencesDict = {}
      sentences = self.createListOfSentences(sample)
      for i in range(len(sentences)):
        if sentences[i] in sentencesDict:
          sentencesDict[sentences[i]] += 1
        else:
          sentencesDict[sentences[i]] = 1
      return sentencesDict

    def createListOfPhrases(self, sample, phraseLength):
      phrases = []
      words = self.getLowerCaseWords(sample)
      for i in range(len(words) - phraseLength + 1):
        phrase = words[i];
        for j in range(1, phraseLength):
          phrase += " " + words[i+j]
        phrases.append(phrase)

      return phrases

    def extractPhrases(self, sample, phraseLength):
      phrasesDict = {}
      phrases = self.createListOfPhrases(sample, phraseLength)
      for i in range(len(phrases)):
        if phrases[i] in phrasesDict:
          phrasesDict[phrases[i]] += 1
        else:
          phrasesDict[phrases[i]] = 1
      return phrasesDict

    def compareCommonWords(self, sample1, sample2):
      wordsDict1 = self.extractWords(sample1)
      wordsDict2 = self.extractWords(sample2)
      result = round(self.compareDictionaries(wordsDict1, wordsDict2), self.precision)
      return result

    def compareSentences(self, sample1, sample2):
      sentenceDict1 = self.extractSentences(sample1)
      sentenceDict2 = self.extractSentences(sample2)
      result = round(self.compareDictionaries(sentenceDict1, sentenceDict2), self.precision)
      return result

    def comparePhrases(self, sample1, sample2):
      result = 0
      for i in range(self.minPhraseLength, self.maxPhraseLength + 1):
        phrasesDict1 = self.extractPhrases(sample1, i)
        phrasesDict2 = self.extractPhrases(sample2, i)
        result += self.compareDictionaries(phrasesDict1, phrasesDict2)

      result = round(result / (self.maxPhraseLength - self.minPhraseLength + 1), self.precision)
      return result

def main():
    with open('file1.txt', 'r') as file:
      sample1 = file.read().replace('\n', '')

    with open('file2.txt', 'r') as file:
      sample2 = file.read().replace('\n', '')

    if sample1 == sample2:
      print("The samples are identical")
      result = 1
    else:
      # First compare frequency of word usage
      tc = textCompare()
      wordResult = tc.compareCommonWords(sample1, sample2)
      print("wordResult: ", wordResult)

      # Then compare freqency of entire sentence reuse
      sentenceResult = tc.compareSentences(sample1, sample2)
      print("sentenceResult: ", sentenceResult)

      # Then compare freqency of phrases between
      phraseResult = tc.comparePhrases(sample1, sample2)
      print("phraseResult: ", phraseResult)

      result = (wordResult + sentenceResult + phraseResult) / 3

    print("File comparison result: ", round(result, 2))

if __name__ == "__main__":
    main()
