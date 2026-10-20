import sys, os
os.chdir('/opt/DSN-DDI')
sys.path.insert(0, '/opt/DSN-DDI/drugbank_test')
import torch, numpy as np, pandas as pd
from data_preprocessing import DrugDataset, DrugDataLoader

A, B = 'DB00972', 'DB00214'  # Azelastine, Torasemide
info = pd.read_csv('Interaction_information.csv')
dev = 'cuda:0' if torch.cuda.is_available() else 'cpu'
res = {}
for name, pkl in [('transductive', 'drugbank_test/transductive_drugbank.pkl'), ('inductive', 'drugbank_test/inductive_drugbank.pkl')]:
    model = torch.load(pkl, map_location=dev).eval()
    probs = []
    for r in range(86):
        ds = DrugDataset([(A, B, r)], disjoint_split=False, shuffle=False)
        batch = next(iter(DrugDataLoader(ds, batch_size=1)))
        pos = [t.to(dev) for t in batch[0]]
        with torch.no_grad():
            probs.append(torch.sigmoid(model(pos)).item())
    res[name] = np.array(probs)
    top = np.argsort(-res[name])[:5]
    print(name, [(int(i), round(float(res[name][i]), 4)) for i in top])
np.save('/workspace/probs.npy', np.stack([res['transductive'], res['inductive']]))
