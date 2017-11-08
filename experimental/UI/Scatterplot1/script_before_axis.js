var data = [];
var a = {};
a['Positive-Negative Sentiment'] = 0.296;
a['Post Score'] = 51261;
a['Author Karma'] = 25300;
a['Upvote Ratio'] = 0.88;
a['Number of Comments'] = 5683;
a['Title'] = 'Republicans just introduced a bill to remove Mueller from the Trump-Russia investigation';
a['Category'] = 'top';
data.push(a);

var b = {};
b['Positive-Negative Sentiment'] = -0.75;
b['Post Score'] = 20081;
b['Author Karma'] = 43261;
b['Upvote Ratio'] = 0.9;
b['Number of Comments'] = 1720;
b['Title'] = 'Robert Mueller is reportedly zeroing in on Jared Kushner over his role in firing James Comey';
b['Category'] = 'top';
data.push(b);

var c = {};
c['Positive-Negative Sentiment'] = 0.0;
c['Post Score'] = 12000;
c['Author Karma'] = 115092;
c['Upvote Ratio'] = 0.75;
c['Number of Comments'] = 2500;
c['Title'] = 'sample title c';
c['Category'] = 'top';
data.push(c);

var e = {};
e['Positive-Negative Sentiment'] = -0.5;
e['Post Score'] = 42000;
e['Author Karma'] = 3246;
e['Upvote Ratio'] = 0.61;
e['Number of Comments'] = 4000;
e['Title'] = 'Donna Brazile’s bombshell about the DNC and Hillary Clinton, explained - Vox';
e['Category'] = 'controversial';
data.push(e);

var d = {};
d['Positive-Negative Sentiment'] = 0.0;
d['Post Score'] = 42;
d['Author Karma'] = 8111;
d['Upvote Ratio'] = 0.52;
d['Number of Comments'] = 170;
d['Title'] = 'Donna Brazile’s bombshell about the DNC and Hillary Clinton, explained - Vox';
d['Category'] = 'controversial';
data.push(d);

function draw_scatterplot(div_id) {
  //var body = d3.select('body')
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
      .attr('id','ySelect')
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
  var w = 500 - margin.left - margin.right
  var formatPercent = d3.format('.2%')

  // Scales
  var colorScale = d3.scale.category20()
  var xScale = d3.scale.linear()
    .domain( [-1,1] ) // -1 to 1 for sentiment compound
    .range([0,w])
  var yScale = d3.scale.linear()
    .domain([
      d3.min([0,d3.min(data,function (d) { return d['Post Score'] })]),
      d3.max([0,d3.max(data,function (d) { return d['Post Score'] })])
      ])
    .range([h,0])
  // SVG
  var svg = body.append('svg')
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
  var circles = svg.selectAll('circle')
      .data(data)
      .enter()
    .append('circle')
      .attr('cx',function (d) { return xScale(d['Positive-Negative Sentiment']) })
      .attr('cy',function (d) { return yScale(d['Post Score']) })
      .attr('r','7')
      .attr('stroke','black')
      .attr('stroke-width',1)
      .attr('fill',function (d,i) {
        if (d['Category'] == 'top') {
          return '#ff772d'
        } else {
          return '#6666ea'
        }
      }) // COLOR DECIDED HERE.
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
  svg.append('g')
      .attr('class','axis')
      .attr('id','xAxis')
      .attr('transform', 'translate(0,' + h + ')')
      .call(xAxis)
    .append('text') // X-axis Label
      .attr('id','xAxisLabel')
      .attr('y',-10)
      .attr('x',w)
      .attr('dy','.71em')
      .style('text-anchor','end')
      .text('Positive-Negative Sentiment')
  // Y-axis
  svg.append('g')
      .attr('class','axis')
      .attr('id','yAxis')
      .call(yAxis)
    .append('text') // y-axis Label
      .attr('id', 'yAxisLabel')
      .attr('transform','rotate(-90)')
      .attr('x',0)
      .attr('y',5)
      .attr('dy','.71em')
      .style('text-anchor','end')
      .text('Post Score')

  function yChange() {
    var value = this.value // get the new y value
    yScale // change the yScale
      .domain([
        d3.min([0,d3.min(data,function (d) { return d[value] })]),
        d3.max([0,d3.max(data,function (d) { return d[value] })])
        ])
    yAxis.scale(yScale) // change the yScale
    d3.select('#yAxis') // redraw the yAxis
      .transition().duration(1000)
      .call(yAxis)
    d3.select('#yAxisLabel') // change the yAxisLabel
      .text(value)
    d3.selectAll('circle') // move the circles
      .transition().duration(1000)
      .delay(0)
        .attr('cy',function (d) { return yScale(d[value]) })
  }

  function xChange() {
    var value = this.value // get the new x value
    xScale // change the xScale
      .domain([
        d3.min([0,d3.min(data,function (d) { return d[value] })]),
        d3.max([0,d3.max(data,function (d) { return d[value] })])
        ])
    xAxis.scale(xScale) // change the xScale
    d3.select('#xAxis') // redraw the xAxis
      .transition().duration(1000)
      .call(xAxis)
    d3.select('#xAxisLabel') // change the xAxisLabel
      .transition().duration(1000)
      .text(value)
    d3.selectAll('circle') // move the circles
      .transition().duration(1000)
      .delay(function (d,i) { return i*100})
        .attr('cx',function (d) { return xScale(d[value]) })
  }
}


draw_scatterplot('#posNegModel');
