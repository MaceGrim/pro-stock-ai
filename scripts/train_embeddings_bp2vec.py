
# Embeddings inspired by {batter, pitcher}2vev found here: https://github.com/airalcorn2/batter-pitcher-2vec

import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from torch.optim.lr_scheduler import LambdaLR
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from tqdm import tqdm


data = pd.read_csv('statcast_data_2016_2023.csv')
data = data.dropna(subset=["events"])

data["events"].value_counts()
events_to_keep = data["events"].value_counts().iloc[:20].index.tolist()
events_to_drop = ["force_out", "caught_stealing_2b", "catcher_interf", "other_out", "pickoff_2b", "caught_stealing_home", "pickoff_1b", "sac_fly_double_play",
                  "caught_stealing_3b", "wild_pitch"]

events_to_keep = [x for x in events_to_keep if x not in events_to_drop]

event_map = {"field_error": "field_out", "grounded_into_double_play": "field_out", "fielders_choice_out": "field_out",
             "fielders_choice": "field_out", "strikeout_double_play": "strikeout", "double_play": "field_out",}

data["events"] = data["events"].replace(event_map)
data = data[data["events"].isin(events_to_keep)]

df = data[["batter", "pitcher", "events"]]

label_encoder_batter = LabelEncoder()
df['batter_codes'] = label_encoder_batter.fit_transform(df['batter'])

label_encoder_pitcher = LabelEncoder()
df['pitcher_codes'] = label_encoder_pitcher.fit_transform(df['pitcher'])

label_encoder_events = LabelEncoder()
df['event_codes'] = label_encoder_events.fit_transform(df['events'])


NUM_BATTERS = df['batter'].nunique()
NUM_PITCHERS = df['pitcher'].nunique()
NUM_EVENTS = df['events'].nunique()
VEC_SIZE = 9
BATCH_SIZE = 1024
NUM_EPOCHS = 50

class BaseballDataset(Dataset):
    def __init__(self, dataframe):
        self.batter = torch.tensor(dataframe['batter_codes'].values, dtype=torch.long)
        self.pitcher = torch.tensor(dataframe['pitcher_codes'].values, dtype=torch.long)
        self.event = torch.tensor(dataframe['event_codes'].values, dtype=torch.long)

    def __len__(self):
        return len(self.batter)

    def __getitem__(self, idx):
        return self.batter[idx], self.pitcher[idx], self.event[idx]

class BaseballModel(nn.Module):
    def __init__(self, num_batters, num_pitchers, vec_size, num_outcomes):
        super(BaseballModel, self).__init__()
        self.vec_size = vec_size
        self.batter_embedding = nn.Embedding(num_batters, vec_size)
        self.pitcher_embedding = nn.Embedding(num_pitchers, vec_size)
        self.fc = nn.Linear(vec_size * 2, num_outcomes)
        self.activation = nn.Sigmoid()

    def forward(self, batter_idx, pitcher_idx):
        batter_embed = self.activation(self.batter_embedding(batter_idx).view(-1, self.vec_size))
        pitcher_embed = self.activation(self.pitcher_embedding(pitcher_idx).view(-1, self.vec_size))
        combined = torch.cat((batter_embed, pitcher_embed), dim=1)
        output = self.fc(combined)
        return output

dataset = BaseballDataset(df)
dataloader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True)

model = BaseballModel(NUM_BATTERS, NUM_PITCHERS, VEC_SIZE, NUM_EVENTS)

optimizer = torch.optim.Adam(model.parameters(), lr=0.00003)  # Initial learning rate

# Define the lambda function for the learning rate schedule
def lr_lambda(epoch):
    # Keep the initial learning rate for the first 15 epochs
    if epoch < 15:
        return 1
    else:  # Then decay by 5% each epoch
        return 0.95 ** (epoch - 15)

# Create the scheduler
scheduler = LambdaLR(optimizer, lr_lambda)

loss_function = nn.CrossEntropyLoss()

# Training loop
model.train()
for epoch in tqdm(range(NUM_EPOCHS)):
    for batter, pitcher, event in dataloader:
        optimizer.zero_grad()
        predictions = model(batter, pitcher)
        loss = loss_function(predictions, event)
        loss.backward()
        optimizer.step()
    scheduler.step()  # Update the learning rate
    print(f"Epoch {epoch+1}, Loss: {loss.item()}")

# Save the model
torch.save(model.state_dict(), 'baseball_model_bp2vec.pth')

# Save the embeddings
batter_embedding = model.batter_embedding.weight.data.numpy()
pitcher_embedding = model.pitcher_embedding.weight.data.numpy()

batter_df = pd.DataFrame(batter_embedding)
pitcher_df = pd.DataFrame(pitcher_embedding)

# Mapping of encoded IDs back to original IDs for batters and pitchers
batter_id_to_original = {encoded: original for original, encoded in zip(df['batter'], df['batter_codes'])}
pitcher_id_to_original = {encoded: original for original, encoded in zip(df['pitcher'], df['pitcher_codes'])}

# Assuming batter_embedding and pitcher_embedding are numpy arrays from your model's embeddings

# Map encoded IDs back to original IDs for batters and pitchers
original_batter_ids = label_encoder_batter.inverse_transform(df['batter_codes'].unique())
original_pitcher_ids = label_encoder_pitcher.inverse_transform(df['pitcher_codes'].unique())

# Add original IDs as a column in batter_df and pitcher_df
batter_df['batter'] = original_batter_ids
pitcher_df['pitcher'] = original_pitcher_ids


# Make sure to adjust the order of columns if needed, so the ID columns are at the beginning
batter_df = batter_df[['batter'] + [col for col in batter_df.columns if col != 'batter']]
pitcher_df = pitcher_df[['pitcher'] + [col for col in pitcher_df.columns if col != 'pitcher']]

for col in batter_df.columns:
    if col != 'batter':
        batter_df[f"embedding_{col}"] = batter_df[col].astype(float)

for col in pitcher_df.columns:
    if col != 'pitcher':
        pitcher_df[f"embedding_{col}"] = pitcher_df[col].astype(float)

# Save the embeddings with original IDs
batter_df.to_csv('batter_embeddings_with_ids.csv', index=False)
pitcher_df.to_csv('pitcher_embeddings_with_ids.csv', index=False)
