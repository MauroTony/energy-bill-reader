import camelot
import matplotlib.pyplot as plt
def plot_table(tables):
    camelot.plot(tables[0], kind='contour')
    plt.show(block=True)

tables = camelot.read_pdf(
    "../pdfs/energia.pdf",
    pages="1",
    flavor="stream",
    edge_tol=50,
)
plot_table(tables)
table_df = tables[0].df
dict_data = table_df.to_dict()