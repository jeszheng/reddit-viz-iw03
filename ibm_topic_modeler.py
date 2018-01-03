import json
from watson_developer_cloud import NaturalLanguageUnderstandingV1
import watson_developer_cloud.natural_language_understanding.features.v1 \
  as Features

# -----------------------------------------------------------------------------#
# ibm_topic_modeler.py
# -----------------------------------------------------------------------------#
# Uses IBM Watson's Natural Language Understanding service to compute
# topics, via the 'keywords' option in their API.
# https://natural-language-understanding-demo.ng.bluemix.net/?cm_mc_uid=55250413417115103371602&cm_mc_sid_50200000=1510686915&cm_mc_sid_52640000=1510686915
# -----------------------------------------------------------------------------#

def ibm_get_topics(titles, num_topics):
    all_titles = ". ".join(titles)

    natural_language_understanding = NaturalLanguageUnderstandingV1(
      username="9aa73582-d1ff-4cb7-9d92-011e3ee81b05",
      password="Chn7dOdZVaaI",
      version="2017-02-27")

    response = natural_language_understanding.analyze(
      text = all_titles,
      features=[
        Features.Keywords(
          limit = num_topics
        )
      ]
    )

    return response
