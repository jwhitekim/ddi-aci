import sys, os
os.chdir('/opt/DSN-DDI')
sys.path.insert(0, '/opt/DSN-DDI/drugbank_test')
import torch, numpy as np, pandas as pd
import warnings; warnings.filterwarnings('ignore')
from data_preprocessing import DrugDataset, DrugDataLoader
import models  # needed for unpickling

A, B = 'DB00238', 'DB00758'
dev = 'cuda:0' if torch.cuda.is_available() else 'cpu'
info = pd.read_csv('Interaction_information.csv')
res = {}
for name in ['transductive_drugbank', 'inductive_drugbank']:
    m = torch.load(f'drugbank_test/{name}.pkl', map_location=dev).eval()
    for (h, t) in [(A, B), (B, A)]:
        ds = DrugDataset([(h, t, r) for r in range(86)], disjoint_split=False, shuffle=False)
        batch = ds.collate_fn(ds.tri_list)
        pos = [x.to(dev) for x in batch[0]]
        with torch.no_grad():
            p = torch.sigmoid(m(pos)).cpu().numpy().ravel()
        res[(name, h, t)] = p
        top = np.argsort(-p)[:5]
        print(name, h, '->', t, [(int(i), round(float(p[i]), 4)) for i in top])
import pickle; pickle.dump(res, open('/tmp/res.pkl', 'wb'))
