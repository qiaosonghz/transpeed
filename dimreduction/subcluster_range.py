import sys
from sklearn.decomposition import PCA

sys.path.append("..")
sys.path.append("./src")
sys.path.append("../src")

from src import space

pe_low = 128
pe_high = 300

subcluster_range = []
num_levels = 2


for num_pe in list(range(pe_low, pe_high, 2)):
    subcluster_range = list(space.get_all_combinations_v2(num_levels, num_pe, [], []))
    print(f'subcluster_range:{subcluster_range}')
    pca = PCA(n_components=1)
    transformed_range = pca.fit_transform(subcluster_range)
    print(f'transformed_range:{transformed_range}')
