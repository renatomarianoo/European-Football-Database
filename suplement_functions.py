import pandas as pd
import seaborn as sns
import xmltodict


def select_all_columns(table_name):
    '''General query for output of all of the columns of a dataframe in the database'''
    query = f"SELECT * FROM {table_name};"
    return query


def clear_barplot(
    ax,
    percent=0,
    vertical=True,
    plot_title="",
    label_on_bars=True,
    pad_top=13,
    pad_bottom=2,
    plot_xlabel="",
    plot_ylabel="",
    legend_visibility=False,
):

    ax.set(xlabel=plot_xlabel, ylabel=plot_ylabel)
    ax.set_title(plot_title, color="black", fontsize=15)
    ax.tick_params(
        axis="both",
        which="both",
        length=0,
    )
    
    # Frames
    if not legend_visibility:
        ax.legend([],frameon=legend_visibility)
    
    if vertical:
        ax.set_yticklabels([])
        sns.despine(left=True)
    else:
        ax.set_xticklabels([])
        sns.despine(bottom=True)

    # Plot on top of the bars
    if label_on_bars:
        if vertical: 
            if any(rect.get_height().is_integer() for rect in ax.containers[0].patches):
                for c in ax.containers:
                    ax.bar_label(c, padding=pad_top, color="black", fontsize=10.5)
            else:
                for c in ax.containers:
                    ax.bar_label(c, padding=pad_top, color="black", fontsize=10.5, fmt='%.2f')
        else: 
            if any(rect.get_width().is_integer() for rect in ax.containers[0].patches):
                for c in ax.containers:
                    ax.bar_label(c, padding=pad_top, color="black", fontsize=10.5)
            else:
                for c in ax.containers:
                    ax.bar_label(c, padding=pad_top, color="black", fontsize=10.5, fmt='%.2f')
            
    if percent != 0:
        ax.bar_label(
            ax.containers[0],
            padding=pad_bottom,
            labels=percent,
            color="#55185D",
            fontsize=9,
        )


def extract_goal_summary(goal_data):
    ''' Extracts the information in the goal column from xml to dictionary. Each dictionary in a cell contains information of a different goal. '''
    goal_summary = []
    if pd.notnull(goal_data):
        goals = xmltodict.parse(goal_data)['goal']

        if goals is not None:
            if type(goals['value']) == list:
                for i, goal in enumerate(goals['value']):
                    goal_info = {
                        'goal_nr': i+1,
                        'event_incident_typefk': goal.get('event_incident_typefk'),
                        'elapsed': goal.get('elapsed'),
                        'player2': goal.get('player2'),
                        'subtype': goal.get('subtype'),
                        'player1': goal.get('player1'),
                        'sortorder': goal.get('sortorder'),
                        'team': goal.get('team'),
                        'id': goal.get('id'),
                        'n': goal.get('n'),
                        'goal_type': goal.get('goal_type')
                    }
                    goal_summary.append(goal_info)
            elif type(goals['value']) == dict:
                goal_info = {
                    'goal_nr': 1,
                    'event_incident_typefk': goals['value'].get('event_incident_typefk'),
                    'elapsed': goals['value'].get('elapsed'),
                    'player2': goals['value'].get('player2'),
                    'subtype': goals['value'].get('subtype'),
                    'player1': goals['value'].get('player1'),
                    'sortorder': goals['value'].get('sortorder'),
                    'team': goals['value'].get('team'),
                    'id': goals['value'].get('id'),
                    'n': goals['value'].get('n'),
                    'goal_type': goals['value'].get('goal_type')
                }
                goal_summary.append(goal_info)
    return goal_summary


def get_season(date):
    '''Function to assign season labels based on dates'''
    
    # Define the start and end months for a season (July to June)
    start_month = 7
    end_month = 6
    
    if date.month >= start_month:  
        return str(date.year) + '/' + str(date.year + 1)
    else:  # Otherwise, it belongs to the previous season
        return str(date.year - 1) + '/' + str(date.year)