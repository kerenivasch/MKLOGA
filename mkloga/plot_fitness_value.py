import matplotlib.pyplot as plt

plt.style.use('seaborn') # pretty matplotlib plots
plt.rcParams['figure.figsize'] = (12, 8)

def fitness_values_extractor(logs_file_path):
    with open(logs_file_path, 'r') as file:
        lines = file.readlines()

    fitness_values = list()
    for line in lines:
        if 'fitness value' in line.lower():
            fitness_values.append(float(line.split(': ')[-1]))
    fitness_values = fitness_values[:-1]

    fitness_values = [fitness_value for i, fitness_value in enumerate(fitness_values) \
                        if i == 0 or (i + 1) % 5 == 0]

    return fitness_values

if __name__ == '__main__':
    searches_to_plot = [
        {
            'display_name': 'Letters Only - Two Hands',
            'logs_file_path': 'searched_characters_placements/letters_only_dir/logs',
            'color': 'k',
            'marker': 'o',
            'linestyle': 'solid'
        },
        {
            'display_name': 'Letters and Punctuations - Two Hands',
            'logs_file_path': 'searched_characters_placements/letters_and_punctuations_dir/logs',
            'color': 'k',
            'marker': 'o',
            'linestyle': 'dashed'
        },
        {
            'display_name': 'Letters Only - Left Handed',
            'logs_file_path': 'searched_characters_placements/letters_only_left_handed_dir/logs',
            'color': 'r',
            'marker': 's',
            'linestyle': 'solid'
        },
        {
            'display_name': 'Letters and Punctuations - Left Handed',
            'logs_file_path': 'searched_characters_placements/letters_and_punctuations_left_handed_dir/logs',
            'color': 'r',
            'marker': 's',
            'linestyle': 'dashed'
        },
        {
            'display_name': 'Letters Only - Right Handed',
            'logs_file_path': 'searched_characters_placements/letters_only_right_handed_dir/logs',
            'color': 'b',
            'marker': 'D',
            'linestyle': 'solid'
        },
        {
            'display_name': 'Letters and Punctuations - Right Handed',
            'logs_file_path': 'searched_characters_placements/letters_and_punctuations_right_handed_dir/logs',
            'color': 'b',
            'marker': 'D',
            'linestyle': 'dashed'
        }
    ]

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    plt.xlabel('Generation Number', fontsize=20)
    plt.ylabel('Fitness Value', fontsize=20)

    for search_to_plot in searches_to_plot:
        fitness_values = fitness_values_extractor(search_to_plot['logs_file_path'])
        ax.plot(
            [1] + [i for i in range(5, 101, 5)],
            fitness_values,
            label=search_to_plot['display_name'],
            linestyle=search_to_plot['linestyle'],
            color=search_to_plot['color'],
            marker=search_to_plot['marker'],
            markersize=8,
            linewidth=2
        )

    plt.xticks([1] + [i for i in range(5, 101, 5)])
    # plt.yticks([])

    for tick in ax.yaxis.get_major_ticks():
        tick.label.set_fontsize(16)
    for tick in ax.xaxis.get_major_ticks():
        tick.label.set_fontsize(16)

    plt.legend(fontsize=15)
    plt.show()
