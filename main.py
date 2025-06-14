from scripts.nettoyage import traiter_tous_les_csv
import os

dprs = ['05', '21', '29']
folder = 'clean_data'

not_cln_dprs = []
for dpr in dprs:
    path = os.path.join(folder, dpr)
    if os.path.exists(path) and len(os.listdir(path)) < 4:
        not_cln_dprs.append(dpr)

traiter_tous_les_csv(not_cln_dprs)