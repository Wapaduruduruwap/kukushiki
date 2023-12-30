image station blink:
    "station"
    pause 0.3
    "black"
    pause 0.3
    repeat

# Определение персонажей игры.
define b = Character('[name]', color="#4db089")
define a = Character('Странный голос из ниоткуда...', color="#cf84b1")
define j = Character('Один из судей', color="#c7a877")
define d = Character('Диана', color="#775bb5")
define m = Character('Марк', color="#5070b5")
define i = Character('Инопланетяне', color="#cf84b1")

define audio.da = "audio/minigames/da.mp3"
define audio.sam = "audio/minigames/sam.mp3"
define audio.snow = "audio/minigames/snow.mp3"
define audio.door = "audio/minigames/door.mp3"
define audio.voices = "audio/minigames/voices.mp3"
define audio.aplo = "audio/minigames/aplo.mp3"
define audio.evro = "audio/minigames/evro.mp3"
define audio.nlo = "audio/minigames/nlo.mp3"

init python:

    import random

    class FeedtheDragonDisplayable(renpy.Displayable):
        def __init__(self):
            renpy.Displayable.__init__(self)
            self.key_pressed = None # This will store which key is held down

            # Set game values
            self.PLAYER_WIDTH = 250
            self.PLAYER_HEIGHT = 200
            self.COIN_WIDTH = 128
            self.COIN_HEIGHT = 128
            self.PLAYER_VELOCITY = 50
            self.COIN_STARTING_VELOCITY = 10
            self.COIN_ACCELERATION = 1
            self.BUFFER_DISTANCE = 100

            self.score = 0
            self.coin_velocity = self.COIN_STARTING_VELOCITY

            # Some displayables we use.
            self.player = Image("images/minigames/dragon.png")
            self.coin = Image("images/minigames/coins.png")

            # The positions of the two displayables.
            self.px = 20
            self.py = 500
            self.pymin = 100
            self.pymax = 1080 - 256
            self.cx = 1920 + 128
            self.cy = random.randint(128, 1080 - 128)
            self.cymin = 100
            self.cymax = 1080 - 128

            # The time of the past render-frame.
            self.oldst = None
            self.lose = False

            return

        # Draws the screen
        def render(self, width, height, st, at):

            # The Render object we'll be drawing into.
            r = renpy.Render(width, height)

            # Figure out the time elapsed since the previous frame.
            if self.oldst is None:
                self.oldst = st
            if self.key_pressed == "up":
                self.py -= self.PLAYER_VELOCITY
            elif self.key_pressed == "down":
                self.py += self.PLAYER_VELOCITY
            dtime = st - self.oldst
            self.oldst = st

            # This draws the player.
            def player(px, py, pymin, pymax):

                # Render the player image.
                player = renpy.render(self.player, width, height, st, at)

                # renpy.render returns a Render object, which we can
                # blit to the Render we're making.
                r.blit(player, (int(self.px), int(self.py)))

            # This draws the coin.
            def coin(cx, cy, cymin, cymax):

                # Render the coin image.
                coin = renpy.render(self.coin, width, height, st, at)

                # renpy.render returns a Render object, which we can
                # blit to the Render we're making.
                r.blit(coin, (int(self.cx), int(self.cy)))

            if self.cx < -128:
                # Player missed the coin
                renpy.sound.play("audio/minigames/miss_sound.ogg")
                self.cx = width + 128
                self.cy = random.randint(128, height - 128)
            else:
                # Move the coin
                self.cx -= self.coin_velocity

            if self.py < self.pymin:
                self.py = self.pymin
            if self.py > self.pymax:
                self.py = self.pymax

            if self.cy < self.cymin:
                self.cy = self.cymin
            if self.cy > self.cymax:
                self.cy = self.cymax

            player(self.px, self.py, self.pymin, self.pymax)
            coin(self.cx, self.cy, self.cymin, self.cymax)

            # Check for collisions
            def is_colliding(player, coin):
                return (
                    self.px <= self.cx + self.COIN_WIDTH and
                    self.px + self.PLAYER_WIDTH >= self.cx and
                    self.py <= self.cy + self.COIN_HEIGHT and
                    self.py + self.PLAYER_HEIGHT >= self.cy
                )

            if is_colliding(player, coin):
                self.score += 1
                renpy.sound.play("audio/minigames/coin_sound.ogg")
                self.coin_velocity += self.COIN_ACCELERATION
                self.cx = width + 128
                self.cy = random.randint(128, height - 128)

            # Check for a loss.
            if self.score == 20:
                self.lose = True

                renpy.timeout(0)

            # Ask that we be re-rendered ASAP, so we can show the next
            # frame.
            renpy.redraw(self, 0)

            # Return the Render object.
            return r

        # Handles events.
        def event(self, ev, x, y, st):

            import pygame

            # The following allows to store which key was held down.
            if ev.type == pygame.KEYDOWN and ev.key == pygame.K_UP and self.key_pressed != "up":
                self.key_pressed = "up"
            elif ev.type == pygame.KEYDOWN and ev.key == pygame.K_DOWN and self.key_pressed != "down":
                self.key_pressed = "down"
            elif ev.type == pygame.KEYUP:
                self.key_pressed = None

            # Ensure the screen updates.
            renpy.restart_interaction()

            # If the player loses, return it.
            if self.lose:
                return self.lose
            else:
                return


    def display_score(st, at):
        return Text(_("Score: ") + "%d" % feed_the_dragon.score + "/20", size=40, color="#bd34ed", outlines=[ (2, "#07a5ab", 0, 0) ]), .1

