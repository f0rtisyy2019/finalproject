$(document).ready(function () {
  function buildCharts(symbol, divId) {
    var stocks = new Stocks('JY722LVZCMDBOJ9S');
    const getData = async function(symb, interval, amount) {
      const result = await stocks.timeSeries({
        symbol: symb,
        interval: interval,
        amount: amount
      });

      if ($('#index').length > 0) {
        // meta data
        var container = d3.select("#symbol-metadata");
        container.html("");
        Object.entries(result[0]).forEach(([key, value]) => 
          container.append("div").text(key + ": " + value)
        );
      }

      // line chart
      var trace1 = {
        x: result.map(d => d.date),
        y: result.map(d => d.open),
        mode: "lines",
        name: "open",
      };
      var trace2 = {
        x: result.map(d => d.date),
        y: result.map(d => d.high),
        mode: "lines",
        name: "high",
      };
      var trace3 = {
        x: result.map(d => d.date),
        y: result.map(d => d.low),
        mode: "lines",
        name: "low",
      };
      var trace4 = {
        x: result.map(d => d.date),
        y: result.map(d => d.close),
        mode: "lines",
        name: "close",
      };
      var stockData = [trace1];
      var layout = {
        title: `Ticker prices for ${symbol} `,
      };
      Plotly.newPlot(divId, stockData, layout);

    }
    getData(symbol, 'daily', 365 * 5);
  }

  function gainVsLose() {
    d3.json("/scrape").then(function(response){
      const display = ['Symbol', 'Price (Intraday)', 'Change', '% Change'];
      const filtered = response.Stocks.map(raw => {
        return Object.keys(raw)
          .filter(key => display.includes(key))
          .reduce((obj, key) => {
            obj[key] = raw[key];
            return obj;
          }, {});
      });
      
      const gainers = filtered.slice(0,3);
      const losers = filtered.slice(3);

      // gainers table
      var gainerTable = d3.select('#stocks_gainers').append('table').attr("class", "table");
      gainerTable.append('thead').append('tr')
        .selectAll('th')
        .data(display).enter()
        .append('th')
        .text(d => d);
      var rows = gainerTable.append('tbody').selectAll('tr')
        .data(gainers).enter()
        .append('tr');
      rows.selectAll('td')
          .data(function(row) {
            return display.map(column => {
              return { column: column, value: row[column] };
            });
          })
          .enter()
          .append('td')
          .text(d=>d.value);

      // losers table
      var loserTable = d3.select('#stocks_losers').append('table').attr("class", "table");
      loserTable.append('thead').append('tr')
        .selectAll('th')
        .data(display).enter()
        .append('th')
        .text(d => d);
      var rows = loserTable.append('tbody').selectAll('tr')
        .data(losers).enter()
        .append('tr');
      rows.selectAll('td')
        .data(function (row) {
          return display.map(column => {
            return { column: column, value: row[column] };
          });
        })
        .enter()
        .append('td')
        .text(d => d.value);
    
    });
  }

  function initHomePage() {
    // Grab a reference to the dropdown select element
    var selector = d3.select("#selDataset");

    // Use the list of sample names to populate the select options
    d3.json("/ticker").then((symbol) => {
      symbol.forEach((data) => {
        selector
          .append("option")
          .text(data)
          .property("value", data);
      });

      // Use the first sample from the list to build the initial plots
      const firstSymbol = symbol[0];
      buildCharts(firstSymbol, 'stock_1');
    });
    gainVsLose();
  }

  $('#selDataset').change(function(value) {
    // Fetch new data each time a new sample is selected
    buildCharts(this.value, 'stock_1');
  });

  function getSingleResults(symbol, start) {
    var stocks = new Stocks('JY722LVZCMDBOJ9S');
    const getSingleData = async function (symb, start) {
      const result = await stocks.timeSeries({
        symbol: symb,
        interval: 'daily',
        start: new Date(start),
        end: new Date()
      });
      console.log(result);
    }
    getSingleData(symbol, start);
  }

  if ($('#result').length > 0) {
    const ticker1 = $('#ticker1').data('symbol');
    const ticker2 = $('#ticker2').data('symbol');
    const ticker3 = $('#ticker3').data('symbol');
    const tickerList = { "ticker1": ticker1, "ticker2": ticker2, "ticker3": ticker3};

    const share = $('#barchart').data('share');
    console.log(share);

    // symbol construct bar chart 
    var trace = {
      x: Object.values(tickerList),
      y: share,
      type: "bar",
    };
 
    var tickerData = [trace];
    var layout = {
      title: `Ticker construct bar chart `,
    };
    Plotly.newPlot('barchart', tickerData, layout);

    // tikcers status
    $('#news').empty();
    Object.entries(tickerList).forEach(([key, value]) => {
      d3.json("/news/" + value).then((data) => {
        const link = data['News']['Link'];
        const title = data['News']['Title'];
        if (link != undefined && title != undefined) {
          $('#news').append('<div><a href="' + link + '" target="_blank">' + title + '</a></div>');
        }
      });
      console.log("value:" + value + " key: " + key);
      buildCharts(value, key);
    });
  }

  if ($('#single').length > 0) {

    d3.json("/ticker").then((symbol) => {
      console.log(symbol)
      var select1 = d3.select("#all_tickers1");
      var select2 = d3.select("#all_tickers2");
      var select3 = d3.select("#all_tickers3");
      symbol.forEach((data) => {
        select1
          .append("option")
          .text(data)
          .property("value", data);
        select2
          .append("option")
          .text(data)
          .property("value", data);
        select3
          .append("option")
          .text(data)
          .property("value", data);
      });
    });

    var slider1 = $('.amount1.slider')[0];
    var slider2 = $('.amount2.slider')[0];
    var slider3 = $('.amount3.slider')[0];
    slider1.oninput = function() {
      slider2.max = 10000 - slider3.value - this.value;
      slider3.max = 10000 - slider2.value - this.value;
      $('.tickerValue1').empty().html('$' + this.value);
      $('.slider2.max_value').empty().html(slider2.max);
      $('.slider3.max_value').empty().html(slider3.max);
    }
    slider2.oninput = function () {
      slider1.max = 10000 - slider3.value - this.value;
      slider3.max = 10000 - slider1.value - this.value;
      $('.tickerValue2').empty().html('$' + this.value);
      $('.slider1.max_value').empty().html(slider1.max);
      $('.slider3.max_value').empty().html(slider3.max);
    }
    slider3.oninput = function () {
      slider1.max = 10000 - slider2.value - this.value;
      slider2.max = 10000 - slider1.value - this.value;
      $('.tickerValue3').empty().html('$' + this.value);
      $('.slider1.max_value').empty().html(slider1.max);
      $('.slider2.max_value').empty().html(slider2.max);
    }
  }

  // Initialize the dashboard
  if ($('#index').length > 0) {
    initHomePage();
  }

});
