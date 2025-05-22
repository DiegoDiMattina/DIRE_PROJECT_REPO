'''
Does all the graph computation and creation. Made for the DIRE project research group
'''
import plotly.graph_objects as go
import os


def plot_top_usage_values(data, top_n=10, save_path="top_websites_usage_values.html", topic="Telegram Data",
                          url_analysis_graph=False):
    save_dir = "../plotly_graphs"
    os.makedirs(save_dir, exist_ok=True)

    sorted_data = sorted(data.items(), key=lambda x: x[1][0], reverse=True)
    top_sites = sorted_data[:top_n]

    labels = [site[0] for site in top_sites]
    middle_values = [site[1][0] for site in top_sites]

    fig = go.Figure(data=[go.Bar(x=labels, y=middle_values, marker_color='skyblue')])

    fig.update_layout(
        title=f"Top {top_n} {'URLs' if url_analysis_graph else 'Websites'} by Usage Value for {topic}",
        xaxis_title="Website",
        yaxis_title="Usage",
        xaxis_tickangle=-45
    )

    full_save_path = os.path.join(save_dir, save_path)
    fig.write_html(full_save_path)
    return full_save_path


def plot_top_views_values(data, top_n=10, save_path="top_websites_views_values.html", topic="Telegram Data",
                          url_analysis_graph=False):
    save_dir = "../plotly_graphs"
    os.makedirs(save_dir, exist_ok=True)

    sorted_data = sorted(data.items(), key=lambda x: x[1][1], reverse=True)
    top_sites = sorted_data[:top_n]

    labels = [site[0] for site in top_sites]
    middle_values = [site[1][1] for site in top_sites]

    fig = go.Figure(data=[go.Bar(x=labels, y=middle_values, marker_color='skyblue')])

    fig.update_layout(
        title=f"Top {top_n} {'URLs' if url_analysis_graph else 'Websites'} by Views Value for {topic}",
        xaxis_title="Website",
        yaxis_title="Views",
        xaxis_tickangle=-45
    )

    full_save_path = os.path.join(save_dir, save_path)
    fig.write_html(full_save_path)
    return full_save_path


def plot_top_forwards_values(data, top_n=10, save_path="top_websites_forward_values.html", topic="Telegram Data",
                             url_analysis_graph=False):
    save_dir = "../plotly_graphs"
    os.makedirs(save_dir, exist_ok=True)

    sorted_data = sorted(data.items(), key=lambda x: x[1][2], reverse=True)
    top_sites = sorted_data[:top_n]

    labels = [site[0] for site in top_sites]
    middle_values = [site[1][2] for site in top_sites]

    fig = go.Figure(data=[go.Bar(x=labels, y=middle_values, marker_color='skyblue')])

    fig.update_layout(
        title=f"Top {top_n} {'URLs' if url_analysis_graph else 'Websites'} by Forwards Value for {topic}",
        xaxis_title="Website",
        yaxis_title="Forwards",
        xaxis_tickangle=-45
    )

    full_save_path = os.path.join(save_dir, save_path)
    fig.write_html(full_save_path)
    return full_save_path


def plot_and_save_top_occurrences(sort_dict, top_n=10, topic="", type=""):
    save_dir = "../plotly_graphs"
    os.makedirs(save_dir, exist_ok=True)

    if len(sort_dict) < top_n:
        top_n = len(sort_dict)

    top_items = list(sort_dict.items())[:top_n]

    labels, values = zip(*top_items)

    fig = go.Figure(data=[go.Bar(x=labels, y=values, marker_color='skyblue')])

    fig.update_layout(
        title=f"Top {top_n} Occurrences {topic}",
        xaxis_title=type,
        yaxis_title="Occurrences",
        xaxis_tickangle=-45
    )

    save_path = os.path.join(save_dir, f'top_occurrences_{topic}.html')
    fig.write_html(save_path)


def make_bar_graph_toxic(data, name):
    save_dir = "../plotly_graphs"
    os.makedirs(save_dir, exist_ok=True)

    fig = go.Figure(data=[go.Bar(x=list(data.keys()), y=list(data.values()), marker_color='skyblue')])

    fig.update_layout(
        title=f"Toxicity Levels {name}",
        xaxis_title="Categories",
        yaxis_title="Scores",
        xaxis_tickangle=-45
    )

    save_path = os.path.join(save_dir, f"{name}.html")
    fig.write_html(save_path)
