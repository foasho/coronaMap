$(function(){
    let areas_data_list = [];
    let patient_list = [];
    let prefectures_list = [];
    for (let index=0; index < 47; index++){
        const select_code = index+1;
        const select_id = "#pref_"+select_code.toString();
        let areas_data;
        if ($(select_id).length){
            areas_data = {
                code: select_code,
                name: $(select_id).data('prefectures'),
                color: $(select_id).data('hex_data'),
                hoverColor: $(select_id).data('hex_data'),
                prefectures: [select_code],
            }
            const prefectures_data = $(select_id).data('prefectures');
            prefectures_list.push(prefectures_data);
            const patient_data = $(select_id).data('patient_num');
            patient_list.push(patient_data);
        }
        else{
            areas_data = {
                code: select_code,
                name: "",
                color: "#000000",
                hoverColor: "#000000",
                prefectures: [select_code],
            }
        }
        areas_data_list.push(areas_data);
    }
    console.log(patient_list);
    const getWidth = $(window).width();//画面の大きさ取得
    const getheight = $(window).height();//画面の高さを取得
    const map_width = getheight*1.30;//MAP描画比から横のサイズを指定
    $("#map-container").japanMap({
        width: map_width,//画面の大きさそのまま描画する
        selection: "area",
        areas: areas_data_list,
        backgroundColor : "#222222",//背景を黒くする
        borderLineColor: "#f2fcff",
        borderLineWidth : 0.25,
        lineColor : "#a0a0a0",
        lineWidth: 1,
        drawsBoxLine: true,
        showsPrefectureName: false,//件名を非表示にする
        prefectureNameType: "short",
        movesIslands : true,
        fontSize : 11,
        fontShadowColor : "#fff",
        onSelect : function(data){
            const select_id = "#pref_"+data.code.toString();
            if ($(select_id).length) {
                const patient_num = $(select_id).data("patient_num");
                const context = data.name + ":" + patient_num.toString() + "人です。";
                alert(context)
            }
            else {
                alert('この地域には、まだコロナウイルス感染者はいません。');
            }
        }
    });

    const sidebar_width = getWidth - map_width-20;
    $('#map_sidebar').append("<div id='side_area'></div>").css(
        {
            "width": sidebar_width.toString(),
            "height": (getheight - 29).toString(),
        }
        );

    //患者数全国グラフの追加
    $('#side_area').append("<canvas id='patient_graph' style='position: relative; height:90vh; width:35vw;'></canvas>");
    let patient_ctx = document.getElementById('patient_graph');
    let patient_chart = new Chart(patient_ctx, {
        type: 'horizontalBar',//タイプを棒グラフに設定
        data: {
            labels: prefectures_list,//都道府県(横軸)
            datasets: [
                {
                    label: '患者数',//表示データの名前
                    data: patient_list,//実際の患者数データ
                    borderColor: "rgba(255,0,0,1)",//ボーダーカラー
                    backgroundColor: "#f22341"//グラフの背景色
                }
            ],
        },
        options: {
            title: {
                display: true,
                text: '都道府県別の患者数',//タイトル名
                fontSize: 24,//タイトルの文字の大きさ
            },
            scales: {
                yAxes: [{
                    ticks: {
                        suggestedMax: 500,
                        suggestedMin: 0,
                        stepSize: 100,
                    },
                    gridLines: {
                        color: "#ffffff",
                    }
                }]
            },
        }
    });

});