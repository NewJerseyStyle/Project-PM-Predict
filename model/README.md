# Model
A module that do sentiment analysis using `NTLK` or `huggingface`.

## API
Both `deep_sent` and `nltk_sent` implements `sentiment_analysis(data)` interface.
### Input of `sentiment_analysis`
- data : `list` of `str`, the strings to be analysised

For each string in the data list, put it into `NTLK` or the `sentiment_pipeline` of `huggingface`,
predict if the string is possitive or negative in its sentiment.
Count the number of positive, negative and neutral labeled strings in the data list.
Calculate the number of positive labeled strings percentage in the number of strings in data list,
the percentage become the positive index to be returned.

### Output of `sentiment_analysis`
`return positive, neutral, negative`
- `positive` = number of strings labeled positive / total number of strings
- `neutral`  = number of strings labeled neutral / total number of strings
- `negative` = number of strings labeled negative / total number of strings

## `model.run()`
The `main()` in `model/main.py` designed for the case of PM analysis read names and lists of strings
that crawled from internet and stored in `TinyDB` to feed into the `API` of `deep_sent` or `nltk_sent`.
