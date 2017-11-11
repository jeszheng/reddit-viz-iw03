function draw_political_scatterplot(data, div_id) {
  if (data.length == 0) {
    return;
  }
  var body = d3.select(div_id)
  var selectData = [
                     { "text" : "Post Score" },
                     { "text" : "Author Karma" },
                     { "text" : "Upvote Ratio" },
                     { "text" : "Number of Comments" },
                   ]
  var selectData_X = [
                    { "text" : "Liberal Sentiment" },
                    { "text" : "Conservative Sentiment" },
                    { "text" : "Libertarian Sentiment" },
                    // { "text" : 'Liberal Conservative Ratio' },
                    { "text" : 'Liberal Conservative Difference' },
                  ]

   // Select X-axis Variable
   var span = body.append('span')
     .text('Select X-Axis variable: ')
   var xInput = body.append('select')
       .attr('id','xSelect')
       .on('change',xChange)
     .selectAll('option')
       .data(selectData_X)
       .enter()
     .append('option')
       .attr('value', function (d) { return d.text })
       .text(function (d) { return d.text ;})
   body.append('br')

  // Select Y-axis Variable
  var span = body.append('span')
      .text('Select Y-Axis variable: ')
  var yInput = body.append('select')
      .attr('id','ySelect-political')
      .on('change',yChange)
    .selectAll('option')
      .data(selectData)
      .enter()
    .append('option')
      .attr('value', function (d) { return d.text })
      .text(function (d) { return d.text ;})
  body.append('br')

  var curXVal = 'Liberal Sentiment';
  var curYVal = 'Post Score';

  // Variables
  var body = d3.select(div_id)
  var margin = { top: 50, right: 50, bottom: 50, left: 50 }
  var h = 500 - margin.top - margin.bottom
  var w = 700 - margin.left - margin.right

  // Scales
  var xScale = d3.scale.linear()
    .domain(
      [d3.min([0,d3.min(data,function (d) { return d['Liberal Sentiment'] })])
      ,d3.max(data,function (d) { return d['Liberal Sentiment'] })] ) // 0 to 1 for political sentiments
    .range([0,w])

  var yScaleScores = [];
  data.forEach(function(d) {
    yScaleScores.push(d['Post Score']);
  });

  var yScale = d3.scale.linear()
    .domain([
      d3.min([0,d3.min(data,function (d) { return d['Post Score'] })]),
      Math.ceil(d3.quantile(yScaleScores, 0.05)/100)*100
      ])
    .range([h,0])
  var svg2 = body.append('svg')
      .attr('height',h + margin.top + margin.bottom)
      .attr('width',w + margin.left + margin.right)
    .append('g')
      .attr('transform','translate(' + margin.left + ',' + margin.top + ')')
  // X-axis
  var xAxis = d3.svg.axis()
    .scale(xScale)
    .ticks(5)
    .orient('bottom')
  // Y-axis
  var yAxis = d3.svg.axis()
    .scale(yScale)
    .ticks(5)
    .orient('left')
  // Circles
  var circles = svg2.selectAll('circle')
      .data(data)
      .enter()
    .append('circle')
      .attr('class','circle-political')
      .attr('cx',function (d) { return xScale(d['Liberal Sentiment']) })
      .attr('cy',function (d) { return yScale(d['Post Score']) })
      .attr('r','5')
      .attr('stroke','black')
      .attr('stroke-width',1)
      .attr('fill',function (d,i) {
        // COLOR DECIDED HERE.
        if (d['Category'] == 'top') {
          return '#78C900'
        } else {
          return '#FF5F0A'
        }
      })
      .on('mouseover', function () {
        d3.select(this)
          .transition()
          .duration(500)
          .attr('r',9)
          .attr('stroke-width',3)
      })
      .on('mouseout', function () {
        d3.select(this)
          .transition()
          .duration(500)
          .attr('r',5)
          .attr('stroke-width',1)
      })
    .append('title') // TOOLTIP FOR EACH CIRCLE
      .text(function (d) { return d['Title']
                          +
                           '\nLiberal Sentiment: ' + d['Liberal Sentiment'] +
                           '\nConservative Sentiment: ' + d['Conservative Sentiment'] +
                           '\nLibertarian Sentiment: ' + d['Libertarian Sentiment'] +
                           '\nPost Score: ' + d['Post Score'] +
                           '\nAuthor Karma: ' + d['Author Karma'] +
                           '\nUpvote Ratio: ' + d['Upvote Ratio'] +
                           '\nNumber of Comments: ' + d['Number of Comments']
                         })
  // X-axis
  svg2.append('g')
      .attr('class','axis')
      .attr('id','xAxis-political')
      .attr('transform', 'translate(0,' + h + ')')
      .call(xAxis)
    .append('text') // X-axis Label
      .attr('id','xAxisLabel-political')
      .attr('y',-15)
      .attr('x',w)
      .attr('dy','.71em')
      .style('text-anchor','end')
      .text('Liberal Sentiment')
  // Y-axis
  svg2.append('g')
      .attr('class','y-axis')
      .attr('id','yAxis-political')
      .call(yAxis)
    .append('text') // y-axis Label
      .attr('id', 'yAxisLabel-political')
      .attr('transform','rotate(-90)')
      .attr('x',0)
      .attr('y',5)
      .attr('dy','.71em')
      .style('text-anchor','end')
      .text('Post Score')

    // Calculate correlation data.
    var top_data =  data.filter(function(d) {return d['Category'] == 'top'});
    var controversial_data = data.filter(function(d) {return d['Category'] == 'controversial'});

    var xSeries_top = top_data.map(function(d) { return d['Liberal Sentiment']; });
		var ySeries_top = top_data.map(function(d) { return d['Post Score']; });
    var correlation_top = calculateCorrelation(xSeries_top, ySeries_top);

    var xSeries_con = controversial_data.map(function(d) { return d['Liberal Sentiment']; });
		var ySeries_con = controversial_data.map(function(d) { return d['Post Score']; });
    var correlation_con = calculateCorrelation(xSeries_con, ySeries_con);

  // Correlation Labels
  svg2.append('g')
      .attr('class','correlation-top')
  .append('text') // top correlation
    .attr('id','correlation-top-pol')
    .attr('x',w)
    .attr('y',5)
    .style('text-anchor','end')
    .style('fill','#24A800')
    .text('top: r = ' + correlation_top.toFixed(3))

  svg2.append('g')
      .attr('class','correlation-con')
  .append('text') // controversial correlation
    .attr('id','correlation-con-pol')
    .attr('x',w)
    .attr('y',22)
    .style('text-anchor','end')
    .style('fill','#ff4d00')
    .text('controversial: r = ' + correlation_con.toFixed(3))

  function yChange() {
    var value = this.value // get the new y value
    var new_yScaleScores = [];
    data.forEach(function(d) {
      new_yScaleScores.push(d[value]);
    });
    var maxYVal;
    if (value == 'Upvote Ratio') {
      maxYVal = 1.0;
    } else {
      function sortNumber(a,b) {
          return a - b;
      }
      var sortedArr = new_yScaleScores.sort(sortNumber); // check that this doesnt mess with new_yScaleScores
      var num_to_exclude = Math.ceil((sortedArr.length * 0.05)/1);
      maxYVal = sortedArr[sortedArr.length - num_to_exclude];
    }
    // if (value == 'Upvote Ratio') {
    //   maxYVal = 1.0;
    // } else if (value == 'Author Karma'){
    //   function sortNumber(a,b) {
    //       return a - b;
    //   }
    //   var sortedArr = new_yScaleScores.sort(sortNumber); // check that this doesnt mess with new_yScaleScores
    //   //console.log(sortedArr);
    //   var num_to_exclude = Math.ceil((sortedArr.length * 0.05)/1);
    //   //console.log(num_to_exclude);
    //   maxYVal = sortedArr[sortedArr.length - num_to_exclude];
    //   //console.log("maxYVal" + maxYVal);
    // } else if (value == 'Number of Comments'){
    //   maxYVal = Math.ceil(d3.quantile(new_yScaleScores, 0.03)/100)*100;
    // } else { // Post Score
    //   maxYVal = Math.ceil(d3.quantile(new_yScaleScores, 0.05)/100)*100;
    // }

    yScale // change the yScale
      .domain([
        d3.min([0,d3.min(data,function (d) { return d[value] })]),
        maxYVal
        ])
    yAxis.scale(yScale) // change the yScale
    d3.select('#yAxis-political') // redraw the yAxis
      .transition().duration(1000)
      .call(yAxis)
    d3.select('#yAxisLabel-political') // change the yAxisLabel
      .text(value)
    d3.selectAll('.circle-political') // move the circles
      .transition().duration(1000)
      .delay(0) // delay = 0 moves all the circles at the same time.
      .attr('cy',function (d) { return yScale(d[value]) })

    // recalculate correlation data

    var top_data = data.filter(function(d) {return d['Category'] == 'top'});
    var controversial_data = data.filter(function(d) {return d['Category'] == 'controversial'});

    var xSeries_top = top_data.map(function(d) { return d[curXVal]; });
    var ySeries_top = top_data.map(function(d) { return d[value]; });
    var correlation_top = calculateCorrelation(xSeries_top, ySeries_top);

    var xSeries_con = controversial_data.map(function(d) { return d[curXVal]; });
    var ySeries_con = controversial_data.map(function(d) { return d[value]; });
    var correlation_con = calculateCorrelation(xSeries_con, ySeries_con);

    d3.select('#correlation-top-pol')
      .transition().duration(500)
      .text('top: r = ' + correlation_top.toFixed(3))

    d3.select('#correlation-con-pol')
      .transition().duration(500)
      .text('controversial: r = ' + correlation_con.toFixed(3))

    curYVal = value;
    // console.log(curXVal + " -vs- " + curYVal);
  }

  function xChange() {
    var value = this.value // get the new x value

    xScale // change the xScale
      .domain([
        d3.min([0,d3.min(data,function (d) { return d[value] })]),
        d3.max([0,d3.max(data,function (d) { return d[value] })])
        // though may want to use percentile eventually...there seems to be
        // some extreme outliers.
        ])
    xAxis.scale(xScale) // change the xScale

    d3.select('#xAxis-political') // redraw the xAxis
      .transition().duration(1000)
      .call(xAxis)
    d3.select('#xAxisLabel-political') // change the xAxisLabel
      .transition().duration(1000)
      .text(value)

    d3.selectAll('.circle-political') // move the circles
      .transition().duration(1000)
      .delay(0) // delay = 0 moves all the circles at the same time.
          .attr('cx',function (d) { return xScale(d[value]) })

    // may difference between liberal/conservative?
    var top_data = data.filter(function(d) {return d['Category'] == 'top'});
    var controversial_data = data.filter(function(d) {return d['Category'] == 'controversial'});

    var xSeries_top = top_data.map(function(d) { return d[value]; });
    var ySeries_top = top_data.map(function(d) { return d[curYVal]; });
    var correlation_top = calculateCorrelation(xSeries_top, ySeries_top);

    var xSeries_con = controversial_data.map(function(d) { return d[value]; });
    var ySeries_con = controversial_data.map(function(d) { return d[curYVal]; });
    var correlation_con = calculateCorrelation(xSeries_con, ySeries_con);

    d3.select('#correlation-top-pol')
      .transition().duration(500)
      .text('top: r = ' + correlation_top.toFixed(3))

    d3.select('#correlation-con-pol')
      .transition().duration(500)
      .text('controversial: r = ' + correlation_con.toFixed(3))

    curXVal = value;
    // console.log(curXVal + " -vs- " + curYVal);
  }
}