default feed_the_dragon = FeedtheDragonDisplayable()

screen feed_the_dragon():

    add "images/cosmo.jpg"

    add feed_the_dragon

    add DynamicDisplayable(display_score) xpos 240 xanchor 0.5 ypos 25

# Игра начинается здесь:
label start:
    play music da
    $ choice_var = 0
    scene space

    "Здравствуйте, дорогие абитуриенты!"
    "Наша новелла позволит вам ненадолго оказаться на месте студента Урфу, института Ирит-Ртф, на специальности прикладная информатика и узнать о профессии UX/UI дизайнер!"
    "Удачи!"

    scene home1
    $ name = renpy.input("Введите мужское имя: ").strip()
    show boy at left
    play sound snow
    b "«Эх, почему именно в субботу они решили устроить этот конкурс?"
    b "Я еще и не успел доделать свою работу. Дак еще в вечернее время…"
    b "Уже зима, и темнеет рано, опять снег пошёл…"
    b "Ладно, зато поддержу друзей.»"

    hide boy
    scene radik
    with fade

    "[name] не спеша идет в институт. И все-таки есть в зиме что-то завораживающее."
    "Почему-то на улице почти нет людей…"
    "Фонари слабо освещают блестящий снег."

    play sound nlo
    "...Странные звуки..."

    "[name] смотрит наверх, откуда исходит странный звук…"

    show boy at left
    b "«Это еще что такое…?»"

    scene nebo
    with fade
    hide boy

    "Не успевает студент подумать о чем-то другом, как появляется яркий, ослепляющий свет, который поднимает его к небу."
    stop music fadeout 1

    play music voices
    scene irit with fade
    pause
    scene outradik
    with fade
    show diana at left
    d 'Блин, ну и где его носит? Нам нужна помощь с подготовкой выступления, он же обещал прийти…'
    show mark at right
    m "Не паникуй раньше времени, у нас оно еще есть. Вдруг у него появились
срочные дела"
    d 'Или он спит! Если так и окажется, я на него обижусь…'
    m "Давай просто подождём."
    stop music fadeout 1

    play music sam
    scene station
    with fade
    show boy at left
    b "«Оххх… что это было?"
    b "Приснится же такое…"
    b "Блин, я же должен был пойти уже на конкурс!!!»"

    "[name] уже хочет направиться к двери, но тут ему приходит осознание…"

    show boy

    b "«Стоп."
    b "Это же не моя комната…"
    "[name] осматривает комнату"
    scene station blink
    with fade
    show boy
    b "Что? Что происходит?"
    b 'Страшно… где я?'
    scene station
    with fade
    show boy
    b 'Так, нужно собраться. Если я хочу отсюда выбраться или хотя бы понять, что со мной происходит…»'
    "[name] решает осмотреть комнату."
    scene door
    with fade
    show boy at left
    b "«Ничего себе... Какая дверь, а что это рядом?"
    b "Наверное, нужно на что-то нажать.»"
    scene tablet
    with fade
    centered "{size=+20}{color=#000000}Пройди тест, чтобы открыть дверь.{/color}{/size}"
    centered "{size=+20}{color=#000000}Как думаешь, как можно назвать дизайнера, который занимается интерфейсами?{/color}{/size}"

