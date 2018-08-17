
/**
 * Created by samsung1 on 2018/5/10.
 */
 //默认三十天
$('#divDateId input').val(moment().subtract('days', 29).format('YYYY-MM-DD') + ' - ' + moment().format('YYYY-MM-DD'));
$('#divDateId').daterangepicker({
    minDate: '01/01/2015',  //最小时间
    maxDate : moment(), //最大时间
    dateLimit : {
        days : 365*5
    }, //起止时间的最大间隔
    showDropdowns : true,
    showWeekNumbers : false, //是否显示第几周
    timePicker : false, //是否显示小时和分钟
    timePickerIncrement : 60, //时间的增量，单位为分钟
    timePicker12Hour : false, //是否使用12小时制来显示时间
    ranges : {
        //'最近1小时': [moment().subtract('hours',1), moment()],
        '今日': [moment().startOf('day'), moment()],
        '昨日': [moment().subtract('days', 1).startOf('day'), moment().subtract('days', 1).endOf('day')],
        '最近7日': [moment().subtract('days', 6), moment()],
        '最近30日': [moment().subtract('days', 29), moment()]
    },
    opens : 'right', //日期选择框的弹出位置
    buttonClasses : [ 'btn btn-default' ],
    applyClass : 'btn-small btn-primary blue',
    cancelClass : 'btn-small',
    format : 'YYYY-MM-DD', //控件中from和to 显示的日期格式
    separator : ' to ',
    locale : {
        applyLabel : '确定',
        cancelLabel : '取消',
        fromLabel : '起始时间',
        toLabel : '结束时间',
        customRangeLabel : '自定义',
        daysOfWeek : [ '日', '一', '二', '三', '四', '五', '六' ],
        monthNames : [ '一月', '二月', '三月', '四月', '五月', '六月',
                       '七月', '八月', '九月', '十月', '十一月', '十二月' ],
                       firstDay : 1
    }   //汉化日期控件
}, function(start, end, label) {
    //格式化日期显示框
    $('#searchDate').val(start.format('YYYY-MM-DD') + ' - ' + end.format('YYYY-MM-DD'));
});

$('#show_data').click(function () {
    var figure_data = $('#figure_data').val();
    // 获取前端选择的日期
    var datarange_data = $('#searchDate').val();
    var x_data = $('#x_data').val();
    var y_data = $('#y_data').val();
    var keyword = $('#keyword').val();
    var data = JSON.stringify({'figure_data':figure_data,'datarange_data':datarange_data,'x_data':x_data,'y_data':y_data,'keyword':keyword});
        $.ajax({
        "type":'POST',
        "url": '/show_figure_data',
        "data": data,
        success:function (data_r) {
            data_res = jQuery.parseJSON(data_r);
            if (data_res['code'] == 500) {
                alert(data_res['message'])
            } else {
                if (data_res['data_s']['figure_data'] == '折线图') {
                    return heightchart_zheixan(data_res['data_s']);
                }else if(data_res['data_s']['figure_data'] == '饼形图'){

                    return heightchart_bingxing(data_res['data_s']);
                }else if(data_res['data_s']['figure_data'] == '柱状图'){
                    return heightchart_zhuzhuang(data_res['data_s']);
                }else  if(data_res['data_s']['figure_data'] == '词云图'){
                    return heightchart_ciyun(data_res['data_s']);
                }else if(data_res['data_s']['figure_data'] == '分布图'){
                    return heightchart_china(data_res['data_s']);
                }
            }
        }
    })

})

