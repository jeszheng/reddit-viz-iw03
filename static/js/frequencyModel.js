function renderPhraseFrequency(data, div_id) {
  var margin = {top: 20, right: 80, bottom: 30, left: 50},
      width = 700 - margin.left - margin.right,
      height = 400 - margin.top - margin.bottom;

  var x = d3.time.scale()
      .range([0, width]);

  var y = d3.scale.linear()
      .range([height, 0]);

  var color = d3.scale.category10();

  var xAxis = d3.svg.axis()
      .scale(x)
      .orient("bottom")
      .ticks(data.length);

  var yAxis = d3.svg.axis()
      .scale(y)
      .orient("left");

  var line = d3.svg.line()
      .interpolate("monotone")
      .x(function(d) { return x(d.date); })
      .y(function(d) { return y(d.frequency); });

  var svg = d3.select(div_id).append("svg")
      .attr("id","phraseFrequencyModelSvg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
      .append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  color.domain(d3.keys(data[0]).filter(function(key) { return key !== "date"; }));

  data.forEach(function(d) {
    var dateFormat = new Date( Math.floor(d.date/10000),
                               Math.floor( (d.date%10000) / 100) - 1,
                               d.date%100,
                               0,0,0);
    d.date = dateFormat;
  });

  var freq_data = color.domain().map(function(name) {
    return {
      name: name,
      values: data.map(function(d) {
        return {date: d.date, frequency: +d[name]};
      })
    };
  });

  x.domain(d3.extent(data, function(d) { return d.date; }));

  y.domain([
    d3.min(freq_data, function(c) { return d3.min(c.values, function(v) { return v.frequency; }); }),
    d3.max(freq_data, function(c) { return d3.max(c.values, function(v) { return v.frequency; }); })
  ]);

  svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis);

  svg.append("g")
      .attr("class", "y axis")
      .call(yAxis)
    .append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 6)
      .attr("dy", ".71em")
      .style("text-anchor", "end")
      .text("number of headlines containing phrase");

  var freq = svg.selectAll(".freq")
      .data(freq_data)
      .enter().append("g")
      .attr("class", "freq");

  freq.append("path")
      .attr("class", "line")
      .attr("d", function(d) { return line(d.values); })
      .attr('stroke-width',7)
      .style("stroke", function(d) {
        if (d.name == 'top') {
          return '#63A500';
        } else {
          return '#FF772D';
        }});
}
