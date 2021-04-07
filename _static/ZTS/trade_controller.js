//--------------------------------------------------------------------------------
// Main Script
//--------------------------------------------------------------------------------
function $_(x) {return document.getElementById(x);} // standard $ is already used by jQuery
$('.otree-btn-next').hide();

// settings variables
var refresh_rate = js_vars.refresh_rate;

// portfolio variables
var data = js_vars.data;                            // data from timeseries file
var cur_day = 0;                                    // current market day starts at 0
var length = js_vars.length;                        // length of data
var news = js_vars.news;                            // list of news that should be displayed
var start_cash = parseFloat(js_vars.cash);          // amount of initial cash
var cash = start_cash;                              // amount of cash
var shares = 0                                      // amount of initial shares a player holds
var share_value = 0;                                // value of shares at current day
var total = cash;                                   // current cash + value of share in possession
var roi_percent = 0.0;                              // Return of Investment in percents
var pandl = 0.0;                                    // Profit & Loss

// chart variables
var y_axis_offset = Math.min(10, 0.25 * data[0]);   // current length of y axis from center
var trading_happened = false;
var finished = false;

/*------------------------------------------------------------------
Function that simulates a day in the market:
    - first buy shares with half of cash
    - updates chart
    - updates portfolio table
------------------------------------------------------------------*/

// setup and first iteration
var chart = init_chart();
update_y_axis(data[0]);
chart.series[0].addPoint([cur_day, data[0]], true, false);
buy_half_shares();
set_buy_sell_amounts();
liveSend(get_trade_report('Start', data[0], 0));

// wait until first interval is over before continuing
setTimeout(function () {
}, refresh_rate);

var interval_func = setInterval(function () {
    // As function is called only at beginning of interval
    // any cleanup of previous interval has to be done at
    // beginning of current interval!

    //----------- clean up of last interval ----------

    // send 'HOLD' report of previous interval
    if(!trading_happened) liveSend(get_trade_report('Hold', data[cur_day], 0));
    trading_happened = false;

    // end interval and send 'END' report if no days left
    if(cur_day >= length-1) {
        clearInterval(interval_func);
        finished = true;
        liveSend(get_trade_report('End', y, 0));
        $('.otree-btn-next').show();
    }

    //----------- start of current interval ----------

    else {
        ++cur_day;
        y = data[cur_day];

        // update chart
        update_y_axis(y);
        chart.series[0].addPoint([cur_day, y], true, false);

        // update views
        $_('table_cash').innerHTML = to_comma_seperated(cash);
        $_('table_shares').innerHTML = to_comma_seperated(shares);
        update_portfolio();
        $_('trade_price').innerHTML = data[cur_day].toFixed(2);
        $_('trade_news').innerHTML = news[cur_day];
    }

}, refresh_rate);

/*------------------------------------------------------------------
Trading Logic:
    - function to buy shares with half of cash (for initialization)
    - function for setting reasonable sell/buy amounts on button
    - on-click-listeners on all buttons in trade
    - functions for buying and selling shares
--------------------------------------------------------------------*/
function buy_half_shares() {
    // Makes a fair split of cash and shares with start money for initialization
    var half_cash = cash / 2.0;
    var half_shares = Math.round(half_cash / data[0]);
    cash -= half_shares * data[0];
    shares = half_shares;
    liveSend(get_trade_report('Buy', data[0], half_shares));
    update_portfolio();

}

function set_buy_sell_amounts() {
    // Values for Buttons are very important b.c. they influence greatly how
    // many shares somebody buys, we tried to make reasonable Values here
    // for most situations. Also we tried to make somewhat nice values (/10*10)
    var min = Math.min.apply(Math, data);
    var max_shares = (Math.ceil((cash/min) / 10) * 10);
    var button_m = Math.max(10, Math.ceil((max_shares/10) / 10) * 10);  // roughly 10 percent of current shares
    $_('trade_btn_sell_m').innerHTML = "Sell " + button_m;
    $_('trade_btn_sell_m').value = button_m;
    $_('trade_btn_buy_m').innerHTML = "Buy " + button_m;
    $_('trade_btn_buy_m').value = button_m;

    var button_l = Math.max(20, Math.ceil((max_shares/5) / 10) * 10)  // roughly 20 percent of current shares
    $_('trade_btn_sell_l').innerHTML = "Sell " + button_l;
    $_('trade_btn_sell_l').value = button_l;
    $_('trade_btn_buy_l').innerHTML = "Buy " + button_l;
    $_('trade_btn_buy_l').value = button_l;
}

