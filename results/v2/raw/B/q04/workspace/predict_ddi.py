import sys, os, warnings
warnings.filterwarnings('ignore')
os.chdir('/opt/DSN-DDI')
sys.path.insert(0, '/opt/DSN-DDI/drugbank_test')
import torch, pandas as pd, numpy as np
from torch_geometric.data import Data, Batch
import data_preprocessing as dp
import models

A, B = 'DB00391', 'DB00875'   # Sulpiride, Flupentixol
dev = 'cpu'
info = pd.read_csv('/opt/DSN-DDI/Interaction_information.csv')
desc = {int(r['Interaction type']): r['Description'] for _, r in info.iterrows()}

def graph(i):
    ei, x = dp.MOL_EDGE_LIST_FEAT_MTX[i]
    return Data(x=x.clone(), edge_index=ei.clone())

def score_all(pkl):
    m = torch.load(pkl, map_location=dev); m.to(dev); m.eval()
    n = 86
    h = Batch.from_data_list([graph(A) for _ in range(n)])
    t = Batch.from_data_list([graph(B) for _ in range(n)])
    b = Batch.from_data_list([dp._create_b if False else dp.BipartiteData(dp.get_bipartite_graph(dp.drug_to_mol_graph[A], dp.drug_to_mol_graph[B]), graph(A).x, graph(B).x) for _ in range(n)])
    rels = torch.arange(n).unsqueeze(0)
    with torch.no_grad():
        return torch.sigmoid(m((h.to(dev), t.to(dev), rels.to(dev), b.to(dev)))).cpu().numpy().ravel()

p = score_all('/opt/DSN-DDI/drugbank_test/transductive_drugbank.pkl')
order = np.argsort(-p)
print('top5:', [(int(i), round(float(p[i]), 4)) for i in order[:5]])
r = int(order[0])
row = dict(drug_a='Sulpiride', drug_b='Flupentixol', relation=r, prob=round(float(p[r]), 6),
           model_used='transductive_drugbank.pkl',
           description=desc[r + 1].replace('#Drug1', 'Sulpiride').replace('#Drug2', 'Flupentixol'))
pd.DataFrame([row]).to_csv('/workspace/ddi_prediction.csv', index=False)
print(row)
