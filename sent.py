from textblob import TextBlob

text = "tangina Kyled"

analysis = TextBlob(text)

print(text)
print(analysis.sentiment.polarity)