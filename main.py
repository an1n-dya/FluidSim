import pygame
import numpy as np
import settings as s
from fluid import Fluid
from visuals import Visuals
from ui import UI
from audio import Audio

class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((s.SCREEN_WIDTH, s.SCREEN_HEIGHT))
        pygame.display.set_caption("FluidSim")
        self.clock = pygame.time.Clock()
        self.fluid = Fluid(s.SIM_RESOLUTION, s.DT, s.DIFFUSION, s.VISCOSITY)
        self.visuals = Visuals(self.screen)
        self.ui = UI()
        self.audio = Audio()
        self.running = True
        self.mouse_pos = (0, 0)
        self.prev_mouse_pos = (0, 0)
        self.frame_count = 0

    def run(self):
        if s.AUDIO_VISUALIZER:
            self.audio.start_stream()

        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(s.FPS)
            self.frame_count += 1

        if s.AUDIO_VISUALIZER:
            self.audio.stop_stream()
        pygame.quit()

    def handle_events(self):
        self.prev_mouse_pos = self.mouse_pos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            self.ui.handle_event(event)
            if event.type == pygame.MOUSEMOTION:
                self.mouse_pos = event.pos

    def update(self):
        self.ui.update(self.clock.get_time() / 1000.0)
        ui_values = self.ui.get_values()
        s.update_settings_from_ui(ui_values)

        mouse_pressed = pygame.mouse.get_pressed()
        if mouse_pressed[0] or mouse_pressed[2]: # Left or Right click
            mx, my = self.mouse_pos
            px, py = self.prev_mouse_pos
            grid_x, grid_y = mx // s.SCALE, my // s.SCALE
            
            if mouse_pressed[0]: # Left click adds density
                self.fluid.add_density(grid_x, grid_y, 400)
            
            if mouse_pressed[2]: # Right click adds velocity
                amount_x = (mx - px) * 0.2
                amount_y = (my - py) * 0.2
                self.fluid.add_velocity(grid_x, grid_y, amount_x, amount_y)

        if s.RANDOM_SPLATS and self.frame_count % s.SPLAT_FREQUENCY == 0:
            self.add_random_splat()

        if s.AUDIO_VISUALIZER and self.audio.audio_data is not None:
            audio_level = np.mean(np.abs(self.audio.audio_data))
            if audio_level > 50: # Threshold
                x, y = np.random.randint(0, s.SIM_RESOLUTION, 2)
                self.fluid.add_density(x, y, audio_level)
                self.fluid.add_velocity(x, y,
                                        (np.random.rand() - 0.5) * audio_level * 0.01,
                                        (np.random.rand() - 0.5) * audio_level * 0.01)

        self.fluid.step(s.VORTICITY)

    def add_random_splat(self):
        x, y = np.random.randint(s.SIM_RESOLUTION // 4, s.SIM_RESOLUTION * 3 // 4, 2)
        self.fluid.add_density(x, y, np.random.randint(500, 1000))
        vel_x = (np.random.rand() - 0.5) * 5
        vel_y = (np.random.rand() - 0.5) * 5
        self.fluid.add_velocity(x, y, vel_x, vel_y)

    def draw(self):
        self.visuals.draw_background()
        self.visuals.draw_fluid(self.fluid)
        self.ui.draw(self.screen)
        pygame.display.flip()

if __name__ == '__main__':
    main = Main()
    main.run()