label quest1:
    scene tablet
    menu:
        "UX/UI-дизайнер":
            scene tablet green
            centered "{size=+20}{color=#000000}Правильный ответ, молодец!{/color}{/size}"
            scene tablet
            centered "{size=+20}{color=#000000}Заказчики хотят создать сайт магазина по продаже бананов, какой цвет будет приорететным на сайте?{/color}{/size}"
        "Дизайнер":
            scene tablet red
            centered "{size=+20}{color=#000000}Неверно! Подумай еще{/color}{/size}"
            jump quest1
        "Графический дизайнер":
            scene tablet red
            centered "{size=+20}{color=#000000}Нет! Подумай еще{/color}{/size}"
            jump quest1
        "Дизайнер интерфейсов":
            scene tablet red
            centered "{size=+20}{color=#000000}Нет! Подумай еще{/color}{/size}"
            jump quest1
label quest2:
    scene tablet
    menu:
        "Зеленый":
            scene tablet red
            centered "{size=+20}Неверно, подумай ещё{color=#000000}{/color}{/size}"
            jump quest2
        "Розовый":
            scene tablet red
            centered "{size=+20}{color=#000000}Нет, подумай хорошенько{/color}{/size}"
            jump quest2
        "Желтый":
            scene tablet green
            centered "{size=+20}{color=#000000}Правильно!{/color}{/size}"
            scene tablet
            centered "{size=+20}{color=#000000}Как часто ты пользуешься поисковыми ресурсами, разными сайтами?{/color}{/size}"
        "Оранжевый":
            scene tablet red
            centered "{size=+20}{color=#000000}Почти, но нет{/color}{/size}"
            jump quest2
label quest3:
    menu:
        "Часто":
            jump quest4
        "Редко":
            jump quest4
        "Иногда":
            jump quest4
        "Пользуюсь книгами":
            jump quest4

label quest4:
    centered "{size=+20}{color=#000000}Что тебе чаще всего не нравится на сайтах?{/color}{/size}"
    menu:
        "Много рекламы":
            centered "{size=+20}{color=#000000}На белом листе изображены два круга: чёрный и красный. Какой притянет больше внимания?{/color}{/size}"
            jump quest5
        "Сложная навигация":
            centered "{size=+20}{color=#000000}На белом листе изображены два круга: чёрный и красный. Какой притянет больше внимания?{/color}{/size}"
            jump quest5
        "Отсутствие конкретной(нужной) информации":
            centered "{size=+20}{color=#000000}На белом листе изображены два круга: чёрный и красный. Какой притянет больше внимания?{/color}{/size}"
            jump quest5
        "Перебор с декором / его отсутстивие":
            centered "{size=+20}{color=#000000}На белом листе изображены два круга: чёрный и красный. Какой притянет больше внимания?{/color}{/size}"
            jump quest5

label quest5:
    menu:
        "Красный":
            scene tablet green
            centered "{size=+20}{color=#000000}Правильный ответ{/color}{/size}"
        "Чёрный":
            scene tablet red
            centered "{size=+20}{color=#000000}Нет! Яркие цвета привлекают больше внимания{/color}{/size}"
            scene tablet
            jump quest5

label perehod:
    scene tablet
    centered "{size=+20}{color=#000000}Ты отлично справился! Но есть ещё одно испытание. Под силу ли оно тебе?{/color}{/size}"
    centered "{size=+20}{color=#000000}В следующем испытании тебе необходимо собрать 20 звёзд, используя клавиши ↑ и ↓. Удачи, студент!{/color}{/size}"
    stop music fadeout 1

