import matplotlib.pyplot as plt


def create_3d_text(angle):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.text(0.5, 0.5, 0.5, "Hello", fontsize=48, ha='center', va='center')
    ax.view_init(azim=angle)
    ax.axis('off')  # Hide axes
    plt.savefig(f'image_{angle}.png')


# Save images from two different angles
create_3d_text(0)  # Front view
create_3d_text(180)  # Rear view
