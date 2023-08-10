import camelot
import matplotlib.pyplot as plt
import json

def plot_table(tables):
    camelot.plot(tables[0], kind='contour')
    plt.show(block=True)

tables = camelot.read_pdf(
    "../pdfs/01-23.pdf",
    pages="1",
    flavor="stream",
    edge_tol=50,
    table_areas=["30,684,300,652"],
)
plot_table(tables)
table_df = tables[0].df
dict_data = table_df.to_dict()
print(json.dumps(dict_data, indent=4))