function buy_shares(amount) {
    amount = parseFloat(amount);
    if(cur_day > 0 && !finished) {
        var cur_price = data[cur_day];
        var cur_total = amount * cur_price;
        if(cur_total <= cash) {
            // We have enough cash to buy amount of shares
            cash -= cur_total;
            shares += amount;
            $_('table_cash').innerHTML = to_comma_seperated(cash);
            $_('table_shares').innerHTML = to_comma_seperated(shares);
            update_portfolio();
            trading_happened = true;

            // send report to server
            liveSend(get_trade_report('Buy', cur_price, amount));
            toastr.success('Success!');
        }
        // else if(cash > 0) {
        //     // We don't have enough cash, but buy as much as possible
        //     var available_amount = cash / cur_price;
        //     cash = 0;
        //     shares += available_amount;
        //     $_('table_cash').innerHTML = to_comma_seperated(cash);
        //     $_('table_shares').innerHTML = to_comma_seperated(shares);

        //     // send report to server
        //     liveSend(get_trade_report('Buy', cur_price, available_amount));
        //     toastr.success('Bought '+available_amount+' shares!');
        // }
        else {
            // We have no cash
            toastr.error('No money!');
        }
    }
}

function sell_shares(amount) {
    amount = parseFloat(amount);
    if(cur_day > 0 && !finished) {
        var cur_price = data[cur_day];
        var cur_shares = shares;
        var cur_total = amount * cur_price;
        if(amount <= cur_shares) {
            // we have enough shares to sell amount
            cash += cur_total;
            shares -= amount;
            $_('table_cash').innerHTML = to_comma_seperated(cash);
            $_('table_shares').innerHTML = to_comma_seperated(shares);
            update_portfolio();
            trading_happened = true;

            // send report to server
            liveSend(get_trade_report('Sell', cur_price, -amount));
            toastr.success('Success!');
        }
        // else if(cur_shares > 0) {
        //     // we don't have enough, but sell rest
        //     var available_amount = cur_shares;
        //     shares = 0;
        //     cash += available_amount * cur_price;
        //     $_('table_cash').innerHTML = to_comma_seperated(cash);
        //     $_('table_shares').innerHTML = to_comma_seperated(shares);

        //     // send report to server
        //     liveSend(get_trade_report('Sell', cur_price, -available_amount));
        //     toastr.success('Sold remaining '+available_amount+' shares!');
        // }
        else {
            // we have no shares left
            toastr.error('No Shares!');
        }
    }
}

/*------------------------------------------------------------------
Portfolio Logic:
    - update portfolio
------------------------------------------------------------------*/
function update_portfolio() {
    share_value = shares * data[cur_day];
    total = cash + share_value;
    pandl = total - start_cash;
    roi_percent = ((total/start_cash)*100) - 100;
    $_('table_share_value').innerHTML = to_comma_seperated(share_value);
    $_('table_total').innerHTML = to_comma_seperated(total);
    $_('table_pandl').innerHTML = to_comma_seperated(pandl);
}

/*------------------------------------------------------------------
Chart Logic:
    - update y axis min and max in chart if necessary
------------------------------------------------------------------*/
function update_y_axis(y) {
    var new_y_offset = Math.abs(y - data[0]);
    //alert("Update y_axis: " + new_y_offset + " " + y_axis_offset);
    if(new_y_offset > y_axis_offset) {
        y_axis_offset = Math.abs(y - data[0]);
        var y_axis_min = data[0] - y_axis_offset;
        var y_axis_max = data[0] + y_axis_offset;
        //alert("Update y_axis");
        chart.yAxis[0].setExtremes(y_axis_min, y_axis_max);
    }
}

/*------------------------------------------------------------------
Helper Functions:
    - get a dictionary with all the info for a trade
    - get current date & time
------------------------------------------------------------------*/
function get_trade_report(action, cur_price, amount) {
    var report_data = {
        "action": action,
        "quantity": amount,
        "price_per_share": cur_price,
        "cash": cash,
        "owned_shares": shares,
        "share_value": share_value,
        "portfolio_value": total,
        "cur_day": cur_day,
        "asset": "SMI",
        "roi_percent": roi_percent,
        "pandl": pandl
    };
    return report_data;
}

function get_time() {
    var today = new Date();
    var date = today.getFullYear()+'-'+(today.getMonth()+1)+'-'+today.getDate();
    var time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
    return date+' '+time;
}

function to_comma_seperated(amount) {
    x = parseInt(amount)
    x = x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    return x;
}