label play_feed_the_dragon:

    window hide  # Hide the window and quick menu while in Feed the Dragon
    $ quick_menu = False

    play music "audio/minigames/04.mp3"

    $ feed_the_dragon.lose = False
    $ feed_the_dragon.score = 0
    $ feed_the_dragon.coin_velocity = feed_the_dragon.COIN_STARTING_VELOCITY
    $ feed_the_dragon.py = 500
    $ feed_the_dragon.cy = random.randint(128, 1080 - 128)

    call screen feed_the_dragon

    play music  "audio/minigames/04.mp3"

    $ quick_menu = True
    window auto

label feed_the_dragon_done:

    if 20 == feed_the_dragon.score:
        jump exit_minigame




label exit_minigame:
    $ choice_var = 1
    stop music
    play music sam
    scene door
    show boy at left
    pause
    play sound door
    scene door open
    with fade
    show boy at left
    b "Дверь открылась! Это было труднее, чем я думал.."
    b "Нужно идти дальше."
    scene iluminate
    with fade
    show boy at right

    b 'Наконец-то я выбрался из этих комнат, но где я теперь?'
    a 'Мы рады приветствовать тебя, человек'
    a 'Ты отлично справился с нашими загадками, мы думаем у тебя есть потенциал, поэтому хотим попросить у тебя помощи…'
    b 'Кто вы?'
    b 'Зачем вы меня заперли? Где я нахожусь?'
    a 'Посмотри за борт корабля.'

    scene space
    with fade

    a 'Мы не хотели причинить тебе вреда, но и боялись спугнуть тебя. Мы впервые на Земле и нам нужна человеческая помощь.'
    a 'Мы готовы довериться тебе, если ты согласишься нам помочь.'

    scene iluminate
    with fade
    show boy at right

    b 'Это шутка какая-то?'
    b 'Я не могу поверить…'
    a 'Нет, мы улетели немного дальше от Земли чтобы нас не заметили другие человеческие существа.'
    b 'Если я буду уверен в своей безопасности, и вы мне объясните зачем вам нужна моя помощь, тогда я возможно подумаю…'
    a 'Хорошо. Сейчас мы тебе всё расскажем.'

    show alien nuna at left

    i "Как ты уже понял мы не человеческие существа, мы представители другой цивилизации."
    i "Мы изучили информацию о работе, которая нам нужна из человеческих источников."
    hide alien nuna

    "«Походу это правда. Все что со мной происходит правда, но они настроены дружелюбно…"
    "О чем я думаю??? Меня же похитили, а я должен был помочь друзьям."
    "Нужно мыслить рационально, как бы не было страшно…"
    "Если я им помогу, они меня отпустят?"
    "А если не помогу?"
    "Даже страшно представить…"
    "Ладно, пока что просто выслушаю их.»"

    show alien nuna at left
    i "Мы участвуем в межгалактической гонке и тот, кто выиграет, сможет представить свой сайт на человеческих ресурсах."
    i "Для нас это очень важно, именно поэтому нам нужна человеческая помощь. У вас это называется дизайн"
    i "интер…инте…"
    i "интерфейсов, какой все-таки у вас сложный язык."
    i "Это профессия UX/UI дизайнер."


label question1:
    menu:
        i "Ты знаешь что-то про нее?"
        "Да":
            jump yesIknow

        "Нет":
            jump noIdontknow

