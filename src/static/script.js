window.onload = () => {
    switch(chartData.method){
        case 'sma':        
            plotSmaChart()
            break
        case 'macd':        
            plotMacdChart()
            break
        default:
            plotSmaChart()
            plotMacdChart()
            break
    }

    persistCriteria(chartData.method, chartData.period)
    printRecommendationsTable(chartData.recommendations)
}

function persistCriteria(method, period) {
    document.querySelector('#method').value = method
    document.querySelector('#period').value = period
}


function printRecommendationsTable(tableHTML) {
    var divTable = document.querySelector('#div-table')
    divTable.innerHTML = tableHTML
    
    var table = divTable.children[0]
    table.id = 'recommendations'
    table.removeAttribute('border')
    table.classList.remove('dataframe')
    table.classList.add('table')
    //TODO: Uncomment the line below once there's a link to the recommendations' sources article
    //table.classList.add('table-hover')        
    
    var tableBody = table.getElementsByTagName('tbody')[0]
    var tableRows = tableBody.getElementsByTagName('tr')

    for (var i = 0; i < tableRows.length;i++) {
        colorTRow(tableRows[i])
    }
}

function colorTRow(row) {
    var rowContent = row.children[2].innerHTML.toLowerCase();
    var hold = rowContent.includes('hold')
    var buy = rowContent.includes('buy')
    var overweight = rowContent.includes('overweight')
    var outperform = rowContent.includes('outperform')
    var marketPerform = rowContent.includes('market perform')
    var equalWeight = rowContent.includes('equal-weight')

    if (hold) { row.classList.add('table-info') } 
    else if (buy) { row.classList.add('table-success') }
    else if (overweight) { row.classList.add('table-secondary') }
    else if (outperform) { row.classList.add('table-dark') } 
    else if (marketPerform) { row.classList.add('table-primary') } 
    else if (equalWeight) { row.classList.add('table-light') }
}

function plotSmaChart() {
    var data = [
        chartData.history,
        chartData.sma30,
        chartData.sma100,
        chartData.bid,
        chartData.ask
    ]
    var layout = {
        title: chartData.layout.title,
        showlegend: true                  
    }
    var config = {
        scrollZoom: true,
        responsive: true
    }
    Plotly.newPlot('sma-chart', data, layout, config)
}

function plotMacdChart() {
    var data = [
        chartData.history,
        //chartData.macd,
        //chartData.signal,
        chartData.bid,
        chartData.ask
    ]
    var layout = {
        title: chartData.layout.title,
        showlegend: true                  
    }
    var config = {
        scrollZoom: true,
        responsive: true
    }
    Plotly.newPlot('macd-chart', data, layout, config)
}