$(document).ready(function() {
    $.get( "/show_index_web_num", function( data ) {
        var data_index = jQuery.parseJSON(data)
        Highcharts.chart('container', {
        title: {
            text: '三个发布网站近七天的发布数据统计展示'
        },
        yAxis: {
            title: {
                text: '职位发布数'
            }
        },
        xAxis: {
            categories: data_index['times']
        },
        credits: {
            enabled: false
        },
        legend: {
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'middle'
        },
        series: [{
            name: 'BOSS网',
            data: data_index['boss']
        }, {
            name: '拉勾网',
            data: data_index['lagou']
        }, {
            name: '智联网',
            data: data_index['zhilian']
        }],
        responsive: {
            rules: [{
                condition: {
                    maxWidth: 500
                },
                chartOptions: {
                    legend: {
                        layout: 'horizontal',
                        align: 'center',
                        verticalAlign: 'bottom'
                    }
                }
            }]
        }
    });
    });
});
function heightchart_zheixan(data_res){ Highcharts.chart('container', {
            title: {
                    text: ''
            },
            yAxis: {
                    title: {
                            text:'number'
                            // text: data_res['y_data']
                    }
            },
            xAxis: {
                    title: {
                            text: ''
                    }
            },
            credits: {
                  enabled:false
            },
            legend: {
                    layout: 'vertical',
                    align: 'right',
                    verticalAlign: 'middle'
            },xAxis: {
                categories: data_res['x_list']
                },
            series: [ {
                    name: data_res['data']['name'],
                    data: data_res['data']['data']
            }],
            responsive: {
                    rules: [{
                            condition: {
                                    maxWidth: 500
                            },
                            chartOptions: {
                                    legend: {
                                            layout: 'horizontal',
                                            align: 'center',
                                            verticalAlign: 'bottom'
                                    }
                            }
                    }]
            }
        });}

// $(document).ready(function() {
//     //任何需要执行的js特效
//     var show_figure = $('#figure_data').val();
//     if(show_figure =='柱状图'){
//         document.getElementById("y_data").disabled=true;
//     }
// });

$(document).ready(function(){
　　　　$('#figure_data').change(function(){
            var show_figure =  $(this).children('option:selected').val();
            if(show_figure=='柱状图'  ){
                document.getElementById("y_data").disabled=true;
            }else  if(show_figure=='分布图'){
                document.getElementById("y_data").disabled=true;
            }else if(show_figure == '词云图'){
                    document.getElementById("y_data").disabled=false;
                    var selObj = $("#y_data");
                    var value="职位名称";
                    var text="职位名称";
                    selObj.append("<option value='"+value+"'>"+text+"</option>");
            }else{
                document.getElementById("y_data").disabled=false;

            }
　　　　})
})
function heightchart_bingxing(data){
    var data_w = data['y_data']
    var colors = Highcharts.getOptions().colors,
    categories = ['BOSS', '拉勾', '智联'],
    data = [{
        y: data['boss']['sum'],
        color: colors[0],
        drilldown: {
            name: 'BOSS',
            categories: data['boss']['data_l'],
            data: data['boss']['data'],
            color: colors[0]
        }
    }, {
        y: data['lagou']['sum'],
        color: colors[1],
        drilldown: {
            name: '拉勾',
            categories: data['lagou']['data_l'],
            data:data['lagou']['data'],
            color: colors[3]
        }
    }, {
        y: data['zhilian']['sum'],
        color: colors[2],
        drilldown: {
            name: '智联',
            categories: data['zhilian']['data_l'],
            data: data['zhilian']['data'],
            color: colors[4]
        }
    }],
    browserData = [],
    versionsData = [],
    i,
    j,
    dataLen = data.length,
    drillDataLen,
    brightness;
// 构建数据数组
for (i = 0; i < dataLen; i += 1) {
    // 添加数据
    browserData.push({
        name: categories[i],
        y: data[i].y,
        color: data[i].color
    });
    // 添加版本数据
    drillDataLen = data[i].drilldown.data.length;
    for (j = 0; j < drillDataLen; j += 1) {
        brightness = 0.2 - (j / drillDataLen) / 5;
        versionsData.push({
            name: data[i].drilldown.categories[j],
            y: data[i].drilldown.data[j],
            color: Highcharts.Color(data[i].color).brighten(brightness).get()
        });
    }
}
// 创建图表

Highcharts.chart('container',{
    chart: {
        type: 'pie'
    },
    title: {
        text: '发布数据占比统计'
    },
    subtitle: {
        text: '内环为发布网站占比，外环为具体的【'+data_w+'】占比'
    },
    credits: {
                  enabled:false
            },
    yAxis: {
        title: {
            text: '总百分比市场份额'
        }
    },
    plotOptions: {
        pie: {
            shadow: false,
            center: ['50%', '50%']
        }
    },
    tooltip: {
        valueSuffix: '%'
    },
    series: [{
        name: '发布数量',
        data: browserData,
        size: '60%', // 指定饼图大小
        dataLabels: {
            formatter: function () {
                return this.y > 5 ? this.point.name : null;
            },
            color: 'white',
            distance: -30
        }
    }, {
        name: '具体占比',
        data: versionsData,
        size: '80%',  // 指定大小
        innerSize: '60%', // 指定内环大小
        dataLabels: {
            formatter: function () {
                // 大于1则显示
                return this.y > 1 ? '<b>' + this.point.name + ':</b> ' + this.y + '%'  : null;
            }
        }
    }]
});
}