label yesIknow:
    i "Тогда расскажи, что ты знаешь, а мы дополним."
    b "Ну насколько мне известно UX/UI дизайнеры работают над тем, как пользователь взаимодействует с интерфейсом."
    b "Они разрабатывают пользовательские сценарии, дизайн системы и обеспечивают удобство использования продукта."
    b "Другие подробности мне неизвестны."
    i "Да, все верно."
    i "Также роль UX/UI дизайнеров состоит из нескольких этапов. В начале проекта они проводят исследования пользовательских потребностей, конкурентного анализа и определяют ключевые требования к проекту."
    i "На основе полученных данных они создают информационную архитектуру продукта, которая позволяет пользователям легко находить нужные им элементы в интерфейсе."
    # другой фон
    i "Затем дизайнеры создают прототип продукта, который помогает визуализировать контент, структуру и функционал взаимодействия."
    i "Далее специалист разрабатывает дизайн системы, включающий в себя цветовую гамму, шрифты, иконки, а также другие графические элементы."
    # другой фон
    i "В итоге UX/UI дизайнеры отвечают за создание привлекательного и продуманного пользовательского интерфейса. Они заботятся о визуальном оформлении сайтов, мобильных приложений, программного обеспечения и других интерактивных продуктов."
    i "Одновременно они также учитывают функциональность и практичность пользовательского интерфейса."
    i "Разделив UX/UI, мы сможем глубже разобраться с этим направлением."
    # другой фон
    i "UX (USER EXPERIENCE) Это пользовательский опыт — всё, что связано с исследованиями «болей» пользователей, анализом и планированием на основе всех этих данных структуры продукта."
    i "UX-дизайнер анализирует пользовательский путь и продумывает структуру продукта."
    # другой фон
    i "UI (USER INTERFACE) Это пользовательский интерфейс: наполнение сайта, его элементы, выбор цветов и шрифтов, визуальная композиция и другие графические элементы."
    i "UI-дизайнер визуализирует структуру продукта: отвечает за то, как будут выглядеть его разделы и страницы в итоге."
    i "Эти направления тесно связаны друг с другом, одно без другого не может эффективно существовать. Если создавать, например, сайт только ради красивого интерфейса — результата не будет."
    # scene station
    b "Ого.."
    jump yes_interesno

label noIdontknow:
    i "Тогда мы тебе расскажем."
    i "UX/UI дизайнеры работают над тем, как пользователь взаимодействует с интерфейсом."
    i "Они разрабатывают пользовательские сценарии, дизайн системы и обеспечивают удобство использования продукта."
    # другой фон
    i "Но также роль UX/UI дизайнеров состоит из нескольких этапов. В начале проекта они проводят исследования пользовательских потребностей, конкурентного анализа и определяют ключевые требования к проекту."
    i "На основе полученных данных они создают информационную архитектуру продукта, которая позволяет пользователям легко находить нужные им элементы в интерфейсе."
    # другой фон
    i "Затем дизайнеры создают прототип продукта, который помогает визуализировать контент, структуру и функционал взаимодействия."
    i "Далее дизайнер разрабатывает дизайн системы, включающий в себя цветовую гамму, шрифты, иконки, а также другие графические элементы."
    # другой фон
    i "В итоге UX/UI дизайнеры отвечают за создание привлекательного и продуманного пользовательского интерфейса. Они заботятся о визуальном оформлении сайтов, мобильных приложений, программного обеспечения и других интерактивных продуктов."
    i "Одновременно они также учитывают функциональность и практичность пользовательского интерфейса."
    i "Разделив UX/UI, мы сможем глубже разобраться с этим направлением."
    # другой фон
    i "UX (USER EXPERIENCE) Это пользовательский опыт — всё, что связано с исследованиями «болей» пользователей, анализом и планированием на основе всех этих данных структуры продукта."
    i "UX-дизайнер анализирует пользовательский путь и продумывает структуру продукта."
    # другой фон
    i "UI (USER INTERFACE) Это пользовательский интерфейс: наполнение сайта, его элементы, выбор цветов и шрифтов, визуальная композиция и другие графические элементы."
    i "UI-дизайнер визуализирует структуру продукта: отвечает за то, как будут выглядеть его разделы и страницы в итоге."
    i "Эти направления тесно связаны друг с другом, одно без другого не может эффективно существовать. Если создавать, например, сайт только ради красивого интерфейса — результата не будет."
    menu:
        i "Тебя заинтересовала эта профессия?"
        "Да":
            jump yes_interesno

        "Нет":
            jump no_figny

