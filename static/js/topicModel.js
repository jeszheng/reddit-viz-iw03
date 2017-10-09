var diameter = 500,
    bubblePadding = -8, //Give negative value in order to overlop the bubbles
    duration = 750,
    delay = 0;

var svg = d3.select('#topicModel').append('svg')
    .attr('width', diameter)
    .attr('height', diameter);

var bubbleNode = d3.layout.pack()
    .size([diameter, diameter])
    .padding(bubblePadding)
    .value(function(d) {
        return d.size = (d.size == '0.0' || d.size == '0') ? '0.1000' : d.size; //0.1000 is considered as a special size for size with value '0' to give some radius for the bubble charts to be drawn
    })

function processData(data) {
    var newDataSet = [];
    for (var i = 0; i < data.length; i++) {
        var name = data[i].label,
            size = data[i].value
        if (data[i].category == 'top') {
          newDataSet.push({ name: name, className: 'bubble-top', size: size });
        } else { // controversial
          newDataSet.push({ name: name, className: 'bubble-controversial', size: size });
        }

    }
    return { children: newDataSet.reverse() };
    // console.log(newDataSet);
}

function drawBubbles(data) {

    var nodes = bubbleNode.nodes(processData(data))
        .filter(function(d) {
            return !d.children;
        }); // filter out the outer bubble

    var bubble = svg.selectAll('.bubble')
        .data(nodes, function(d) {
            return d.name;
        });

    // exit
    var bubbleExit = bubble.exit()
        .transition()
        .duration(duration + delay)
        .style('opacity', 0)
        .remove();

    var bubbleEnter = bubble.enter()
        .append('g')
        .attr('class', 'bubble')
        // Position the g element like the circle element used to be.
        .attr('transform', function(d) {
            return 'translate(' + d.x + ',' + d.y + ')';
        })

    var bubbleCircle = bubbleEnter.append('circle')
        .attr('r', function(d) {
            return d.r;
        })
        .attr('class', function(d) {
            return d.className;
        })
        .style('opacity', 0)
        .transition()
        .duration(duration)
        .style('opacity', 1);

    var bubbleLabel = bubbleEnter.append('text')
        .attr('class', 'bubble-label')
        .attr('dy', '.3em')
        .attr('text-anchor', 'middle')
        .attr('font-size', function(d) {
            //return (d.r > 85) ? (d.r / 5)+'px' : (d.r / 3)+'px';
            var len = d.name.substring(0, d.r / 5).length;
            var size = d.r / 5;
            size *= 10 / len;
            size += 1;
            size = (size < 18) ? size : 18;
            return Math.round(size) + 'px';
        })
        .text(function(d) {
            //return d.title;
            var text = d.name.substring(0, d.r / 5);
            return text;
        })
        .style('opacity', 0.2)
        .transition()
        .duration(duration)
        .style('opacity', 1);;

    // update - This only applies to updating nodes
    var bubbleCircleUpdate = bubble.select('circle').transition()
        .duration(duration)
        .delay(function(d, i) {
            delay = i * 7;
            return delay;
        })
        .attr('r', function(d) {
            return d.r;
        })
        .style('opacity', 0)
        .transition()
        .duration(duration)
        .style('opacity', 1);


    var bubbleLableUpdate = bubble.select('text').transition()
        .duration(duration)
        .delay(function(d, i) {
            delay = i * 7;
            return delay;
        })
        .attr('dy', '.3em')
        .attr('text-anchor', 'middle')
        .attr('font-size', function(d) {
            //return (d.r > 85) ? (d.r / 5)+'px' : (d.r / 3)+'px';
            var len = d.name.substring(0, d.r / 5).length;
            var size = d.r / 3;
            size *= 10 / len;
            size += 1;
            size = (size < 18) ? size : 18;
            return Math.round(size) + 'px';
        })
        .text(function(d) {
            //return d.title;
            var text = d.name.substring(0, d.r / 5);
            return text;
        })
        .style('opacity', 0)
        .transition()
        .duration(duration)
        .style('opacity', 1);
}

// drawBubbles(topics);
