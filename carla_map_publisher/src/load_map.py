import carla
import matplotlib.pyplot as plt
import networkx as nx


client = carla.Client("localhost", 2000)
client.set_timeout(10.0)

world = client.get_world()
carla_map = world.get_map()

topology = carla_map.get_topology()

Graph = nx.DiGraph()

for start_wp, end_wp in topology:

    Graph.add_node(
        start_wp.id,
        x=start_wp.transform.location.x,
        y=start_wp.transform.location.y,
        z=start_wp.transform.location.z,
        road_id=start_wp.road_id,
        lane_id=start_wp.lane_id
    )

    Graph.add_node(
        end_wp.id,
        x=end_wp.transform.location.x,
        y=end_wp.transform.location.y,
        z=end_wp.transform.location.z,
        road_id=end_wp.road_id,
        lane_id=end_wp.lane_id
    )

    Graph.add_edge(start_wp.id, end_wp.id)

print(Graph)
print(Graph.number_of_nodes())
print(Graph.number_of_edges())

# Extract node positions
pos = {
    n: (Graph.nodes[n]["x"], Graph.nodes[n]["y"])
    for n in Graph.nodes()
}

origin_node = [15223939949176792440]
destination_node = [18053682451657546901]

origin= 15223939949176792440
destination= 18053682451657546901

# Create figure and axis
fig, ax = plt.subplots(figsize=(12, 12))


# Draw edges
nx.draw_networkx_edges(
    Graph,
    pos,
    ax=ax,
    edge_color="black",
    width=0.7,
    arrows=True,
    arrowstyle="-|>",
    arrowsize=6,
    connectionstyle="arc3,rad=0.0"
)

# Draw nodes
nx.draw_networkx_nodes(
    Graph,
    pos,
    ax=ax,
    node_size=15,
    node_color="blue"
)

# mark origin node
nx.draw_networkx_nodes(
    Graph,
    pos,
    nodelist=origin_node,
    node_color="yellow",
    node_size=100,
    ax=ax
)

# mark destination node
nx.draw_networkx_nodes(
    Graph,
    pos,
    nodelist=destination_node,
    node_color="yellow",
    node_size=100,
    ax=ax
)

path = nx.shortest_path(
    Graph,
    source=origin,
    target=destination
)

print(path)

path_edges = list(zip(path[:-1], path[1:]))

nx.draw_networkx_edges(
    Graph,
    pos,
    edgelist=path_edges,
    edge_color="red",
    width=3,
    ax=ax
)

nx.draw_networkx_nodes(
    Graph,
    pos,
    nodelist=path,
    node_color="green",
    node_size=50,
    ax=ax
)

# (Optional) Draw node IDs
#nx.draw_networkx_labels(Graph, pos, ax=ax, font_size=6)

ax.set_aspect("equal", adjustable="box")
ax.set_xlabel("X (m)")
ax.set_ylabel("Y (m)")
ax.set_title("CARLA Town10HD Road Network (Topology)")
ax.grid(True, linestyle="--", alpha=0.5)

plt.show()