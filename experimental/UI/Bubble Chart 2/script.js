var width = 800,
  height = 600,
  padding = 1.5, // separation between same-color nodes
  clusterPadding = 16, // separation between different-color nodes
  maxRadius = 24;

var n = 100, // total number of nodes
  m = 20; // number of distinct clusters

// Need to adjust.
var color = d3.scale.category10()
  .domain(d3.range(m));

// The largest node for each cluster.
var clusters = new Array(m);
var nodes = [];

// get the json data from the file
function draw() {
  var data = [];
  var data_element_1 = {};
  data_element_1['keyword'] = 'bob';
  data_element_1['weight'] = 0.1119806865;
  data_element_1['category'] = 'sales';
  data.push(data_element_1);
  var data_element_2 = {};
  data_element_2['keyword'] = 'bill';
  data_element_2['weight'] = 0.2399712579;
  data_element_2['category'] = 'warehouse';
  data.push(data_element_2);
  var data_element_3 = {};
  data_element_3['keyword'] = 'alice';
  data_element_3['weight'] = 0.3860940337;
  data_element_3['category'] = 'warehouse';
  data.push(data_element_3);
  var data_element_4 = {};
  data_element_4['keyword'] = 'mallory';
  data_element_4['weight'] = 0.4406652485;
  data_element_4['category'] = 'sales';
  data.push(data_element_4);
  var data_element_5 = {};
  data_element_5['keyword'] = 'eve';
  data_element_5['weight'] = 0.5399712579;
  data_element_5['category'] = 'warehouse';
  data.push(data_element_5);


  for (var i = 0; i < data.length; i++) {
    var obj = data[i];
    for (var key in obj) {
      var weight = obj['weight']; // weight
      var r = weight * 100; // radius
      var n = obj['keyword']; // keyword
      var div = obj['category']; // category
      d = {
        cluster: div,
        radius: r,
        keyword: n,
        category: div,
        weight: weight
      };
    }
    if (!clusters[i] || (r > clusters[i].radius)) clusters[i] = d;
    nodes.push(d);
  }

  // Use the pack layout to initialize node positions.
  d3.layout.pack()
    .sort(null)
    .size([width, height])
    .children(function(d) {
      return d.values;
    })
    .value(function(d) {
      return d.radius * d.radius;
    })
    .nodes({
      values: d3.nest()
        .key(function(d) {
          return d.cluster;
        })
        .entries(nodes)
    });

  var force = d3.layout.force()
    .nodes(nodes)
    .size([width, height])
    .gravity(.03)
    .charge(0)
    .on("tick", tick)
    .start();

  var svg = d3.select("#bubbleChart").append("svg")
    .attr("width", width)
    .attr("height", height);

  var node = svg.selectAll("g")
    .data(nodes)
    .enter().append("g").call(force.drag);

  var circles = node.append("circle")
    .style("fill", function(d) {
      // COLOR DECIDED HERE, TODO CHANGE.
      return color(d.cluster);
    })

  //add text to the group
  node.append("text")
    .text(function(d) {
      return d.keyword;
    })
    .attr('text-anchor', 'middle')
    .text(function(d) {
      return d.keyword
    })
    .style("stroke", "white");


  node.selectAll("circle").transition()
    .duration(750)
    .delay(function(d, i) {
      return i * 5;
    })
    .attrTween("r", function(d) {
      var i = d3.interpolate(0, d.radius);
      return function(t) {
        return d.radius = i(t);
      };
    });


  function tick(e) {
    node.each(cluster(10 * e.alpha * e.alpha))
      .each(collide(.5))
      .attr("transform", function(d) {
        var k = "translate(" + d.x + "," + d.y + ")";
        return k;
      })
  }


  // Move d to be adjacent to the cluster node.
  function cluster(alpha) {
    return function(d) {

      var cluster = clusters[d.index];

      if (cluster === d) return;
      var x = d.x - cluster.x,
        y = d.y - cluster.y,
        l = Math.sqrt(x * x + y * y),
        r = d.radius + cluster.radius;
      if (l != r) {
        l = (l - r) / l * alpha;
        d.x -= x *= l;
        d.y -= y *= l;
        cluster.x += x;
        cluster.y += y;
      }
    };
  }

  // Resolves collisions between d and all other circles.
  function collide(alpha) {
    var quadtree = d3.geom.quadtree(nodes);
    return function(d) {
      var r = d.radius + maxRadius + Math.max(padding, clusterPadding),
        nx1 = d.x - r,
        nx2 = d.x + r,
        ny1 = d.y - r,
        ny2 = d.y + r;
      quadtree.visit(function(quad, x1, y1, x2, y2) {
        if (quad.point && (quad.point !== d)) {
          var x = d.x - quad.point.x,
            y = d.y - quad.point.y,
            l = Math.sqrt(x * x + y * y),
            r = d.radius + quad.point.radius + (d.cluster === quad.point.cluster ? padding : clusterPadding);
          if (l < r) {
            l = (l - r) / l * alpha;
            d.x -= x *= l;
            d.y -= y *= l;
            quad.point.x += x;
            quad.point.y += y;
          }
        }
        return x1 > nx2 || x2 < nx1 || y1 > ny2 || y2 < ny1;
      });
    };
  }
}

draw();
