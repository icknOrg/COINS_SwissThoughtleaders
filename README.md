# COINS_SwissThoughtleaders
A Repository for Data Storage for the Seminar COINS - Topic Swiss Thoughtleaders 

## Goal of the project
The Project started with a list of people that could pontentially be called Swiss Thoughtleaders. In order to question this statement we collected data on the various people 
consisting of 

- Twitter data fetched with Griffin
- Google Search Results
- Wikipedia Links, Backlinks, Publications and Awards in 2020/2021
- Sentiment Analysis from Google News Articles in the year 2021

Each area calculates an index for each person. In the end the various factors are combined into one general index where the highest number is closest to be considered a Thoughtleader based on our collected data. 

## Sentiment Analysis
The different Google News Articles are assigned a weight based on how often the name of the person is mentioned in the description of the artcicle (mostly 0 to 3). With that non-correlated articles are later deleted in the Analysis. 

The Sentiment is assigned in 2 ways: 
- by comparing positive and negative words of the SentiWS [1] dataset with the articles and assigning the sentiment of majority to the overall article. 
- by using the SentimentModel which includes the German model of BERT [2] that assigns the sentiments automatically to the articles. 

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
- The Index List then gets normalized in a Min/Max way and is returned as Dataframe to be completed with the rest of the analysis.
- For calculating the Thoughtleader score the Sentiment score is divided by 5 as otherwise the sentiment score would be weighted higher relatively to the Twitter and Wikipedia score.

## Twitter Data (fetched with Griffin)
We used the fetcher from Griffin to extract Twitter data for each Thoughtleader candidate for analysing their tweets sand comparing their vocabulary [3]. Building on that, we calculated an index describing the overall trend of each profile. 

The twitter index is calculated from the different values that are representative for the 6 honest signals [5] and the followers count/100. 

```python
 combined['central_leadership'] = combined['degree'] + combined['betweenness']
    combined['rotation_leadership'] = combined['betweenness_oscillation']
    combined['balanced_contribution'] = combined['contribution_index']
    combined['rapid_responses'] = (1/combined['ego_art']) + (1/combined['ego_nudges']) + (1/combined['alter_nudges']) + (1/combined['alter_art'])
    combined['honest_language'] = combined['sentiment_avg'] + combined['emotionality_avg']
    combined['shared_context'] = combined['complexity_avg']
    combined['Twitter'] = combined['central_leadership'] + combined['rotation_leadership'] + combined['balanced_contribution'] + combined['rapid_responses'] + combined['honest_language'] + combined['shared_context']+(combined['followers_count']/100)
```
The end result is normalized in a range from [0,1].

## Google Search Results
For getting the Google Search Results of each person, we manually researched in Google, where we set the filter to results of the last year and put the name into "" to make sure that only relevant results were included. Then, these numbers were put into our initial Thoughtleader.csv file, for both the German-speaking and the Swiss people.

## Wikipedia
For each of the potential Thoughtleaders of our initial list who has a Wikipedia entry, a Wikipedia Index [0,1] is calculated based on the following aspects:
  - number of backlinks 
  - number of links
  - number of awards won in 2020/21
  - number of publications in 2020/21

This information was fetched using the Python library wikipediaapi. Doing so, Awards and Publications were multiplied by 50 as they are seen as important as 50 links or backlinks. Furthermore, the min-max normalization is used to get a score between 0 and 1.

```python
#Calculate Wikipedia score
wikipedia_score = links + backlinks + 50*auszeichnungen + 50*publications
#Normalize with min_max
wikipedia_score['Wikipedia_score']=(wikipedia_score['Wikipedia_score']-wikipedia_score['Wikipedia_score'].min())/(wikipedia_score['Wikipedia_score'].max()-wikipedia_score['Wikipedia_score'].min())
```
## Thoughtleader Score
The Thoughtleader Score was calculated by adding the 4 different factors described above and deviding the results by 4. 

The labels for the classification were 1 (classified as Thoughtleader) and 0 (not classified as Thoughtleader) based on the earlier calculated Thoughtleader Score. 
For the separated German-speaking and Swiss list, the persons with the upper 30% of the Thoughtleader Score were classified as Thoughtleaders. For the concatenated list of
both 50% were used instead. 

## Classification
We decided to predict the membership of the people to our Thoughtleader Tribe in a four-fold way:

First, the thoughtleader score was calculated for the Swiss and German-speaking people separately and based on this they were labelled as a Thoughtleader or not. 

Second, the thoughtleader score was calculated for both the Swiss and German-speaking people all together and based on this they were labelled as a Thoughtleader or not.

Based on each approach two prediction models were created: 
  1. a model was trained on the Swiss people and was then used for predicting the German-speaking people's Thoughtleader Tribe membership.
  2. a model was trained by the German-speaking people and then used for predicting the Swiss people's Thoughtleader Tribe membership.

#### For execution of these two approaches, please follow this instruction:
  - For executing the first approach, the thoughtleader_index.py and create_classification_df need to be used and the min-max nominalization need to be done in the Wikipedia.py     and Twitter_final.py.
  - For executing the second approach, the thoughtleader_index_all.py and create_classification_all_df need to be used and the min-max nominalization need to be commented out in     the Wikipedia.py and Twitter_final.py.

The two implemented Machine Learning Models are a Neural Network and a Random Forest.

The results were as followed (shown is the accuracy of the training/test evaluation and the amount of predicted thoughtleaders).



 |            RUN              |   RF Accuracy    |      RF TLs      |   NN Accuracy    |      NN TLs    | 
 |          :---:              |      :---:       |      :---:       |      :---:       |       :---:    |
 | Train on SW Predict DE      |       0.93       |       44/54      |       0.93       |       17/54    | 
 | Train on DE Predict SW      |       0.94       |      36/100      |       0.88       |       0/100    |         
 | ALL Train on SW Predict DE  |       0.93       |        1/54      |       0.86       |        9/54    |
 | ALL Train on DE Predict SW  |       0.71       |      18/100      |       0.94       |       3/100    |              



## References
<a id="1">[1]</a> 
R. Remus, U. Quasthoff & G. Heyer: SentiWS - a Publicly Available German-language Resource for Sentiment Analysis. 
In: Proceedings of the 7th International Language Ressources and Evaluation (LREC'10), 2010.

<a id="2">[2]</a> 
Guhr O, Schumann AK, Bahrmann F, Böhme HJ. Training a Broad-Coverage German Sentiment Classification Model for Dialog Systems. 
In: Proceedings of the 12th Language Resources and Evaluation Conference 2020 May (pp. 1627-1632).

<a id="3">[3]</a> 
Frick, K., Guertler, D., & Gloor, P. A. (2013). Coolhunting for the world's thought leaders. arXiv preprint arXiv:1308.1160.

<a id="4">[4]</a> 
Gloor, P. A., Colladon, A. F., de Oliveira, J. M., Rovelli, P., Galbier, M., & Vogel, M. (2019). Identifying tribes on twitter through shared context. In Collaborative innovation networks (pp. 91-111). Springer, Cham.

<a id="5">[5]</a> 
Gloor, P. A. (2017). Sociometrics and human relationships: Analyzing social networks to manage brands, predict trends, and improve organizational performance. Emerald Group Publishing.