function heightchart_zhuzhuang(data){
Highcharts.chart('container',{
    chart: {
        type: 'column'
    },
    credits: {
                  enabled:false
            },
    title: {
        text: '近一年月发布招聘信息量'
    },
    subtitle: {
        text: '数据来源: Ocean Jobs'
    },
    xAxis: {
        categories: data['month'],
        crosshair: true
    },
    yAxis: {
        min: 0,
        title: {
            text: '条'
        }
    },
    tooltip: {
        // head + 每个 point + footer 拼接成完整的 table
        headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
        pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
        '<td style="padding:0"><b>{point.y:.1f} 条</b></td></tr>',
        footerFormat: '</table>',
        shared: true,
        useHTML: true
    },
    plotOptions: {
        column: {
            borderWidth: 0
        }
    },
    series: [{
        name: 'BOSS',
        data: data['data']['boss']
    }, {
        name: '拉勾',
        data: data['data']['lagou']
    }, {
        name: '智联',
        data: data['data']['zhilian']
    }]
});}

function heightchart_ciyun(data){
    var text = data['data'];
    var data = text
    .split(/[,\. ]+/g)
    .reduce(function (arr, word) {
        var obj = arr.find(function (obj) {
            return obj.name === word;
        });
        if (obj) {
            obj.weight += 1;
        } else {
            obj = {
                name: word,
                weight: 1
            };
            arr.push(obj);
        }
        return arr;
    }, []);
    Highcharts.chart('container', {
        series: [{
            type: 'wordcloud',
            data: data
        }],
        credits: {
                  enabled:false
            },
        title: {
            text: '词云图'
        }
    });

}
function heightchart_china(data){
		var dom = document.getElementById("container");
        var myChart = echarts.init(dom);
        var app = {};
        option = null;
        var geoCoordMap = {
            "海门":[121.15,31.89],
            "鄂尔多斯":[109.781327,39.608266],
            "招远":[120.38,37.35],
            "舟山":[122.207216,29.985295],
            "齐齐哈尔":[123.97,47.33],
            "盐城":[120.13,33.38],
            "赤峰":[118.87,42.28],
            "青岛":[120.33,36.07],
            "乳山":[121.52,36.89],
            "金昌":[102.188043,38.520089],
            "泉州":[118.58,24.93],
            "莱西":[120.53,36.86],
            "日照":[119.46,35.42],
            "胶南":[119.97,35.88],
            "南通":[121.05,32.08],
            "拉萨":[91.11,29.97],
            "云浮":[112.02,22.93],
            "梅州":[116.1,24.55],
            "文登":[122.05,37.2],
            "上海":[121.48,31.22],
            "攀枝花":[101.718637,26.582347],
            "威海":[122.1,37.5],
            "承德":[117.93,40.97],
            "厦门":[118.1,24.46],
            "汕尾":[115.375279,22.786211],
            "潮州":[116.63,23.68],
            "丹东":[124.37,40.13],
            "太仓":[121.1,31.45],
            "曲靖":[103.79,25.51],
            "烟台":[121.39,37.52],
            "福州":[119.3,26.08],
            "瓦房店":[121.979603,39.627114],
            "即墨":[120.45,36.38],
            "抚顺":[123.97,41.97],
            "玉溪":[102.52,24.35],
            "张家口":[114.87,40.82],
            "阳泉":[113.57,37.85],
            "莱州":[119.942327,37.177017],
            "湖州":[120.1,30.86],
            "汕头":[116.69,23.39],
            "昆山":[120.95,31.39],
            "宁波":[121.56,29.86],
            "湛江":[110.359377,21.270708],
            "揭阳":[116.35,23.55],
            "荣成":[122.41,37.16],
            "连云港":[119.16,34.59],
            "葫芦岛":[120.836932,40.711052],
            "常熟":[120.74,31.64],
            "东莞":[113.75,23.04],
            "河源":[114.68,23.73],
            "淮安":[119.15,33.5],
            "泰州":[119.9,32.49],
            "南宁":[108.33,22.84],
            "营口":[122.18,40.65],
            "惠州":[114.4,23.09],
            "江阴":[120.26,31.91],
            "蓬莱":[120.75,37.8],
            "韶关":[113.62,24.84],
            "嘉峪关":[98.289152,39.77313],
            "广州":[113.23,23.16],
            "延安":[109.47,36.6],
            "太原":[112.53,37.87],
            "清远":[113.01,23.7],
            "中山":[113.38,22.52],
            "昆明":[102.73,25.04],
            "寿光":[118.73,36.86],
            "盘锦":[122.070714,41.119997],
            "长治":[113.08,36.18],
            "深圳":[114.07,22.62],
            "珠海":[113.52,22.3],
            "宿迁":[118.3,33.96],
            "咸阳":[108.72,34.36],
            "铜川":[109.11,35.09],
            "平度":[119.97,36.77],
            "佛山":[113.11,23.05],
            "海口":[110.35,20.02],
            "江门":[113.06,22.61],
            "章丘":[117.53,36.72],
            "肇庆":[112.44,23.05],
            "大连":[121.62,38.92],
            "临汾":[111.5,36.08],
            "吴江":[120.63,31.16],
            "石嘴山":[106.39,39.04],
            "沈阳":[123.38,41.8],
            "苏州":[120.62,31.32],
            "茂名":[110.88,21.68],
            "嘉兴":[120.76,30.77],
            "长春":[125.35,43.88],
            "胶州":[120.03336,36.264622],
            "银川":[106.27,38.47],
            "张家港":[120.555821,31.875428],
            "三门峡":[111.19,34.76],
            "锦州":[121.15,41.13],
            "南昌":[115.89,28.68],
            "柳州":[109.4,24.33],
            "三亚":[109.511909,18.252847],
            "自贡":[104.778442,29.33903],
            "吉林":[126.57,43.87],
            "阳江":[111.95,21.85],
            "泸州":[105.39,28.91],
            "西宁":[101.74,36.56],
            "宜宾":[104.56,29.77],
            "呼和浩特":[111.65,40.82],
            "成都":[104.06,30.67],
            "大同":[113.3,40.12],
            "镇江":[119.44,32.2],
            "桂林":[110.28,25.29],
            "张家界":[110.479191,29.117096],
            "宜兴":[119.82,31.36],
            "北海":[109.12,21.49],
            "西安":[108.95,34.27],
            "金坛":[119.56,31.74],
            "东营":[118.49,37.46],
            "牡丹江":[129.58,44.6],
            "遵义":[106.9,27.7],
            "绍兴":[120.58,30.01],
            "扬州":[119.42,32.39],
            "常州":[119.95,31.79],
            "潍坊":[119.1,36.62],
            "重庆":[106.54,29.59],
            "台州":[121.420757,28.656386],
            "南京":[118.78,32.04],
            "滨州":[118.03,37.36],
            "贵阳":[106.71,26.57],
            "无锡":[120.29,31.59],
            "本溪":[123.73,41.3],
            "克拉玛依":[84.77,45.59],
            "渭南":[109.5,34.52],
            "马鞍山":[118.48,31.56],
            "宝鸡":[107.15,34.38],
            "焦作":[113.21,35.24],
            "句容":[119.16,31.95],
            "北京":[116.46,39.92],
            "徐州":[117.2,34.26],
            "衡水":[115.72,37.72],
            "包头":[110,40.58],
            "绵阳":[104.73,31.48],
            "乌鲁木齐":[87.68,43.77],
            "枣庄":[117.57,34.86],
            "杭州":[120.19,30.26],
            "淄博":[118.05,36.78],
            "鞍山":[122.85,41.12],
            "溧阳":[119.48,31.43],
            "库尔勒":[86.06,41.68],
            "安阳":[114.35,36.1],
            "开封":[114.35,34.79],
            "济南":[117,36.65],
            "德阳":[104.37,31.13],
            "温州":[120.65,28.01],
            "九江":[115.97,29.71],
            "邯郸":[114.47,36.6],
            "临安":[119.72,30.23],
            "兰州":[103.73,36.03],
            "沧州":[116.83,38.33],
            "临沂":[118.35,35.05],
            "南充":[106.110698,30.837793],
            "天津":[117.2,39.13],
            "富阳":[119.95,30.07],
            "泰安":[117.13,36.18],
            "诸暨":[120.23,29.71],
            "郑州":[113.65,34.76],
            "哈尔滨":[126.63,45.75],
            "聊城":[115.97,36.45],
            "芜湖":[118.38,31.33],
            "唐山":[118.02,39.63],
            "平顶山":[113.29,33.75],
            "邢台":[114.48,37.05],
            "德州":[116.29,37.45],
            "济宁":[116.59,35.38],
            "荆州":[112.239741,30.335165],
            "宜昌":[111.3,30.7],
            "义乌":[120.06,29.32],
            "丽水":[119.92,28.45],
            "洛阳":[112.44,34.7],
            "秦皇岛":[119.57,39.95],
            "株洲":[113.16,27.83],
            "石家庄":[114.48,38.03],
            "莱芜":[117.67,36.19],
            "常德":[111.69,29.05],
            "保定":[115.48,38.85],
            "湘潭":[112.91,27.87],
            "金华":[119.64,29.12],
            "岳阳":[113.09,29.37],
            "长沙":[113,28.21],
            "衢州":[118.88,28.97],
            "廊坊":[116.7,39.53],
            "菏泽":[115.480656,35.23375],
            "合肥":[117.27,31.86],
            "武汉":[114.31,30.52],
            "大庆":[125.03,46.58]
        };

        var convertData = function (data) {
            var res = [];
            for (var i = 0; i < data.length; i++) {
                var geoCoord = geoCoordMap[data[i].name];
                if (geoCoord) {
                    res.push({
                        name: data[i].name,
                        value: geoCoord.concat(data[i].value)
                    });
                }
            }
            return res;
        };

        option = {
            backgroundColor: '#404a59',
            title: {
                text: '全国城市招聘数据分布统计图',
                subtext: 'data from Ocean Jobs',
                x:'center',
                textStyle: {
                    color: '#fff'
                }
            },
            tooltip: {
                trigger: 'item',
                formatter: function (params) {
                    return params.name + ' : ' + params.value[2];
                }
            },
            legend: {
                orient: 'vertical',
                y: 'bottom',
                x:'right',
                data:['发布职位信息数量'],
                textStyle: {
                    color: '#fff'
                }
            },
            visualMap: {
                min: 0,
                max: data['sum_all'],
                y:'60',
                x:'60',
                calculable: true,
                inRange: {
                    color: ['#50a3ba', '#eac736', '#d94e5d']
                },
                textStyle: {
                    color: '#fff'
                }
            },
            geo: {
                map: 'china',
                label: {
                    emphasis: {
                        show: false
                    }
                },
                 roam: true,
                itemStyle: {
                    normal: {
                        areaColor: '#323c48',
                        borderColor: '#111'
                    },
                    emphasis: {
                        areaColor: '#2a333d'
                    }
                }
            },
            series: [
                {
                    name: 'pm2.5',
                    type: 'scatter',
                    coordinateSystem: 'geo',
                    data: convertData(data['data']),
                    symbolSize: 12,
                    label: {
                        normal: {
                            show: false
                        },
                        emphasis: {
                            show: false
                        }
                    },
                    itemStyle: {
                        emphasis: {
                            borderColor: '#fff',
                            borderWidth: 1
                        }
                    }
                }
            ]
        };
        if (option && typeof option === "object") {
            myChart.setOption(option, true);
        }
};