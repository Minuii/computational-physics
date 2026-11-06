import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.integrate import odeint
import pandas as pd
from datetime import datetime

class DoublePendulum:
    def __init__(self, L1=1.0, L2=1.0, m1=1.0, m2=1.0, theta1=120, theta2=30):
        # pendulum params
        self.L1 = L1  # length of pendulum 1
        self.L2 = L2  # length of pendulum 2
        self.m1 = m1  # mass of bob 1
        self.m2 = m2  # mass of bob 2
        self.g = 9.81  # gravity
        
        # initial angles (convert to radians)
        self.theta1_0 = np.radians(theta1)
        self.theta2_0 = np.radians(theta2)
        
        # initial state [theta1, omega1, theta2, omega2]
        self.state0 = [self.theta1_0, 0, self.theta2_0, 0]
        
        # data storage
        self.time_data = []
        self.theta1_data = []
        self.theta2_data = []
        self.omega1_data = []
        self.omega2_data = []
        self.x1_data = []
        self.y1_data = []
        self.x2_data = []
        self.y2_data = []
        self.energy_data = []
        
        # trail storage
        self.trail_x = []
        self.trail_y = []
        self.max_trail = 500
        
    def derivatives(self, state, t):
        """Calculate derivatives for ODE solver"""
        th1, w1, th2, w2 = state
        
        dth = th2 - th1
        
        # equations of motion for double pendulum
        den1 = (self.m1 + self.m2) * self.L1 - self.m2 * self.L1 * np.cos(dth) * np.cos(dth)
        den2 = (self.L2 / self.L1) * den1
        
        dth1_dt = w1
        
        dw1_dt = ((self.m2 * self.L1 * w1 * w1 * np.sin(dth) * np.cos(dth) +
                   self.m2 * self.g * np.sin(th2) * np.cos(dth) +
                   self.m2 * self.L2 * w2 * w2 * np.sin(dth) -
                   (self.m1 + self.m2) * self.g * np.sin(th1)) / den1)
        
        dth2_dt = w2
        
        dw2_dt = ((-self.m2 * self.L2 * w2 * w2 * np.sin(dth) * np.cos(dth) +
                   (self.m1 + self.m2) * self.g * np.sin(th1) * np.cos(dth) -
                   (self.m1 + self.m2) * self.L1 * w1 * w1 * np.sin(dth) -
                   (self.m1 + self.m2) * self.g * np.sin(th2)) / den2)
        
        return [dth1_dt, dw1_dt, dth2_dt, dw2_dt]
    
    def calc_energy(self, theta1, omega1, theta2, omega2):
        """Calculate total energy"""
        # positions
        x1 = self.L1 * np.sin(theta1)
        y1 = -self.L1 * np.cos(theta1)
        x2 = x1 + self.L2 * np.sin(theta2)
        y2 = y1 - self.L2 * np.cos(theta2)
        
        # velocities
        vx1 = self.L1 * omega1 * np.cos(theta1)
        vy1 = self.L1 * omega1 * np.sin(theta1)
        vx2 = vx1 + self.L2 * omega2 * np.cos(theta2)
        vy2 = vy1 + self.L2 * omega2 * np.sin(theta2)
        
        # kinetic energy
        KE = 0.5 * self.m1 * (vx1**2 + vy1**2) + 0.5 * self.m2 * (vx2**2 + vy2**2)
        
        # potential energy
        PE = self.m1 * self.g * y1 + self.m2 * self.g * y2
        
        return KE + PE
    
    def simulate(self, duration=20, fps=60):
        """Run simulation"""
        dt = 1.0 / fps
        t = np.arange(0, duration, dt)
        
        # solve ODE
        sol = odeint(self.derivatives, self.state0, t)
        
        # store data
        for i, time in enumerate(t):
            theta1, omega1, theta2, omega2 = sol[i]
            
            # positions
            x1 = self.L1 * np.sin(theta1)
            y1 = -self.L1 * np.cos(theta1)
            x2 = x1 + self.L2 * np.sin(theta2)
            y2 = y1 - self.L2 * np.cos(theta2)
            
            # energy
            E = self.calc_energy(theta1, omega1, theta2, omega2)
            
            # store
            self.time_data.append(time)
            self.theta1_data.append(np.degrees(theta1))
            self.theta2_data.append(np.degrees(theta2))
            self.omega1_data.append(np.degrees(omega1))
            self.omega2_data.append(np.degrees(omega2))
            self.x1_data.append(x1)
            self.y1_data.append(y1)
            self.x2_data.append(x2)
            self.y2_data.append(y2)
            self.energy_data.append(E)
        
        return sol, t
    
    def animate_pendulum(self, duration=20, fps=60):
        """Animate the pendulum"""
        sol, t = self.simulate(duration, fps)
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        # pendulum plot
        ax1.set_xlim(-2.5, 2.5)
        ax1.set_ylim(-2.5, 2.5)
        ax1.set_aspect('equal')
        ax1.grid(True, alpha=0.3)
        ax1.set_title('Double Pendulum')
        
        line, = ax1.plot([], [], 'o-', lw=2, color='black', markersize=8)
        trail, = ax1.plot([], [], 'r-', lw=1, alpha=0.5)
        time_text = ax1.text(0.02, 0.95, '', transform=ax1.transAxes)
        
        # angle plot
        ax2.set_xlim(0, duration)
        ax2.set_ylim(-180, 180)
        ax2.set_xlabel('Time (s)')
        ax2.set_ylabel('Angle (degrees)')
        ax2.set_title('Angles over Time')
        ax2.grid(True, alpha=0.3)
        
        angle1_line, = ax2.plot([], [], 'b-', label='θ1', lw=2)
        angle2_line, = ax2.plot([], [], 'r-', label='θ2', lw=2)
        ax2.legend()
        
        def init():
            line.set_data([], [])
            trail.set_data([], [])
            angle1_line.set_data([], [])
            angle2_line.set_data([], [])
            return line, trail, angle1_line, angle2_line, time_text
        
        def update(frame):
            theta1, omega1, theta2, omega2 = sol[frame]
            
            x1 = self.L1 * np.sin(theta1)
            y1 = -self.L1 * np.cos(theta1)
            x2 = x1 + self.L2 * np.sin(theta2)
            y2 = y1 - self.L2 * np.cos(theta2)
            
            # update pendulum
            line.set_data([0, x1, x2], [0, y1, y2])
            
            # update trail
            self.trail_x.append(x2)
            self.trail_y.append(y2)
            if len(self.trail_x) > self.max_trail:
                self.trail_x.pop(0)
                self.trail_y.pop(0)
            trail.set_data(self.trail_x, self.trail_y)
            
            # update angles
            angle1_line.set_data(self.time_data[:frame], self.theta1_data[:frame])
            angle2_line.set_data(self.time_data[:frame], self.theta2_data[:frame])
            
            time_text.set_text(f'Time: {t[frame]:.2f}s')
            
            return line, trail, angle1_line, angle2_line, time_text
        
        anim = FuncAnimation(fig, update, frames=len(t), init_func=init,
                           blit=True, interval=1000/fps, repeat=True)
        
        plt.tight_layout()
        plt.show()
    
    def export_to_excel(self, filename=None):
        """Export all data to Excel"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f'double_pendulum_data_{timestamp}.xlsx'
        
        # create dataframe
        df = pd.DataFrame({
            'Time (s)': self.time_data,
            'Theta1 (deg)': self.theta1_data,
            'Theta2 (deg)': self.theta2_data,
            'Omega1 (deg/s)': self.omega1_data,
            'Omega2 (deg/s)': self.omega2_data,
            'X1 (m)': self.x1_data,
            'Y1 (m)': self.y1_data,
            'X2 (m)': self.x2_data,
            'Y2 (m)': self.y2_data,
            'Total Energy (J)': self.energy_data
        })
        
        # write to excel with formatting
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Simulation Data', index=False)
            
            # add parameters sheet
            params_df = pd.DataFrame({
                'Parameter': ['L1 (m)', 'L2 (m)', 'm1 (kg)', 'm2 (kg)', 
                             'Initial θ1 (deg)', 'Initial θ2 (deg)', 'g (m/s²)'],
                'Value': [self.L1, self.L2, self.m1, self.m2,
                         np.degrees(self.theta1_0), np.degrees(self.theta2_0), self.g]
            })
            params_df.to_excel(writer, sheet_name='Parameters', index=False)
        
        print(f"Data exported to {filename}")
        return filename


# Example usage
if __name__ == "__main__":
    print("=" * 50)
    print("DOUBLE PENDULUM SIMULATOR")
    print("=" * 50)
    
    # get user input
    print("\nEnter pendulum parameters:")
    
    try:
        L1 = float(input("Length of rod 1 (m) [default=1.0]: ") or "1.0")
        L2 = float(input("Length of rod 2 (m) [default=1.0]: ") or "1.0")
        m1 = float(input("Mass of bob 1 (kg) [default=1.0]: ") or "1.0")
        m2 = float(input("Mass of bob 2 (kg) [default=1.0]: ") or "1.0")
        theta1 = float(input("Initial angle 1 (degrees) [default=120]: ") or "120")
        theta2 = float(input("Initial angle 2 (degrees) [default=30]: ") or "30")
        duration = float(input("Simulation duration (seconds) [default=20]: ") or "20")
        
        print("\n" + "=" * 50)
        print("CONFIGURATION:")
        print(f"  L1 = {L1} m, L2 = {L2} m")
        print(f"  m1 = {m1} kg, m2 = {m2} kg")
        print(f"  θ1 = {theta1}°, θ2 = {theta2}°")
        print(f"  Duration = {duration} s")
        print("=" * 50 + "\n")
        
    except ValueError:
        print("Invalid input! Using default values...")
        L1, L2, m1, m2 = 1.0, 1.0, 1.0, 1.0
        theta1, theta2 = 120, 30
        duration = 20
    
    # create pendulum
    pendulum = DoublePendulum(
        L1=L1,
        L2=L2,
        m1=m1,
        m2=m2,
        theta1=theta1,
        theta2=theta2
    )
    
    # run simulation
    print("Running simulation...")
    pendulum.animate_pendulum(duration=duration, fps=60)
    
    # export data
    export = input("\nExport data to Excel? (y/n) [default=y]: ") or "y"
    if export.lower() == 'y':
        custom_name = input("Enter filename (or press Enter for auto-name): ").strip()
        if custom_name and not custom_name.endswith('.xlsx'):
            custom_name += '.xlsx'
        pendulum.export_to_excel(custom_name if custom_name else None)
    
    print("\nSimulation complete!")
    print(f"Total data points: {len(pendulum.time_data)}")
    print(f"Energy conservation: {np.std(pendulum.energy_data):.6f} J (lower is better)")