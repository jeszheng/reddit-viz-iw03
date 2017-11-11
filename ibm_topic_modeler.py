import json
from watson_developer_cloud import NaturalLanguageUnderstandingV1
import watson_developer_cloud.natural_language_understanding.features.v1 \
  as Features

def ibm_get_topics(titles):
    all_titles = ". ".join(titles)

    natural_language_understanding = NaturalLanguageUnderstandingV1(
      username="9aa73582-d1ff-4cb7-9d92-011e3ee81b05",
      password="Chn7dOdZVaaI",
      version="2017-02-27")

    response = natural_language_understanding.analyze(
      text = all_titles,
      features=[
        Features.Keywords(
          limit = 6
        )
      ]
    )

    return response
