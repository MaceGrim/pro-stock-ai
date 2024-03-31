import pandas as pd
from pybaseball import statcast, pitching_stats, batting_stats, playerid_reverse_lookup
import pybaseball
from tqdm import tqdm
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

# Add:
# PCA Columns
# t-SNE Columns
# Summary Statistics from statcast data

batter_embedding = pd.read_csv('./embeddings/batter_embeddings_with_ids.csv')
pitcher_embedding = pd.read_csv('./embeddings/pitcher_embeddings_with_ids.csv')

batter_embedding["batter"] = batter_embedding["batter"].astype(int)
pitcher_embedding["pitcher"] = pitcher_embedding["pitcher"].astype(int)

# Add PCA columns for batters
print("Adding PCA columns for batters...")
pca = PCA(n_components=3)
pca_columns = pca.fit_transform(batter_embedding.iloc[:, 1:])
pca_columns = pd.DataFrame(pca_columns, columns=[f'pca_{i}' for i in range(3)])
batter_embedding = pd.concat([batter_embedding, pca_columns], axis=1)

# Add PCA columns for pitchers
print("Adding PCA columns for pitchers...")
pca = PCA(n_components=3)
pca_columns = pca.fit_transform(pitcher_embedding.iloc[:, 1:])
pca_columns = pd.DataFrame(pca_columns, columns=[f'pca_{i}' for i in range(3)])
pitcher_embedding = pd.concat([pitcher_embedding, pca_columns], axis=1)


# Add t-SNE columns for batters
print("Adding t-SNE columns for batters...")
tsne = TSNE(n_components=3)
tsne_columns = tsne.fit_transform(batter_embedding.iloc[:, 1:])
tsne_columns = pd.DataFrame(tsne_columns, columns=[f'tsne_{i}' for i in range(3)])
batter_embedding = pd.concat([batter_embedding, tsne_columns], axis=1)

# Add t-SNE columns for pitchers
print("Adding t-SNE columns for pitchers...")
tsne = TSNE(n_components=3)
tsne_columns = tsne.fit_transform(pitcher_embedding.iloc[:, 1:])
tsne_columns = pd.DataFrame(tsne_columns, columns=[f'tsne_{i}' for i in range(3)])
pitcher_embedding = pd.concat([pitcher_embedding, tsne_columns], axis=1)

# Add summary statistics from statcast data
start_year = 2016
end_year = 2023

batting_stats_df = batting_stats(start_season=start_year, end_season=end_year)
pitching_stats_df = pitching_stats(start_season=start_year, end_season=end_year)

# Map player IDs to FanGraphs IDs
all_player_ids = list(set(batting_stats_df["IDfg"].unique().tolist() + pitching_stats_df["IDfg"].unique().tolist()))
player_ids = playerid_reverse_lookup(all_player_ids, key_type="fangraphs")
player_ids = player_ids[['key_fangraphs', 'key_mlbam']]

# Create dictionary to map FanGraphs IDs to MLBAM IDs
player_ids_dict = dict(zip(player_ids['key_fangraphs'], player_ids['key_mlbam']))

batting_stats_df['IDmlbam'] = batting_stats_df['IDfg'].map(player_ids_dict)
pitching_stats_df['IDmlbam'] = pitching_stats_df['IDfg'].map(player_ids_dict)

# Only keep WAR for now, figure out how to easily aggregate different stat types across years (rates and counting stats)
batting_stats_df = batting_stats_df[['IDmlbam', 'WAR', "Name"]]
pitching_stats_df = pitching_stats_df[['IDmlbam', 'WAR', "Name"]]

batting_stats_groupby = batting_stats_df.groupby('IDmlbam').sum().reset_index()
pitching_stats_groupby = pitching_stats_df.groupby('IDmlbam').sum().reset_index()

batting_stats_groupby = batting_stats_groupby.merge(batting_stats_df[['IDmlbam', 'Name']], on='IDmlbam', how='left')
pitching_stats_groupby = pitching_stats_groupby.merge(pitching_stats_df[['IDmlbam', 'Name']], on='IDmlbam', how='left')

# Add summary statistics to embeddings
batter_embedding = batter_embedding.merge(batting_stats_groupby, left_on='batter', right_on='IDmlbam', how='left')
pitcher_embedding = pitcher_embedding.merge(pitching_stats_groupby, left_on='pitcher', right_on='IDmlbam', how='left')

batter_embedding = batter_embedding.drop_duplicates(subset=['batter']).dropna()
pitcher_embedding = pitcher_embedding.drop_duplicates(subset=['pitcher']).dropna()

batter_embedding.to_csv('./embeddings/batter_bp2vec.csv', index=False)
pitcher_embedding.to_csv('./embeddings/pitcher_bp2vec.csv', index=False)
