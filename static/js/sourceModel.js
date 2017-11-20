function drawSourceModel(data, div_id) {
  if (data.length == 0) {
    return;
  }
  var chart = AmCharts.makeChart(div_id, {
    "type": "pie",
    "startDuration": 0,
    "theme": "none",
    "addClassNames": true,
    "innerRadius": "30%",
    "defs": {
      "filter": [{
        "id": "shadow",
        "width": "200%",
        "height": "200%",
        "feOffset": {
          "result": "offOut",
          "in": "SourceAlpha",
          "dx": 0,
          "dy": 0
        },
        "feGaussianBlur": {
          "result": "blurOut",
          "in": "offOut",
          "stdDeviation": 5
        },
        "feBlend": {
          "in": "SourceGraphic",
          "in2": "blurOut",
          "mode": "normal"
        }
      }]
    },
    "dataProvider": [{
      "source": "Fox News",
      "count": data['fox']
    }, {
      "source": "American Newspaper",
      "count": data['american_news']
    }, {
      "source": "International Newspaper",
      "count": data['international']
    }, {
      "source": "Local Newspaper",
      "count": data['blog_opinion']
    }, {
      "source": "Internet Media Site",
      "count": data['digital_media']
    }, {
      "source": "Political Newspaper/Journal",
      "count": data['political_journal']
    }, {
      "source": "Blog/Opinion Site",
      "count": data['blog_opinion']
    }, {
      "source": "Academic or Professional Association",
      "count": data['academic_professional']
    }, {
      "source": "National Government Site",
      "count": data['gov']
    }, {
      "source": "Magazine",
      "count": data['magazine']
    }, {
      "source": "Non-profit Organization Site",
      "count": data['non_profit']
    }, {
      "source": "Social Media",
      "count": data['social_media']
    }, {
      "source": "Tech News Site",
      "count": data['tech']
    }, {
      "source": "Other",
      "count": data['other']
    }, {
      "source": "Video",
      "count": data['video']
    }],
    "valueField": "count",
    "titleField": "source",
  });

  chart.addListener("rollOverSlice", function(e) {
    handleRollOver(e);
  });
}

function handleRollOver(e){
  var wedge = e.dataItem.wedge.node;
  wedge.parentNode.appendChild(wedge);
}
