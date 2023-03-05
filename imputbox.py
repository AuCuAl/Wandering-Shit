import pygame
import pyperclip


class InputBox:
    def __init__(self, rect: pygame.Rect = pygame.Rect(100, 100, 140, 32)) -> None:
        """
        rect，传入矩形实体，传达输入框的位置和大小
        """
        self.boxBody: pygame.Rect = rect
        self.color_inactive = pygame.Color('lightskyblue3')  # 未被选中的颜色
        self.color_active = pygame.Color('dodgerblue2')  # 被选中的颜色
        self.color = self.color_inactive  # 当前颜色，初始为未激活颜色
        self.active = False
        self.text = ''
        self.done = False
        self._visible = True
        self.font = pygame.font.SysFont('SimSun ', 32)

    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, value):
        self._visible = value

    def dealEvent(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.boxBody.collidepoint(event.pos):  # 若按下鼠标且位置在文本框
                self.active = not self.active
            else:
                self.active = False
            self.color = self.color_active if(
                self.active) else self.color_inactive
        if event.type == pygame.KEYDOWN:  # 键盘输入响应
            if self.active:
                key_pressed = pygame.key.get_pressed()
                if key_pressed[pygame.K_BACKSPACE]:
                    self.text = self.text[:-1]
                elif key_pressed[pygame.K_LCTRL] and key_pressed[pygame.K_v]:
                    self.text += pyperclip.paste()
                else:
                    self.text += event.unicode

    def draw(self, screen: pygame.surface.Surface):
        if not self._visible:
            return
        txtSurface = self.font.render(self.text, False, self.color)  # 文字转换为图片
        width = max(self.boxBody.w, txtSurface.get_width()+10)  # 当文字过长时，延长文本框
        self.boxBody.w = width
        screen.blit(txtSurface, (self.boxBody.x + 5, self.boxBody.y + self.boxBody.h / 2 - txtSurface.get_height() / 2))
        pygame.draw.rect(screen, self.color, self.boxBody, 2)
