import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15

import "components"
import "charts"

Window {
    id: window
    minimumWidth: 1280
    minimumHeight: 720
    visible: true
    color: "#F5F5F5"
    title: "Dashboard graphiques en direct"



    /*
    Chart{
        width: 400
        height: 300
        property int test : 65;
        onPaint: {
            //bar
            bar( {

                labels : ["January","February","March","April","May","June","July"],
                datasets : [
                    {
                        fillColor : "rgba(220,220,220,0.5)",
                        strokeColor : "rgba(220,220,220,1)",
                        data : [test,59,90,81,56,55,40]
                    },
                    {
                        fillColor : "rgba(151,187,205,0.5)",
                        strokeColor : "rgba(151,187,205,1)",
                        data : [28,48,40,19,96,27,7]
                    }
                ]
            });

            // line
            line({
                 labels : ["January","February","March","April","May","June","July","Test"],
                 labels.append("testB")
                 datasets : [
                     {
                         fillColor : "rgba(220,220,220,0.5)",
                         strokeColor : "rgba(220,220,220,1)",
                         pointColor : "rgba(220,220,220,1)",
                         pointStrokeColor : "#fff",
                         data : [65,59,90,81,56,55,40]
                     },
                     {
                         fillColor : "rgba(151,187,205,0.5)",
                         strokeColor : "rgba(151,187,205,1)",
                         pointColor : "rgba(151,187,205,1)",
                         pointStrokeColor : "#fff",
                         data : [28,48,40,19,96,27,100]
                     }
                 ]
            });
        }

        Timer
        {
            id:t
            interval: 100
            repeat: true
            running: true
            onTriggered:{
                test+=1
                requestPaint();
            }
        }
        Component.onCompleted: {
            console.debug("this is the chart.js by qml you can use it just like use the chart.js ",
                          "you can look the Chart.js in http://chartjs.org/");

        }
    }
    */


    /*
    //Signal utilisé pour détecter quand le fenêtre est fermée et quitter l'application
    signal closed()

    onVisibilityChanged: {
        if(!window.visible) {
            closed()
        }
    }
    */
}