label yes_interesno:
    "«Хм, а это и правда интересно звучит, тем более я немного игроман… еще и в школе всегда помогал в творческих проектах."
    "Мне бы подошла такая профессия, но непонятно востребована она или нет, мне бы не хотелось сидеть без работы»"
    b "А не могли бы вы еще рассказать? Про карьерный рост, например…"
    i "Карьерный рост для UX/UI дизайнера может быть достаточно быстрым и прогнозируемым, особенно если есть соответствующие навыки и опыт работы. Востребованность этой профессии на рынке труда также остается на очень высоком уровне."
    i "UX/UI дизайнер, как и любой другой программист, делится на 4 уровня профессионализма: стажёр, джуниор, мидл, синьёр — в зависимости от опыта работы так же и варьируется его заработная плата."
    i "Более того, развитие технологий, таких как искусственный интеллект, интернет ресурсы и виртуальная реальность, создает новые возможности для UX/UI дизайнеров, которые могут внедрять инновационные и уникальные решения."
    i "Мы хотим, чтобы ты помог нам создать не только красивый сайт, но и сделать его удобным для пользователей."
    i "Мы хотим стать первыми, кто покажет людям красоты нашей галактики."
    i "Ты согласен помочь нам?"
    "«А я могу стать тем, кто положил начало этой связи…»"
    menu:
         "Я согласен":
             jump DADADA
         "Нет, отпустите меня, пожалуйста":
             jump bad_end

label no_figny:
    i "Жаль, что мы не смогли тебя заинтересовать"
    i "но возможно тебе будет интересна информация о том, что карьерный рост для UX/UI дизайнера может быть достаточно быстрым и прогнозируемым, особенно если есть соответствующие навыки и опыт работы."
    i "Востребованность этой профессии на рынке труда также остается на очень высоком уровне."
    b "Я бы все-таки хотел заниматься другой деятельностью…"
    i "Хорошо. Но согласен ли ты помочь нам?"
    menu:
        i "Ты согласен помочь нам?"
        "Я согласен":
            jump DADADA
        "Нет, отпустите меня пожалуйста":
            jump bad_end
label DADADA:
    b "Но после этого, я хочу, чтобы вы меня отпустили"
    i "Без проблем."
    i "Тогда пройдем в комнату, где есть все ресурсы для работы."
    scene computer
    with fade
    show alien nuna at left
    show boy at right
    b "Что ж, тогда приступим к работе.."
    scene black_time
    with fade
    pause
    scene site
    pause
    scene computer
    with fade
    show boy at right
    show alien nuna at left
    b "Готово!"
    b 'Сделал всё, что смог.'
    b "«Хм, а это ведь хорошая идея для конкурса."
    b "Надеюсь, я успею на него.»"
    i "Отлично, тогда пришла пора прощаться."
    i 'Спасибо тебе за помощь.'
    b '«поскорее бы обратно..»'
    stop music fadeout 1

    play music da
    scene nebo
    with fade
    b "«ох, как голова болит.."
    b "Почему я на снегу?»"
    scene radik
    with fade
    show boy at left
    b "«Что произошло?"
    b "Я потерял сознание..? Или просто упал и ударился головой?"
    b "Ничего не помню.."
    b "Вот это сон.. Ашалеть"
    b "Я же на конкурс шёл, надо бежать»"
    stop music fadeout 1
    scene outradik
    play music voices
    with fade
    show boy at right
    show diana at left
    d "Да уж, мне интересно, чем ты был занят всё это время.."
    b "Привет, я сам не знаю.. Я упал, пока шёл к вам, вырубился, ничего не помню. Как очнулся, сразу побежал сюда."
    hide diana
    show mark at left
    m "ЧТО?? Ты в порядке?"
    hide mark
    show diana at left
    d "Извини.. Сейчас всё нормально?"
    b "Да, только голова побаливает, но всё в порядке, спасибо."
    b "Кстати, у меня есть идея для выступления!"
    d "Это отличная новость, как раз скоро наша очередь"
    scene black
    with fade
    show boy
    b "Удивительно, но я представил идею из сна."
    b "Как мне вообще могло такое присниться? Хотя я даже рад.."
    scene outradik
    with fade
    show judge at right
    j "Подводя итоги, хотелось бы сказать, что многие работы были хороши, но победителями сегодняшнего конкурса становятся.."
    j 'Участники команды "Kukushiki"!'
    j "Апплодисменты им!"
    play sound aplo
    hide judge
    show diana at left
    d "Не может быть!"
    show boy at right
    b "Поздравляю нас!"
    hide diana
    show mark at left
    m "Ого.. Мы так хорошо поработали!"
    m "Тебя, [name], надо особенно похвалить, ты здорово нас удивил!"
    b "Да ладно тебе, мы все постарались."
    stop music fadeout 1
    scene black ten
    pause
    scene nlo
    with fade
    "*смотрят людские новости*"
    'Канал "Новости"' "[name] проделал огромную работу. Благодаря ему масштабный проект был спасён. Этот известный дизайнер воплотил в реальность все запросы заказчиков!"
    'Канал "Новости"' "Теперь он самый востребованный UX/UI дизайнер."
    i "А он молодец."
    i "И нам помог выиграть и сам прославился. Не зря мы выбрали именно его."
    i "Интересно, он хоть что-то помнит?"
    scene white
    with fade
    centered "{size=+20}{color=#000000}Спасибо, что прошли нашу новеллу! Надеемся, вам понравилось, и мы помогли вам подробнее узнать о профессии UX/UI дизайнер!{/color}{/size}"
    centered "{size=+20}{color=#000000}Над новеллой работали:{/color}{/size}"
    play music evro
    centered "{size=+20}{color=#000000}Суркина Мария{/color}{/size}"
    centered "{size=+20}{color=#000000}Метелева Дарья{/color}{/size}"
    centered "{size=+20}{color=#000000}Федорова Алина{/color}{/size}"
    centered "{size=+20}{color=#000000}Потанина Анастасия{/color}{/size}"
    centered "{size=+20}{color=#000000}Матович Стефан{/color}{/size}"
    scene cats
    with fade
    pause
    return

