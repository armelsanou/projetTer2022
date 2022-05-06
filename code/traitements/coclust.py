from coclust.coclustering import CoclustMod
from coclust.coclustering import CoclustSpecMod
from coclust.evaluation.internal import best_modularity_partition
import dash_bootstrap_components as dbc

import numpy as np
import matplotlib.pyplot as plt



from io import BytesIO
import base64
#Armel don't forget that you have to update the code for all coclust algorithm by adding try catch for the case that only one document is found
def coclustmod(dtm, n_clusters = 2):
  try:
    coclust = CoclustMod(n_clusters)
    coclust.fit(dtm.to_numpy())
    
    return coclust
  except:
    print("only one found")

    return dbc.Container(
      dbc.Alert("Only one document was found during your research, can not apply clustering on one element", 
            is_open=True,
            duration=4000,color="warning"),
      className="p-5",
      )
	

def coclustspecmod(df, n_clusters = 2):
	coclust = CoclustSpecMod(n_clusters)
	coclust.fit(df.to_numpy())
	
	return coclust

def bestModularityPartition(dtm,n_min = 2, n_max = 8):
	clusters_range = range(n_min, n_max)
	model, modularities = best_modularity_partition(dtm.to_numpy(), clusters_range, n_rand_init=1)
	
	return (model, modularities)
	
def _remove_ticks():
    plt.tick_params(axis='both', which='both', bottom='off', top='off',
                    right='off', left='off')


# 

def plot_cluster_sizes(model):
 
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111)
    prop_list = list(plt.rcParams['axes.prop_cycle'])
    colors = [prop_list[0]['color'], prop_list[1]['color']]
    x = []
    y = []
    for i in range(model.n_clusters):
        number_of_rows, number_of_columns = model.get_shape(i)
        x.append(number_of_rows)
        y.append(number_of_columns)
    data = [x, y]
    shift = .8 / len(data * 2)
    location = np.arange(model.n_clusters)
    legend_rects = []
    for i in range(2):
        cols = ax.bar(location + i * shift, data[i], width=shift,
                      color=colors[i % len(colors)], align='center')
        legend_rects.append(cols[0])
        for c in cols:
            h = c.get_height()
            ax.text(c.get_x() + c.get_width() / 2., h + 5, '%d' % int(h),
                    ha='center', va='bottom')
    ax.set_xticks(location + (shift / 2.))
    ax.set_xticklabels(['coclust-' + str(i) for i in range(model.n_clusters)])
    plt.xlabel('Co-clusters')
    plt.ylabel('Sizes')
    plt.tight_layout()
    ax.legend(legend_rects, ('Rows', 'Columns'))

    #_remove_ticks()
    plt.tick_params(axis='both', which='both', bottom='on', top='off',
                    right='off', left='off')
    return fig

# cluster terms
def plot_cluster_top_terms(in_data, all_terms, nb_top_terms, model):

  if all_terms is None:
    logger.warning("Term labels cannot be found. Use input argument "
                       "'term_labels_filepath' in function "
                       "'load_doc_term_data' if term labels are available.")
    return

  x_label = "number of occurences"
    
  plt.subplots(figsize=(8, 20))
    #plt.subplots_adjust(hspace=0.200)
  plt.suptitle("      Top %d terms" % nb_top_terms, size=15)
  number_of_subplots = model.n_clusters
  valid_clusters = []
  for i in range(number_of_subplots):
    if len(model.get_indices(i)[1]) >=nb_top_terms and len(model.get_indices(i)[0])>0:
      valid_clusters.append(i)

  for i, v in enumerate(valid_clusters):
        # Get the row/col indices corresponding to the given cluster
        
    row_indices, col_indices = model.get_indices(v)
    # Get the submatrix corresponding to the given cluster
    cluster = model.get_submatrix(in_data, v)
    
    # Count the number of each term
    p = cluster.sum(0)
    t = p.flatten()
    # Obtain all term names for the given cluster
    tmp_terms = np.array(all_terms)[col_indices]
    # Get the first n terms
    max_indices = t.argsort()[::-1][:nb_top_terms]

    pos = np.arange(nb_top_terms)

    #v = v + 1
    ax1 = plt.subplot(number_of_subplots, 1, i+1)
    ax1.barh(pos, t[max_indices][::-1], color='blue')
    ax1.set_title("Cluster %d (%d terms)" % (v+1, len(col_indices)), size=11)

    plt.yticks(.4 + pos, tmp_terms[max_indices][::-1], size=9.5)
    plt.xlabel(x_label, size=9)
    plt.margins(y=0.05)
    #_remove_ticks()
    plt.tick_params(axis='both', which='both', bottom='on', top='off',
    right='off', left='off')

  # Tight layout often produces nice results
  # but requires the title to be spaced accordingly
  plt.tight_layout()
  plt.subplots_adjust(top=0.88)

  return plt




# fig_to_uri
def fig_to_uri(fig):
	out_img = BytesIO()
	fig.savefig(out_img, format='png')
	fig.clf()
	plt.close('all')
	out_img.seek(0) # rewind file
	encoded = base64.b64encode(out_img.read()).decode("ascii").replace("\n", "")

	return "data:image/png;base64,{}".format(encoded)

# reorganized matrix

def plot_reorganized_matrix(X, model, precision=0.8, markersize=0.9):
	
	plt.figure(figsize=(20,8))
	row_indices = np.argsort(model.row_labels_)
	col_indices = np.argsort(model.column_labels_)
	X_reorg = X[row_indices, :]
	X_reorg = X_reorg[:, col_indices]
	plt.spy(X_reorg, precision=precision, markersize=markersize)
	_remove_ticks()
	return plt

# Modularity

def plot_convergence(criteria, criterion_name, marker='o'):

    plt.plot(criteria, marker=marker)
    plt.ylabel(criterion_name)
    plt.xlabel('Iterations')
    _remove_ticks()
    return plt

# Max modularities

def plot_max_modularities(max_modularities, range_n_clusters):

    # Prepare a subplot and set the axis tick values and labels
    fig, ax = plt.subplots()
    fig.canvas.draw()
    labels = np.arange(1, (len(max_modularities)), 1)
    plt.xticks(np.arange(0, len(max_modularities) + 1, 1))
    labels = range_n_clusters
    ax.set_xticklabels(labels)

    # Plot all max modularities
    plt.plot(max_modularities, marker='o')

    # Set the axis titles
    plt.ylabel("Final Modularity", size=10)
    plt.xlabel("Number of clusters", size=10)

    # Set the axis limits
    plt.xlim(-0.5, (len(max_modularities) - 0.5))
    plt.ylim((min(max_modularities) - 0.05 * min(max_modularities)),
             (max(max_modularities) + 0.05 * max(max_modularities)))

    # Set the main plot titlee
    plt.title("\nMax. modularity for %d clusters (%.4f)\n" %
              (range_n_clusters[max_modularities.index(max(max_modularities))],
               max(max_modularities)), size=12)

    # Remove automatic ticks
    plt.tick_params(axis='both', which='both', bottom='off', top='off',
                    right='off', left='off')

    # Plot a dashed vertical line at best partition
    plt.axvline(np.argmax(max_modularities), linestyle="dashed")
    return plt
