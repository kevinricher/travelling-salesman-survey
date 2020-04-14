import pandas as pd
from matplotlib import pyplot as plt


time_means = pd.DataFrame(columns=['BF', 'BNB', 'NN', 'RNN', 'ANN', 'GA'])
time_std_devs = pd.DataFrame(columns=['BF', 'BNB', 'NN', 'RNN', 'ANN', 'GA'])

normalized_distance_means = pd.DataFrame(
    columns=['BNB', 'NN', 'RNN', 'ANN', 'GA'])
normalized_distance_std_devs = pd.DataFrame(
    columns=['BNB', 'NN', 'RNN', 'ANN', 'GA'])

nn_normalized_distance_means = pd.DataFrame(columns=['NN', 'RNN', 'ANN', 'GA'])
nn_normalized_distance_std_devs = pd.DataFrame(
    columns=['NN', 'RNN', 'ANN', 'GA'])

for i in range(0, 61):
    j = i+5  # Dummy index for referencing file names, actual instance size.
    # -- TIME -- #
    time_df = pd.read_csv('./times/tsp_times_{}.csv'.format(j))
    time_df = time_df.drop(['Size'], axis=1)
    time_df_means = time_df.mean(axis=0, skipna=True)
    time_df_means.name = j
    time_df_std_devs = time_df.std(axis=0, skipna=True)
    time_df_std_devs.name = j
    time_means = time_means.append(time_df_means)
    time_std_devs = time_std_devs.append(time_df_std_devs)

    # Plot absolute time for all algorithms up to 65.

    # -- DISTANCE -- #
    distance_df = pd.read_csv(
        './distances/tsp_distances_{}.csv'.format(j))
    distance_df = distance_df.drop(['Size', 'BF'], axis=1)

    # Plot comparison of approximate vs. exact at low sizes.
    # Absolute length as % of optimal for NN options and GA.
    if j <= 17:
        # Calculate percentages normalized to optimal length.
        normalized_distances = distance_df.div(
            distance_df['BNB'], axis=0)
        nd_means = normalized_distances.mean(axis=0, skipna=True)
        nd_means.name = j
        nd_std_devs = normalized_distances.std(axis=0, skipna=True)
        nd_std_devs.name = j
        normalized_distance_means = normalized_distance_means.append(nd_means)
        normalized_distance_std_devs = normalized_distance_std_devs.append(
            nd_std_devs)

    # Plot % improvement of nearest neighbour alterations.
    # NN vs repeated NN vs altered NN.
    if j > 17:
        distance_df = distance_df.drop(['BNB'], axis=1)
        # Calculate percentages normalized to NN length.
        normalized_distances = distance_df.div(
            distance_df['NN'], axis=0)
        nn_nd_means = normalized_distances.mean(axis=0, skipna=True)
        nn_nd_means.name = j
        nn_nd_std_devs = normalized_distances.std(axis=0, skipna=True)
        nn_nd_std_devs.name = j

        nn_normalized_distance_means = nn_normalized_distance_means.append(
            nn_nd_means)
        nn_normalized_distance_std_devs = nn_normalized_distance_std_devs.append(
            nn_nd_std_devs)


# print("Mean times:")
# print(time_means)
# print("Time standard deviations:")
# print(time_std_devs)

# print("Mean normalized distances:")
# print(normalized_distance_means)
# print("Normalized distance standard deviations:")
# print(normalized_distance_std_devs)

# print("NN Mean normalized distances:")
# print(nn_normalized_distance_means)
# print("NN Normalized distance standard deviations:")
# print(nn_normalized_distance_std_devs)

# -- Time plots -- #
# time_means.plot()
# plt.yscale('log')
# plt.grid()
# plt.legend(loc='center right', bbox_to_anchor=(
#     1.1, 0.75), ncol=1, fancybox=True, shadow=True)
# plt.ylabel('Mean Run-time [log(s)]')
# plt.xlabel('Number of Cities')
# plt.axis('tight')
# plt.show()

# time_std_devs.plot()
# plt.yscale('log')
# plt.grid()
# plt.legend(loc='center right', bbox_to_anchor=(
#     1.1, 0.75), ncol=1, fancybox=True, shadow=True)
# plt.ylabel('Run-time Standard Deviation [log(s)]')
# plt.xlabel('Number of Cities')
# plt.show()

# # -- Distance Plots -- #
# normalized_distance_means.plot()
# plt.ylabel('Tour Mean Distance Normalized to Branch and Bound')
# plt.xlabel('Number of Cities')
# plt.legend(loc='best', fancybox=True, shadow=True)
# plt.grid()
# plt.show()

# normalized_distance_std_devs.plot()
# plt.ylabel('Tour Distance Standard Deviation Normalized to Branch and Bound')
# plt.xlabel('Number of Cities')
# plt.legend(loc='best', fancybox=True, shadow=True)
# plt.grid()
# plt.show()

# nn_normalized_distance_means.plot()
# plt.ylabel('Tour Mean Distance Normalized to Nearest Neighbour')
# plt.xlabel('Number of Cities')
# plt.legend(loc='best', fancybox=True, shadow=True)
# plt.grid()
# plt.show()

# nn_normalized_distance_std_devs.plot()
# plt.ylabel('Tour Distance Standard Deviation Normalized to Nearest Neighbour')
# plt.xlabel('Number of Cities')
# plt.legend(loc='best', fancybox=True, shadow=True)
# plt.show()
