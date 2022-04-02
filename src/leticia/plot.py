import numpy as np
import json
import matplotlib.pyplot as plt
from matplotlib import animation, colors
from matplotlib.colors import Normalize, TwoSlopeNorm
import numpy.ma as ma

# Load data from ./output
output_json = json.load(open('output/output.json'))
n_row = output_json['n_row']
n_col = output_json['n_col']
params = output_json['params']

points = np.load('output/points.npy')
variables = np.load('output/variables.npy')
current_variables = variables.reshape(variables.shape[0], variables.shape[1],
                                      -1)[np.arange(len(points)), :, points]
linear_combination = np.einsum('j,ijkl->ikl', params, variables)
current_linear_combination = linear_combination.reshape(
    variables.shape[0], -1)[np.arange(len(points)), points]

print(np.array(params).shape)
print(np.array(variables).shape)
print(np.array(linear_combination).shape)

list_probabilities = np.load('output/probabilities.npy')
list_probabilities.sum(0)
list_probabilities /= list_probabilities.sum((1, 2))[:, np.newaxis, np.newaxis]
list_probabilities[-1] = 0


def truncate_colormap(cmap, minval=0.0, maxval=1.0, n=100):
    new_cmap = colors.LinearSegmentedColormap.from_list(
        'trunc({n},{a:.2f},{b:.2f})'.format(n=cmap.name, a=minval, b=maxval),
        cmap(np.linspace(minval, maxval, n)))
    return new_cmap


cmap = plt.get_cmap('RdYlBu')
new_cmap = truncate_colormap(cmap, 0.3, 0.7)


class Animation():

    def __init__(self, n_row, n_col, points, linear_combination,
                 list_probabilities):
        self.fig, self.ax = plt.subplots()
        self.points = points
        self.linear_combination = linear_combination
        self.list_probabilities = list_probabilities
        self.n_row = n_row
        self.n_col = n_col

        self.im1 = self.ax.imshow(
            np.ones((self.n_row, self.n_col), dtype='bool'),
            interpolation='none',
            cmap=new_cmap,
        )
        self.cb = self.fig.colorbar(self.im1)

        self.mask = np.ones((self.n_row, self.n_col), dtype='bool')
        masked_grid = ma.masked_array(np.ones((n_row, n_col)), mask=~self.mask)
        self.im2 = self.ax.imshow(masked_grid, cmap="Greens", vmin=0, vmax=1.2)

    def __call__(self, i):
        print(i)
        self.im1.set_array(
            ma.masked_array(self.linear_combination[i],
                            mask=self.list_probabilities[i] == 0))

        self.im1.set_norm(
            TwoSlopeNorm(
                vmin=self.linear_combination[i].min(
                    where=~np.isinf(self.linear_combination[i])
                    & (self.list_probabilities[i] != 0),
                    initial=-10),
                vcenter=0,
                vmax=self.linear_combination[i].max(
                    where=~np.isinf(self.linear_combination[i])
                    & (self.list_probabilities[i] != 0),
                    initial=1),
            ))

        self.mask[:] = 0
        self.mask.flat[self.points[:i]] = 1
        data = np.ones((n_row, n_col))
        if i > 0:
            self.ax.set_title(
                f'{i=};\n {current_variables[i-1]} = {current_linear_combination[i-1]:0.4f}'
            )
            data.flat[self.points[i - 1]] = 1.2

        masked_grid = ma.masked_array(data, mask=~self.mask)
        self.im2.set_array(masked_grid)

        return self.im1, self.im2,


#fig_animation = Animation(n_row, n_col, points, list_probabilities)
#fig_animation.animate(len(points))
#plt.show()

fig_animation = Animation(n_row, n_col, points, linear_combination,
                          list_probabilities)
anim = animation.FuncAnimation(
    fig_animation.fig,
    func=fig_animation,
    frames=len(points) + 1,
    interval=1,
    blit=True,
)

#plt.show()
with open('output/output.html', 'w') as f:
    f.write(anim.to_jshtml())
#anim.save('animation.mp4', fps=3, extra_args=['-vcodec', 'libx264'])
