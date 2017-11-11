function draw_posneg_scatterplot(data, div_id) {
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

  // Select Y-axis Variable
  var span = body.append('span')
      .text('Select Y-Axis variable: ')
  var yInput = body.append('select')
      .attr('id','ySelect-posneg')
      .on('change',yChange)
    .selectAll('option')
      .data(selectData)
      .enter()
    .append('option')
      .attr('value', function (d) { return d.text })
      .text(function (d) { return d.text ;})
  body.append('br')

  // Variables
  var body = d3.select(div_id)
  var margin = { top: 50, right: 50, bottom: 50, left: 50 }
  var h = 500 - margin.top - margin.bottom
  var w = 700 - margin.left - margin.right

  // Scales
  var xScale = d3.scale.linear()
    .domain( [-1,1] ) // -1 to 1 for sentiment compound
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
  var svg1 = body.append('svg')
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
  var circles = svg1.selectAll('circle')
      .data(data)
      .enter()
    .append('circle')
      .attr('class','circle-posneg')
      .attr('cx',function (d) { return xScale(d['Positive-Negative Sentiment']) })
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
                           '\nPositive-Negative Sentiment: ' + d['Positive-Negative Sentiment'] +
                           '\nPost Score: ' + d['Post Score'] +
                           '\nAuthor Karma: ' + d['Author Karma'] +
                           '\nUpvote Ratio: ' + d['Upvote Ratio'] +
                           '\nNumber of Comments: ' + d['Number of Comments']
                         })
  // X-axis
  svg1.append('g')
      .attr('class','axis')
      .attr('id','xAxis-posneg')
      .attr('transform', 'translate(0,' + h + ')')
      .call(xAxis)
    .append('text') // X-axis Label
      .attr('id','xAxisLabel-posneg')
      .attr('y',-15)
      .attr('x',w)
      .attr('dy','.71em')
      .style('text-anchor','end')
      .text('Positive-Negative Sentiment')
  // Y-axis
  svg1.append('g')
      .attr('class','y-axis')
      .attr('id','yAxis-posneg')
      .call(yAxis)
    .append('text') // y-axis Label
      .attr('id', 'yAxisLabel-posneg')
      .attr('transform','rotate(-90)')
      .attr('x',0)
      .attr('y',5)
      .attr('dy','.71em')
      .style('text-anchor','end')
      .text('Post Score')

    // Calculate correlation data.
    var top_data =  data.filter(function(d) {return d['Category'] == 'top'});
    var controversial_data = data.filter(function(d) {return d['Category'] == 'controversial'});

    var xSeries_top = top_data.map(function(d) { return d['Positive-Negative Sentiment']; });
		var ySeries_top = top_data.map(function(d) { return d['Post Score']; });
    var correlation_top = calculateCorrelation(xSeries_top, ySeries_top);

    var xSeries_con = controversial_data.map(function(d) { return d['Positive-Negative Sentiment']; });
		var ySeries_con = controversial_data.map(function(d) { return d['Post Score']; });
    var correlation_con = calculateCorrelation(xSeries_con, ySeries_con);

  // Correlation Labels
  svg1.append('g')
      .attr('class','correlation-top')
  .append('text') // top correlation
    .attr('id','correlation-top-posneg')
    .attr('x',w)
    .attr('y',5)
    .style('text-anchor','end')
    .style('fill','#24A800')
    .text('top: r = ' + correlation_top.toFixed(3))

  svg1.append('g')
      .attr('class','correlation-con')
  .append('text') // controversial correlation
    .attr('id','correlation-con-posneg')
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
      //console.log(sortedArr);
      var num_to_exclude = Math.ceil((sortedArr.length * 0.05)/1);
      //console.log(num_to_exclude);
      maxYVal = sortedArr[sortedArr.length - num_to_exclude];
      //console.log("maxYVal" + maxYVal);
    }

    // else if (value == 'Author Karma'){
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
    d3.select('#yAxis-posneg') // redraw the yAxis
      .transition().duration(1000)
      .call(yAxis)
    d3.select('#yAxisLabel-posneg') // change the yAxisLabel
      .text(value)
    d3.selectAll('.circle-posneg') // move the circles
      .transition().duration(1000)
      .delay(0) // delay = 0 moves all the circles at the same time.
      .attr('cy',function (d) { return yScale(d[value]) })

    // recalculate correlation data

    var top_data = data.filter(function(d) {return d['Category'] == 'top'});
    var controversial_data = data.filter(function(d) {return d['Category'] == 'controversial'});

    var xSeries_top = top_data.map(function(d) { return d['Positive-Negative Sentiment']; });
    var ySeries_top = top_data.map(function(d) { return d[value]; });
    var correlation_top = calculateCorrelation(xSeries_top, ySeries_top);

    var xSeries_con = controversial_data.map(function(d) { return d['Positive-Negative Sentiment']; });
    var ySeries_con = controversial_data.map(function(d) { return d[value]; });
    var correlation_con = calculateCorrelation(xSeries_con, ySeries_con);

    d3.select('#correlation-top-posneg')
      .transition().duration(500)
      .text('top: r = ' + correlation_top.toFixed(3))

    d3.select('#correlation-con-posneg')
      .transition().duration(500)
      .text('controversial: r = ' + correlation_con.toFixed(3))
  }

  // function xChange() {
  //   var value = this.value // get the new x value
  //   xScale // change the xScale
  //     .domain([
  //       d3.min([0,d3.min(data,function (d) { return d[value] })]),
  //       d3.max([0,d3.max(data,function (d) { return d[value] })])
  //       ])
  //   xAxis.scale(xScale) // change the xScale
  //   d3.select('#xAxis-posneg') // redraw the xAxis
  //     .transition().duration(1000)
  //     .call(xAxis)
  //   d3.select('#xAxisLabel-posneg') // change the xAxisLabel
  //     .transition().duration(1000)
  //     .text(value)
  //   d3.selectAll('.circle-posneg') // move the circles
  //     .transition().duration(1000)
  //     .delay(function (d,i) { return i*100})
  //       .attr('cx',function (d) { return xScale(d[value]) })
  // }
}
