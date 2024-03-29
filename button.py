import pygame

class Button:
    """Basic animated button class."""
    def __init__(self,text,width,height,pos,elevation,screen,gui_font,img = None):
        #Core attributes 
        self.pressed = False
        self.howered = False
        self.elevation = elevation
        self.dynamic_elecation = elevation
        self.original_y_pos = pos[1]
        self.original_x_pos = pos[0]
        self.screen = screen
        self.img = img

        # top rectangle 
        self.top_rect = pygame.Rect(pos,(width,height))
        self.top_color = '#F7F6F2'
        # bottom rectangle 
        self.bottom_rect = pygame.Rect(pos,(width,height))
        self.bottom_color = '#2C3639'
        #text
        self.text = text
        self.gui_font = gui_font
        self.text_surf = gui_font.render(self.text,True,'#000000')
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)

    def draw(self):
        """Draws button. Returns true if clicked."""
        # elevation logic
        self.text_surf = self.gui_font.render(self.text,True,'#000000')
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)
        self.top_rect.y = self.original_y_pos - self.dynamic_elecation
        self.text_rect.center = self.top_rect.center
        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elecation      
        pygame.draw.rect(self.screen,self.bottom_color, self.bottom_rect,border_radius = 12)
        pygame.draw.rect(self.screen,self.top_color, self.top_rect,border_radius = 12)
        
        if self.img != None:
            self.screen.blit(self.img, (self.original_x_pos,self.original_y_pos - self.dynamic_elecation))
        else:
            self.screen.blit(self.text_surf, self.text_rect)
        
        return self.check_click()

    def check_click(self):
        action = False
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.howered = True
            self.top_color = '#FFFFFF'
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elecation = 0
                self.pressed = True
            else:
                self.dynamic_elecation = self.elevation
                if self.pressed == True:
                    action = True
                    self.pressed = False
        else:
            self.howered = False
            self.dynamic_elecation = self.elevation
            self.top_color = '#F7F6F2'
        return action