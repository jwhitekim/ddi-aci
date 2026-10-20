import os, sys, warnings
warnings.filterwarnings('ignore')
os.chdir('/opt/DSN-DDI')
sys.path.insert(0, '/opt/DSN-DDI/drugbank_test')
import torch, numpy as np, pandas as pd
import data_preprocessing as dp
import models, layers

A, B = 'DB01232', 'DB01244'
info = pd.read_csv('Interaction_information.csv').sort_values('Interaction type').reset_index(drop=True)
desc = {int(r['Interaction type']) - 1: r['Description'] for _, r in info.iterrows()}
device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
ds = dp.DrugDataset([(A, B, 0)], disjoint_split=False, shuffle=False)

def score(pkl):
    m = torch.load(pkl, map_location=device); m.to(device).eval()
    out = []
    with torch.no_grad():
        for r in range(86):
            ds.tri_list = [(A, B, r)]
            pos, _ = ds.collate_fn(ds.tri_list)
            pos = [t.to(device) for t in pos]
            out.append(torch.sigmoid(m(pos)).item())
    return np.array(out)

res = {'transductive': score('drugbank_test/transductive_drugbank.pkl'),
       'inductive': score('drugbank_test/inductive_drugbank.pkl')}
for k, v in res.items():
    print(k, 'top5:', [(int(i), round(float(v[i]), 4)) for i in np.argsort(-v)[:5]])
np.save('/tmp/res.npy', res, allow_pickle=True)
