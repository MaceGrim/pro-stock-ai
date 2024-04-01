import "./style.css";
import Plotly from "plotly.js-dist-min";
import Papa from "papaparse";

const csvFilePath = "app-data/batter_bp2vec.csv";

function plot3DScatter(xData, yData, zData) {
    var trace = {
        x: xData,
        y: yData,
        z: zData,
        mode: "markers",
        type: "scatter3d",
        marker: {
            size: 4,
            color: zData, 
            colorscale: "Viridis", 
            opacity: 0.8,
            line: {
                width: 1,
                color: "rgb(255, 255, 255, 0.5)", 
            },
        },
        hoverinfo: "x+y+z+text", 
    };

    var layout = {
        title: "3D PCA Scatter Plot of Batters",
        autosize: true,
        margin: { l: 0, r: 0, b: 0, t: 30 },
        scene: {
            xaxis: { title: "PCA 0" },
            yaxis: { title: "PCA 1" },
            zaxis: { title: "PCA 2" },
            aspectratio: { x: 1, y: 1, z: 1 },
            camera: { eye: { x: 1.25, y: 1.25, z: 1.25 } },
        },
        paper_bgcolor: "rgba(0,0,0,0)", 
        plot_bgcolor: "rgba(0,0,0,0)",
    };

    Plotly.newPlot("scatterPlot", [trace], layout, { responsive: true });
}

fetch(csvFilePath)
    .then((response) => response.text())
    .then((csvData) => {
        Papa.parse(csvData, {
            complete: (results) => {
                const rows = results.data;
                const xData = rows.map((row) => row["pca_0"]);
                const yData = rows.map((row) => row["pca_1"]);
                const zData = rows.map((row) => row["pca_2"]);

                plot3DScatter(xData, yData, zData);
            },
            header: true,
        });
    })
    .catch((error) => console.error("Error loading the CSV file:", error));
