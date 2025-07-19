import pygame
import numpy as np
import settings as s
from scipy.ndimage import gaussian_filter

class Visuals:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.background_image = None
        if s.BACKGROUND_IMAGE:
            try:
                self.background_image = pygame.image.load(s.BACKGROUND_IMAGE).convert()
                self.background_image = pygame.transform.scale(self.background_image, (s.SCREEN_WIDTH, s.SCREEN_HEIGHT))
            except pygame.error:
                print(f"Warning: Could not load background image at {s.BACKGROUND_IMAGE}")
                self.background_image = None

    def draw_background(self):
        if self.background_image:
            self.screen.blit(self.background_image, (0, 0))
        else:
            self.screen.fill(s.BACKGROUND_COLOR)

    def draw_fluid(self, fluid):
        density = np.clip(fluid.density, 0, 255)
        surface = pygame.Surface((s.SIM_RESOLUTION, s.SIM_RESOLUTION))
        
        if s.COLORFUL:
            color_array = self.get_colorful(density)
        else:
            color_array = self.get_monochromatic(density)
            
        pygame.surfarray.blit_array(surface, color_array)
        surface = pygame.transform.scale(surface, (s.SCREEN_WIDTH, s.SCREEN_HEIGHT))
        
        if s.BLOOM:
            surface = self.apply_bloom(surface)
        if s.SUNRAYS:
            surface = self.apply_sunrays(surface)
        
        self.screen.blit(surface, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)

    def get_monochromatic(self, density):
        color_array = np.zeros((s.SIM_RESOLUTION, s.SIM_RESOLUTION, 3))
        color_array[..., 0] = density
        color_array[..., 1] = density
        color_array[..., 2] = density
        return color_array
    
    def get_colorful(self, density):
        color_array = np.zeros((s.SIM_RESOLUTION, s.SIM_RESOLUTION, 3))
        hue = (pygame.time.get_ticks() / 1000.0) * 50 % 360
        color = pygame.Color(0)
        color.hsva = (hue, 100, 100, 100)
        color_array[..., 0] = density * (color.r / 255.0)
        color_array[..., 1] = density * (color.g / 255.0)
        color_array[..., 2] = density * (color.b / 255.0)
        return color_array

    def apply_bloom(self, surface):
        bloom_surface = pygame.Surface((s.SCREEN_WIDTH, s.SCREEN_HEIGHT))
        bloom_surface.blit(surface, (0, 0))
        
        bloom_array = pygame.surfarray.array3d(bloom_surface)
        
        threshold_mask = np.mean(bloom_array, axis=2) > s.BLOOM_THRESHOLD * 255
        bloom_array[~threshold_mask] = 0
        
        bloom_array = gaussian_filter(bloom_array, sigma=(s.BLOOM_INTENSITY * 10, s.BLOOM_INTENSITY * 10, 0))
        
        pygame.surfarray.blit_array(bloom_surface, bloom_array)
        surface.blit(bloom_surface, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
        return surface

    def apply_sunrays(self, surface):
        sunrays_surface = pygame.Surface((s.SCREEN_WIDTH, s.SCREEN_HEIGHT), pygame.SRCALPHA)
        center = (s.SCREEN_WIDTH // 2, s.SCREEN_HEIGHT // 2)

        for i in range(0, 360, 5):
            end_pos = (center[0] + 1000 * np.cos(np.radians(i)), center[1] + 1000 * np.sin(np.radians(i)))
            pygame.draw.line(sunrays_surface, (255, 255, 255, int(255 * s.SUNRAYS_WEIGHT * 0.1)), center, end_pos, 2)
            
        temp_surface = surface.copy()
        temp_surface.blit(sunrays_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        surface.blit(temp_surface, (0, 0))
        return surface
