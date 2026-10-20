import os, sys
os.chdir('/opt/DSN-DDI'); sys.path.insert(0, '/opt/DSN-DDI/drugbank_test')
import torch, numpy as np
import data_preprocessing as dp
from data_preprocessing import DrugDataset
dev = 'cpu'
def run(pkl, pairs):
    model = torch.load(pkl, map_location=dev).eval()
    out = {}
    for a, b in pairs:
        ds = DrugDataset([(a, b, 0)], disjoint_split=False, shuffle=False)
        scores = []
        for r in range(86):
            ds.tri_list = [(a, b, r)]
            pos, _ = ds.collate_fn([(a, b, r)])
            with torch.no_grad():
                scores.append(torch.sigmoid(model([t.to(dev) for t in pos])).item())
        out[(a, b)] = np.array(scores)
    return out
if __name__ == '__main__':
    pairs = [('DB00972','DB00214'), ('DB00682','DB00945')]
    for pkl in ['transductive_drugbank.pkl', 'inductive_drugbank.pkl']:
        res = run('drugbank_test/'+pkl, pairs)
        for k, s in res.items():
            top = np.argsort(-s)[:3]
            print(pkl, k, [(int(t), round(float(s[t]),4)) for t in top])
