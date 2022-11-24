//--------------------------------------------------------------------------------
// Trade Controller Script
//--------------------------------------------------------------------------------
function $_(x) {return document.getElementById(x);} // standard $ is already used by jQuery
$('.otree-btn-next').hide();

// static settings variables
const refresh_rate = js_vars.refresh_rate;              // duration of a day in ms
const graph_buffer = js_vars.graph_buffer;              // buffer margin at top and bottom of chart [0, 1]
const prices = JSON.parse('[' + js_vars.prices + ']');  // prices from timeseries file
const length = prices.length;                           // length of prices
const news = js_vars.news;                              // list of news that should be displayed
const asset = js_vars.asset;                            // name of the asset (name of the timeseries file)
const start_cash = parseFloat(js_vars.cash);            // amount of initial cash
const start_shares = parseInt(js_vars.shares);          // amount of initial shares
const restore = localStorage.cur_day ? true : false;    // check if page was refreshed and we continue where we left off

// dynamic portfolio variables 
// NOTE: store relevant vars in localStorage, so they are not lost if page is refreshed, or session restarted
if (!restore) {
    localStorage.cur_day = 0;                                   // current day initialized to zero
    localStorage.cash = start_cash;                             // amount of cash
    localStorage.shares = start_shares;                         // amount of initial shares a player holds
    localStorage.y_axis_offset = Math.min(1, 0.25 * prices[0]); // initial length of y axis from center
}
var y = prices[parseInt(localStorage.cur_day)]              // current share price
var share_value = 0.0                                       // value of shares at current day
var total = parseFloat(localStorage.cash);                  // current cash + value of share in possession
var roi_percent = 0.0;                                      // return of Investment in percents
var pandl = 0.0;                                            // profit & Loss

/*------------------------------------------------------------------
Function that simulates a day in the market:
    - first buy shares with half of cash
    - updates chart
    - updates portfolio table
------------------------------------------------------------------*/

// setup and first iteration
set_buy_sell_amounts();
var chart = init_chart(prices.slice(0, parseInt(localStorage.cur_day) + 1));
update_y_axis(y);
if (!restore) {
    liveSend(get_trade_report('Start', prices[0], 0));
}

// wait until first interval is over before continuing
setTimeout(function () {
}, refresh_rate);

var interval_func = setInterval(function () {
    // As function is called only at beginning of interval
    // any cleanup of previous interval has to be done at
    // beginning of current interval!

    //----------- clean up of last interval ----------

    // end interval and send 'END' report if no days left
    if(parseInt(localStorage.cur_day) >= length - 1) {
        clearInterval(interval_func);
        liveSend(get_trade_report('End', y, 0));
        alert('Current round has finished, you can continue by clicking ok and then next.');
        disable_buttons();
        localStorage.clear();
        $('.otree-btn-next').show();

    //----------- start of current interval ----------

    } else {
        localStorage.cur_day = parseInt(localStorage.cur_day) + 1;
        y = prices[parseInt(localStorage.cur_day)];

        // update chart
        update_y_axis(y);
        chart.series[0].addPoint([parseInt(localStorage.cur_day), y], true, false);

        // update views
        update_portfolio();
        $_('trade_price').innerHTML = prices[parseInt(localStorage.cur_day)].toFixed(2);
        $_('trade_news').innerHTML = news[parseInt(localStorage.cur_day)];
    }

}, refresh_rate);

/*------------------------------------------------------------------
Trading Logic:
    - function for setting reasonable sell/buy amounts on button
    - on-click-listeners on all buttons in trade
    - functions for buying and selling shares
--------------------------------------------------------------------*/
function set_buy_sell_amounts() {
    values = js_vars.trading_button_values;
    $_('trade_btn_sell_s').innerHTML = "Sell " + values[0];
    $_('trade_btn_sell_s').value = values[0];
    $_('trade_btn_buy_s').innerHTML = "Buy " + values[0];
    $_('trade_btn_buy_s').value = values[0];
    $_('trade_btn_sell_m').innerHTML = "Sell " + values[1];
    $_('trade_btn_sell_m').value = values[1];
    $_('trade_btn_buy_m').innerHTML = "Buy " + values[1];
    $_('trade_btn_buy_m').value = values[1];
    $_('trade_btn_sell_l').innerHTML = "Sell " + values[2];
    $_('trade_btn_sell_l').value = values[2];
    $_('trade_btn_buy_l').innerHTML = "Buy " + values[2];
    $_('trade_btn_buy_l').value = values[2];
}

