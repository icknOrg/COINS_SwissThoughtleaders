# COINS_SwissTribeleaders
A Repository for Data Storage for the Seminar COINS - Topic Swiss Tribeleaders 

## Goal of the project
The Project started with a list of people that could pontentially be called Swiss Thoughtleaders. In order to question this statement we collected data on the various people 
consisting of 

- Twitter data fetched with Griffin
- Google Search Results
- Wikipedia Backlinks, Publications and Awards in 2020/2021
- Sentiment Analysis from Google News Articles in the year 2021

Each area calculates an index for each person. In the end the various factors are combined into one general index where the highest number is closest to be considered a Thoughtleader
based on our collected data. 

## Sentiment Analysis
The different Google News Articles are assigned a weight based on how often the name of the person is mentioned in the description of the artcicle (mostly 0 to 3). With that non-
correlated articles are later deleted in the Analysis. 

The Sentiment is assigned in 2 ways: 
- by comparing positive and negative words of the SentiWS [1] dataset with the articles and assigning the sentiment of majority to the overall article. 
- by using the SentimentModel which includes the German model of BERT [2] and assigns the sentiments automatically to the articles. 

The Sentiment Index is calculated by: 
- comparing the two sentiments of an article an adding up the amount of articles for a specific value times the weight that was assigned in the beginning.
- these specific values consist of:
  - negative
  - neg_bit (when one sentiment is negative and the other one neutral) 
  - neutral
  - pos_bit (when one sentiment is positive and the other one neutral) 
  - positive 
- the different values are then cumulated and the mean is calculated. 
- If the highest value is the cumulated negative value, the standard deviation is calculated, divided by 10 and then substracted from the mean, as seen here:

```python
 if (negative_value+positive_value+neutral_value+pos_bit_value+neg_bit_value) > 0: 
            mean = (negative_value*1+neg_bit_value*2+neutral_value*3+pos_bit_value*4+positive_value*5)/(negative_value+positive_value+neutral_value+pos_bit_value+neg_bit_value)
            if negative_value == max(negative_value, neg_bit_value, positive_value, pos_bit_value, neutral_value):
                var = (1-mean)**2*negative_value+(2-mean)**2*neg_bit_value+(3-mean)**2*neutral_value+(4-mean)**2*pos_bit_value+(5-mean)**2*positive_value
                std_var = math.sqrt(var)
                index_value = mean - (std_var/10); 
                sentiment_index.append(index_value)
```
- The same is done for the highest positive value, where the standard deviation divided by 10 is added to the mean. For the neg_bit and pos_bit values the same is done with a division by 50.
- The Index List gets then normalized in a Min/Max way and returned as Dataframe to be completed with the rest of the analysis.

## Twitter Data (fetched with Griffin)

## Google Search Results

## Wikipedia
For each of the potential Thoughtleaer of our initial list disposing of a Wikipedia entry, a Wikipedia Index [0,1] is calculated based on the following aspects:
  - # of backlinks 
  - # of links
  - # of awards won in 2020/21
  - # of publications in 2020/21
This information was fetched using the Python library wikipediaapi. Doing so, Awards and Publications were multiplied by 50 as they are seen as important as 50 links or backlinks. Furthermore, the min-max normalization is used to get a score between 0 and 1.

## References
<a id="1">[1]</a> 
R. Remus, U. Quasthoff & G. Heyer: SentiWS - a Publicly Available German-language Resource for Sentiment Analysis. 
In: Proceedings of the 7th International Language Ressources and Evaluation (LREC'10), 2010.

<a id="2">[2]</a> 
Guhr O, Schumann AK, Bahrmann F, Böhme HJ. Training a Broad-Coverage German Sentiment Classification Model for Dialog Systems. 
In: Proceedings of the 12th Language Resources and Evaluation Conference 2020 May (pp. 1627-1632).

<a id="3">[3]</a> 
Frick, K., Guertler, D., & Gloor, P. A. (2013). Coolhunting for the world's thought leaders. arXiv preprint arXiv:1308.1160.
