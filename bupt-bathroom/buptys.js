var vm = new Vue({
  el: '#app',
  data: function() {
    return {
      data: {
        total: '0',
        pttotal: '0'
      },
      girl: {
        total: '0',
        pttotal: '0'
      },
      girllist: [
        {
          value: 0,
          name: '女浴室喷头占用数'
        },
        {
          value: 0,
          name: '女浴室喷头空闲数'
        }
      ],
      boy: {
        total: '0',
        pttotal: '0'
      },
      boylist: [
        {
          value: 0,
          name: '男浴室喷头占用数'
        },
        {
          value: 0,
          name: '男浴室喷头空闲数'
        }
      ],
      boytotal: '0', //男喷头总数
      girltotal: '0', //女喷头总数
      nowgirltotal: '0', //当前女总人数
      nowgirlpt: '0', //当前女喷头数
      nowboytotal: '0', //当前男总人数
      nowboypt: '0' //当前男喷头数
    };
  },
  created: function() {
    this.getajax();
  },
  methods: {
    getajax: function() {
      var self = this;
      $.ajax({
        type: 'post',
        url: '/buptys/wap/default/get-data',
        async: true,
        success: function(data) {
          self.boytotal = data.d.data.total.male_shower; //男喷头总数
          self.girltotal = data.d.data.total.female_shower; //女喷头总数
          self.nowgirltotal = data.d.data.now.female; //当前女总人数
          self.nowgirlpt = data.d.data.now.female_shower; //当前女喷头数
          self.nowboytotal = data.d.data.now.male; //当前男总人数
          self.nowboypt = data.d.data.now.male_shower; //当前男喷头数
          self.data.pttotal =
            parseInt(self.girltotal) + parseInt(self.boytotal);
          self.data.total =
            parseInt(self.nowgirltotal) + parseInt(self.nowboytotal);
          self.girl.total = self.nowgirltotal;
          self.girl.pttotal = self.girltotal;
          self.boy.total = self.nowboytotal;
          self.boy.pttotal = self.boytotal;
          self.girllist = [
            {
              value: self.nowgirlpt,
              name: '女浴室喷头占用数'
            },
            {
              value: parseInt(self.girltotal) - parseInt(self.nowgirlpt),
              name: '女浴室喷头空闲数'
            }
          ];
          self.boylist = [
            {
              value: self.nowboypt,
              name: '男浴室喷头占用数'
            },
            {
              value: parseInt(self.boytotal) - parseInt(self.nowboypt),
              name: '男浴室喷头空闲数'
            }
          ];
          Vue.nextTick(function() {
            echartsinit();
          });
        }
      });
    }
  }
});
Vue.nextTick(function() {
  var width = $(window).width();
  if (width == 414) {
    $('#app .tent .botto>div em.plus').css('top', '0.24rem');
  }
});

function echartsinit() {
  option = {
    series: [
      {
        name: '访问来源',
        type: 'pie',
        radius: ['25%', '42%'],
        center: ['50%', '65%'],
        color: ['#F5CB20', '#E7396F'],
        startAngle: 270,
        clockwise: false,
        labelLine: {
          length: 0,
          length2: 0
        },
        label: {
          normal: {
            formatter: function(params, ticket, callback) {
              return '';
            }
            //
          }
        },
        data: vm.girllist
      }
    ]
  };
  var myChart = echarts.init(document.getElementById('girl'));

  myChart.setOption(option);

  options = {
    series: [
      {
        name: '访问来源',
        type: 'pie',
        radius: ['25%', '42%'],
        center: ['50%', '65%'],
        color: ['#F5CB20', '#7AF4FF'],
        startAngle: 270,
        clockwise: false,
        labelLine: {
          length: 0,
          length2: 0
        },
        label: {
          normal: {
            formatter: function(params, ticket, callback) {
              return '';
            }
          }
        },
        data: vm.boylist
      }
    ]
  };
  optiongirl = {
    series: [
      {
        name: '访问来源',
        type: 'pie',
        radius: ['30%', '45%'],
        center: ['50%', '60%'],
        color: ['#F5CB20', '#E7396F'],
        startAngle: 270,
        clockwise: false,
        labelLine: {
          length: 0,
          length2: 0
        },
        label: {
          normal: {
            formatter: function(params, ticket, callback) {
              return '';
            }
          }
        },
        data: vm.girllist
      }
    ]
  };
  var myCharts = echarts.init(document.getElementById('boy'));
  myCharts.setOption(options);
  var myChartgirl = echarts.init(document.getElementById('girl-iphone'));
  myChartgirl.setOption(optiongirl);
  optionboy = {
    series: [
      {
        name: '访问来源',
        type: 'pie',
        radius: ['30%', '45%'],
        center: ['50%', '60%'],
        color: ['#F5CB20', '#7AF4FF'],
        startAngle: 270,
        clockwise: false,
        labelLine: {
          length: 0,
          length2: 0
        },
        label: {
          normal: {
            formatter: function(params, ticket, callback) {
              return '';
            }
          }
        },
        data: vm.boylist
      }
    ]
  };
  var myChartboy = echarts.init(document.getElementById('boy-iphone'));
  myChartboy.setOption(optionboy);
}
setInterval(function() {
  vm.getajax();
}, 60000);
