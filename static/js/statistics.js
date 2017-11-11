// returns the correlation.
function calculateCorrelation(xSeries, ySeries) {
  var reduceSumFunc = function(prev, cur) { return prev + cur; };

  var xBar = xSeries.reduce(reduceSumFunc) * 1.0 / xSeries.length;
  var yBar = ySeries.reduce(reduceSumFunc) * 1.0 / ySeries.length;

  var ssXX = xSeries.map(function(d) { return Math.pow(d - xBar, 2); })
    .reduce(reduceSumFunc);

  var ssYY = ySeries.map(function(d) { return Math.pow(d - yBar, 2); })
    .reduce(reduceSumFunc);

  var ssXY = xSeries.map(function(d, i) { return (d - xBar) * (ySeries[i] - yBar); })
    .reduce(reduceSumFunc);

  var correlation = ssXY / Math.sqrt(ssXX * ssYY);

  return correlation;
}


function calculateMean(series) {
  var reduceSumFunc = function(prev, cur) { return prev + cur; };
  return series.reduce(reduceSumFunc) * 1.0 / series.length;
}

function calculateMedian(values) {
  values.sort( function(a,b) {return a - b;} );
  var half = Math.floor(values.length/2);
  if(values.length % 2)
    return values[half];
  else
  return (values[half-1] + values[half]) / 2.0;
}


function sortNumber(a,b) {
    return a - b;
}