label bad_end:
    i "Жаль.. Придётся искать другого претендента.."
    i "Тогда будем прощаться, но прежде:"
    b "Чт.."
    stop music fadeout 1
    play music da
    scene white
    with fade
    pause
    scene radik
    with fade
    show boy at left
    b "«Что произошло?"
    b "Я потерял сознание..? Или просто упал и ударился головой?"
    b "Ничего не помню.."
    b "Голова болит.."
    b "А зачем я сюда шёл?"
    b "ААА, я же спешил на конкурс..»"
    stop music fadeout 1
    scene outradik
    play music voices
    with fade
    show boy at right
    show diana at left
    d "Где ты был всё это время? Ты же обещал нам помочь!"
    b "Я упал по дороге сюда и потерял сознание.."
    hide diana
    show mark at left
    m "Ты в порядке? Скоро наш выход."
    b "Да.. Но я ничего не придумал к конкурсу.."
    b "Извините."
    hide mark
    show diana at left
    d "Эх, выступим с тем, что есть."
    scene res
    pause
    scene outradik
    with fade
    show judge at right
    j 'Выигрывает команды "..."'
    hide judge
    show diana at left
    d "Этого стоило ожидать."
    d "Мы сделали всё, что смогли, мы молодцы."
    show boy at right
    b "Это из-за меня, простите.."
    hide diana
    show mark at left
    m "Всё хорошо, просто постарайся в следующий раз."
    b "Обязательно, спасибо вам!"
    stop music fadeout 1
    scene white
    with fade
    centered "{size=+20}{color=#000000}Спасибо, что прошли нашу новеллу! Надеемся, вам понравилось, и мы помогли вам подробнее узнать о профессии UX/UI дизайнер!{/color}{/size}"
    centered "{size=+20}{color=#000000}Над новеллой работали:{/color}{/size}"
    play music evro
    centered "{size=+20}{color=#000000}Суркина Мария{/color}{/size}"
    centered "{size=+20}{color=#000000}Метелева Дарья{/color}{/size}"
    centered "{size=+20}{color=#000000}Федорова Алина{/color}{/size}"
    centered "{size=+20}{color=#000000}Потанина Анастасия{/color}{/size}"
    centered "{size=+20}{color=#000000}Матович Стефан{/color}{/size}"
    scene cats
    with fade
    pause
    return
