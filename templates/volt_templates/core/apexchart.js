var options = {
    chart: {
      type: 'line'
    },
    series: [{
      name: 'Portfolio value',
      data: {{portfolio_equity_values|safe}}
    }],
    xaxis: {
      categories: {{portfolio_equity_dates|safe}}

    },
    theme: {
      palette: 'palette5' // upto palette10
    }
  }
  

  var chart = new ApexCharts(document.querySelector("#chart"), options);
  
  chart.render();