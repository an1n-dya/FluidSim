import numpy as np
from scipy.ndimage import map_coordinates

class Fluid:
    def __init__(self, size, dt, diff, visc):
        self.size = size
        self.dt = dt
        self.diff = diff
        self.visc = visc

        self.s = np.zeros((size, size))
        self.density = np.zeros((size, size))

        self.vx = np.zeros((size, size))
        self.vy = np.zeros((size, size))

        self.vx0 = np.zeros((size, size))
        self.vy0 = np.zeros((size, size))
        
        # Vorticity related arrays
        self.curl = np.zeros((size, size))

    def step(self, vorticity_amount):
        # Vorticity confinement
        if vorticity_amount > 0:
            self._vorticity_confinement(vorticity_amount)

        self._diffuse(1, self.vx0, self.vx, self.visc)
        self._diffuse(2, self.vy0, self.vy, self.visc)

        self._project(self.vx0, self.vy0, self.vx, self.vy)

        self._advect(1, self.vx, self.vx0, self.vx0, self.vy0)
        self._advect(2, self.vy, self.vy0, self.vx0, self.vy0)

        self._project(self.vx, self.vy, self.vx0, self.vy0)

        self._diffuse(0, self.s, self.density, self.diff)
        self._advect(0, self.density, self.s, self.vx, self.vy)
        self.density *= 0.995 # fade out

    def add_density(self, x, y, amount):
        if 0 <= x < self.size and 0 <= y < self.size:
            self.density[x, y] += amount

    def add_velocity(self, x, y, amount_x, amount_y):
        if 0 <= x < self.size and 0 <= y < self.size:
            self.vx[x, y] += amount_x
            self.vy[x, y] += amount_y
            
    def _vorticity_confinement(self, amount):
        # Calculate curl
        self.curl[1:-1, 1:-1] = (self.vy[2:, 1:-1] - self.vy[:-2, 1:-1] -
                                 (self.vx[1:-1, 2:] - self.vx[1:-1, :-2])) * 0.5
        
        # Calculate gradient of curl magnitude
        grad_curl_x = (np.abs(self.curl[2:, 1:-1]) - np.abs(self.curl[:-2, 1:-1])) * 0.5
        grad_curl_y = (np.abs(self.curl[1:-1, 2:]) - np.abs(self.curl[1:-1, :-2])) * 0.5

        # Normalize gradient
        magnitude = np.sqrt(grad_curl_x**2 + grad_curl_y**2) + 1e-5
        grad_curl_x /= magnitude
        grad_curl_y /= magnitude
        
        # Apply confinement force
        force_x = grad_curl_y * self.curl[1:-1, 1:-1]
        force_y = -grad_curl_x * self.curl[1:-1, 1:-1]
        
        self.vx[1:-1, 1:-1] += amount * force_x * self.dt
        self.vy[1:-1, 1:-1] += amount * force_y * self.dt
        self._set_bnd(1, self.vx)
        self._set_bnd(2, self.vy)


    def _lin_solve(self, b, x, x0, a, c):
        c_recip = 1.0 / c
        for _ in range(20):
            x[1:-1, 1:-1] = (x0[1:-1, 1:-1] + a * (x[2:, 1:-1] + x[:-2, 1:-1] + x[1:-1, 2:] + x[1:-1, :-2])) * c_recip
            self._set_bnd(b, x)

    def _diffuse(self, b, x, x0, diff):
        a = self.dt * diff * (self.size - 2) * (self.size - 2)
        self._lin_solve(b, x, x0, a, 1 + 6 * a)

    def _project(self, veloc_x, veloc_y, p, div):
        div[1:-1, 1:-1] = -0.5 * (veloc_x[2:, 1:-1] - veloc_x[:-2, 1:-1] + veloc_y[1:-1, 2:] - veloc_y[1:-1, :-2]) / self.size
        p.fill(0)
        self._set_bnd(0, div)
        self._set_bnd(0, p)
        self._lin_solve(0, p, div, 1, 6)
        veloc_x[1:-1, 1:-1] -= 0.5 * (p[2:, 1:-1] - p[:-2, 1:-1]) * self.size
        veloc_y[1:-1, 1:-1] -= 0.5 * (p[1:-1, 2:] - p[1:-1, :-2]) * self.size
        self._set_bnd(1, veloc_x)
        self._set_bnd(2, veloc_y)

    def _advect(self, b, d, d0, veloc_x, veloc_y):
        dtx = self.dt * (self.size - 2)
        dty = self.dt * (self.size - 2)

        i, j = np.meshgrid(np.arange(self.size), np.arange(self.size), indexing='ij')
        tmp_x = np.clip(i - dtx * veloc_x, 0.5, self.size - 1.5)
        tmp_y = np.clip(j - dty * veloc_y, 0.5, self.size - 1.5)

        coords = np.array([tmp_x.flatten(), tmp_y.flatten()])
        d_flat = map_coordinates(d0, coords, order=1, mode='constant', cval=0)
        d[:] = d_flat.reshape(self.size, self.size)
        self._set_bnd(b, d)

    def _set_bnd(self, b, x):
        x[0, :] = -x[1, :] if b == 1 else x[1, :]
        x[-1, :] = -x[-2, :] if b == 1 else x[-2, :]
        x[:, 0] = -x[:, 1] if b == 2 else x[:, 1]
        x[:, -1] = -x[:, -2] if b == 2 else x[:, -2]
        x[0, 0] = 0.5 * (x[1, 0] + x[0, 1])
        x[0, -1] = 0.5 * (x[1, -1] + x[0, -2])
        x[-1, 0] = 0.5 * (x[-2, 0] + x[-1, 1])
        x[-1, -1] = 0.5 * (x[-2, -1] + x[-1, -2])
