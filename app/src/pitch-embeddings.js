import "./style.css";
import Scatterplot from "deepscatter";

// these are data categories from othe mega 2.7 gb data file not using yet but maybe someday
const dataCategories = [
    "pitch_type",
    "game_date",
    "release_speed",
    "release_pos_x",
    "release_pos_z",
    "player_name",
    "batter",
    "pitcher",
    "events",
    "description",
    "spin_dir",
    "spin_rate_deprecated",
    "break_angle_deprecated",
    "break_length_deprecated",
    "zone",
    "des",
    "game_type",
    "stand",
    "p_throws",
    "home_team",
    "away_team",
    "type",
    "hit_location",
    "bb_type",
    "balls",
    "strikes",
    "game_year",
    "pfx_x",
    "pfx_z",
    "plate_x",
    "plate_z",
    "on_3b",
    "on_2b",
    "on_1b",
    "outs_when_up",
    "inning",
    "inning_topbot",
    "hc_x",
    "hc_y",
    "tfs_deprecated",
    "tfs_zulu_deprecated",
    "fielder_2",
    "umpire",
    "sv_id",
    "vx0",
    "vy0",
    "vz0",
    "ax",
    "ay",
    "az",
    "sz_top",
    "sz_bot",
    "hit_distance_sc",
    "launch_speed",
    "launch_angle",
    "effective_speed",
    "release_spin_rate",
    "release_extension",
    "game_pk",
    "pitcher.1",
    "fielder_2.1",
    "fielder_3",
    "fielder_4",
    "fielder_5",
    "fielder_6",
    "fielder_7",
    "fielder_8",
    "fielder_9",
    "release_pos_y",
    "estimated_ba_using_speedangle",
    "estimated_woba_using_speedangle",
    "woba_value",
    "woba_denom",
    "babip_value",
    "iso_value",
    "launch_speed_angle",
    "at_bat_number",
    "pitch_number",
    "pitch_name",
    "home_score",
    "away_score",
    "bat_score",
    "fld_score",
    "post_away_score",
    "post_home_score",
    "post_bat_score",
    "post_fld_score",
    "if_fielding_alignment",
    "of_fielding_alignment",
    "spin_axis",
    "delta_home_win_exp",
    "delta_run_exp",
    "year",
];

const prefs = {
    source_url: "/pro-stock-ai/app-data/ds/", // the output of the quadfeather tiling engine
    max_points: 1000000, // a full cap.
    alpha: 25, // Target saturation for the full page.
    zoom_balance: 0.7, // Rate at which points increase size. https://observablehq.com/@bmschmidt/zoom-strategies-for-huge-scatterplots-with-three-js
    point_size: 5, // Default point size before application of size scaling
    background_color: "#ffffff00",
    click_function: "console.log(JSON.stringify(datum, undefined, 2))",

    encoding: {
        x: {
            field: "x",
            transform: "literal",
        },
        y: {
            field: "y",
            transform: "literal",
        },
        color: {
            constant: "#2D0368",
        },
    },
};

// this initializes the scatter plot viz
const scatterplot = new Scatterplot("#viz");
scatterplot.plotAPI(prefs);

// this updates the source url for the scatter plot viz when submit is clicked
document.getElementById("submit-ds").addEventListener("click", () => {
  prefs.source_url = document.getElementById("source-url").value;
  document.querySelector("#viz").innerHTML = ``;
  const scatterplot = new Scatterplot("#viz");
  
  scatterplot.plotAPI(prefs).catch(error => {
    document.querySelector("#viz").innerHTML = `<img src="../pro-stock-ai/rockies-sad.gif" alt="sad rockies" /> <p>Can't find that data. Please try again.</p>`;
    console.error("yikes");
  });
});


