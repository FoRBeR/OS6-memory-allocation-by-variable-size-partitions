import pygame

pygame.init()


class Window:
    def __init__(self):
        self.disk = 65536
        self.busy_mem = 0
        self.table = [[True, 0, 65536]]  # таблица областей [свободна ли, индекс начала, размер]
        self.queue = []  # очередь задач, которые не поместились

        self.clean_app = pygame.image.load('pic/clean_app.bmp')
        self.font = pygame.font.Font('font/CascadiaCode-ExtraLight.ttf', 30)

        self.enter_pressed = pygame.image.load('pic/pressed_button.bmp')
        self.enter_button_rect = pygame.Rect(130, 135, 250, 50)
        self.enter_rect = pygame.Rect(262, 34, 200, 50)
        self.is_writing = False
        self.text_written = ''

        self.full_info = False
        self.switch_on = pygame.image.load('pic/switch_on.bmp')
        self.switch_rect = pygame.Rect(426, 246, 76, 39)

        self.clean_task = pygame.image.load('pic/command.bmp')
        self.clean_queue = pygame.image.load('pic/queue.bmp')
        self.task_button = pygame.image.load('pic/command_button.bmp')
        self.queue_button = pygame.image.load('pic/queue_button.bmp')
        self.tasks_rect = pygame.Rect(517, 3, 318, 696)
        self.queue_rect = pygame.Rect(837, 3, 318, 696)
        self.tasks_pos = 0  # позиция перемотки колесиком задач, в пикселях
        self.max_tasks_pos = 0  # максимальная перемотка задач
        self.queue_pos = 0  # позиция перемотки колесиком очереди, в пикселях
        self.max_queue_pos = 0  # максимальная перемотка очереди
        self.tasks_buttons_rects = []
        self.queue_buttons_rects = []

    def check_queue(self):
        old_queue = self.queue.copy()
        self.queue = []
        for i in old_queue:
            self.add_task(i)

    def add_task(self, size):
        for i in range(len(self.table)):
            if self.table[i][0] and self.table[i][2] == size:
                self.table[i][0] = False
                self.busy_mem += size
                return
            elif self.table[i][0] and self.table[i][2] > size:
                self.table[i][0] = False
                x = self.table[i][2]
                self.table[i][2] = size
                self.table.insert(i + 1, [True, self.table[i][1] + self.table[i][2], x - size])
                self.busy_mem += size
                return
        self.queue.append(size)

    def check_table(self):
        changes = True
        while changes:
            changes = False
            for i in range(1, len(self.table)):
                if self.table[i][0] and self.table[i - 1][0]:
                    self.table[i - 1][2] += self.table[i][2]
                    self.table.pop(i)
                    changes = True
                    break

    def del_task(self, index):
        count = -1
        for i in self.table:
            if not i[0]:
                count += 1
                if count == index:
                    i[0] = True
                    self.busy_mem -= i[2]
                    self.check_table()

    def gen_work_surf(self):
        count = 0
        for i in self.table:
            if not i[0]:
                count += 1
        if count == 0:
            return pygame.Surface((0, 0))
        self.max_tasks_pos = 0
        if count * 85 - 9 > 616:
            self.max_tasks_pos = count * 85 - 616
        surf = pygame.Surface((300, count * 85 - 9))
        surf.fill((235, 208, 247))
        count = 0
        self.tasks_buttons_rects = []
        for i in self.table:
            if not i[0]:
                task_surf = self.clean_task.copy()
                button = self.task_button.copy()
                self.tasks_buttons_rects.append(button.get_rect(x=711, y=97 + 85 * count - self.tasks_pos))
                task_surf.blit(button, (185, 15))
                text = self.font.render(str(i[2]), True, (0, 0, 0))
                task_surf.blit(text, (90, 20))
                surf.blit(task_surf, (0, count * 85))
                count += 1
        return surf

    def gen_queue_surf(self):
        if len(self.queue) == 0:
            return pygame.Surface((0, 0))
        self.max_queue_pos = 0
        if len(self.queue) * 85 - 9 > 616:
            self.max_queue_pos = len(self.queue) * 85 - 616
        surf = pygame.Surface((300, len(self.queue) * 85 - 9))
        surf.fill((235, 208, 247))
        count = 0
        self.queue_buttons_rects = []
        for i in self.queue:
            queue_surf = self.clean_queue.copy()
            button = self.queue_button.copy()
            self.queue_buttons_rects.append(button.get_rect(x=1031, y=97 + 85 * count - self.queue_pos))
            queue_surf.blit(button, (185, 15))
            text = self.font.render(str(i), True, (0, 0, 0))
            queue_surf.blit(text, (90, 20))
            surf.blit(queue_surf, (0, count * 85))
            count += 1
        return surf

    def gen_info_surf(self):
        surf = pygame.Surface((512, 383))
        surf.fill((235, 208, 247))
        line = pygame.Surface((65536, 2))
        line.fill((0, 255, 0))
        for i in self.table:
            if not i[0]:
                pygame.draw.rect(line, (225, 31, 15), (i[1], 0, i[2], 1))
        for i in range(128):
            surf.blit(line, (0, i * 3), area=(i * 512, 0, 512, 1))
        return surf

    def event_work(self, event):
        self.check_queue()
        match event.type:
            case pygame.MOUSEBUTTONDOWN if self.enter_rect.collidepoint(event.pos) and event.button == 1:
                self.is_writing = True
            case pygame.MOUSEBUTTONDOWN if self.switch_rect.collidepoint(event.pos) and event.button == 1:
                self.is_writing = False
                self.full_info = False if self.full_info else True
            case pygame.MOUSEBUTTONDOWN if self.enter_button_rect.collidepoint(event.pos) and event.button == 1:
                self.is_writing = False
                if self.text_written != '' and 0 < int(self.text_written) < self.disk:
                    self.add_task(int(self.text_written))
                    self.text_written = ''
            case pygame.MOUSEBUTTONDOWN if self.tasks_rect.collidepoint(event.pos) and (
                    event.button == 4 or event.button == 5):
                match event.button:
                    case 4:
                        self.tasks_pos -= 20
                        if self.tasks_pos < 0:
                            self.tasks_pos = 0
                    case 5:
                        self.tasks_pos += 20
                        if self.tasks_pos > self.max_tasks_pos:
                            self.tasks_pos = self.max_tasks_pos
            case pygame.MOUSEBUTTONDOWN if self.queue_rect.collidepoint(event.pos) and (
                    event.button == 4 or event.button == 5):
                match event.button:
                    case 4:
                        self.queue_pos -= 20
                        if self.queue_pos < 0:
                            self.queue_pos = 0
                    case 5:
                        self.queue_pos += 20
                        if self.queue_pos > self.max_queue_pos:
                            self.queue_pos = self.max_queue_pos
            case pygame.MOUSEBUTTONDOWN if event.button == 1 and event.pos[1] > 80:
                self.is_writing = False
                for i in range(len(self.tasks_buttons_rects)):
                    if self.tasks_buttons_rects[i].collidepoint(event.pos):
                        self.del_task(i)
                for i in range(len(self.queue_buttons_rects)):
                    if self.queue_buttons_rects[i].collidepoint(event.pos):
                        self.queue.pop(i)  # удаление элемента из очереди
            case pygame.MOUSEBUTTONDOWN if event.button == 1:
                self.is_writing = False
            case pygame.KEYDOWN if self.is_writing:
                if len(self.text_written) < 5:
                    if event.key == pygame.K_0 or event.key == pygame.K_KP_0:
                        self.text_written += '0'
                    elif event.key == pygame.K_1 or event.key == pygame.K_KP_1:
                        self.text_written += '1'
                    elif event.key == pygame.K_2 or event.key == pygame.K_KP_2:
                        self.text_written += '2'
                    elif event.key == pygame.K_3 or event.key == pygame.K_KP_3:
                        self.text_written += '3'
                    elif event.key == pygame.K_4 or event.key == pygame.K_KP_4:
                        self.text_written += '4'
                    elif event.key == pygame.K_5 or event.key == pygame.K_KP_5:
                        self.text_written += '5'
                    elif event.key == pygame.K_6 or event.key == pygame.K_KP_6:
                        self.text_written += '6'
                    elif event.key == pygame.K_7 or event.key == pygame.K_KP_7:
                        self.text_written += '7'
                    elif event.key == pygame.K_8 or event.key == pygame.K_KP_8:
                        self.text_written += '8'
                    elif event.key == pygame.K_9 or event.key == pygame.K_KP_9:
                        self.text_written += '9'
                if event.key == pygame.K_BACKSPACE:
                    if self.text_written != '':
                        self.text_written = self.text_written[:-1]

    def update(self):
        surf = self.clean_app.copy()
        # обработка ввода команды
        if pygame.mouse.get_pressed()[0] and self.enter_button_rect.collidepoint(pygame.mouse.get_pos()):
            surf.blit(self.enter_pressed, self.enter_button_rect)
        if self.is_writing:
            self.text_written += '|'
        if len(self.text_written) != 0:
            text = self.font.render(self.text_written, True, (0, 0, 0))
            text_rect = text.get_rect(center=(361, 58))
            surf.blit(text, text_rect)
            if self.text_written[-1] == '|':
                self.text_written = self.text_written[:-1]
        # обработка информации о памяти
        free_mem = str(self.disk - self.busy_mem)
        text = self.font.render(free_mem, True, (0, 0, 0))
        text_rect = text.get_rect(center=(199, 237))
        surf.blit(text, text_rect)
        text = self.font.render(str(self.busy_mem), True, (0, 0, 0))
        text_rect = text.get_rect(center=(199, 285))
        surf.blit(text, text_rect)
        if self.full_info:
            surf.blit(self.switch_on, self.switch_rect)
            surf.blit(self.gen_info_surf(), (2, 315))
        # отрисовка запущенного
        work_surf = pygame.Surface((300, 616))
        work_surf.fill((235, 208, 247))
        work_surf.blit(self.gen_work_surf(), (0, 0), area=(0, self.tasks_pos, 300, 616))
        surf.blit(work_surf, (527, 83))
        # отрисовка очереди
        work_surf = pygame.Surface((300, 616))
        work_surf.fill((235, 208, 247))
        work_surf.blit(self.gen_queue_surf(), (0, 0), area=(0, self.queue_pos, 300, 616))
        surf.blit(work_surf, (847, 83))
        sc.blit(surf, (0, 0))


sc = pygame.display.set_mode((1157, 700))
clock = pygame.time.Clock()
win = Window()
while True:
    for e in pygame.event.get():
        match e.type:
            case pygame.QUIT:
                quit()
            case _:
                win.event_work(e)
    win.update()
    pygame.display.update()
    clock.tick(60)
