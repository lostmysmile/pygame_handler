import pygame

pygame.init()
screen = pygame.display.set_mode((600, 200))
pygame.display.set_caption("Pygame text input test")

font = pygame.font.Font(None, 32)
text = ""

pygame.key.start_text_input()
pygame.key.set_text_input_rect(pygame.Rect(20, 70, 400, 35))

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.TEXTINPUT:
            text += event.text

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_BACKSPACE:
                text = text[:-1]

    screen.fill("green")
    screen.blit(
        font.render(text, True, "black"),
        (20, 70),
    )
    pygame.display.flip()

pygame.key.stop_text_input()
pygame.quit()