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
function draw_bubbles(data, div_id) {

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

  var svg = d3.select(div_id).append("svg")
    .attr("width", width)
    .attr("height", height);

  var node = svg.selectAll("g")
    .data(nodes)
    .enter().append("g").call(force.drag);

  var circles = node.append("circle")
    .style("fill", function(d) {
      // COLOR DECIDED HERE.
      switch(d.category) {
        case 'top-0':
            return '#ff4d00';
        case 'top-1':
            return '#ff772d';
        case 'top-2':
            return '#f9955f';
        case 'top-3':
            return '#ffc095';
        case 'controversial-0':
            return '#5252e0';
        case 'controversial-1':
            return '#6666ea';
        case 'controversial-2':
            return '#8585e1';
        case 'controversial-3':
            return '#bebef2';
        default:
            return color(d.cluster);
      }
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
    .style("fill", "white")
    .attr('font-size', function(d) {
        //return (d.r > 85) ? (d.r / 5)+'px' : (d.r / 3)+'px';
        var len = d.keyword.length;
        var size = d.r / 5;
        size *= 13 / len;
        size += 1;
        size = (size < 15) ? size : 15;
        return Math.round(size) + 'px';
    });


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

      if (cluster === d) {
        return;
      }
      var x = d.x - cluster.x, // cluster is undefined apparently. how does this relate to different places?
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
