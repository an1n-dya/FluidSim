import pygame
import pygame_gui
import settings as s

class UI:
    def __init__(self):
        self.manager = pygame_gui.UIManager((s.SCREEN_WIDTH, s.SCREEN_HEIGHT))
        self.create_ui_elements()

    def create_ui_elements(self):
        y_pos = 10
        
        # Labels and Sliders
        pygame_gui.elements.UILabel(relative_rect=pygame.Rect((10, y_pos), (200, 20)), text="Density Diffusion", manager=self.manager)
        y_pos += 25
        self.sliders = {
            'density': pygame_gui.elements.UIHorizontalSlider(
                relative_rect=pygame.Rect((10, y_pos), (200, 20)), start_value=s.DIFFUSION,
                value_range=(0.0, 0.001), manager=self.manager),
        }
        y_pos += 30

        pygame_gui.elements.UILabel(relative_rect=pygame.Rect((10, y_pos), (200, 20)), text="Velocity Diffusion", manager=self.manager)
        y_pos += 25
        self.sliders['velocity'] = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((10, y_pos), (200, 20)), start_value=s.VISCOSITY,
            value_range=(0.0, 0.00001), manager=self.manager)
        y_pos += 30

        pygame_gui.elements.UILabel(relative_rect=pygame.Rect((10, y_pos), (200, 20)), text="Vorticity", manager=self.manager)
        y_pos += 25
        self.sliders['vorticity'] = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((10, y_pos), (200, 20)), start_value=s.VORTICITY,
            value_range=(0.0, 5.0), manager=self.manager)
        y_pos += 30

        pygame_gui.elements.UILabel(relative_rect=pygame.Rect((10, y_pos), (200, 20)), text="Bloom Intensity", manager=self.manager)
        y_pos += 25
        self.sliders['bloom_intensity'] = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((10, y_pos), (200, 20)), start_value=s.BLOOM_INTENSITY,
            value_range=(0.1, 1.5), manager=self.manager)
        y_pos += 30

        pygame_gui.elements.UILabel(relative_rect=pygame.Rect((10, y_pos), (200, 20)), text="Bloom Threshold", manager=self.manager)
        y_pos += 25
        self.sliders['bloom_threshold'] = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((10, y_pos), (200, 20)), start_value=s.BLOOM_THRESHOLD,
            value_range=(0.1, 1.0), manager=self.manager)
        y_pos += 30

        pygame_gui.elements.UILabel(relative_rect=pygame.Rect((10, y_pos), (200, 20)), text="Sunrays Weight", manager=self.manager)
        y_pos += 25
        self.sliders['sunrays_weight'] = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((10, y_pos), (200, 20)), start_value=s.SUNRAYS_WEIGHT,
            value_range=(0.0, 1.0), manager=self.manager)
        y_pos += 40

        # Toggles
        self.toggles = {
            'shading': pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10, y_pos), (100, 30)), text='Shading', manager=self.manager),
            'colorful': pygame_gui.elements.UIButton(relative_rect=pygame.Rect((120, y_pos), (100, 30)), text='Colorful', manager=self.manager),
        }
        y_pos += 40
        self.toggles['bloom'] = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10, y_pos), (100, 30)), text='Bloom', manager=self.manager)
        self.toggles['sunrays'] = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((120, y_pos), (100, 30)), text='Sunrays', manager=self.manager)
        y_pos += 40
        self.toggles['random_splats'] = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10, y_pos), (120, 30)), text='Random Splats', manager=self.manager)

    def handle_event(self, event):
        self.manager.process_events(event)
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.toggles['shading']: s.SHADING = not s.SHADING
                if event.ui_element == self.toggles['colorful']: s.COLORFUL = not s.COLORFUL
                if event.ui_element == self.toggles['bloom']: s.BLOOM = not s.BLOOM
                if event.ui_element == self.toggles['sunrays']: s.SUNRAYS = not s.SUNRAYS
                if event.ui_element == self.toggles['random_splats']: s.RANDOM_SPLATS = not s.RANDOM_SPLATS

    def update(self, time_delta):
        self.manager.update(time_delta)

    def draw(self, screen):
        self.manager.draw_ui(screen)

    def get_values(self):
        values = {slider: control.get_current_value() for slider, control in self.sliders.items()}
        values.update({
            'shading': s.SHADING,
            'colorful': s.COLORFUL,
            'bloom': s.BLOOM,
            'sunrays': s.SUNRAYS,
            'random_splats': s.RANDOM_SPLATS
        })
        return values
