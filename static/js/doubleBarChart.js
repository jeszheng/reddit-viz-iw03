function render(data, div_id) {
  if (data.length == 0) {
    return;
  }

  var chart,
  width = 350,
  bar_height = 50, // BAR HEIGHT HERE
  height = bar_height * data.length;
  //var rightOffset = width + labelArea;
  var rightOffset = width; // make the bars back to back

  var top = "top-relevance";
  var con = "con-relevance";
  var xFrom = d3.scale.linear()
          .range([0, width]);
  var xTo = d3.scale.linear()
          .range([0, width]);
  var y = d3.scale.ordinal()
          .rangeBands([20, height]);

  var sub_const_top = d3.min(data,function (d) { return d[top] }) - 0.01;
  var mult_const = 1200;
  var sub_const_con = d3.min(data,function (d) { return d[con] }) - 0.01;
  var add_const = 200;

  var chart = d3.select(div_id)
          .append('svg')
          .attr('class', 'chart')
          .attr('width', 700)
          .attr('height', height + 50);

  xFrom.domain(d3.extent(data, function (d) {
      return d[top]*mult_const + add_const;
  }));
  xTo.domain(d3.extent(data, function (d) {
      return d[con]*mult_const + add_const;
  }));

  y.domain(data.map(function (d) {
      return d.index;
  }));

  var yPosByIndex = function (d) {
      return y(d.index);
  };
  chart.selectAll("rect.left")
          .data(data)
          .enter().append("rect")
          .attr("x", function (d) {
              return width - (d[top]-sub_const_top)*mult_const - add_const;
          })
          .attr("y", yPosByIndex)
          .attr("class", "left")
          .attr("width", function (d) {
              return (d[top]-sub_const_top)*mult_const + add_const;
          })
          .attr("height", y.rangeBand())
          .attr('stroke','white')
          .attr('stroke-width',3)
          .attr('fill',function (d) {
            // COLOR DECIDED HERE.
            var colors = ['#63A500', '#71B709', '#8EB712', '#A9BC18', '#B4C625', '#BCD123', '#BCD123', '#BCD123', '#BCD123'];
            return colors[d['index']];
          })
          .append('title') // TOOLTIP
            .text(function (d) { return d['top-keyword']+"\nRelevance: " + parseFloat(d[top]*100).toFixed(2)+"%" });
  chart.selectAll("text.leftscore")
          .data(data)
          .enter().append("text")
          .attr("x", function (d) {
              return width - 40; // make it be next to the divider.
          })
          .attr("y", function (d) {
              return y(d.index) + y.rangeBand() / 2;
          })
          .attr("dx", "20")
          .attr("dy", ".36em")
          .attr("text-anchor", "end")
          .attr('class', 'leftscore')
          .attr('font-size', '15px')
          .text(function(d){return d['top-keyword'];});

  chart.selectAll("rect.right")
          .data(data)
          .enter().append("rect")
          .attr("x", rightOffset)
          .attr("y", yPosByIndex)
          .attr("class", "right")
          .attr("width", function (d) {
              return (d[con]-sub_const_con)*mult_const + add_const;
          })
          .attr("height", y.rangeBand())
          .attr('stroke','white')
          .attr('stroke-width',3)
          .attr('fill',function (d) {
            // COLOR DECIDED HERE.
            var colors = ['#FF772D', '#FF812D', '#FF8B2D', '#FC942D', '#FC9F2D', '#FCAD2D', '#FCAD2D', '#FCAD2D', '#FCAD2D'];
            return colors[d['index']];
          })
          .append('title') // TOOLTIP
            .text(function (d) { return d['con-keyword']+ "\nRelevance: " + parseFloat(d[con]*100).toFixed(2)+"%"});
  chart.selectAll("text.score")
          .data(data)
          .enter().append("text")
          .attr("x", function (d) {
              return rightOffset + 20;
          })
          .attr("y", function (d) {
              return y(d.index) + y.rangeBand() / 2;
          })
          .attr("dx", -5)
          .attr("dy", ".36em")
          .attr('class', 'score')
          .attr('font-size', '15px')
          .text(function(d){return d['con-keyword'];});
}
