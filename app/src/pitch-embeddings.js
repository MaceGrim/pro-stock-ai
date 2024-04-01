import "./style.css";
import Scatterplot from "deepscatter";

const dataCategories = [
  "pitch_type", "game_date", "release_speed", "release_pos_x", "release_pos_z", "player_name", 
  "batter", "pitcher", "events", "description", "spin_dir", "spin_rate_deprecated", 
  "break_angle_deprecated", "break_length_deprecated", "zone", "des", "game_type", "stand", 
  "p_throws", "home_team", "away_team", "type", "hit_location", "bb_type", "balls", "strikes", 
  "game_year", "pfx_x", "pfx_z", "plate_x", "plate_z", "on_3b", "on_2b", "on_1b", "outs_when_up", 
  "inning", "inning_topbot", "hc_x", "hc_y", "tfs_deprecated", "tfs_zulu_deprecated", "fielder_2", 
  "umpire", "sv_id", "vx0", "vy0", "vz0", "ax", "ay", "az", "sz_top", "sz_bot", "hit_distance_sc", 
  "launch_speed", "launch_angle", "effective_speed", "release_spin_rate", "release_extension", 
  "game_pk", "pitcher.1", "fielder_2.1", "fielder_3", "fielder_4", "fielder_5", "fielder_6", 
  "fielder_7", "fielder_8", "fielder_9", "release_pos_y", 
  "estimated_ba_using_speedangle", "estimated_woba_using_speedangle", "woba_value", "woba_denom", 
  "babip_value", "iso_value", "launch_speed_angle", "at_bat_number", "pitch_number", "pitch_name", 
  "home_score", "away_score", "bat_score", "fld_score", "post_away_score", "post_home_score", 
  "post_bat_score", "post_fld_score", "if_fielding_alignment", "of_fielding_alignment", "spin_axis", 
  "delta_home_win_exp", "delta_run_exp", "year"
];

const prefs = {
    source_url: '/pro-stock-ai/app-data/ds/', // the output of the quadfeather tiling engine
    max_points: 1000000, // a full cap.
    alpha: 25, // Target saturation for the full page.
    zoom_balance: 0.7, // Rate at which points increase size. https://observablehq.com/@bmschmidt/zoom-strategies-for-huge-scatterplots-with-three-js
    point_size: 5, // Default point size before application of size scaling
    background_color: '#ffffff00',
    click_function: 'console.log(JSON.stringify(datum, undefined, 2))',

    // encoding API based roughly on Vega Lite: https://vega.github.io/vega-lite/docs/encoding.html
    encoding: {
      x: {
        field: 'x',
        transform: 'literal',
      },
      y: {
        field: 'y',
        transform: 'literal',
      },
      color: {
        constant: '#2D0368',
      },
    },
  };

  const scatterplot = new Scatterplot('#viz');
  scatterplot.plotAPI(prefs);
