import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


class MobiusStrip:
    """A class to model a Möbius strip and compute its geometric properties."""

    def __init__(self, R=1.0, w=0.5, n=100):
        """
        Initialize the Möbius strip with given parameters.
        
        Parameters:
        - R (float): Radius from center to the strip's midline (default: 1.0)
        - w (float): Width of the strip (default: 0.5)
        - n (int): Resolution (number of points in each parametric direction, default: 100)
        """
        self.R = R
        self.w = w
        self.n = n
        self.u = np.linspace(0, 2 * np.pi, n)
        self.v = np.linspace(-w / 2, w / 2, n)
        self.U, self.V = np.meshgrid(self.u, self.v)
        self.mesh = None
        self._generate_mesh()

    def _generate_mesh(self):
        """Generate the 3D mesh of the Möbius strip using parametric equations."""
        u, v = self.U, self.V
        x = (self.R + v * np.cos(u / 2)) * np.cos(u)
        y = (self.R + v * np.cos(u / 2)) * np.sin(u)
        z = v * np.sin(u / 2)
        self.mesh = (x, y, z)

    def compute_surface_area(self):
        """
        Compute the surface area using numerical integration.
        Uses the cross product of partial derivatives to approximate the area.
        """
        u, v = self.U, self.V
        # Partial derivatives with respect to u and v
        x_u = -(self.R + v * np.cos(u / 2)) * np.sin(u) - \
            (v / 2) * np.sin(u / 2) * np.cos(u)
        y_u = (self.R + v * np.cos(u / 2)) * np.cos(u) - \
            (v / 2) * np.sin(u / 2) * np.sin(u)
        z_u = (v / 2) * np.cos(u / 2)

        x_v = np.cos(u / 2) * np.cos(u)
        y_v = np.cos(u / 2) * np.sin(u)
        z_v = np.sin(u / 2)

        # Cross product magnitude gives the area element
        integrand = np.sqrt((y_u * z_v - z_u * y_v)**2 +
                            (z_u * x_v - x_u * z_v)**2 +
                            (x_u * y_v - y_u * x_v)**2)

        # Numerical integration over u and v
        du = self.u[1] - self.u[0]
        dv = self.v[1] - self.v[0]
        area = np.sum(integrand) * du * dv
        return area

    def compute_edge_length(self):
        """
        Compute the edge length of the Möbius strip (single boundary).
        Approximates by summing segment lengths along v = w/2.
        """
        u = self.u
        # Parametric equations for the edge at v = w/2
        x = (self.R + (self.w / 2) * np.cos(u / 2)) * np.cos(u)
        y = (self.R + (self.w / 2) * np.cos(u / 2)) * np.sin(u)
        z = (self.w / 2) * np.sin(u / 2)

        # Compute derivatives with respect to u
        dx_du = -(self.R + (self.w / 2) * np.cos(u / 2)) * \
            np.sin(u) - (self.w / 4) * np.sin(u / 2) * np.cos(u)
        dy_du = (self.R + (self.w / 2) * np.cos(u / 2)) * \
            np.cos(u) - (self.w / 4) * np.sin(u / 2) * np.sin(u)
        dz_du = (self.w / 4) * np.cos(u / 2)

        # Arc length integrand
        integrand = np.sqrt(dx_du**2 + dy_du**2 + dz_du**2)
        du = u[1] - u[0]
        length = np.sum(integrand) * du
        return length

    def plot(self):
        """Visualize the Möbius strip in 3D."""
        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_subplot(111, projection='3d')
        x, y, z = self.mesh
        ax.plot_surface(x, y, z, cmap='viridis', alpha=0.8)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title('Möbius Strip')
        plt.savefig('mobius_strip.png')
        plt.close()


if __name__ == "__main__":
    # Create a Möbius strip instance
    mobius = MobiusStrip(R=4.0, w=0.4, n=100)

    # Compute geometric properties
    area = mobius.compute_surface_area()
    edge_length = mobius.compute_edge_length()

    # Print results
    print(f"Surface Area: {area:.4f} square units")
    print(f"Edge Length: {edge_length:.4f} units")

    # Generate 3D plot
    mobius.plot()