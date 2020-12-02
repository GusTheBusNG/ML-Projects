import math

def cleanText(text):
  text = text.lower()
  text = text.strip()
  for chars in text:
    if chars in """[]!.,"-!-@;':#$%^&*()+/?""":
      text = text .replace(chars, " ")

  return text

def countWords(words, isSpam, counted):
  for word in words:
    if word in counted:
      if isSpam == 1:
        counted[word][1] = counted[word][1] + 1
      else:
        counted[word][0] = counted[word][0] + 1
    else:
      if isSpam == 1:
        counted[word] = [0, 1]
      else:
        counted[word] = [1, 0]
  
  return counted

def makePercent(k, counted, spams, hams):
  for key in counted:
    counted[key][0] = (counted[key][0] + k) / (2 * k + hams)
    counted[key][1] = (counted[key][1] + k) / (2 * k + spams)

  return counted

def getData(file):
  line = file.readline()
  spam = 0
  ham = 0
  counted = dict()
  while line != "":
    isSpam = int(line[:1])
    if isSpam == 1:
      spam = spam + 1
    elif isSpam == 0:
      ham = ham + 1
    line = cleanText(line[1:])
    words = line.split()
    words = set(words)
    counted = countWords(words, isSpam, counted)
    
    line = file.readline()
  return (makePercent(1, counted, spam, ham), ham, spam)

def cleanoutStops(vocab, stopFile):
  stopWord = stopFile.readline()
  while stopWord != "":
    stopWord = cleanText(stopWord)
    vocab.pop(stopWord, None)
    stopWord = stopFile.readline()

  return vocab

def getTestData(file):
  line = file.readline()
  testData = []
  while line != "":
    isSpam = int(line[:1])
    line = cleanText(line[1:])
    words = line.split()
    words = set(words)
    testData.append([words, isSpam])

    line = file.readline()

  return testData

def getProb(vocab, testData):
  hamProb = []
  spamProb = []
  for test in testData:
    hamTotal = 1
    spamTotal = 1
    for word in vocab:
      if word in test[0]:
        hamTotal = hamTotal * vocab[word][0]
        spamTotal = spamTotal * vocab[word][1]
      else:
        hamTotal = hamTotal * (1 - vocab[word][0])
        spamTotal = spamTotal * (1 - vocab[word][1])
    hamProb.append(hamTotal)
    spamProb.append(spamTotal)

  return (hamProb, spamProb)
    
def compare(testData, hamProbs, spamProbs, hamTotal, spamTotal):
  tp = 0
  fp = 0
  tn = 0
  fn = 0

  hamProbTotal = hamTotal / (hamTotal + spamTotal)
  spamProbTotal = spamTotal / (hamTotal + spamTotal)
  for test, hamProb, spamProb in zip(testData, hamProbs, spamProbs):
    prob = 1 / (1 + math.exp(math.log(hamProb * hamProbTotal) - math.log(spamProb * spamProbTotal)))
    trueResult = test[1]
    if prob >= 0.5:
      if trueResult == 1:
        tp = tp + 1
      else:
        fp = fp + 1
    else:
      if trueResult == 0:
        tn = tn + 1
      else:
        fn = fn + 1

  print(f"FP: {fp}\nFN: {fn}\nTP: {tp}\nTN: {tn}")
  accuracy = (tp + tn) / (tp + tn + fp + fn)
  print(f"Accuracy: {accuracy}")
  precision = tp / (tp + fp)
  print(f"Precision: {precision}")
  recall = tp / (tp + fn)
  print(f"Recall: {recall}")
  f1 = 2 * 1 / (1/precision + 1/recall)
  print(f"F1: {f1}")

def main():
  dataFilename = input("Training file: ")
  dataFile = open(dataFilename, "r")

  (vocab, hamTotal, spamTotal) = getData(dataFile)
  
  stopFilename = input("Stop file: ")
  stopFile = open(stopFilename, "r")
  vocab = cleanoutStops(vocab, stopFile)

  testFilename = input("Test file: ")
  testFile = open(testFilename, "r")
  testData = getTestData(testFile)
  (hamProb, spamProb) = getProb(vocab, testData)
  compare(testData, hamProb, spamProb, hamTotal, spamTotal)

if __name__ == "__main__":
  main()