function buy_shares(amount) {
    amount = parseInt(amount);
    if(parseInt(localStorage.cur_day)) {
        var cur_price = prices[parseInt(localStorage.cur_day)];
        var cur_total = amount * cur_price;
        if(cur_total <= parseFloat(localStorage.cash)) {
            // We have enough cash to buy amount of shares
            localStorage.cash = parseFloat(localStorage.cash) - cur_total;
            localStorage.shares = parseInt(localStorage.shares) + amount;
            update_portfolio();

            // send report to server
            liveSend(get_trade_report('Buy', cur_price, amount));
            toastr.remove(); toastr.success('Success!');
        }
        else if(parseFloat(localStorage.cash) > 0) {
            // We don't have enough cash, but buy as much as possible
            var available_amount = Math.floor(parseFloat(localStorage.cash) / cur_price);
            localStorage.cash = 0;
            localStorage.shares = parseInt(localStorage.shares) + available_amount;
            update_portfolio();
            // send report to server
            liveSend(get_trade_report('Buy', cur_price, available_amount));
            toastr.remove(); toastr.success('Bought '+available_amount+' shares!');
        }
        else {
            // We have no cash
            toastr.remove(); toastr.error('No money!');
        }
    }
}

function sell_shares(amount) {
    amount = parseInt(amount);
    if(parseInt(localStorage.cur_day) > 0) {
        var cur_price = prices[parseInt(localStorage.cur_day)];
        var cur_shares = parseInt(localStorage.shares);
        var cur_total = amount * cur_price;
        if(amount <= cur_shares) {
            // we have enough shares to sell amount
            localStorage.cash = parseFloat(localStorage.cash) + cur_total;
            localStorage.shares = parseInt(localStorage.shares) - amount;
            update_portfolio();
            // send report to server
            liveSend(get_trade_report('Sell', cur_price, -amount));
            toastr.remove(); toastr.success('Success!');
        }
         else if(cur_shares > 0) {
            // we don't have enough, but sell rest
            var available_amount = cur_shares;
            localStorage.shares = 0;
            localStorage.cash = parseFloat(localStorage.cash) + available_amount * cur_price;
            update_portfolio();
            // send report to server
            liveSend(get_trade_report('Sell', cur_price, -available_amount));
            toastr.remove(); toastr.success('Sold remaining '+available_amount+' shares!',);
         }
        else {
            // we have no shares left
            toastr.remove(); toastr.error('No Shares!');
        }
    }
}

/*------------------------------------------------------------------
Portfolio Logic:
    - update portfolio
------------------------------------------------------------------*/
function update_portfolio() {
    share_value = parseInt(localStorage.shares) * prices[parseInt(localStorage.cur_day)];
    total = parseFloat(localStorage.cash) + share_value;
    pandl = total - start_cash;
    roi_percent = ((total/start_cash)*100) - 100;
    $_('table_cash').innerHTML = to_comma_separated(parseFloat(localStorage.cash));
    $_('table_shares').innerHTML = to_comma_separated(parseInt(localStorage.shares));
    $_('table_share_value').innerHTML = to_comma_separated(share_value);
    $_('table_total').innerHTML = to_comma_separated(total);
    $_('table_pandl').innerHTML = to_comma_separated(pandl);
}

/*------------------------------------------------------------------
Chart Logic:
    - update y axis min and max in chart if necessary
------------------------------------------------------------------*/
function update_y_axis(y) {
    var y_axis_offset = parseFloat(localStorage.y_axis_offset)
    var new_y_offset = Math.abs(y - prices[0]) * (1 + graph_buffer);
    if(new_y_offset > y_axis_offset) {
        localStorage.y_axis_offset = new_y_offset;
        var y_axis_min = prices[0] - new_y_offset;
        var y_axis_max = prices[0] + new_y_offset;
        chart.yAxis[0].setExtremes(y_axis_min, y_axis_max);
    }
}

/*------------------------------------------------------------------
Helper Functions:
    - get a dictionary with all the info for a trade
    - disable the buttons once trading period is over
    - get current date & time
    - to comma seperated adds a comma for thousands for readability
------------------------------------------------------------------*/
function get_trade_report(action, cur_price, amount) {
    var report_data = {
        "action": action,
        "quantity": amount,
        "time": get_datetime(),
        "price_per_share": cur_price,
        "cash": parseFloat(localStorage.cash),
        "owned_shares": parseInt(localStorage.shares),
        "share_value": share_value,
        "portfolio_value": total,
        "cur_day": parseInt(localStorage.cur_day),
        "asset": asset,
        "roi_percent": roi_percent,
        "pandl": pandl
    };
    return report_data;
}

function disable_buttons() {
    $_('trade_btn_sell_s').disabled = true;
    $_('trade_btn_sell_m').disabled = true;
    $_('trade_btn_sell_l').disabled = true;
    $_('trade_btn_buy_s').disabled = true;
    $_('trade_btn_buy_m').disabled = true;
    $_('trade_btn_buy_l').disabled = true;
}

function get_datetime() {
    var today = new Date();
    var date = today.getFullYear()+'-'+(today.getMonth()+1)+'-'+today.getDate();
    var time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
    return date+' '+time;
}

function to_comma_separated(amount) {
    x = parseInt(amount)
    x = x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    return x;
}